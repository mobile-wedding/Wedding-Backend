from app.utils.clip_model import get_image_features
from app.utils.gpt_model import get_style_tag_from_gpt
from app.crud import photo as crud_photo
from sqlalchemy.orm import Session
from PIL import Image
import requests
from io import BytesIO

def classify_photos_with_clip_and_gpt(db: Session, photos):
    for photo in photos:
        print(f"Processing photo {photo.id}: {photo.photo_url}")

        try:
            # 1. CLIP 피처 추출
            image_features = get_image_features(photo.photo_url)
            print(f"Extracted features for photo {photo.id}")

            # 2. GPT로 스타일 태그 요청
            style_tag = get_style_tag_from_gpt(image_features)
            print(f"GPT response for photo {photo.id}: {style_tag}")

            # 3. DB에 저장
            crud_photo.update_photo_style(db, photo.id, style_tag)
            print(f"Updated photo {photo.id} with tag: {style_tag}")

        except Exception as e:
            print(f"Error processing photo {photo.id}: {e}")