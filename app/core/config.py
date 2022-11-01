from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union
#= "postgresql://postgres:secret@localhost:5432/items"


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str

    class Config:
        case_sensitive = True


settings = Settings()
