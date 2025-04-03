from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.database import get_db

router = APIRouter(
    prefix="",
    tags=["Users"]
)

# 회원가입 API
@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 기존 이메일 중복 체크 함수가 없으면 아래처럼 직접 처리
    existing_user = db.query(crud_user.User).filter(crud_user.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)

# 특정 사용자 조회 API
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.find_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 사용자 삭제 API
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = crud_user.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# 로그인 API
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.login_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": db_user.id, "email": db_user.email}