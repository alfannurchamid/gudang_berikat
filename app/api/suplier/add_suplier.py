from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.suplier import Suplier
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddSuplierData(BaseModel):
    nama_suplier: str
    asal_negara: str


async def add_suplier(data: AddSuplierData, session=Depends(get_db_session)):

    with Session(db_engine) as session:
        suplier = Suplier(
            nama_suplier=data.nama_suplier, asal_negara=data.asal_negara
        )
        session.add(suplier)
        session.commit()

        return Response(status_code=204)
