from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Session  #Session is SQLAlchemy's object used to interact with the database.
from collections.abc import Generator   #Generator is used here mainly for type hinting.
from app.core.config import settings

class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.database_url,
    echo=True,
)

# Create a database session → give it to FastAPI → close it when the request is finished.
def get_db() -> Generator[Session, None, None]:   #This function is a generator that yields Session objects.
    db = SessionLocal()  #SessionLocal is a session factory.

    try:           #The try is there because we want to guarantee that the database session gets closed afterward.
        yield db   #Here is the database session. Use it. When you're finished, come back here and I'll clean it up."
    finally:
        db.close()
        

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)