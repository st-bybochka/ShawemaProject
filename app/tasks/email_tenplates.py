from email.message import EmailMessage

from pydantic import EmailStr
from app.config import settings

def create_register_email(
        data: dict,
        email_to: EmailStr,
):
    email = EmailMessage()
    email["Subject"] = "Подтверждение регистрации"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Подтвердите регистрацию на сайте</h1>
        """,
        subtype="html"
    )
    return email