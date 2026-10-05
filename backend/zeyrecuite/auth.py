"""Authentication: users, password hashing, and session tokens.

Local-first and dependency-free (uses stdlib PBKDF2). Sessions are stored in
the database with an expiry so the app can be restarted without losing login
state. A default account is seeded on first run so the dashboard is usable
immediately; the password can be changed from the Profile view.
"""
from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from .models import Session as SessionModel
from .models import User

SESSION_TTL = timedelta(days=7)
_PBKDF2_ITERATIONS = 200_000


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
        return None
    if not verify_password(password, user.password_hash, user.password_salt):
        return None
    return user


def create_session(session: Session, user: User) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + SESSION_TTL
    session.add(SessionModel(token=token, user_id=user.id, expires_at=expires))
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


def get_user_for_token(session: Session, token: str | None) -> User | None:
    if not token:
        return None
    row = session.query(SessionModel).filter(SessionModel.token == token).first()
    if not row:
        return None
    expires = _as_utc(row.expires_at)
    if expires and expires < _utcnow():
        session.delete(row)
        session.commit()
        return None
    return session.get(User, row.user_id)


def revoke_session(session: Session, token: str) -> None:
    row = session.query(SessionModel).filter(SessionModel.token == token).first()
    if row:
        session.delete(row)
        session.commit()


def change_password(session: Session, user: User, new_password: str) -> None:
    pw_hash, salt = hash_password(new_password)
    user.password_hash = pw_hash
    user.password_salt = salt
    session.commit()


def seed_default_user(session: Session) -> None:
    """Create a default account on first run if none exists."""
    if session.query(User).count() == 0:
        create_user(session, "admin", "zeyrecuite", "Administrator")
