from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.anniversary import AnniversaryCreate, AnniversaryResponse
from app.crud import anniversary as crud_anniv
from app.database import get_db

router = APIRouter(prefix="/api/anniversary", tags=["Anniversary"])

@router.post("/", response_model=AnniversaryResponse)
def create_anniversary(anniv: AnniversaryCreate, db: Session = Depends(get_db)):
    return crud_anniv.create_anniversary(db, anniv)

@router.get("/{invitation_id}", response_model=list[AnniversaryResponse])
def get_by_invitation(invitation_id: int, db: Session = Depends(get_db)):
    return crud_anniv.get_anniversaries_by_invitation(db, invitation_id)