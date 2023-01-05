from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.transaksi_in import Transaksi_in
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetTransaksiInData(BaseModel):
    no_daftar: str


class GetTransaksiInResponseModel(BaseModel):
    no_daftar: str
    tanggal_daftar: datetime.date
    id_user: int
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


class GetTransaksiInDataResponsemodel(BaseResponseModel):
    data: GetTransaksiInResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_transaksi_in': '2',
                    'nama_transaksi_in': 'PT.Berkah Abadi',
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_transaksi_in(data: GetTransaksiInData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Transaksi_in.no_daftar,
            Transaksi_in.tanggal_daftar,
            Transaksi_in.id_user,
            Transaksi_in.id_suplier,
            Transaksi_in.kode_barang,
            Transaksi_in.id_po,
            Transaksi_in.jumlah,
            Transaksi_in.tanggal,
            Transaksi_in.saldo_jml,
            Transaksi_in.no_sppb,
            Transaksi_in.tanggal_sppb,
            Transaksi_in.no_invoice,
            Transaksi_in.tanggal_invoice,
            Transaksi_in.jenis,
            Transaksi_in.vlauta,
            Transaksi_in.exchane_rate,
            Transaksi_in.total_harga_invoice,
            Transaksi_in.discount,
            Transaksi_in.freight,
            Transaksi_in.tanggal_jatuh_tempo,
            Transaksi_in.grad_total,
        ).where(Transaksi_in.no_daftar == data.no_daftar)
    ).fetchone()

    return GetTransaksiInDataResponsemodel(data=GetTransaksiInResponseModel(
        no_daftar=response.no_daftar,
        tanggal_daftar=response.tanggal_daftar,
        id_user=response.id_user,
        id_suplier=response.id_suplier,
        kode_barang=response.kode_barang,
        id_po=response.id_po,
        jumlah=response.jumlah,
        tanggal=response.tanggal,
        saldo_jml=response.saldo_jml,
        no_sppb=response.no_sppb,
        tanggal_sppb=response.tanggal_sppb,
        no_invoice=response.no_invoice,
        tanggal_invoice=response.tanggal_invoice,
        jenis=response.jenis,
        vlauta=response.vlauta,
        exchane_rate=response.exchane_rate,
        total_harga_invoice=response.total_harga_invoice,
        discount=response.discount,
        freight=response.freight,
        tanggal_jatuh_tempo=response.tanggal_jatuh_tempo,
        grad_total=response.grad_total
    ))
