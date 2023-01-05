from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.standar_doc import StandarDoc
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetStandarDocData(BaseModel):
    id_doc: str


class GetStandarDocResponseModel(BaseModel):
    nomor: str


class GetStandarDocDataResponsemodel(BaseResponseModel):
    data: GetStandarDocResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_doc': 'BC 2.3',
                    'nomor': '123456-123123-144123',
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_standar_doc(data: GetStandarDocData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            StandarDoc.nomor
        ).where(StandarDoc.id_doc == data.id_doc)
    ).fetchone()

    return GetStandarDocDataResponsemodel(data=GetStandarDocResponseModel(
        nomor=response.nomor
    ))
