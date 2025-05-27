import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# S3 클라이언트 생성
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file_obj, filename: str, content_type: str) -> str:
    """S3에 파일 업로드하고 URL 리턴"""
    s3.upload_fileobj(
        file_obj,
        AWS_S3_BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": content_type}
    )
    file_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
    return file_url


def upload_files_to_s3(files: list[tuple], folder: str = "") -> list[str]:
    urls = []
    for file_obj, filename, content_type in files:
        key = f"{folder}/{filename}" if folder else filename
        s3.upload_fileobj(
            file_obj,
            AWS_S3_BUCKET_NAME,
            key,
            ExtraArgs={"ContentType": content_type}
        )
        file_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        urls.append(file_url)
    return urls