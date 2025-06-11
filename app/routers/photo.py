from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import photo as crud_photo
from app.schemas.photo import PhotoResponse
from app.utils.s3 import upload_files_to_s3
from app.schemas.photo import PhotoCreate

router = APIRouter(
    prefix="/photo",
    tags=["Photo"]
)

@router.post("/upload")
async def upload_photos(
    invitation_id: int = Form(...),   # ✅ invitation_id를 form에서 받음
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        upload_targets = [(f.file, f.filename, f.content_type) for f in files]
        urls = upload_files_to_s3(upload_targets)

        for url in urls:
            photo_data = PhotoCreate(photo_url=url, invitation_id=invitation_id)
            crud_photo.create_photo(db, photo_data)

        return {"uploaded_urls": urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PhotoResponse])
def get_all_photos(db: Session = Depends(get_db)):
    return crud_photo.get_all_photos(db)

@router.delete("/{photo_id}")
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = crud_photo.get_photo_by_id(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    try:
        crud_photo.delete_photo(db, photo_id)
        return {"message": "Photo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{invitation_id}", response_model=List[PhotoResponse])
def get_photos_by_invitation(invitation_id: int, db: Session = Depends(get_db)):
    return crud_photo.get_photos_by_invitation_id(db, invitation_id)