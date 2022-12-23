from fastapi import APIRouter, Depends, HTTPException, Query, status
# from sqlalchemy.ext.asyncio import Session
from sqlalchemy.orm import Session
from typing import Any, Optional, List

from app.crud import crud_customer, crud_cat
from app.api import deps

from app.schemas.customer import Customer, CustomerFull, CustomerCreate, CustomerUpdate

router = APIRouter()


@router.get("/", status_code=200, response_model=List[CustomerFull])
def get_all_customers(
        *, db: Session = Depends(deps.get_db)
) -> List[Optional[CustomerFull]]:
    # results = await crud.customer.get_multi(db=db, skip=0, limit=10)
    results = crud_customer.customer.get_multi(db=db, skip=0, limit=10)

    return results


@router.get("/search", status_code=200, response_model=List[CustomerFull])
def search_customers(
        *,
        search_name: Optional[str] = Query(None, min_length=3, example="Bob"),
        max_results: Optional[int] = 10,
        db: Session = Depends(deps.get_db),
) -> List[Optional[CustomerFull]]:
    """
    Search for customers based on theirs name
    """
    # results = await crud.cat.get_multi_by_name(db=db, limit=max_results, name=search_name)
    results = crud_customer.customer.get_multi_by_name(db=db, limit=max_results, name=search_name)
    return results


@router.get("/search-by-cat-name", status_code=200, response_model=List[CustomerFull])
def search_customers_by_cat_name(
        *,
        cat_name: Optional[str] = Query(None, min_length=3, example="Smokey"),
        max_results: Optional[int] = 10,
        db: Session = Depends(deps.get_db),
) -> List[Optional[CustomerFull]]:
    """
    Search for customers based on names of their cats
    """
    # results = await crud.cat.get_multi_by_name(db=db, limit=max_results, name=search_name)
    results = crud_customer.customer.get_multi_by_cat_name(db=db, limit=max_results, cat_name=cat_name)
    return results


@router.get("/{customer_id}", status_code=200, response_model=CustomerFull)
def find_customer(
        *,
        customer_id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single customer by ID
    """
    # result = await crud.customer.get(db=db, id=customer_id)
    result = crud_customer.customer.get(db=db, id=customer_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Owner you are looking for (ID {customer_id}) not found! :("
        )

    return result


@router.post("/post", status_code=201, response_model=CustomerFull)
def create_customer(
        *, customer_in: CustomerCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new customer entry in the database.
    """

    # customer = await crud.customer.create(db=db, obj_in=customer_in)
    customer = crud_customer.customer.create(db=db, obj_in=customer_in)

    return customer


@router.post("/add-customer-cat", status_code=201, response_model=CustomerFull)
def customer_add_cat(
        *, db: Session = Depends(deps.get_db), customer_id: int, cat_id: int
) -> CustomerFull:
    """
        Update the cats.
    """
    cat_obj = crud_cat.cat.get(db=db, id=cat_id)
    customer_obj = crud_customer.customer.get(db=db, id=customer_id)
    if not cat_obj:
        raise HTTPException(status_code=404, detail="Cat not found")
    if not customer_obj:
        raise HTTPException(status_code=404, detail="Customer (owner) not found")

    updated_customer = crud_customer.customer.add_cat(db=db, customer_obj=customer_obj, cat_obj=cat_obj)
    if not updated_customer:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Customer already has cat named {cat_obj.name} (id={cat_obj.id})")
    return updated_customer


@router.put("/update-customer/{customer_id}", status_code=200, response_model=CustomerFull)
def update_customer(
        *, customer_in: CustomerUpdate, customer_id: int, db: Session = Depends(deps.get_db)
) -> Any:
    # updated_customer = await crud.customer.update(db=db, obj_in=customer_in, db_obj_id=customer_id)
    # updated_customer = crud.customer.update(db=db, obj_in=customer_in, db_obj_id=customer_id)
    customer_obj = crud_customer.customer.get(db=db, id=customer_id)
    updated_customer = crud_customer.customer.update(db=db, obj_in=customer_in, db_obj=customer_obj)
    if not updated_customer:
        raise HTTPException(
            status_code=404, detail=f"Owner you want to update (ID {customer_id}) not found! :("
        )
    return updated_customer


@router.delete("/delete-customer/{customer_id}", status_code=200, response_model=CustomerFull)
def delete_customer(
        *, customer_id: int, db: Session = Depends(deps.get_db)
) -> CustomerFull:
    # deleted_customer = await crud.customer.remove(db=db, id=customer_id)
    deleted_customer = crud_customer.customer.remove(db=db, id=customer_id)
    return deleted_customer


@router.delete("/remove-customer-cat", status_code=201, response_model=CustomerFull)
def customer_remove_cat(
        *, db: Session = Depends(deps.get_db), customer_id: int, cat_id: int
) -> CustomerFull:
    """
        Update the cats.
    """
    cat_obj = crud_cat.cat.get(db=db, id=cat_id)
    customer_obj = crud_customer.customer.get(db=db, id=customer_id)
    if not cat_obj:
        raise HTTPException(status_code=404, detail="Cat not found")
    if not customer_obj:
        raise HTTPException(status_code=404, detail="Customer (owner) not found")

    updated_customer = crud_customer.customer.remove_cat(db=db, customer_obj=customer_obj, cat_obj=cat_obj)
    if not updated_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer (owner) doesn`t have cat named {cat_obj.name} (id={cat_obj.id})")
    return updated_customer
