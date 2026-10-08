"""SQLAlchemy engine/session setup for ZEYRECUITE (SQLite, local-first)."""
from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import AppConfig, database_url_for

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def _make_engine(url: str):
    from sqlalchemy import event

    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, connect_args=connect_args, future=True)

    if url.startswith("sqlite"):

        @event.listens_for(engine, "connect")
        def _set_sqlite_pragmas(dbapi_connection, _record):  # pragma: no cover
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA busy_timeout=5000")
            # SQLite leaves foreign keys OFF by default; the models declare FKs
            # (Job → Application/Feedback, User → Session) and they must be
            # enforced so deletes cascade instead of leaving orphaned rows that
            # skew learning weights / run analytics.
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


class Database:
    """Holds the engine and a session factory for the app lifetime."""

    def __init__(self, url: str):
        self.url = url
        self.engine = _make_engine(url)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False, future=True)

    def create_all(self) -> None:
        from . import models  # noqa: F401  (register models on the metadata)

        Base.metadata.create_all(self.engine)
        self.migrate()

    def migrate(self) -> None:
        """Add any columns that exist on the models but not yet in the DB.

        SQLite's ``create_all`` only creates missing *tables*, so this performs
        a lightweight, idempotent column migration for schema evolution.
        """
        from sqlalchemy import inspect, text

        inspector = inspect(self.engine)
        existing_tables = set(inspector.get_table_names())
        with self.engine.begin() as conn:
            for table in Base.metadata.sorted_tables:
                if table.name not in existing_tables:
                    continue
                current = {c["name"] for c in inspector.get_columns(table.name)}
                for col in table.columns:
                    if col.name in current:
                        continue
                    col_type = col.type.compile(dialect=self.engine.dialect)
                    conn.execute(
                        text(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {col_type}')
                    )
        # One-time rebuild: make profiles.role / profiles.current_country
        # nullable. SQLite cannot relax a NOT NULL constraint in place, so the
        # table is rebuilt (data preserved) only when the old schema is
        # detected. Idempotent — runs at most once per database.
        if "profiles" in existing_tables:
            cols = {c["name"]: c for c in inspector.get_columns("profiles")}
            if cols.get("current_country", {}).get("nullable") is False:
                self._make_profile_columns_nullable()

        # Reconcile constraints/indexes so an upgraded database behaves like a
        # fresh one (bug #13): SQLite's ALTER-based column migration never adds
        # them retroactively, so without this pass feedback rows multiply and a
        # concurrent scan can race jobs.fingerprint undetected.
        from sqlalchemy.schema import CreateIndex

        # 1. Purge rows that violate the (now connection-enforced) foreign keys —
        #    legacy databases allowed orphans because FKs were off by default.
        for child, fk_col, parent in (
            ("feedback", "job_id", "jobs"),
            ("applications", "job_id", "jobs"),
            ("sessions", "user_id", "users"),
        ):
            if child in existing_tables and parent in existing_tables:
                with self.engine.begin() as conn:
                    conn.execute(text(
                        f"DELETE FROM {child} WHERE {fk_col} IS NULL OR {fk_col} "
                        f"NOT IN (SELECT id FROM {parent})"
                    ))

        # 2. Collapse duplicate feedback down to the newest row per job so the
        #    unique index below can be created.
        if "feedback" in existing_tables:
            with self.engine.begin() as conn:
                conn.execute(text(
                    "DELETE FROM feedback WHERE id NOT IN "
                    "(SELECT MAX(id) FROM feedback GROUP BY job_id)"
                ))

        # 3. Create any indexes the models declare but the legacy DB predates
        #    (table.indexes + column-level unique=True), idempotently.
        inspector = inspect(self.engine)
        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue
            have = {ix["name"] for ix in inspector.get_indexes(table.name)}
            cols_now = {c["name"] for c in inspector.get_columns(table.name)}
            for col in table.columns:
                if not col.unique or col.name not in cols_now:
                    continue
                covered = any(
                    ix.get("unique") and ix.get("column_names") == [col.name]
                    for ix in inspector.get_indexes(table.name)
                )
                if covered:
                    continue
                stmt = (
                    f'CREATE UNIQUE INDEX IF NOT EXISTS "uq_{table.name}_{col.name}" '
                    f'ON "{table.name}" ("{col.name}")'
                )
                try:
                    with self.engine.begin() as conn:
                        conn.execute(text(stmt))
                except Exception as exc:  # noqa: BLE001 — legacy duplicate rows
                    logger.warning("could not create unique index on %s.%s: %s",
                                   table.name, col.name, exc)
            for idx in table.indexes:
                if idx.name in have:
                    continue
                stmt = str(CreateIndex(idx).compile(dialect=self.engine.dialect))
                if "IF NOT EXISTS" not in stmt:
                    parts = stmt.split(" ", 2)  # CREATE [UNIQUE] INDEX <name> ...
                    stmt = f"{parts[0]} {parts[1]} IF NOT EXISTS {parts[2]}"
                try:
                    with self.engine.begin() as conn:
                        conn.execute(text(stmt))
                except Exception as exc:  # noqa: BLE001 — legacy duplicate rows
                    logger.warning("could not create index %s: %s", idx.name, exc)

    def _make_profile_columns_nullable(self) -> None:
        """Rebuild the profiles table so role/current_country are nullable.

        SQLite cannot relax a NOT NULL constraint in place, so the table is
        rebuilt from the current model definition (data preserved). The column
        list is derived from the model metadata intersected with the columns
        actually present in the old table, so this is safe regardless of which
        schema version the old table was created with.
        """
        from sqlalchemy import inspect, text

        from . import models  # noqa: F401  (register models on the metadata)

        table = models.Base.metadata.tables["profiles"]
        old_cols = {c["name"] for c in inspect(self.engine).get_columns("profiles")}
        cols = [c for c in table.columns if c.name in old_cols]
        col_defs = ", ".join(
            f'"{c.name}" {c.type.compile(dialect=self.engine.dialect)}'
            + (" NOT NULL" if c.primary_key else "")
            for c in cols
        )
        names = ", ".join(f'"{c.name}"' for c in cols)
        # Convert legacy empty-string placeholders to NULL for the two columns
        # that were previously NOT NULL with empty-string defaults.
        select_exprs = ", ".join(
            f'NULLIF("{c.name}", \'\')' if c.name in ("role", "current_country") else f'"{c.name}"'
            for c in cols
        )
        with self.engine.begin() as conn:
            conn.execute(text(f"CREATE TABLE profiles_new ({col_defs})"))
            conn.execute(text(f"INSERT INTO profiles_new ({names}) SELECT {select_exprs} FROM profiles"))
            conn.execute(text("DROP TABLE profiles"))
            conn.execute(text("ALTER TABLE profiles_new RENAME TO profiles"))

    def session(self) -> Session:
        return self.SessionLocal()


def build_database(config: AppConfig) -> Database:
    """Create a Database bound to the configured SQLite file."""
    url = database_url_for(config)
    if url.startswith("sqlite:///"):
        db_path = Path(url[len("sqlite:///"):])
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return Database(url)
