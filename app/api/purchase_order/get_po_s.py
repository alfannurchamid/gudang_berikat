from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
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
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_purchase_orders(session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Purchase_order.id_po,
            Purchase_order.tgl_po,
            Purchase_order.id_suplier,
            Purchase_order.tgl_minta_kirim,
            Purchase_order.kode_barang,
            Purchase_order.jumlah_order,
            Purchase_order.harga_satuan,
            Purchase_order.remark,
            Purchase_order.vlauta,
            Purchase_order.id_akun_payment,
            Purchase_order.discount,
            Purchase_order.ppn,
        )
    ).all()
    datalist = []

    for Custome in response:
        datalist.append(Custome)

    return GetPurchaseOrdersDataResponsemodel(data=GetPurchaseOrdersResponseModel(
        data=datalist
    ))
