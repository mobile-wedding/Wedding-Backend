from pydantic import BaseModel
from datetime import date

class AnniversaryCreate(BaseModel):
    invitation_id: int
    anniversary_date: date
    description: str

class AnniversaryResponse(BaseModel):
    id: int
    invitation_id: int
    anniversary_date: date
    description: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2 대응 (구 orm_mode)