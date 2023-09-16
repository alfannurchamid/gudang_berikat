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


class GetPurchaseOrdersResponseModel(BaseModel):
    data: List[object]


class GetPurchaseOrdersDataResponsemodel(BaseResponseModel):
    data: GetPurchaseOrdersResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'id_po': 1,
                        "tgl_po": "2023-01-05",
                        "id_suplier": 2,
                        "tgl_minta_kirim": "2023-01-05",
                        "kode_barang": "083888127 B",
                        "jumlah_order": 200,
                        "harga_satuan": 30,
                        "remark": "nggatau contoh",
                        "vlauta": "USD",
                        "id_akun_payment": 2,
                        "discount": 1,
                        "ppn": 12,
                        "exrate": 15000,
                        "grand_total": 624518,
                        "nomorpo": "7239417"
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


sql = "SELECT * FROM purchase_order JOIN baarang on  purchase_order.kode_barang = baarang.kode_barang JOIN suplier on  purchase_order.id_suplier = suplier.id_suplier ORDER BY done"


async def get_data_purchase_orders(session=Depends(get_db_session)):
    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:
        # print("tes")
        datalist.append(Custome)

    return GetPurchaseOrdersDataResponsemodel(data=GetPurchaseOrdersResponseModel(
        data=datalist
    ))
