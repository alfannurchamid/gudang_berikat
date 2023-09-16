from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.dependencies.autentication import Autentication

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.standar_doc import StandarDoc
from sqlalchemy.orm import Session
from app.models.user_log import UserLog
from app.utils.db import db_engine
import datetime


class AddStandarDocData(BaseModel):
    nomor: str
    jenis: bool
    jenis_dokumen: str
    tanggal: datetime.date


async def add_standar_doc(data: AddStandarDocData, payload=Depends(Autentication()), session=Depends(get_db_session)):

    with Session(db_engine) as session:
        standar_doc = StandarDoc(
            nomor=data.nomor,
            jenis=data.jenis,
            jenis_dokumen=data.jenis_dokumen,
            tanggal=data.tanggal
        )
        session.add(standar_doc)
        user_id = payload.get('uid', 0)

        jenis_nya = "t_out_add"

        jenis_dokumen = "penjualan"
        if data.jenis:
            jenis_dokumen = "pemasukan"
            jenis_nya = "t_in_add"

        user_log = UserLog(
            id_user=user_id, jenis={jenis_nya}, keterangan=f"membuat dokumen {jenis_dokumen} , no {data.nomor}", id_doc=data.nomor)

        session.add(user_log)

        session.commit()

        return Response(status_code=204)
