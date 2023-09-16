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


class GetLabaRugiData(BaseModel):
    mulai: Optional[datetime.date]
    ahir: datetime.date
    type: bool


class GetAkunResponseModel(BaseModel):
    hpp: object
    operasional: object
    pendapatan: int


class GetLabaRugiDataResponsemodel(BaseResponseModel):
    data: GetAkunResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'pendapatan': 8000,
                    'hpp': {
                        'data_list': [{
                            'nama_akun': 'bank bri',
                            'saldo': 20000}],
                        'total_hpp': 900000,
                    },
                    'oprasional': {
                        'data_list': [{
                            'nama_akun': 'hutang bank',
                            'saldo': 20000}],
                        'total_oprasional': 90000,
                    },

                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


saldo = 0


def get_current_saldo(id_akun, mulai, ahir, session):
    # print(id_akun)
    global saldo
    sal_awal = session.execute(sa.text(
        f"SELECT current_saldo from jurnal_umum WHERE id_akun = '{id_akun}' AND tanggal < '{mulai}' ORDER BY id_jurnal DESC LIMIT 1  ")).scalar()
    # print(id_akun, sal_awal)
    sql = f"SELECT current_saldo from jurnal_umum WHERE id_akun = '{id_akun}' AND tanggal BETWEEN '{mulai}' AND '{ahir}'"
    s = session.execute(sa.text(sql)).all()
    saldo_awal = 0
    saldo_ahir = 0
    if s:
        i = 0
        for l_saldo in s:
            i += 1
            if i == 1:
                # print("pooooooongg", l_saldo[0])
                saldo_awal = l_saldo[0]
                saldo_ahir = l_saldo[0]
            if i == len(s):
                # print("iiiiiiiiiiiii", i)
                saldo_ahir = l_saldo[-1]
        if i > 1:
            if sal_awal:
                saldo = saldo_ahir - sal_awal
            else:
                saldo = saldo_ahir
        else:
            if sal_awal:
                saldo = saldo_awal - sal_awal
            else:
                saldo = saldo_awal
    else:
        saldo = 0

    # print("saldo", saldo)


async def get_laba_rugi(data: GetLabaRugiData, session=Depends(get_db_session)):
    data_post = jsonable_encoder(data)
    pendapatan = 0

    total_hpp = 0
    list_hpp = []

    list_oprasional = []
    total_operasioanal = 0
    datalist = []

    sql = "select * from akun"
    response = session.execute(
        sa.text(sql)
    ).all()

    for Akuna in response:
        id_2 = Akuna.id_akun[0:2]

        if 'mulai' in data_post and data_post['mulai']:
            awal = data.mulai

        else:
            split_date = str(data.ahir).split("-")
            awal = split_date[0]+'-'+split_date[1]+'-' + "01"

        id = Akuna.id_akun
        get_current_saldo(
            id, awal, data.ahir, session)

        Akuna = {
            'nama_akun': Akuna.nama_akun,
            'saldo': saldo
        }

        saldo_ini = saldo

        match id_2:
            case '5.':
                list_hpp.append(Akuna)
                total_hpp += saldo_ini
            case '6.':
                list_oprasional.append(Akuna)
                total_operasioanal += saldo_ini
            case '4.':
                pendapatan += saldo_ini

        datalist.append(Akuna)
    hpp = {
        'datalist': list_hpp,
        'total_hpp': total_hpp
    }

    operasional = {
        'datalist': list_oprasional,
        'total_op': total_operasioanal
    }

    return GetLabaRugiDataResponsemodel(data=GetAkunResponseModel(
        hpp=hpp,
        operasional=operasional,
        pendapatan=pendapatan
    ))
