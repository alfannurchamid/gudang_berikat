from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.akun import Akun
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetAkunsResponseModel(BaseModel):
    data: List[object]


class GetAkunsDataResponsemodel(BaseResponseModel):
    data: GetAkunsResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'id_akun': '1',
                        'nama_akun': 'Contoh Nama akun',
                        'pos_kredit_akun': True,
                        'kategori_akun': 'sumber'
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_akuns(session=Depends(get_db_session)):
    response = session.execute(
        sa.text("SELECT * FROM akun")
    ).all()
    datalist = []

    for Akuna in response:
        # print(Akuna.pos_akun_debit)
        datalist.append(Akuna)

    return GetAkunsDataResponsemodel(data=GetAkunsResponseModel(
        data=datalist
    ))
