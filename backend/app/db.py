from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[1]
DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'devsentry.db'}")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
class Base(DeclarativeBase): pass
def get_db():
    db = Session()
    try: yield db
    finally: db.close()
