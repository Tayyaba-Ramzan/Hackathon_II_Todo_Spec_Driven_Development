from sqlmodel import create_engine, Session
from typing import Generator
from fastapi import Depends
from settings import settings  # Import settings from the centralized settings module

# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=True  # Set to True to see SQL queries in the logs
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to provide database sessions.
    """
    with Session(engine) as session:
        yield session