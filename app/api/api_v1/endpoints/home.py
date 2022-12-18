from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_cat as crud
from app.api import deps
from app.schemas.cat import Cat
from typing import List, Optional

router = APIRouter()


@router.get("/", status_code=200, response_model=List[Cat])
async def get_all_cats(
        *, db: AsyncSession = Depends(deps.get_db)
) -> List[Optional[Cat]]:
    results = await crud.cat.get_multi_by_name(db=db, limit=10, name="")

    return results
