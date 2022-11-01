from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional

from app.crud import crud_customer as crud
from app.api import deps
# from app.schemas.customer import Cat, CatCreate, CatUpdate, CatSearchResults

router = APIRouter()
