from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.akun import Akun
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetAkunData(BaseModel):
    id_akun: str


class GetAkunResponseModel(BaseModel):
    id_akun: str
    nama_akun: str
    kategori_akun: str
    pos_akun_debit: bool


class GetAkunDataResponsemodel(BaseResponseModel):
    data: GetAkunResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_akun': '1',
                    'nama_akun': 'Contoh Nama akun',
                    'pos_kredit_akun': True,
                    'kategori_akun': 'sumber'
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_akun(data: GetAkunData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Akun.nama_akun,
            Akun.kategori_akun,
            Akun.pos_akun_debit
        ).where(Akun.id_akun == data.id_akun)
    ).fetchone()

    return GetAkunDataResponsemodel(data=GetAkunResponseModel(
        id_akun=data.id_akun,
        nama_akun=response.nama_akun,
        kategori_akun=response.kategori_akun,
        pos_akun_debit=response.pos_akun_debit
    ))
