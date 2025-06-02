from sqlalchemy.orm import Session
from app.utils.models import Photo
from app.schemas.photo import PhotoCreate
from sqlalchemy.orm import Session


def create_photo(db: Session, photo_data: PhotoCreate):
    photo = Photo(**photo_data.model_dump())
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

def update_photo_style(db: Session, photo_id: int, style_tag: str):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        photo.style_tag = style_tag
        db.commit()
        db.refresh(photo)
    return photo

def get_photos_by_invitation(db: Session, invitation_id: int):
    return db.query(Photo).filter(Photo.invitation_id == invitation_id).all()

def update_photo_order(db: Session, photo_id: int, order: int):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        photo.order = order
        db.commit()