# Python 3.9 이미지 사용
FROM python:3.12.6-slim

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "wedding_backend:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]