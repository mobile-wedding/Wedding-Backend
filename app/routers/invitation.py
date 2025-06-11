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

# ✅ 5. 보안코드 검증 API
@router.get("/verify/{invitation_id}/{code}")
def verify_security_code(invitation_id: int, code: str, db: Session = Depends(get_db)):
    invitation = crud_invitation.find_invitation(db, invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    if invitation.security_code != code:
        raise HTTPException(status_code=403, detail="Invalid security code")
    
    return {"message": "Security code verified"}