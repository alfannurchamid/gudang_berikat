from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetBarangResponseModel(BaseModel):
    kode_barang: str
    nama_barang: str
    saldo: int

    bm: float
    ppn: float
    pph: float
    satuan: str
    id_akun_peresediaan: str
    id_akun_beban: str


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

                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_barang(kode_barang: str, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Barang.kode_barang,
            Barang.nama_barang,
            Barang.harga,
            Barang.saldo,
            Barang.satuan,
            Barang.bm,
            Barang.ppn,
            Barang.pph,
            Barang.akun_persediaan,
            Barang.akun_beban
        ).where(Barang.kode_barang == kode_barang)
    ).fetchone()
    print(response.kode_barang)

    return GetBarangDataResponsemodel(data=GetBarangResponseModel(
        kode_barang=response.kode_barang,
        nama_barang=response.nama_barang,
        saldo=response.saldo,
        id_akun_beban=response.akun_beban,
        id_akun_peresediaan=response.akun_persediaan,
        bm=response.bm,
        ppn=response.ppn,
        pph=response.pph,
        satuan=response.satuan,

    ))
