from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder


from app.dependencies.autentication import Autentication
from typing import Optional
import json

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from app.models.user_log import UserLog
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddBarangData(BaseModel):
    nama_barang: str
    kode_barang: str
    satuan: str
    harga: Optional[float]
    bm: Optional[float]
    ppn: Optional[float]
    pph: Optional[float]
    id_beban: str
    id_persediaan: str


async def add_barang(data: AddBarangData, payload=Depends(Autentication()), session=Depends(get_db_session)):

    colum_harga = ""
    colum_bm = ""
    colum_ppn = ""
    colum_pph = ""

    value_harga = ""
    value_bm = ""
    value_ppn = ""
    value_pph = ""

    datanya = jsonable_encoder(data)
    check_kode = session.execute(
        sa.select(Barang.kode_barang).where(Barang.kode_barang ==
                                            data.kode_barang)
    ).scalar()
    if check_kode:
        raise HTTPException(
            400, detail='kode barang sudah terdaftar')

    if "harga" in datanya and datanya["harga"]:
        colum_harga = ",harga"
        value_harga = f",'{datanya['harga']}'"

    if "bm" in datanya and datanya["bm"]:
        colum_bm = ",bm"
        value_bm = f",'{datanya['bm']}'"

    if "ppn" in datanya and datanya["ppn"]:
        colum_ppn = ",ppn"
        value_ppn = f",'{datanya['ppn']}'"

    if "pph" in datanya and datanya["pph"]:
        colum_pph = ",pph"
        value_pph = f",'{datanya['pph']}'"

    sql = f"INSERT INTO baarang (nama_barang,kode_barang,satuan,akun_beban,akun_persediaan{colum_bm}{colum_ppn}{colum_pph}) VALUES ('{data.nama_barang}' ,'{data.kode_barang}' ,'{data.satuan}','{data.id_beban}','{data.id_persediaan}'  {value_bm} {value_ppn} {value_pph})"
    print(sql)

    user_id = payload.get('uid', 0)
    user_log = UserLog(
        id_user=user_id, jenis='bar_add', keterangan=f"menambah barang -{data.nama_barang}", id_doc=data.nama_barang)

    result = session.execute(sa.text(sql))
    # if result.rowcount == 0:
    #     raise HTTPException(400, detail=' terjadi masalah')

    # with Session(db_engine) as session:
    # session.add(barang)
    # session.add(user_log)
    session.commit()

    return Response(status_code=204)
