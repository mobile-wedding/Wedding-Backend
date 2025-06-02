from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import photo as crud_photo
from app.service.layout import arrange_photos_with_gpt

router = APIRouter(prefix="/photo", tags=["Photo"])

@router.post("/layout/{invitation_id}")
def layout_photos(invitation_id: int, db: Session = Depends(get_db)):
    photos = crud_photo.get_photos_by_invitation(db, invitation_id)
    
    if not photos:
        raise HTTPException(status_code=404, detail="No photos found for this invitation")

    try:
        arrange_photos_with_gpt(db, photos)
        return {"message": "Photo layout arranged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))