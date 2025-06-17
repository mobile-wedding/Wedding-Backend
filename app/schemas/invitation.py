from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InvitationBase(BaseModel):
    groom_name: str
    bride_name: str
    wedding_date: datetime
    location: str
    message: str
    bank_name: Optional[str] = None
    account: Optional[str] = None

class InvitationCreate(InvitationBase):
    pass

class InvitationResponse(InvitationBase):
    id: int
    security_code: str
    user_id: int
    
    class Config:
        from_attributes = True

class InvitationUpdate(BaseModel):
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    wedding_date: Optional[datetime] = None
    location: Optional[str] = None
    message: Optional[str] = None