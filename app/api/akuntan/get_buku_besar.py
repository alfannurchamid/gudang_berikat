from typing import List, Optional
from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
import asyncio


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.akun import Akun
from app.models.jurnal_umum import JurnalUmum
from sqlalchemy.orm import Session
from app.utils.db import db_engine
import datetime


class GetBukuBesarData(BaseModel):
    tanggal_awal: datetime.date
    tanggal_ahir: datetime.date
    id_akun: str
    type: bool


class GetAkunResponseModel(BaseModel):
    list_jurnal: list[object]
    saldo_awal: int
    saldo_ahir: int


class GetBukuBesarDataResponsemodel(BaseResponseModel):
    data: GetAkunResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'list_jurnal': [
                        {
                            'debet': 0,
                            'kredit': 0,
                            'tanggal': '2023-01-01',
                            'keterangan': 0
                        }
                    ],
                    'saldo_awal': 0,
                    'saldo_ahir': 0

                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_buku_besar(data: GetBukuBesarData, session=Depends(get_db_session)):
    data_list = []
    data_post = jsonable_encoder(data)
    saldo_awal = 0
    # menga,bil saldo awal
    get_saldo_awal = session.execute(sa.text(
        f""" SELECT current_saldo FROM jurnal_umum  WHERE id_akun = '{data.id_akun}' AND tanggal < '{data.tanggal_awal}'  ORDER BY id_jurnal DESC """)).fetchone()

    if get_saldo_awal:
        print('saldo awalll ', get_saldo_awal[0])
        saldo_awal = get_saldo_awal[0]
    if 4 < int(data.id_akun[0]) < 7:
        saldo_awal = 0
    sql = f"SELECT  tanggal, debet ,kredit ,keterangan ,current_saldo from jurnal_umum WHERE id_akun = '{data.id_akun}' AND tanggal BETWEEN '{data.tanggal_awal}' AND '{data.tanggal_ahir}' ORDER BY tanggal ASC "

    data_get = session.execute(sa.text(sql)).all()

    akumulasi = 0
    saldo_ahir = 0

    for data_g in data_get:
        print(data_g)
        data_list.append(data_g)
        if data.type:
            akumulasi += data_g.debet
            akumulasi -= data_g.kredit
        else:
            akumulasi -= data_g.debet
            akumulasi += data_g.kredit

        saldo_ahir = data_g.current_saldo

    return GetBukuBesarDataResponsemodel(data=GetAkunResponseModel(
        list_jurnal=data_list,
        saldo_ahir=saldo_ahir,
        saldo_awal=saldo_awal
    ))
