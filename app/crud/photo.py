from sqlalchemy.orm import Session
from app.utils.models import Photo

def create_photo(db: Session, photo_url: str):
    photo = Photo(photo_url=photo_url)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

def get_all_photos(db: Session):
    return db.query(Photo).filter(Photo.is_deleted == False).all()

def get_photo_by_id(db: Session, photo_id: int):
    return db.query(Photo).filter(Photo.id == photo_id).first()

def delete_photo(db: Session, photo_id: int):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        return None
    db.delete(photo)
    db.commit()
    return True