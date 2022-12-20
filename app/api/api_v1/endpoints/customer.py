from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional, List

from app.crud import crud_customer as crud
from app.api import deps
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get("/", status_code=200, response_model=List[Customer])
async def get_all_customers(
        *, db: AsyncSession = Depends(deps.get_db)
) -> List[Optional[Customer]]:
    results = await crud.customer.get_multi(db=db, skip=0, limit=10)

    return results


@router.get("/{customer_id}", status_code=200, response_model=Customer)
async def find_customer(
        *,
        customer_id: int,
        db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single customer by ID
    """
    result = await crud.customer.get(db=db, id=customer_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Owner you are looking for (ID {customer_id}) not found! :("
        )

    return result


# @router.get("/search-by-cat/", status_code=200, response_model=List[Customer])
# async def search_customers(
#         *,
#         search_name: Optional[str] = Query(None, min_length=3, example="Smokey"),
#         max_results: Optional[int] = 10,
#         db: AsyncSession = Depends(deps.get_db),
# ) -> List[Optional[Cat]]:
#     """
#     Search for cats based on theirs name
#     """
#     results = await crud.cat.get_multi_by_name(db=db, limit=max_results, name=search_name)
#     return results


@router.post("/post", status_code=201, response_model=Customer)
async def create_customer(
        *, customer_in: CustomerCreate, db: AsyncSession = Depends(deps.get_db)
) -> dict:
    """
    Create a new customer entry in the database.
    """

    customer = await crud.customer.create(db=db, obj_in=customer_in)

    return customer


@router.put("/update-customer/{customer_id}", status_code=200, response_model=Customer)
async def update_customer(
        *, customer_in: CustomerUpdate, customer_id: int, db: AsyncSession = Depends(deps.get_db)
) -> Any:
    updated_customer = await crud.customer.update(db=db, obj_in=customer_in, db_obj_id=customer_id)
    if not updated_customer:
        raise HTTPException(
            status_code=404, detail=f"Owner you want to update (ID {customer_id}) not found! :("
        )
    return updated_customer


@router.delete("/delete-customer/{customer_id}", status_code=200, response_model=Customer)
async def delete_customer(
        *, customer_id: int, db: AsyncSession = Depends(deps.get_db)
) -> Customer:
    deleted_customer = await crud.customer.remove(db=db, id=customer_id)
    return deleted_customer
