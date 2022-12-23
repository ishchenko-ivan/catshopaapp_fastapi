from fastapi import APIRouter, Depends, HTTPException, Query, status
# from sqlalchemy.ext.asyncio import Session
from sqlalchemy.orm import Session
from typing import Any, Optional, List

from app.crud import crud_cat, crud_customer
from app.api import deps
from app.schemas.cat import Cat, CatFull, CatCreate, CatUpdate

router = APIRouter()


@router.get("/", status_code=200, response_model=List[CatFull])
def get_all_cats(
        *, db: Session = Depends(deps.get_db)
) -> List[Optional[CatFull]]:
    # results = await crud.cat.get_multi(db=db, skip=0, limit=10)
    results = crud_cat.cat.get_multi(db=db, skip=0, limit=10)

    return results


@router.get("/search", status_code=200, response_model=List[CatFull])
def search_cats(
        *,
        search_name: Optional[str] = Query(None, min_length=3, example="Smokey"),
        max_results: Optional[int] = 10,
        db: Session = Depends(deps.get_db),
) -> List[Optional[CatFull]]:
    """
    Search for cats based on theirs name
    """
    # results = await crud.cat.get_multi_by_name(db=db, limit=max_results, name=search_name)
    results = crud_cat.cat.get_multi_by_name(db=db, limit=max_results, name=search_name)
    return results


@router.get("/{cat_id}", status_code=200, response_model=CatFull)
def find_cat(
        *,
        cat_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single cat by ID
    """
    # result = await crud.cat.get(db=db, id=cat_id)
    result = crud_cat.cat.get(db=db, id=cat_id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Kitty you are looking for (ID {cat_id}) not found! :("
        )

    return result


@router.post("/post-cat", status_code=201, response_model=CatFull)
def create_cat(
        *, cat_in: CatCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new cat entry in the database.
    """
    # if cat_in.owner_id == 0:
    #     cat_in.owner_id = None
    # cat = await crud.cat.create(db=db, obj_in=cat_in)
    cat = crud_cat.cat.create(db=db, obj_in=cat_in)

    return cat


@router.post("/add-cat-owner", status_code=201, response_model=CatFull)
def cat_add_owner(
        *, db: Session = Depends(deps.get_db), cat_id: int, owner_id: int
) -> CatFull:
    """
        Update the owners.
    """
    owner_obj = crud_customer.customer.get(db=db, id=owner_id)
    cat_obj = crud_cat.cat.get(db=db, id=cat_id)
    if not owner_obj:
        raise HTTPException(status_code=404, detail="Owner not found")
    if not cat_obj:
        raise HTTPException(status_code=404, detail="Cat not found")

    updated_cat = crud_cat.cat.add_owner(db=db, cat_obj=cat_obj, owner_obj=owner_obj)
    if not updated_cat:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Cat already has owner named {owner_obj.name} (id={owner_obj.id})")
    return updated_cat


@router.put("/update-cat/{cat_id}", status_code=200, response_model=CatFull)
def update_cat(
        *, cat_in: CatUpdate, cat_id: int, db: Session = Depends(deps.get_db)
) -> Any:
    # updated_cat = await crud.cat.update(db=db, obj_in=cat_in, db_obj_id=cat_id)
    cat_obj = crud_cat.cat.get(db=db, id=cat_id)
    updated_cat = crud_cat.cat.update(db=db, obj_in=cat_in, db_obj=cat_obj)
    if not updated_cat:
        raise HTTPException(
            status_code=404, detail=f"Kitty you want to update (ID {cat_id}) not found! :("
        )
    return updated_cat


@router.delete("/delete-cat/{cat_id}", status_code=200, response_model=CatFull)
def delete_cat(
        *, cat_id: int, db: Session = Depends(deps.get_db)
) -> CatFull:
    # deleted_cat = await crud.cat.remove(db=db, id=cat_id)
    deleted_cat = crud_cat.cat.remove(db=db, id=cat_id)
    return deleted_cat


@router.delete("/remove-cat-owner", status_code=201, response_model=CatFull)
def cat_remove_owner(
        *, db: Session = Depends(deps.get_db), cat_id: int, owner_id: int
) -> CatFull:
    """
        Update the owners.
    """
    owner_obj = crud_customer.customer.get(db=db, id=owner_id)
    cat_obj = crud_cat.cat.get(db=db, id=cat_id)
    if not owner_obj:
        raise HTTPException(status_code=404, detail="Owner not found")
    if not cat_obj:
        raise HTTPException(status_code=404, detail="Cat not found")

    updated_cat = crud_cat.cat.remove_owner(db=db, cat_obj=cat_obj, owner_obj=owner_obj)
    if not updated_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cat doesn`t have owner named {owner_obj.name} (id={owner_obj.id})")
    return updated_cat
