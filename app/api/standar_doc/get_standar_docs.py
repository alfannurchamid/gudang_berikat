from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.standar_doc import StandarDoc
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetStandarDocsResponseModel(BaseModel):
    data: List[object]


class GetStandarDocsDataResponsemodel(BaseResponseModel):
    data: GetStandarDocsResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'id': 1,
                        'jenis': True,
                        'jenis_dokumen': "BC.23",
                        'tanggal': '2023-01-01',
                        'done': False
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_standar_docs(session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            StandarDoc.id_doc,
            StandarDoc.nomor,
            StandarDoc.jenis,
            StandarDoc.jenis_dokumen,
            StandarDoc.tanggal,
            StandarDoc.done
        )
    ).all()
    datalist = []

    for Bara in response:
        datalist.append(Bara)

    return GetStandarDocsDataResponsemodel(data=GetStandarDocsResponseModel(
        data=datalist
    ))
