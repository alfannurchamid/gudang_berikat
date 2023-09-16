from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder

from typing import List, Optional


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel

from app.models.barang import Barang
from app.models.suplier import Suplier
from app.models.transaksi_in import Transaksi_in
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetLaporan_mutasiData(BaseModel):
    mulai: str
    ahir: str


class GetLaporan_mutasiResponseModel(BaseModel):
    data: List[object]


class GetLaporan_mutasiDataResponsemodel(BaseResponseModel):
    data: GetLaporan_mutasiResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        "jenis_in": "BC 2.3",
                        "no_daftar_in": "0004168",
                        "tanggal_daftar_in": "2023-01-12",
                        "tanggal_in": "2023-01-12",
                        "kode_barang_in": "56031300 B",
                        "nama_barang_in": "SPUNBOWN BLA BLA B",
                        "satuan": "KGM",
                        "harga_satuan_in": 1.3,
                        "nilai_pabean_in": 1000000,
                        "no_daftar_out": "0004168",
                        "tanggal_daftar_out": "2023-01-12",
                        "tanggal_out": "2023-01-12",
                        "kode_barang_out": "56031300 B",
                        "satuan": "KGM",
                        "harga_satuan_out": 1.3,
                        "nilai_pabean_out": 1000000
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_lap_mutasi(data: GetLaporan_mutasiData, session=Depends(get_db_session)):
    data_range = jsonable_encoder(data)
    sql = "SELECT * FROM baarang  LIMIT 5"

    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:
        data_one = {
            "kode_barang": Custome.kode_barang,
            "nama_barang": Custome.nama_barang,
            "satuan": Custome.satuan,
        }

        datetime_str = '2023-01-01'

        x = 0
        pemasukan = 0
        pengeluaran = 0
        opname = 0
        penyesuaian = 0
        saldo_ahir = 0
        keterangan = ""

        tanggal_ahir = datetime.strptime(datetime_str, '%Y-%m-%d')
        tanggal_ahir = tanggal_ahir.date()

        # sql with range

        sql2 = f"SELECT jumlah, saldo_jml,tanggal FROM transaksi_in  WHERE kode_barang = '{Custome.kode_barang}' AND tanggal BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tanggal "
        sql3 = f"SELECT jumlah, saldo_jml, tanggal  FROM transaksi_out  WHERE kode_barang = '{Custome.kode_barang}' AND tanggal BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tanggal"
        sql4 = f"SELECT * FROM rijek  WHERE kode_barang = '{Custome.kode_barang}' AND tgl_rijek BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tgl_rijek"
        sql5 = f"SELECT * FROM opname  WHERE kode_barang = '{Custome.kode_barang}' AND tgl_opname BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tgl_opname"

        # count pemasukan
        response2 = session.execute(sa.text(sql2))
        for Data_in in response2:
            pemasukan += Data_in.jumlah
            saldo_ahir = Data_in.saldo_jml
            tanggal_ini = Data_in.tanggal
            print(tanggal_ini)
            tanggal_ahir = tanggal_ini
            print(tanggal_ahir)

        # count pengeluaran
        response3 = session.execute(sa.text(sql3))
        for Data_in in response3:
            pengeluaran += Data_in.jumlah
            tanggal_ini = Data_in.tanggal
            if tanggal_ini >= tanggal_ahir:
                saldo_ahir = Data_in.saldo_jml
                tanggal_ahir = tanggal_ini

        # count penyesuaian
        response4 = session.execute(sa.text(sql4))
        for Data_in in response4:
            penyesuaian += Data_in.jumlah_rijek
            tanggal_ini = Data_in.tgl_rijek
            if tanggal_ini >= tanggal_ahir:
                saldo_ahir = Data_in.saldo_jml

        # count opname
        response5 = session.execute(sa.text(sql5))
        for Data_in in response5:
            print("OPNAMEEE")
            opname = Data_in.jml_opname
            keterangan = Data_in.keterangan

        data_one.update({'saldo_awal': 0,
                         "pemasukan": pemasukan,
                         "saldo_ahir": saldo_ahir,
                         "pengeluaran": pengeluaran,
                         "penyesuaian": penyesuaian,
                         "stok_opname": opname,
                         "selisih": pemasukan - pengeluaran - opname,
                         "ket": keterangan
                         })

        # print("tes")
        datalist.append(data_one)

    return GetLaporan_mutasiDataResponsemodel(data=GetLaporan_mutasiResponseModel(
        data=datalist
    ))
