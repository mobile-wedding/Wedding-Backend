from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InvitationCreate(BaseModel):
    groom_name: str
    bride_name: str
    wedding_date: datetime
    location: str
    message: str

class InvitationResponse(BaseModel):
    id: int
    groom_name: str
    bride_name: str
    wedding_date: datetime
    location: str
    message: str
    security_code: str  
    
    class Config:
        from_attributes = True  

class InvitationUpdate(BaseModel):
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    wedding_date: Optional[datetime] = None
    location: Optional[str] = None
    message: Optional[str] = None