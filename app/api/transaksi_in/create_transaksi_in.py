
from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime
from fastapi.encoders import jsonable_encoder
from typing import List
import json
from datetime import datetime as dt
from app.dependencies.autentication import Autentication

from app.dependencies.get_db_session import get_db_session

from app.models.barang import Barang
from app.models.purchase_order import Purchase_order
from app.models.standar_doc import StandarDoc
from app.models.user_log import UserLog

from app.utils.db import db_engine


class AddTransaksiInData(BaseModel):
    no_daftar: str
    no_pengajuan: str
    tanggal_daftar: str
    id_suplier: int
    kode_barang: str
    id_po: int
    jumlah: int
    harga_satuan: float
    saldo_jml: int
    no_sppb: str
    tanggal_sppb: str
    nomor_invoice: str
    tanggal_invoice: str
    jenis: str
    vlauta: str
    exchane_rate: float
    total_harga_invoice: float
    discount: float
    freight: float
    lokasi: str

    grad_total: float
    administrasi_import_idr: float
    pabean: float
    pembayaran: str


async def create_transaksi_in(data: AddTransaksiInData,  payload=Depends(Autentication()), session=Depends(get_db_session)):

    NOW = dt.now()

    today = NOW.strftime("%Y-%m-%d")

    values_to_update1 = {}
    values_to_update1.update({'done': True})
    result = session.execute(
        sa.update(Purchase_order).values(
            **values_to_update1).where(Purchase_order.id_po == data.id_po)
    )
    if result.rowcount == 0:
        raise HTTPException(400, detail='Transaksi in not found')

    result = session.execute(
        sa.update(StandarDoc).values(
            **values_to_update1).where(StandarDoc.nomor == data.no_daftar)
    )
    if result.rowcount == 0:
        raise HTTPException(400, detail='Transaksi in not found')

    session.commit()

    print(today)
    # generate akun dan nominal dari client
    a = data.pembayaran.replace("'", '"')
    # print(a)
    # data_str = f"""{a}"""
    # data_pembayaran = json.loads(data_str)
    # for bayar in data_pembayaran["data"]:
    #     print(bayar)

    # ambil saldo barang
    saldoBarang = session.execute(
        sa.select(
            Barang.saldo
        ).where(Barang.kode_barang == data.kode_barang)
    ).scalar()
    print(saldoBarang)
    # # update saldo barang
    newSaldo = data.jumlah + saldoBarang
    values_to_update = {'saldo': newSaldo}

    # result = session.execute(
    #     sa.update(Barang).values(
    #         **values_to_update).where(Barang.kode_barang == data.kode_barang)
    # )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Barang not found')

    # sql = f"INSERT INTO transaksi_in(no_pengajuan, no_daftar, tanggal_daftar, id_suplier, id_user, kode_barang, jumlah, tanggal, saldo_jml, id_po, no_sppb, tanggal_sppb, nomor_invoice, tanggal_invoice, jenis, vlauta, exchange_rate, total_harga_invoice, discount, freight, tanggal_jatuh_tempo, grand_total, harga_satuan)VALUES('{data.no_pengajuan}', '{data.no_daftar}', '{data.tanggal_daftar}', {data.id_suplier}, 1, '{data.kode_barang}', {data.jumlah}', '{today}', {newSaldo}, {data.id_po}, '{data.no_sppb}', '{data.tanggal_sppb}', '{data.nomor_invoice}', '{data.tanggal_invoice}', '{data.jenis}', '{data.vlauta}', {data.exchane_rate}, {data.total_harga_invoice}, {data.discount}, {data.freight}, '{today}', {data.grad_total},{data.harga_satuan})"
    sql = f"""
INSERT INTO gudang1.transaksi_in
(no_pengajuan, no_daftar, tanggal_daftar, id_suplier, id_user, kode_barang, jumlah, tanggal, saldo_jml, id_po, no_sppb, tanggal_sppb, nomor_invoice, tanggal_invoice, jenis, vlauta, exchange_rate, total_harga_invoice, discount, freight, tanggal_jatuh_tempo, grand_total, harga_satuan ,lokasi, administrasi_import, pabean)
VALUES('{data.no_pengajuan}', '{data.no_daftar}', '{data.tanggal_daftar}', {data.id_suplier}, 1, '{data.kode_barang}', {data.jumlah}, '{today}', {newSaldo}, {data.id_po}, '{data.no_sppb}', '{data.tanggal_sppb}', '{data.nomor_invoice}', '{data.tanggal_invoice}', '{data.jenis}', '{data.vlauta}', {data.exchane_rate}, {data.total_harga_invoice}, {data.discount}, {data.freight}, '{today}', {data.grad_total}, {data.harga_satuan}, '{data.lokasi}',{data.administrasi_import_idr}, {data.pabean});
    """

    session.execute(sa.text(sql))

    user_id = payload.get('uid', 0)
    user_log = UserLog(
        id_user=user_id, jenis='t_in_add', keterangan=f"memncatat dokumen pemasukan {data.jenis} no: -{data.no_daftar}", id_doc=data.no_daftar)

    session.add(user_log)
    session.commit()

    return Response(status_code=204)
