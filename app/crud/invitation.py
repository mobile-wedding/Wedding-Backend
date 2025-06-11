from sqlalchemy.orm import Session
from app.utils.models import Invitation
from app.schemas.invitation import InvitationCreate, InvitationUpdate
from fastapi import HTTPException
from app.utils.security import generate_security_code
from datetime import timedelta
from app.utils.models import Anniversary

def create_invitation(db: Session, user_id: int, invitation: InvitationCreate):
    try:
        new_invite = Invitation(
            user_id=user_id,
            groom_name=invitation.groom_name,
            bride_name=invitation.bride_name,
            wedding_date=invitation.wedding_date,
            location=invitation.location,
            message=invitation.message,
            security_code=generate_security_code()
        )
        db.add(new_invite)
        db.commit()
        db.refresh(new_invite)

        try:
            # ✅ 1주년 기념일 생성
            one_year = new_invite.wedding_date + timedelta(days=365)
            anniversary = Anniversary(
                invitation_id=new_invite.id,
                anniversary_date=one_year,
                description="1주년 리마인드"
            )
            db.add(anniversary)
            db.commit()
        except Exception as e:
            print("❌ Anniversary 저장 실패:", e)

        return new_invite
    except Exception as e:
        db.rollback()
        print("❌ Invitation 저장 실패:", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create invitation: {str(e)}")

def find_invitation(db: Session, invitation_id: int):
    invite = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return invite

def update_invitation(db: Session, invitation_id: int, update_data: InvitationUpdate):
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # ✅ 수정하려는 필드만 업데이트
    update_fields = update_data.dict(exclude_unset=True)  # 입력된 것만 추출
    for key, value in update_fields.items():
        setattr(invitation, key, value)

    db.commit()
    db.refresh(invitation)
    return invitation

def delete_invitation(db: Session, invitation_id: int):
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invitation:
        return None
    db.delete(invitation)
    db.commit()
    return True