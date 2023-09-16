from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.suplier import Suplier
from sqlalchemy.orm import Session
from app.utils.db import db_engine

from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog


class AddSuplierData(BaseModel):
    nama_suplier: str
    asal_negara: str


async def add_suplier(data: AddSuplierData, payload=Depends(Autentication()), session=Depends(get_db_session)):

    with Session(db_engine) as session:
        suplier = Suplier(
            nama_suplier=data.nama_suplier, asal_negara=data.asal_negara
        )

        user_id = payload.get('uid', 0)
        user_log = UserLog(
            id_user=user_id, jenis='sup_add', keterangan=f"menambah suplier {data.nama_suplier}")

        session.add(user_log)

        session.add(suplier)
        session.commit()

        return Response(status_code=204)
