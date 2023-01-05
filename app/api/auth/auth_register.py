import email
from os import access
from tabnanny import check
from pydantic import BaseModel, root_validator
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from werkzeug.security import generate_password_hash

from app.dependencies.get_db_session import get_db_session
from app.models.user import User


class RegisterData(BaseModel):
    username: str
    full_name: str
    noWa: str
    access: int
    jabatan: str
    password: str
    confirm_password: str

    @root_validator
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if confirm_password != password:
            raise ValueError('Confirm password tidak cocok')

        return values


async def auth_register(data: RegisterData, session=Depends(get_db_session)):
    # check ussername already existed

    # check_email = session.execute(
    #     sa.select(User.id).where(User.email == data.email)
    # ).scalar()
    # if check_email:
    #     raise HTTPException(
    #         400, detail='email sudah digunakan ,silahkan gunakan email lain ')
    check_noWa = session.execute(
        sa.select(User.id_user).where(User.noWa == data.noWa)
    ).scalar()
    if check_noWa:
        raise HTTPException(
            400, detail='nomor whatsapp sudah digunakan ,silahkan gunakan nomor lain ')

    check_username = session.execute(
        sa.select(User.id_user).where(User.username == data.username)
    ).scalar()
    if check_username:
        raise HTTPException(
            400, detail='username sudah digunakan ,silahkan coba username lain')

    encripted_password = generate_password_hash(data.password)

    user = User(
        username=data.username,
        full_name=data.full_name,
        password=encripted_password,
        jabatan=data.jabatan,
        noWa=data.noWa,
        access=data.access,
    )

    session.add(user)
    session.commit()

    return Response(status_code=201)
