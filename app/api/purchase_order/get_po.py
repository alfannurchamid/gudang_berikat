from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetPurchaseOrderData(BaseModel):
    id_po: str


class GetPurchaseOrderResponseModel(BaseModel):
    id_po: str
    tgl_po: datetime.date
    id_suplier: int
    tgl_minta_kirim: datetime.date
    kode_barang: str
    jumlah_order: int
    harga_satuan: int
    remark: str
    vlauta: str
    id_akun_payment: int
    discount: int
    ppn: int


class GetPurchaseOrderDataResponsemodel(BaseResponseModel):
    data: GetPurchaseOrderResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
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
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_purchase_order(data: GetPurchaseOrderData, session=Depends(get_db_session)):
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
        ).where(Purchase_order.id_po == data.id_po)
    ).fetchone()

    return GetPurchaseOrderDataResponsemodel(data=GetPurchaseOrderResponseModel(
        id_po=response.id_po,
        tgl_po=response.tgl_po,
        id_suplier=response.id_suplier,
        tgl_minta_kirim=response.tgl_minta_kirim,
        kode_barang=response.kode_barang,
        jumlah_order=response.jumlah_order,
        harga_satuan=response.harga_satuan,
        remark=response.remark,
        vlauta=response.vlauta,
        id_akun_payment=response.id_akun_payment,
        discount=response.discount,
        ppn=response.ppn,
    ))
