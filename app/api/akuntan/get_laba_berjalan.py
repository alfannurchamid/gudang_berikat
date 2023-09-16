import datetime
from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.api_models import BaseResponseModel
from app.dependencies.get_db_session import get_db_session
from typing import List, Optional


from app.models.regulator_jurnal import RegulatorJurnal
from app.models.jurnal_umum import JurnalUmum
from app.models.akun import Akun


from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog


class GetLabaResponseModel(BaseModel):
    saldo: int


class GetLabaBerjalanDataResponsemodel(BaseResponseModel):
    data: GetLabaResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_akun': '1',
                    'nama_akun': 'Contoh Nama akun',
                    'pos_kredit_akun': True
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_laba_berjalan(tanggal: datetime.date, session=Depends(get_db_session)):
    response = session.execute(sa.text(
        f"SELECT saldo FROM jurnal_umun WHERE id_akun = '3.5' ORDER BY id_jurnal DESC LIMIT 1"))
    return GetLabaBerjalanDataResponsemodel(data=GetLabaResponseModel(saldo=response))
