from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime
from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddPurchase_orderData(BaseModel):
    nomor_po: str
    tgl_po: datetime.date
    id_suplier: int
    tgl_minta_kirim: datetime.date
    kode_barang: str
    jumlah_order: int
    harga_satuan: float
    remark: str
    vlauta: str
    id_akun_payment: str
    discount: float
    ppn: float
    exrate: float
    grand_total: float
    administrasi_import: float


class AddPurchaseOrdersResponseModel(BaseModel):
    id_po: str


class AddPurchaseOrdersDataResponsemodel(BaseResponseModel):
    data: AddPurchaseOrdersResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_po':   "123",
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def add_purchase_order(data: AddPurchase_orderData, payload=Depends(Autentication()), session=Depends(get_db_session)):

    with Session(db_engine) as session:
        purchase_order = Purchase_order(
            nomor_po=data.nomor_po,
            tgl_po=data.tgl_po,
            id_suplier=data.id_suplier,
            tgl_minta_kirim=data.tgl_minta_kirim,
            kode_barang=data.kode_barang,
            jumlah_order=data.jumlah_order,
            harga_satuan=data.harga_satuan,
            remark=data.remark,
            vlauta=data.vlauta,
            id_akun_payment=data.id_akun_payment,
            discount=data.discount,
            ppn=data.ppn,
            exrate=data.exrate,
            grand_total=data.grand_total,
            administrasi_import=data.administrasi_import

        )
        user_id = payload.get('uid', 0)
        user_log = UserLog(
            id_user=user_id, jenis='po_add', keterangan=f"membuat purchase order {data.nomor_po}", id_doc=data.nomor_po)

        session.add(user_log)
        session.add(purchase_order)
        session.commit()

        id_po = ""

        id_po = session.execute(sa.select(Purchase_order.id_po).order_by(
            Purchase_order.id_po.desc())).scalar()
        # print("id_po nya", id_po)

        return AddPurchaseOrdersDataResponsemodel(data=AddPurchaseOrdersResponseModel(id_po=str(id_po)))
