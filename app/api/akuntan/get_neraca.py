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


class GetNeracaData(BaseModel):
    tanggal: Optional[datetime.date]


class GetAkunResponseModel(BaseModel):
    aktiva: object
    kewajiban: object


class GetNeracaDataResponsemodel(BaseResponseModel):
    data: GetAkunResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'aktiva': {
                        'akuns': [{
                            'nama_akun': 'bank bri',
                            'saldo': 20000}]
                    },
                    'kewajiban': {
                        'akuns': [{
                            'nama_akun': 'hutang bank',
                            'saldo': 20000}]
                    }

                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


saldo = 0


async def get_current_saldo(id_akun, tanggal, session):
    sql = f"SELECT current_saldo from jurnal_umum WHERE id_akun = '{id_akun}' AND tanggal <= '{tanggal}'  ORDER BY  id_jurnal DESC LIMIT 1"
    global saldo
    a = session.execute(sa.text(sql)).fetchone()
    if a:
        saldo = a[0]
    else:
        saldo = 0

    print(saldo)


async def get_neraca(data: GetNeracaData, session=Depends(get_db_session)):
    data_post = jsonable_encoder(data)

    is_cari_standar = False
    if 'tanggal' in data_post and data_post['tanggal'] and data_post['tanggal'] != 'skip':
        is_cari_standar = True

    kewajiban = {}

    total_aktiva_lancar = 0
    total_aktiva_tetap = 0

    list_ak_l = []
    list_ak_t = []

    list_hj_pd = []
    list_hj_pj = []

    list_modal = []

    total_hutang = 0
    total_modal = 0

    datalist = []

    sql = "select * from akun WHERE saldo != 0"
    response = session.execute(
        sa.text(sql)
    ).all()
    for Akuna in response:
        id_2 = Akuna.id_akun[0:3]
        # print(id_2)

        if Akuna.id_akun[0] == '3':
            id_2 = '3.x'

        saldo_ini = Akuna.saldo
        nama_4 = Akuna.nama_akun

        if is_cari_standar:
            id = Akuna.id_akun
            await get_current_saldo(
                id, data.tanggal, session)
            print(id_2)
            Akuna = {
                'nama_akun': Akuna.nama_akun,
                'saldo': saldo
            }
            saldo_ini = saldo

        if id_2 == '1.4':
            sal_sementara = -saldo_ini

            Akuna = {
                'nama_akun': nama_4,
                'saldo': sal_sementara
            }

        match id_2:
            case '1.1':
                list_ak_l.append(Akuna)
                total_aktiva_lancar += saldo_ini
            case '1.2':
                list_ak_l.append(Akuna)
                total_aktiva_lancar += saldo_ini
            case '1.3':
                list_ak_t.append(Akuna)
                total_aktiva_tetap += saldo_ini
            case '1.4':
                list_ak_t.append(Akuna)
                total_aktiva_tetap -= saldo_ini
            case '2.1':
                list_hj_pd.append(Akuna)
                total_hutang += saldo_ini
            case '2.2':
                list_hj_pj.append(Akuna)
                total_hutang += saldo_ini
            case '3.x':
                list_modal.append(Akuna)
                print(Akuna)
                total_modal += saldo_ini

        datalist.append(Akuna)
    aktiva = {
        'aktiva_lancar': {
            'datalist': list_ak_l,
            'total': total_aktiva_lancar
        },
        'aktiva_tetap': {
            'datalist': list_ak_t,
            'total': total_aktiva_tetap
        },
        'total_aktiva': total_aktiva_tetap + total_aktiva_lancar
    }

    kewajiban = {
        'hutang_jpd': {
            'datalist': list_hj_pd,
        },
        'hutang_jpj': {
            'datalist': list_hj_pj,
        },
        'total_hutang': total_hutang,
        'modal': {
            'datalist': list_modal,
        },
        'total_modal': total_modal
    }
    return GetNeracaDataResponsemodel(data=GetAkunResponseModel(
        aktiva=aktiva,
        kewajiban=kewajiban
    ))
