from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddBarangData(BaseModel):
    nama_barang: str
    kode_barang: str
    satuan: str
    lokasi: str
    harga: int


async def add_barang(data: AddBarangData, session=Depends(get_db_session)):
    check_kode = session.execute(
        sa.select(Barang.kode_barang).where(Barang.kode_barang ==
                                            data.kode_barang)
    ).scalar()
    if check_kode:
        raise HTTPException(
            400, detail='kode barang sudah terdaftar')

    with Session(db_engine) as session:
        barang = Barang(
            nama_barang=data.nama_barang, kode_barang=data.kode_barang, satuan=data.satuan, lokasi=data.lokasi, harga=data.harga
        )
        session.add(barang)
        session.commit()

        return Response(status_code=204)
