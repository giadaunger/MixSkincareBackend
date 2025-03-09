from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Skapar databastabeller om de inte redan finns."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Hantera databassessioner."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
