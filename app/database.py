import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# Load .env file
load_dotenv()

# ✅ MySQL 접속 URL 구성
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

# 디버깅을 위한 출력
print(f"Database connection URL: mysql+pymysql://{MYSQL_USER}:****@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# ✅ SQLAlchemy 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# ✅ 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ 모델 Base
Base = declarative_base()

# ✅ FastAPI 의존성으로 쓸 DB 세션
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ DB 테이블 초기화 함수
def initialize_database():
    from app.utils.models import Base
    Base.metadata.create_all(bind=engine)