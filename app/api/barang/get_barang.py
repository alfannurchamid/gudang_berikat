from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetBarangData(BaseModel):
    kode_barang: str


class GetBarangResponseModel(BaseModel):
    kode_barang: str
    nama_barang: str
    saldo: int
    harga: int
    lokasi: str
    satuan: str


class GetBarangDataResponsemodel(BaseResponseModel):
    data: GetBarangResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'kode_barang': '00494C10009GH',
                    'nama_barang': 'kainddariluar 100persen cotton',
                    'satuan': 'KGM',
                    'saldo': 30230,
                    'harga': 1,
                    'lokasi': 'D'
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_barang(data: GetBarangData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Barang.kode_barang,
            Barang.nama_barang,
            Barang.harga,
            Barang.lokasi,
            Barang.saldo,
            Barang.satuan
        ).where(Barang.kode_barang == data.kode_barang)
    ).fetchone()
    print(response.kode_barang)

    return GetBarangDataResponsemodel(data=GetBarangResponseModel(
        kode_barang=response.kode_barang,
        nama_barang=response.nama_barang,
        saldo=response.saldo,
        harga=response.harga,
        lokasi=response.lokasi,
        satuan=response.satuan,

    ))
