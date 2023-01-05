from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.akun import Akun
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddAkunData(BaseModel):
    nama_akun: str
    kategoti_akun: str
    pos_akun_debit: bool


async def add_akun(data: AddAkunData, session=Depends(get_db_session)):

    with Session(db_engine) as session:
        akun = Akun(
            nama_akun=data.nama_akun,
            kategori_akun=data.kategoti_akun,
            pos_akun_debit=data.pos_akun_debit

        )
        session.add(akun)
        session.commit()

        return Response(status_code=204)
