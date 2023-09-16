from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from datetime import datetime as dt

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.transaksi_out import Transaksi_out
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetTransaksiOutData(BaseModel):
    no_daftar: str


class GetTransaksiOutResponseModel(BaseModel):
    no_daftar: str
    no_pengajuan: str
    tanggal_daftar: datetime.date
    id_user: int
    id_customer: int
    kode_barang: str
    nomor_daftar_in: str

    jumlah: int
    harga_satuan: float
    tanggal: datetime.date
    saldo_jml: int
    no_sppb: str
    tanggal_sppb: datetime.date
    nomor_invoice: str
    tanggal_invoice: datetime.date
    jenis: str
    vlauta: str
    exchange_rate: float
    total_harga_invoice: float
    discount: float

    tanggal_jatuh_tempo: datetime.date
    grand_total: float
    satuan: str
    nama_barang: str
    lokasi: str
    ppn: int
    ppn_v: int

    nama_customer: str


class GetTransaksiOutDataResponsemodel(BaseResponseModel):
    data: GetTransaksiOutResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    "no_daftar": "0004168",
                    "no_pengajuan": "060825-027936-20230081-66666",
                    "tanggal_daftar": "2023-01-12",
                    "id_user": 1,
                    "id_customer": 2,
                    "kode_barang": "56031300 B",

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
                    "exchange_rate": 13000,
                    "total_harga_invoice": 44599,
                    "discount": 0,
                    "ppn": 200000,
                    "tanggal_jatuh_tempo": "2023-01-12",
                    "grand_total": 44599,
                    "lokasi": "B",

                    "nama_siplier": "xia sio"
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


NOW = dt.now()

today = NOW.strftime("%Y-%m-%d")


async def get_data_transaksi_out(data: GetTransaksiOutData, session=Depends(get_db_session)):

    sql = f"SELECT  * , transaksi_out.ppn as ppn_v FROM transaksi_out JOIN baarang on  transaksi_out.kode_barang = baarang.kode_barang WHERE transaksi_out.no_daftar = '{data.no_daftar}'"
    response = session.execute(sa.text(sql))
    response1 = GetTransaksiOutResponseModel(
        no_daftar="",
        no_pengajuan="",
        tanggal_daftar=NOW,
        id_user=0,
        id_customer=0,
        kode_barang="",
        nomor_daftar_in="",


        jumlah=0,
        harga_satuan=0,
        tanggal=NOW,
        saldo_jml=0,
        no_sppb="",
        tanggal_sppb=NOW,
        nomor_invoice="",
        tanggal_invoice=NOW,
        jenis="",
        vlauta="",
        exchange_rate=0,
        total_harga_invoice=0,
        discount=0,
        ppn=0, ppn_v=0,

        tanggal_jatuh_tempo=NOW,
        grand_total=0,
        nama_barang="",
        satuan="",
        lokasi="",
        nama_customer="",

    )

    for a in response:
        # print(a.lokasi)
        response1 = a
    nama_customer = ""

    sql = f"""SELECT nama_customer FROM customer WHERE id_customer = {response1.id_customer} LIMIT 1"""
    response3 = session.execute(sa.text(sql))
    data_po = response3.mappings().fetchone()
    nama_customer = data_po.nama_customer

    # print(data_po)
    return GetTransaksiOutDataResponsemodel(data=GetTransaksiOutResponseModel(
        no_daftar=response1.no_daftar,
        no_pengajuan=response1.no_pengajuan,
        tanggal_daftar=response1.tanggal_daftar,
        id_user=response1.id_user,
        id_customer=response1.id_customer,
        kode_barang=response1.kode_barang,
        ppn_v=response1.ppn_v,

        jumlah=response1.jumlah,
        harga_satuan=response1.harga_satuan,
        tanggal=response1.tanggal,
        saldo_jml=response1.saldo_jml,
        no_sppb=response1.no_sppb,
        tanggal_sppb=response1.tanggal_sppb,
        nomor_invoice=response1.nomor_invoice,
        tanggal_invoice=response1.tanggal_invoice,
        jenis=response1.jenis,
        vlauta=response1.vlauta,
        exchange_rate=response1.exchange_rate,
        total_harga_invoice=response1.total_harga_invoice,
        discount=response1.discount,
        ppn=response1.ppn,
        nomor_daftar_in=response1.nomor_daftar_in,

        tanggal_jatuh_tempo=response1.tanggal_jatuh_tempo,
        grand_total=response1.grand_total,
        nama_barang=response1.nama_barang,
        satuan=response1.satuan,
        lokasi=response1.lokasi,
        nama_customer=nama_customer,

    ))
