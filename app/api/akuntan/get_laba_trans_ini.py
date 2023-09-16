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


class GetLabaTransIni(BaseModel):
    saldo: int


class GetLabaIniResponseModel(BaseResponseModel):
    data: GetLabaTransIni

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


async def get_laba_trans_ini(id_akun: str, no_daftar: str, session=Depends(get_db_session)):
    response = session.execute(sa.text(
        f'''select kredit from jurnal_umum WHERE keterangan LIKE "%pengeluaran%{no_daftar}%" AND id_akun ="{id_akun}" LIMIT 1 ''')).scalar()
    print(id_akun, no_daftar)
    # print(type(response))
    # print(response)
    return GetLabaIniResponseModel(data=GetLabaTransIni(saldo=response))
