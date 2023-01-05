from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import Optional
from fastapi.encoders import jsonable_encoder


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class EditBarangData(BaseModel):
    kode_barang: str
    saldo: Optional[int]
    harga: Optional[int]
    lokasi: Optional[str]
    aktif: Optional[bool]


async def update_data_barang(data: EditBarangData, session=Depends(get_db_session)):
    barang_data = jsonable_encoder(data)
    values_to_update = {}

    if 'saldo' in barang_data and barang_data['saldo']:
        # menghitung saldo
        get_saldo = session.execute(
            sa.select(Barang.saldo).where(
                Barang.kode_barang == data.kode_barang)
        ).scalar()
        # print(get_saldo)
        new_saldo = get_saldo + barang_data['saldo']
        if new_saldo < 0:
            raise HTTPException(
                400, detail='perhitungan stok melebihi batas baawah (kurang dari NOL) ')
        # print(barang_data['saldo'])
        values_to_update.update({'saldo': new_saldo})
    if 'harga' in barang_data and barang_data['harga']:
        values_to_update.update({'harga': barang_data['harga']})
    if 'aktif' in barang_data and barang_data['aktif'] == False or barang_data['aktif'] == True:
        # print(barang_data['aktif'])
        values_to_update.update({'aktif': barang_data['aktif']})

    result = session.execute(
        sa.update(Barang).values(
            **values_to_update).where(Barang.kode_barang == data.kode_barang)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='User not found')
    session.commit()
    return Response(status_code=204)
