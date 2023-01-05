
# tessssssssssssssssssssssssssssssssssssssssssssssssss

# from typing import List

# from fastapi import (BackgroundTasks, Depends, File, Form, HTTPException,
#                      UploadFile, status)
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
# from pydantic import BaseModel, EmailStr

# from app.config import config
# from app.models import user

# conf = ConnectionConfig(
#     MAIL_USERNAME=config.EMAIL,
#     MAIL_PASSWORD=config.PASSWORD,
#     MAIL_FROM=config.EMAIL,
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )


# class EmailSchema(BaseModel):
#     email: List[EmailStr]


# async def send_email(email: EmailSchema, username: str):

#     message = MessageSchema(
#         subject="veryfikasi akun surveyer BSPN ",
#         recipients=email.email,
#         body="1234",
#         subtype='html'  # type: ignore
#     )
#     return
