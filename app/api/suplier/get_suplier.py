from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.suplier import Suplier
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetSuplierData(BaseModel):
    id_suplier: str


class GetSuplierResponseModel(BaseModel):
    id_suplier: str
    nama_suplier: str
    asal_negara: str


class GetSuplierDataResponsemodel(BaseResponseModel):
    data: GetSuplierResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_suplier': '00494C10009GH',
                    'nama_suplier': 'kainddariluar 100persen cotton',
                    'asal_negara': 'KGM'
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_suplier(data: GetSuplierData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Suplier.nama_suplier,
            Suplier.asal_negara
        ).where(Suplier.id_suplier == data.id_suplier)
    ).fetchone()

    return GetSuplierDataResponsemodel(data=GetSuplierResponseModel(

        id_suplier=data.id_suplier,
        nama_suplier=response.nama_suplier,
        asal_negara=response.asal_negara
    ))
