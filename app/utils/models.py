from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime


Base = declarative_base()

# 🧑 사용자 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invitations = relationship("Invitation", back_populates="user", cascade="all, delete-orphan")


# 💌 청첩장 모델
class Invitation(Base):
    __tablename__ = "invitations"
    __table_args__ = {"extend_existing": True}  # 중복 정의 방지

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    groom_name = Column(String(100), nullable=False)
    bride_name = Column(String(100), nullable=False)
    wedding_date = Column(DateTime, nullable=False)
    location = Column(String(255))
    message = Column(String(1000))
    bank_name = Column(String(50), nullable=True)
    account = Column(String(100), nullable=True)  
    security_code = Column(String(6), nullable=False)  

    user = relationship("User", back_populates="invitations")
    anniversaries = relationship("Anniversary", back_populates="invitation")
    photos = relationship("Photo", back_populates="invitation", cascade="all, delete-orphan")
    guests = relationship("Guest", back_populates="invitation", cascade="all, delete-orphan")

# 📸 사진 모델
class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id", ondelete="CASCADE"))
    photo_url = Column(String(500), nullable=False)
    style_tag = Column(String(50))  # 예: 메인, 커플, 식장 등
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    invitation = relationship("Invitation", back_populates="photos")

# 🧑‍🤝‍🧑 하객 RSVP 모델
class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    attending = Column(Boolean, nullable=False)  # 참석 여부
    num_guests = Column(Integer, default=0)      # 동반 인원
    message = Column(String(1000))

    invitation = relationship("Invitation", back_populates="guests")

class Anniversary(Base):
    __tablename__ = "anniversaries"

    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id"), nullable=False)
    anniversary_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)

    invitation = relationship("Invitation", back_populates="anniversaries")