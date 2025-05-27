from pydantic import BaseModel
from datetime import datetime

class PhotoResponse(BaseModel):
    id: int
    photo_url: str
    style_tag: str | None = None
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True