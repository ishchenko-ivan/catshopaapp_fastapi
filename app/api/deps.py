from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal


# def get_db() -> Generator:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with SessionLocal() as session:
        yield session
        await session.commit()