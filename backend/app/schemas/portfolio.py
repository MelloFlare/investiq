from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PortfolioCreate(BaseModel):
    user_id: UUID
    name: str

class PortfolioResponse(PortfolioCreate):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
