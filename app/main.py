from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, initialize_database
from app.utils.models import Base
from app.routers import user 
from app.routers import invitation # 현재 구현된 라우터만 먼저 등록
from app.routers import photo
from app.routers import classify
# FastAPI 앱 초기화
app = FastAPI(
    title="모바일 청첩장 API",
    description="GPT + CLIP 기반 사진 분류로 청첩장을 자동 생성하는 API",
    contact={
        "name": "jongbeom",
        "email": "sfhk199999@gmail.com",
    },
    redoc_url="/docs/redoc",
    openapi_url="/openapi.json",
)


# CORS 설정 (프론트엔드 주소에 맞게 수정)
origins = [
    "http://localhost:5173",  # 개발용
    "https://your-wedding-invitation.com",  # 실제 배포 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 테이블 생성 및 초기화
initialize_database()

# 라우터 등록
app.include_router(user.router, prefix="/api/user", tags=["Users"])
app.include_router(invitation.router, prefix="/api/invitation", tags=["Invitations"])
app.include_router(photo.router, prefix="/api")
app.include_router(classify.router)