from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.utils.mailer import send_email
from app.utils.models import Invitation, User
from datetime import datetime, timedelta

def send_anniversary_reminders():
    db: Session = SessionLocal()
    today = datetime.date()

    invitations = db.query(Invitation).join(User).filter(
        (Invitation.wedding_date + timedelta(days=365)).cast(Date) == today
    ).all()

    for invitation in invitations:
        user_email = invitation.user.email
        groom = invitation.groom_name
        bride = invitation.bride_name

        subject = f"🎉 {groom} & {bride}님의 결혼 1주년을 축하드립니다!"
        body = f"""
        안녕하세요,

            오늘은 {groom}님과 {bride}님의 결혼 1주년입니다!
        모바일 청첩장 서비스를 이용해 주셔서 감사합니다.

        앞으로도 행복한 날만 가득하길 바랍니다 💍💐

        - 모바일 청첩장 팀
        """
        send_email(user_email, subject, body)
        print(f"✅ 이메일 전송 완료: {user_email}")

    db.close()

if __name__ == "__main__":
    send_anniversary_reminders()