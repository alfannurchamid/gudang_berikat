from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
from app.models.barang import Barang
from app.models.suplier import Suplier
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetTransaksi_in_IdResponseModel(BaseModel):
    data: List[object]


class GetTransaksi_in_IdDataResponsemodel(BaseResponseModel):
    data: GetTransaksi_in_IdResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'nomor_daftar': 1,
                        "nama_barang": "7239417"
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


NOW = datetime.now()

today = NOW.strftime("%Y-%m-%d")

print(today)

sql = f"SELECT transaksi_in.no_daftar, baarang.nama_barang  FROM transaksi_in JOIN baarang on transaksi_in.kode_barang = baarang.kode_barang WHERE transaksi_in.done = false AND acc = true"


async def get_data_transaksi_in_id(session=Depends(get_db_session)):
    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:

        datalist.append(Custome)

    return GetTransaksi_in_IdDataResponsemodel(data=GetTransaksi_in_IdResponseModel(
        data=datalist
    ))
