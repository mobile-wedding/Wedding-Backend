from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PhotoCreate(BaseModel):
    invitation_id: int
    photo_url: str
    style_tag: Optional[str] = None

class PhotoResponse(BaseModel):
    id: int
    invitation_id: Optional[int]  # ✅ None을 허용
    photo_url: str
    style_tag: Optional[str]
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True