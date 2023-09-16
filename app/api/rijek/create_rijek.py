from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json
from datetime import datetime as dt

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.rejek import Rijek
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class CreateRijekData(BaseModel):
    kode_barang: str
    jumlah: int
    no_daftar: str
    type: bool
    id_user: int


async def create_rijek(data: CreateRijekData, session=Depends(get_db_session)):

    NOW = dt.now()
    today = NOW.strftime("%Y-%m-%d")

    check_kode = session.execute(
        sa.select(Barang.saldo).where(Barang.kode_barang ==
                                      data.kode_barang)
    ).scalar()
    if not check_kode:
        raise HTTPException(
            400, detail='kode barang tidak ditemukan')
    new_saldo = check_kode - data.jumlah

    rijek = Rijek(
        tgl_rijek=today, kode_barang=data.kode_barang, jumlah_rijek=data.jumlah, saldo_jml=new_saldo, type=data.type, no_daftar=data.no_daftar, id_user=data.id_user
    )

    with Session(db_engine) as session:

        session.add(rijek)
        session.commit()

        return Response(status_code=204)
