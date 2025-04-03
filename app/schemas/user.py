from pydantic import BaseModel, EmailStr

# 🔐 회원가입 요청용
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 🔑 로그인 요청용
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 👤 유저 정보 응답용
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# 🔑 로그인 응답용
class LoginResponse(BaseModel):
    message: str
    user_id: int
    email: str