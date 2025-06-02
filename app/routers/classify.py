
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.classify import classify_photos_with_clip_and_gpt
from app.crud import photo as crud_photo

router = APIRouter()

@router.post("/classify/{invitation_id}")
def classify_photos(invitation_id: int, db: Session = Depends(get_db)):
    photos = crud_photo.get_photos_by_invitation(db, invitation_id)

    if not photos:
        raise HTTPException(status_code=404, detail="No photos found for this invitation")

    try:
        classify_photos_with_clip_and_gpt(db, photos)
        return {"message": "Photos classified successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
