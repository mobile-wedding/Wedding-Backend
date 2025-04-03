from sqlalchemy.orm import Session
from app.utils.models import User
from app.schemas.user import UserCreate, UserLogin
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1️⃣ 사용자 생성 (회원가입)
def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2️⃣ 특정 사용자 조회 (ID로)
def find_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 3️⃣ 사용자 삭제 (탈퇴)
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    return None

# 4️⃣ 사용자 로그인 (이메일 + 비밀번호 검증)
def login_user(db: Session, login_data: UserLogin):
    db_user = db.query(User).filter(User.email == login_data.email).first()
    if db_user and pwd_context.verify(login_data.password, db_user.password_hash):
        return db_user
    return None