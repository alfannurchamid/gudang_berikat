from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from datetime import datetime as dt

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.transaksi_in import Transaksi_in
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetTransaksiInData(BaseModel):
    no_daftar: str


class GetTransaksiInResponseModel(BaseModel):
    no_daftar: str
    no_pengajuan: str
    tanggal_daftar: datetime.date
    id_user: int
    id_suplier: int
    kode_barang: str
    id_po: int
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
    freight: float
    tanggal_jatuh_tempo: datetime.date
    grand_total: float
    satuan: str
    nama_barang: str
    lokasi: str
    no_po: str
    nama_suplier: str
    administrasi_import: int


class GetTransaksiInDataResponsemodel(BaseResponseModel):
    data: GetTransaksiInResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
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
                    "exchange_rate": 13000,
                    "total_harga_invoice": 44599,
                    "discount": 0,
                    "freight": 0,
                    "tanggal_jatuh_tempo": "2023-01-12",
                    "grand_total": 44599,
                    "lokasi": "B",
                    "id_po": 9,
                    "nama_siplier": "xia sio",
                    "administrasi_import": 0

                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


NOW = dt.now()

today = NOW.strftime("%Y-%m-%d")


async def get_data_transaksi_in(data: GetTransaksiInData, session=Depends(get_db_session)):

    sql = f"SELECT * FROM transaksi_in JOIN baarang on  transaksi_in.kode_barang = baarang.kode_barang WHERE transaksi_in.no_daftar = '{data.no_daftar}'"
    response = session.execute(sa.text(sql))
    response1 = GetTransaksiInResponseModel(
        no_daftar="",
        no_pengajuan="",
        tanggal_daftar=NOW,
        id_user=0,
        id_suplier=0,
        kode_barang="",
        id_po=0,
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
        freight=0,
        tanggal_jatuh_tempo=NOW,
        grand_total=0,
        nama_barang="",
        satuan="",
        lokasi="",
        nama_suplier="",
        no_po="",
        administrasi_import=0


    )

    for a in response:
        # print(a.lokasi)
        response1 = a
    nama_suplier = ""
    no_po = ""

    sql = f"""SELECT nama_suplier, nomor_po FROM  purchase_order JOIN suplier on  purchase_order.id_suplier =  suplier.id_suplier WHERE purchase_order.id_po = {response1.id_po} LIMIT 1"""
    response3 = session.execute(sa.text(sql))
    data_po = response3.mappings().fetchone()
    nama_suplier = data_po.nama_suplier
    no_po = data_po.nomor_po
    # print(data_po)
    return GetTransaksiInDataResponsemodel(data=GetTransaksiInResponseModel(
        no_daftar=response1.no_daftar,
        no_pengajuan=response1.no_pengajuan,
        tanggal_daftar=response1.tanggal_daftar,
        id_user=response1.id_user,
        id_suplier=response1.id_suplier,
        kode_barang=response1.kode_barang,
        id_po=response1.id_po,
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
        freight=response1.freight,
        tanggal_jatuh_tempo=response1.tanggal_jatuh_tempo,
        grand_total=response1.grand_total,
        nama_barang=response1.nama_barang,
        satuan=response1.satuan,
        lokasi=response1.lokasi,
        nama_suplier=nama_suplier,
        no_po=no_po,
        administrasi_import=response1.administrasi_import



    ))
