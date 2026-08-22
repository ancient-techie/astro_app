"""
Storage layer for saved birth details.
------------------------------------
Why this file exists: on Render (and most free PaaS tiers) the web
service's local disk is NOT guaranteed to survive a redeploy or a
restart after the app spins down from inactivity - a plain SQLite file
sitting next to app.py would quietly get wiped. To make the same code
work both locally and in production:

  - Locally (no DATABASE_URL set) it falls back to a SQLite file,
    local.db, right next to this script - zero setup for development.
  - In production, set the DATABASE_URL environment variable to a
    *hosted* database (e.g. Render's own PostgreSQL, or a free
    external one like Neon/Supabase) and the exact same code stores
    data there instead - which persists independently of the web
    service's disk, so it survives redeploys and spin-down/spin-up.

Render (and Heroku) hand out connection strings that start with
"postgres://"; SQLAlchemy 1.4+/2.x require "postgresql://", so that
prefix is rewritten automatically below.
"""

import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

_DEFAULT_SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local.db")

_raw_url = os.environ.get("DATABASE_URL", "").strip()
if not _raw_url:
    _raw_url = f"sqlite:///{_DEFAULT_SQLITE_PATH}"
elif _raw_url.startswith("postgres://"):
    _raw_url = _raw_url.replace("postgres://", "postgresql://", 1)

# pool_pre_ping checks each connection before using it and transparently
# reconnects if it went stale - important for hosted free-tier Postgres,
# which tends to drop idle connections while this app is asleep.
engine = create_engine(_raw_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
Base = declarative_base()


class BirthRecord(Base):
    __tablename__ = "birth_records"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    city = Column(String(200))
    dob = Column(String(10))   # "YYYY-MM-DD", stored as the form sends it
    tob = Column(String(5))    # "HH:MM"
    lat = Column(String(50))
    lng = Column(String(50))
    tz = Column(String(100))
    style = Column(String(10), default="south")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    """Create the table if it doesn't exist yet. Safe to call every startup."""
    Base.metadata.create_all(bind=engine)


def _row_to_dict(row):
    return {
        "id": row.id,
        "name": row.name,
        "city": row.city,
        "date": row.dob,
        "time": row.tob,
        "lat": row.lat,
        "lng": row.lng,
        "tz": row.tz,
        "style": row.style,
        "created_at": row.created_at,
        "updated_at": row.updated_at,
    }


def save_birth_record(form):
    """Insert a new saved record, or update the existing one for the same
    person (matched on name + city + date of birth + time of birth) so that
    regenerating the same chart repeatedly doesn't pile up duplicates.
    Returns the record id.
    """
    session = SessionLocal()
    try:
        existing = (
            session.query(BirthRecord)
            .filter_by(name=form["name"], city=form["city"], dob=form["date"], tob=form["time"])
            .first()
        )
        if existing:
            existing.lat = form["lat"]
            existing.lng = form["lng"]
            existing.tz = form["tz"]
            existing.style = form["style"]
            existing.updated_at = datetime.utcnow()
            session.commit()
            return existing.id

        record = BirthRecord(
            name=form["name"],
            city=form["city"],
            dob=form["date"],
            tob=form["time"],
            lat=form["lat"],
            lng=form["lng"],
            tz=form["tz"],
            style=form["style"],
        )
        session.add(record)
        session.commit()
        return record.id
    finally:
        session.close()


def list_birth_records():
    """All saved records, most recently saved first."""
    session = SessionLocal()
    try:
        rows = session.query(BirthRecord).order_by(BirthRecord.updated_at.desc()).all()
        return [_row_to_dict(r) for r in rows]
    finally:
        session.close()


def get_birth_record(record_id):
    session = SessionLocal()
    try:
        row = session.get(BirthRecord, record_id)
        return _row_to_dict(row) if row else None
    finally:
        session.close()
