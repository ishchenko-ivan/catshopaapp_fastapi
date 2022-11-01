from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional, List

from app.crud import crud_cat as crud
from app.api import deps
from app.schemas.cat import Cat, CatCreate, CatUpdate

router = APIRouter()


@router.get("/{cat_id}", status_code=200, response_model=Cat)
async def find_cat(
        *,
        cat_id: int,
        db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single cat by ID
    """
    result = await crud.cat.get(db=db, id=cat_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Kitty you are looking for (ID {cat_id}) not found! :("
        )

    return result


@router.get("/search/", status_code=200, response_model=List[Cat])
async def search_cats(
        *,
        search_name: Optional[str] = Query(None, min_length=3, example="Smokey"),
        max_results: Optional[int] = 10,
        db: AsyncSession = Depends(deps.get_db),
) -> List[Optional[Cat]]:
    """
    Search for cats based on theirs name
    """
    results = await crud.cat.get_multi_by_name(db=db, limit=max_results, name=search_name)
    return results


@router.post("/", status_code=201, response_model=Cat)
async def create_cat(
        *, cat_in: CatCreate, db: AsyncSession = Depends(deps.get_db)
) -> dict:
    """
    Create a new cat entry in the database.
    """
    if cat_in.owner_id == 0:
        cat_in.owner_id = None
    cat = await crud.cat.create(db=db, obj_in=cat_in)

    return cat


@router.put("/update-cat/{cat_id}", status_code=200, response_model=Cat)
async def update_cat(
        *, cat_in: CatUpdate, cat_id: int, db: AsyncSession = Depends(deps.get_db)
) -> Any:
    updated_cat = await crud.cat.update(db=db, obj_in=cat_in, db_obj_id=cat_id)
    if not updated_cat:
        raise HTTPException(
            status_code=404, detail=f"Kitty you want to update (ID {cat_id}) not found! :("
        )
    return updated_cat


@router.delete("/delete-cat/{cat_id}", status_code=200, response_model=Cat)
async def delete_cat (
        *, cat_id: int, db: AsyncSession = Depends(deps.get_db)
) -> Cat:
    deleted_cat = await crud.cat.remove(db=db, id=cat_id)
    return deleted_cat
