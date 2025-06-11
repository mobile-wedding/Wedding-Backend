from sqlalchemy.orm import Session
from app.utils.models import Anniversary
from app.schemas.anniversary import AnniversaryCreate

def create_anniversary(db: Session, anniv: AnniversaryCreate):
    new_anniv = Anniversary(
        invitation_id=anniv.invitation_id,
        anniversary_date=anniv.anniversary_date,
        description=anniv.description
    )
    db.add(new_anniv)
    db.commit()
    db.refresh(new_anniv)
    return new_anniv

def get_anniversaries_by_invitation(db: Session, invitation_id: int):
    return db.query(Anniversary).filter(Anniversary.invitation_id == invitation_id).all()