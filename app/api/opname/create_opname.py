from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json
from datetime import datetime as dt

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.opname import Opname
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class CreateOpnameData(BaseModel):
    kode_barang: str
    ket: str
    jumlah: int


async def create_opname(data: CreateOpnameData, session=Depends(get_db_session)):
    NOW = dt.now()

    today = NOW.strftime("%Y-%m-%d")
    check_kode = session.execute(
        sa.select(Barang.kode_barang).where(Barang.kode_barang ==
                                            data.kode_barang)
    ).scalar()
    if not check_kode:
        raise HTTPException(
            400, detail='kode barang tidak ditemukan')

    opname = Opname(
        tgl_opname=today, kode_barang=data.kode_barang, jml_opname=data.jumlah, keterangan=data.ket
    )

    with Session(db_engine) as session:

        session.add(opname)
        session.commit()

        return Response(status_code=204)
