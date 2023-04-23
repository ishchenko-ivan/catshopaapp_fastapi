from fastapi import FastAPI, APIRouter
from app.api.api_v1.api import api_router
from app.core.config import settings

root_router = APIRouter()
app = FastAPI(
    title="Cats Pro Grooming",
    description="Groom your cats!",
    version="1.3.3.7",
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Beautiful faces smiling over us
