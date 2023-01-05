from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.transaksi_in import Transaksi_in
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddTransaksiInData(BaseModel):
    no_daftar: str
    tanggal_daftar: datetime.date
    id_suplier: int
    kode_barang: str
    id_po: int
    jumlah: int
    tanggal: datetime.date
    saldo_jml: int
    no_sppb: str
    tanggal_sppb: datetime.date
    no_invoice: str
    tanggal_invoice: datetime.date
    jenis: str
    vlauta: str
    exchane_rate: int
    total_harga_invoice: int
    discount: int
    freight: int
    tanggal_jatuh_tempo: datetime.date
    grad_total: int


async def create_transaksi_in(data: AddTransaksiInData, session=Depends(get_db_session)):

    with Session(db_engine) as session:
        transaksi_in = Transaksi_in(
            no_daftar=data.no_daftar,
            tanggal_daftar=data.tanggal_daftar,
            id_user=1,
            id_suplier=data.id_suplier,
            kode_barang=data.kode_barang,
            id_po=data.id_po,
            jumlah=data.jumlah,
            tanggal=data.tanggal,
            saldo_jml=data.saldo_jml,
            no_sppb=data.no_sppb,
            tanggal_sppb=data.tanggal_sppb,
            no_invoice=data.no_invoice,
            tanggal_invoice=data.tanggal_invoice,
            jenis=data.jenis,
            vlauta=data.vlauta,
            exchane_rate=data.exchane_rate,
            total_harga_invoice=data.total_harga_invoice,
            discount=data.discount,
            freight=data.freight,
            tanggal_jatuh_tempo=data.tanggal_jatuh_tempo,
            grad_total=data.grad_total,


        )
        session.add(transaksi_in)
        session.commit()

        return Response(status_code=204)
