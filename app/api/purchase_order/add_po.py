from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddPurchase_orderData(BaseModel):
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


async def add_purchase_order(data: AddPurchase_orderData, session=Depends(get_db_session)):

    with Session(db_engine) as session:
        purchase_order = Purchase_order(
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
            ppn=data.ppn
        )
        session.add(purchase_order)
        session.commit()

        return Response(status_code=204)
