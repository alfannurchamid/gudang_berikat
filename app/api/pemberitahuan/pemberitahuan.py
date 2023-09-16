from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.barang import Barang
from app.models.transaksi_in import Transaksi_in
from app.models.transaksi_out import Transaksi_out
from app.models.user import User
from sqlalchemy.orm import Session
from app.utils.db import db_engine

from app.utils.row_encoder import AlchemyEncoder


class GetPemberitahuansResponseModel(BaseModel):
    data: List[object]


class GetPemberitahuansDataResponsemodel(BaseResponseModel):
    data: GetPemberitahuansResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'type': 'pengajuan',
                        'no_daftar': 'kainddariluar 100persen cotton',
                        'jenis_dokumen': 'KGM',
                        'jenis': 30230,
                        'tanggal': 1,
                        'done': False,
                        'id_pengajuan': 8
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


class data_return (BaseModel):
    data: List[object]


async def get_data(type: bool, session):
    datalist = []
    # DOKUMEN BARANG IN
    # AMBIL DOKUMENS YANG BELUM DONE
    # PERCABANGAN JENIS DOKUMEN
    if type:
        sql = f"""SELECT * FROM transaksi_in WHERE acc = {False}  """
    else:
        sql = f"""SELECT * FROM transaksi_out WHERE acc = {False} """
    response = session.execute(
        sa.text(sql)
    ).all()

    for Bara in response:
        a = {}
        # AMBIL PENGAJUAN YANG NO_DAFTAR NYA = DOKUMEN_IN
        sql2 = f"""SELECT * FROM pengajuan_penyesuaian WHERE no_daftar = "{Bara['no_daftar']}" AND jenis = {type}"""
        pengajuan = session.execute(sa.text(sql2)).all()

        # AMBIL NAMA PENGAJU
        response2 = session.execute(sa.select(User.full_name).where(
            User.id_user == Bara["id_user"])).scalar()
        pengaju = response2

        if len(pengajuan) == 0:
            print("tidak ada ")
            a = {'type': "acc",
                 'jenis': type,
                 'no_daftar': Bara['no_daftar'],
                 'tanggal': Bara['tanggal'],
                 'jenis_dokumen': Bara['jenis'],
                 'pengaju': pengaju,
                 'done': False,

                 }
            datalist.append(a)

        else:
            print(pengajuan[0])
            data_pengajuan = pengajuan[0]
            print("ada penyesuaian")
            a = {'type': "penyesuaian",
                 'jenis': type,
                 'no_daftar': Bara['no_daftar'],
                 'tanggal': data_pengajuan['tanggal'],
                 'jenis_dokumen': Bara['jenis'],
                 'pengaju': pengaju,
                 'done': False,
                 'id_pengajuan': data_pengajuan['id_pengajuan']
                 }
            datalist.append(a)
    return datalist


async def get_pemberitahuans(session=Depends(get_db_session)):
    datalist = []

    # GET DATA IN DARI DEF GLOBAL
    data_in = []
    data_in = await get_data(True, session)
    if data_in:
        for datain in data_in:
            datalist.append(datain)

    # GET DATA OUT DARI DEF GLOBAL
    data_out = []

    data_out = await get_data(False, session)
    if data_out:
        for dataout in data_out:
            datalist.append(dataout)
    sql3 = "SELECT * FROM transaksi_out join pengajuan_penyesuaian on transaksi_out.no_daftar = pengajuan_penyesuaian.no_daftar WHERE pengajuan_penyesuaian.done = false "

    data_penye_out = session.execute(sa.text(sql3)).all()

    list_peny_out = []
    for dt_peny_out in data_penye_out:
        # AMBIL NAMA PENGAJU
        response2 = session.execute(sa.select(User.full_name).where(
            User.id_user == dt_peny_out["id_user"])).scalar()
        response3 = session.execute(sa.select(Transaksi_out.jenis).where(
            Transaksi_out.no_daftar == dt_peny_out['no_daftar'])).scalar()
        pengaju = response2
        a = {'type': "penyesuaian",
             'jenis': False,
             'no_daftar': dt_peny_out['no_daftar'],
             'tanggal': dt_peny_out['tanggal'],
             'jenis_dokumen': response3,
             'pengaju': pengaju,
             'done': False,
             'id_pengajuan': dt_peny_out['id_pengajuan']
             }
        list_peny_out.append(a)
    for c in list_peny_out:
        datalist.append(c)

        print(c)

    return GetPemberitahuansDataResponsemodel(data=GetPemberitahuansResponseModel(
        data=datalist
    ))
