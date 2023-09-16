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


class GetLaporan_posisisData(BaseModel):
    mulai: Optional[str]
    ahir: Optional[str]
    yes: str


class GetLaporan_posisisResponseModel(BaseModel):
    data: List[object]


class GetLaporan_posisisDataResponsemodel(BaseResponseModel):
    data: GetLaporan_posisisResponseModel

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


async def get_data_lap_posisi(data: GetLaporan_posisisData, session=Depends(get_db_session)):
    sql = f"SELECT * FROM transaksi_in JOIN baarang on  transaksi_in.kode_barang = baarang.kode_barang WHERE transaksi_in.acc = {True} ORDER BY transaksi_in.tanggal LIMIT 5"
    data_range = jsonable_encoder(data)
    if "mulai" in data_range and data_range["mulai"]:
        print("pindahhh")
        sql = f"SELECT * FROM transaksi_in JOIN baarang on  transaksi_in.kode_barang = baarang.kode_barang WHERE transaksi_in.acc = {True} AND  transaksi_in.tanggal BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' "

    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:
        nilai_pab_in = Custome.jumlah * Custome.harga_satuan * Custome.exchange_rate
        data_one = {
            "jenis_in": Custome.jenis,
            "no_daftar_in": Custome.no_daftar,
            "tanggal_daftar_in": Custome.tanggal_daftar,
            "tanggal_in": Custome.tanggal,
            "kode_barang_in": Custome.kode_barang,
            "jumlah_in": Custome.jumlah,
            "nama_barang_in": Custome.nama_barang,
            "satuan": Custome.satuan,
            "nilai_pabean_in": nilai_pab_in,
            "harga_satuan_in": Custome.harga_satuan,
            "saldo_jml_in": Custome.saldo_jml,
            "pabean_in": Custome.pabean
        }
        sql2 = f"SELECT * FROM transaksi_out WHERE nomor_daftar_in = '{Custome.no_daftar}' AND  acc = {True}"
        response2 = session.execute(sa.text(sql2))
        data_one.update({'jenis_out': "",
                         "no_daftar_out": "",
                         "tanggal_daftar_out": "",
                         "tanggal_out": "",
                         "jumlah_out": "",
                         "nilai_pabean_out": "",
                         "pabean_out": ""
                         })
        if response2:

            for Data_out in response2:
                print("aaaaaaaaaaaaaaaaaa")
                data_one.update({'jenis_out': Data_out.jenis,
                                 "no_daftar_out": Data_out.no_daftar,
                                 "tanggal_daftar_out": Data_out.tanggal_daftar,
                                 "tanggal_out": Data_out.tanggal,
                                 "jumlah_out": Data_out.jumlah,
                                 "nilai_pabean_out": Data_out.jumlah * Data_out.harga_satuan,
                                 "harga_satuan_out": Data_out.harga_satuan,
                                 "saldo_jml_out": Data_out.saldo_jml,
                                 "pabean_out": Data_out.pabean

                                 })

        # print("tes")
        datalist.append(data_one)

    return GetLaporan_posisisDataResponsemodel(data=GetLaporan_posisisResponseModel(
        data=datalist
    ))
