from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.penyesuaian import Penyesuaian
from sqlalchemy.orm import Session
from app.utils.db import db_engine

from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog


class AddPenyesuaianData(BaseModel):
    jenis: bool
    no_daftar: str
    id_user: str


async def add_penyesuaian(data: AddPenyesuaianData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    jenis = "pengeluaran"

    with Session(db_engine) as session:
        penyesuaian = Penyesuaian(
            jenis=data.jenis,
            no_daftar=data.no_daftar,
            id_user=data.id_user
        )

        jenis_nya = "t_out_add_peny"
        jenis_dokumen = "penjualan"
        if data.jenis:
            jenis_dokumen = "pemasukan"
            jenis_nya = "t_in_add_peny"

        user_id = payload.get('uid', 0)
        user_log = UserLog(
            id_user=user_id, jenis=jenis_nya, keterangan=f"mengajukan penyesuaian {jenis_dokumen},dokumen  no: -{data.no_daftar}", id_doc=data.no_daftar)

        session.add(user_log)
        session.add(penyesuaian)
        session.commit()

        return Response(status_code=204)
