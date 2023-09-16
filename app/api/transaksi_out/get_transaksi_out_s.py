from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel

from app.models.barang import Barang
from app.models.suplier import Suplier
from app.models.transaksi_out import Transaksi_out
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetTransaksiOutsResponseModel(BaseModel):
    data: List[object]


class GetTransaksiOutsDataResponsemodel(BaseResponseModel):
    data: GetTransaksiOutsResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        "no_daftar": "0004168",
                        "no_pengajuan": "060825-027936-20230081-66666",
                        "tanggal_daftar": "2023-01-12",
                        "id_user": 1,
                        "id_suplier": 2,
                        "kode_barang": "56031300 B",
                        "id_po": 1,
                        "jumlah": 34300,
                        "harga_satuan": 1.3,
                        "tanggal": "2023-01-12",
                        "saldo_jml": 44872,
                        "no_sppb": "087817/KCB 1066/2023",
                        "tanggal_sppb": "2023-01-12",
                        "nomor_invoice": "hjf766",
                        "tanggal_invoice": "2023-01-12",
                        "jenis": "BC 2.3",
                        "vlauta": "USD",
                        "exchane_rate": 13000,
                        "total_harga_invoice": 44599,
                        "discount": 0,
                        "freight": 0,
                        "tanggal_jatuh_tempo": "2023-01-12",
                        "grad_total": 44599
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_transaksi_outs(type: bool, session=Depends(get_db_session)):
    sql = "SELECT * FROM transaksi_out JOIN baarang on  transaksi_out.kode_barang = baarang.kode_barang  WHERE transaksi_out.acc = False"
    if type:
        sql = "SELECT * FROM transaksi_out JOIN baarang on  transaksi_out.kode_barang = baarang.kode_barang  WHERE transaksi_out.acc = True"

    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:

        datalist.append(Custome)

    return GetTransaksiOutsDataResponsemodel(data=GetTransaksiOutsResponseModel(
        data=datalist
    ))
