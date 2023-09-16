from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
import datetime

from app.dependencies.autentication import Autentication
from app.models.standar_doc import StandarDoc
from app.models.user_log import UserLog


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.transaksi_out import Transaksi_out
from app.models.transaksi_in import Transaksi_in
from sqlalchemy.orm import Session
from app.utils.db import db_engine
from datetime import datetime as dt


class AddTransaksiOutData(BaseModel):
    no_daftar: str
    no_pengajuan: str
    tanggal_daftar: datetime.date
    id_customer: int
    kode_barang: str
    jumlah: int
    harga_satuan: int

    saldo_jml: int
    no_sppb: str
    tanggal_sppb: datetime.date
    nomor_invoice: str
    tanggal_invoice: datetime.date
    vlauta: str
    exchane_rate: int
    total_harga_invoice: int
    discount: int
    ppn: int
    grand_total: float
    jenis: str
    nomor_daftar_in: str
    lokasi: str


async def create_transaksi_out(data: AddTransaksiOutData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    NOW = dt.now()

    values_to_update = {}
    values_to_update.update({'done': True})
    result = session.execute(
        sa.update(Transaksi_in).values(
            **values_to_update).where(Transaksi_in.no_daftar == data.nomor_daftar_in)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Transaksi in not found')

    result = session.execute(
        sa.update(StandarDoc).values(
            **values_to_update).where(StandarDoc.nomor == data.no_daftar)
    )
    if result.rowcount == 0:
        raise HTTPException(400, detail='Transaksi in not found')

    session.commit()

    jum = session.execute(sa.select(
        Transaksi_in.jumlah
    ).where(Transaksi_in.no_daftar == data.nomor_daftar_in)
    ).fetchone()
    print(jum[0])
    newsaldo = jum[0] - data.jumlah
    print(newsaldo)

    today = NOW.strftime("%Y-%m-%d")
    with Session(db_engine) as session:
        transaksi_out = Transaksi_out(
            no_daftar=data.no_daftar,
            no_pengajuan=data.no_pengajuan,
            tanggal_daftar=data.tanggal_daftar,
            id_customer=data.id_customer,
            id_user=1,
            kode_barang=data.kode_barang,
            tanggal_sppb=data.tanggal_sppb,
            no_sppb=data.no_sppb,
            jumlah=data.jumlah,
            harga_satuan=data.harga_satuan,
            tanggal=today,
            saldo_jml=newsaldo,
            nomor_invoice=data.nomor_invoice,
            tanggal_invoice=data.tanggal_invoice,
            vlauta=data.vlauta,
            exchane_rate=data.exchane_rate,
            total_harga_invoice=data.total_harga_invoice,
            discount=data.discount,
            ppn=data.ppn,
            tanggal_jatuh_tempo=today,
            grand_total=data.grand_total,
            jenis=data.jenis,
            nomor_daftar_in=data.nomor_daftar_in,
            lokasi=data.lokasi
        )

        session.add(transaksi_out)
        user_id = payload.get('uid', 0)
        user_log = UserLog(
            id_user=user_id, jenis='t_out_acc', keterangan=f"memncatat dokumen pengeluaran {data.jenis} no: -{data.no_daftar}", id_doc=data.no_daftar)

        session.add(user_log)
        session.commit()

    return Response(status_code=204)
