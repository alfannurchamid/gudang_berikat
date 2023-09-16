from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.standar_doc import StandarDoc
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetStandarDocIdData(BaseModel):
    jenis: bool
    jenis_dok: str


class GetStandarDocIdsResponseModel(BaseModel):
    data: List[object]


class GetStandarDocIdsDataResponsemodel(BaseResponseModel):
    data: GetStandarDocIdsResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'id_doc': '00494C10009GH',
                        'nomor_daftar': '780966'
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_standar_docs_id(data: GetStandarDocIdData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            StandarDoc.id_doc,
            StandarDoc.nomor,
            StandarDoc.jenis_dokumen,
            StandarDoc.jenis,
            StandarDoc.tanggal,
            StandarDoc.done
        ).where(StandarDoc.jenis_dokumen == data.jenis_dok, StandarDoc.jenis == data.jenis and StandarDoc.done == False)
    ).all()
    datalist = []

    for Bara in response:
        print(Bara)
        print(data.jenis_dok)
        datalist.append(Bara)

    return GetStandarDocIdsDataResponsemodel(data=GetStandarDocIdsResponseModel(
        data=datalist
    ))
