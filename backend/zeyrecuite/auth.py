"""Authentication: users, password hashing, and session tokens.

Local-first and dependency-free (uses stdlib PBKDF2). Sessions are stored in
the database as sha256 hashes (the raw token is returned exactly once to the
client) with an expiry so the app can be restarted without losing login state.

A default ``admin`` account is seeded on first run so the dashboard is usable
immediately. Its password is never hardcoded: set the
``ZEYRECUITE_ADMIN_PASSWORD`` environment variable before the first start, or
a random one-time password is generated and written to the server log. The
password can be changed from the Profile view (which revokes every other
session).
"""
from __future__ import annotations

import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from .models import Session as SessionModel
from .models import User

SESSION_TTL = timedelta(days=7)
_PBKDF2_ITERATIONS = 200_000
MIN_PASSWORD_LENGTH = 8

logger = logging.getLogger("zeyrecuite.auth")

# Fixed salt used to hash a password for a *nonexistent* user so an unknown
# username costs the same time as a real PBKDF2 verification (prevents username
# enumeration by response timing).
_TIMING_SALT = os.urandom(16)


def validate_password(password: str) -> None:
    """Reject weak passwords (non-string / shorter than MIN_PASSWORD_LENGTH)."""
    if not isinstance(password, str) or len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"password must be at least {MIN_PASSWORD_LENGTH} characters long")


def _hash_token(token: str) -> str:
    """One-way hash for storing session tokens (the raw token is never stored)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    """Return (hex_hash, hex_salt) for a password using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return digest.hex(), salt.hex()


def verify_password(password: str, hex_hash: str, hex_salt: str) -> bool:
    candidate, _ = hash_password(password, bytes.fromhex(hex_salt))
    return secrets.compare_digest(candidate, hex_hash)


def create_user(session: Session, username: str, password: str, display_name: str | None = None) -> User:
    validate_password(password)
    pw_hash, salt = hash_password(password)
    user = User(
        username=username.strip(),
        password_hash=pw_hash,
        password_salt=salt,
        display_name=display_name or username.strip(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(session: Session, username: str, password: str) -> User | None:
    user = session.query(User).filter(User.username == username.strip()).first()
    if not user:
        # Spend the same PBKDF2 time as a real verification so a missing user
        # cannot be distinguished from a wrong password by response timing.
        hash_password(password, _TIMING_SALT)
        return None
    if not verify_password(password, user.password_hash, user.password_salt):
        return None
    return user


def create_session(session: Session, user: User) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + SESSION_TTL
    # Store only the sha256 hash: a leaked DB dump cannot be replayed as a
    # valid session (the raw token exists solely in the client's memory).
    session.add(SessionModel(token=_hash_token(token), user_id=user.id, expires_at=expires))
    session.commit()
    return token


def _utcnow() -> datetime:
    """Current UTC time, aware."""
    return datetime.now(timezone.utc)


def _as_utc(dt: datetime | None) -> datetime | None:
    """Normalize a possibly-naive datetime to aware UTC (SQLite drops tzinfo)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def purge_expired_sessions(session: Session) -> int:
    """Delete *every* expired session row, not just the one being presented.

    Without this, the table only ever shrinks when an expired token happens to
    be shown again, so it grows without bound as logins accumulate.
    """
    now = _utcnow()
    expired_ids: list[int] = []
    for row_id, raw_expires in session.query(SessionModel.id, SessionModel.expires_at).all():
        expires = _as_utc(raw_expires)
        if expires and expires < now:
            expired_ids.append(row_id)
    if expired_ids:
        session.query(SessionModel).filter(SessionModel.id.in_(expired_ids)).delete(
            synchronize_session=False
        )
        session.commit()
    return len(expired_ids)


def get_user_for_token(session: Session, token: str | None) -> User | None:
    if not token:
        return None
    # Opportunistically purge all expired sessions on the hot path so cleanup
    # does not depend on the (unlikely) presentation of each dead token.
    purge_expired_sessions(session)
    row = session.query(SessionModel).filter(SessionModel.token == _hash_token(token)).first()
    if not row:
        return None
    expires = _as_utc(row.expires_at)
    if expires and expires < _utcnow():
        session.delete(row)
        session.commit()
        return None
    return session.get(User, row.user_id)


def revoke_session(session: Session, token: str) -> None:
    row = session.query(SessionModel).filter(SessionModel.token == _hash_token(token)).first()
    if row:
        session.delete(row)
        session.commit()


def change_password(
    session: Session, user: User, new_password: str, *, keep_token: str | None = None
) -> None:
    """Change a user's password and revoke every other session.

    A compromised account's existing tokens must die when the password changes;
    the session that performed the change (``keep_token``) is kept so the user is
    not immediately logged out of the browser they are using.
    """
    validate_password(new_password)
    pw_hash, salt = hash_password(new_password)
    user.password_hash = pw_hash
    user.password_salt = salt
    query = session.query(SessionModel).filter(SessionModel.user_id == user.id)
    if keep_token:
        query = query.filter(SessionModel.token != _hash_token(keep_token))
    query.delete(synchronize_session=False)
    session.commit()


def seed_default_user(session: Session) -> None:
    """Create a default account on first run if none exists.

    The password comes from the ``ZEYRECUITE_ADMIN_PASSWORD`` environment
    variable when set; otherwise a random one-time password is generated and
    logged. There is no hardcoded fallback, so deleting the admin user can never
    resurrect a known backdoor — the next seed is random too.
    """
    if session.query(User).count() != 0:
        return
    password = os.environ.get("ZEYRECUITE_ADMIN_PASSWORD", "").strip()
    if password:
        create_user(session, "admin", password, "Administrator")
        return
    password = secrets.token_urlsafe(12)
    create_user(session, "admin", password, "Administrator")
    logger.warning(
        "Seeded the default 'admin' account with a one-time random password: %s "
        "Change it from the Profile view, or set ZEYRECUITE_ADMIN_PASSWORD "
        "before first start to choose your own.",
        password,
    )
