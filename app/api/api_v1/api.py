from fastapi import APIRouter

from app.api.api_v1.endpoints import cat, home, customer

api_router = APIRouter()
api_router.include_router(home.router)
api_router.include_router(cat.router, prefix="/cats", tags=["cats"])
api_router.include_router(customer.router, prefix="/owners", tags=["owners"])