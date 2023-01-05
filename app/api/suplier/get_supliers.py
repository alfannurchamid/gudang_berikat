from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.suplier import Suplier
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetSupliersResponseModel(BaseModel):
    data: List[object]


class GetSupliersDataResponsemodel(BaseResponseModel):
    data: GetSupliersResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'nama_suplier': 'Contoh Nama Suplier',
                        'asal_negara': 'CN'
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_supliers(session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Suplier.id_suplier,
            Suplier.nama_suplier,
            Suplier.asal_negara
        )
    ).all()
    datalist = []

    for Suplie in response:
        datalist.append(Suplie)

    return GetSupliersDataResponsemodel(data=GetSupliersResponseModel(
        data=datalist
    ))
