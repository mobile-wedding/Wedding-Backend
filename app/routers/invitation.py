# app/routers/invitation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.invitation import InvitationCreate, InvitationUpdate
from app.crud import invitation as crud_invitation

router = APIRouter(
    prefix="",
    tags=["Invitations"]
)

# 청첩장 생성 API
@router.post("/{user_id}")
def create_invitation(user_id: int, invitation: InvitationCreate, db: Session = Depends(get_db)):
    return crud_invitation.create_invitation(db, user_id, invitation)

# 청첩장 조회 API
@router.get("/{invitation_id}")
def get_invitation(invitation_id: int, db: Session = Depends(get_db)):
    return crud_invitation.find_invitation(db, invitation_id)

@router.patch("/{invitation_id}")
def update_invitation(invitation_id: int, update_data: InvitationUpdate, db: Session = Depends(get_db)):
    return crud_invitation.update_invitation(db, invitation_id, update_data)

@router.delete("/{invitation_id}")
def delete_invitation(invitation_id: int, db: Session = Depends(get_db)):
    result = crud_invitation.delete_invitation(db, invitation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return {"message": "Invitation deleted successfully"}