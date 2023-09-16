from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime
from datetime import datetime as dt

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetPurchaseOrderData(BaseModel):
    id_po: str


class GetPurchaseOrderResponseModel(BaseModel):
    nomor_po: str
    id_po: str
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
    satuan: str
    nama_barang: str
    nama_suplier: str
    administrasi_import: float
    bm: float
    pph: float
    ppn_index: float


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
                    "exrate": 15000,
                    "grand_total": 624518,
                    "satuan": "",
                    "nama_barang": "",
                    "nama_suplier": ""
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


NOW = dt.now()

today = NOW.strftime("%Y-%m-%d")


async def get_data_purchase_order(data: GetPurchaseOrderData, session=Depends(get_db_session)):

    sql = "SELECT * , purchase_order.harga_satuan as hargasat FROM purchase_order JOIN baarang on  purchase_order.kode_barang = baarang.kode_barang JOIN suplier on  purchase_order.id_suplier = suplier.id_suplier LIMIT 1"
    sql = f"SELECT * ,baarang.ppn as ppn_index FROM purchase_order JOIN baarang on  purchase_order.kode_barang = baarang.kode_barang JOIN suplier on  purchase_order.id_suplier = suplier.id_suplier  WHERE purchase_order.id_po = {data.id_po}"

    response = session.execute(sa.text(sql))
    response1 = GetPurchaseOrderResponseModel(
        nomor_po="",
        id_po=data.id_po,
        tgl_po=NOW,
        id_suplier=1,
        tgl_minta_kirim=NOW,
        kode_barang="",
        jumlah_order=0,
        harga_satuan=0,
        remark="",
        vlauta="",
        id_akun_payment="1",
        discount=0,
        ppn=0,
        exrate=0,
        grand_total=0,
        nama_barang="",
        satuan="",
        nama_suplier="",
        administrasi_import=0,
        bm=0,
        pph=0,
        ppn_index=0
    )

    for a in response:

        response1 = a

    return GetPurchaseOrderDataResponsemodel(data=GetPurchaseOrderResponseModel(
        nomor_po=response1.nomor_po,
        id_po=data.id_po,
        tgl_po=response1.tgl_po,
        id_suplier=response1.id_suplier,
        tgl_minta_kirim=response1.tgl_minta_kirim,
        kode_barang=response1.kode_barang,
        jumlah_order=response1.jumlah_order,
        harga_satuan=response1.harga_satuan,
        remark=response1.remark,
        vlauta=response1.vlauta,
        id_akun_payment=response1.id_akun_payment,
        discount=response1.discount,
        ppn=response1.ppn,
        exrate=response1.exrate,
        grand_total=response1.grand_total,
        nama_barang=response1.nama_barang,
        satuan=response1.satuan,
        nama_suplier=response1.nama_suplier,
        administrasi_import=response1.administrasi_import,
        bm=response1.bm,
        pph=response1.pph,
        ppn_index=response1.ppn_index
    ))
