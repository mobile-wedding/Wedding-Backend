from sqlalchemy.orm import Session
from app.utils.clip_model import get_image_features
from app.utils.gpt_model import get_photo_order_from_gpt
from app.crud import photo as crud_photo

def arrange_photos_with_gpt(db: Session, photos):
    photo_data = []
    
    for photo in photos:
        caption = get_image_features(photo.photo_url)
        photo_data.append({
            "id": photo.id,
            "style": photo.style_tag or "없음",
            "caption": caption
        })

    photo_order = get_photo_order_from_gpt(photo_data)

    for order, photo_id in enumerate(photo_order):
        crud_photo.update_photo_order(db, photo_id, order)