from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL


# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
engine = create_async_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
