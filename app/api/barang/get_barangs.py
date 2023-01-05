from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetBarangsResponseModel(BaseModel):
    data: List[object]


class GetBarangsDataResponsemodel(BaseResponseModel):
    data: GetBarangsResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'kode_barang': '00494C10009GH',
                        'nama_barang': 'kainddariluar 100persen cotton',
                        'satuan': 'KGM',
                        'saldo': 30230,
                        'harga': 1,
                        'lokasi': 'D'
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_barangs(session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Barang.kode_barang,
            Barang.nama_barang,
            Barang.harga,
            Barang.lokasi,
            Barang.saldo,
            Barang.satuan
        )
    ).all()
    datalist = []

    for Bara in response:
        datalist.append(Bara)

    return GetBarangsDataResponsemodel(data=GetBarangsResponseModel(
        data=datalist
    ))
