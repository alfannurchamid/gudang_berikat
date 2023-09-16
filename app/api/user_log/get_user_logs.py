from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
from fastapi.encoders import jsonable_encoder
import sqlalchemy as sa
from typing import List, Optional


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.user_log import UserLog
from app.models.user import User

from app.utils.db import db_engine


class GetUserLogData(BaseModel):
    type: Optional[str]
    index: Optional[int]
    tanggal_awal: Optional[str]
    tanggal_ahir: Optional[str]


class GetUserLogResponseModel(BaseModel):
    data: List[object]


class GetUserLogDataResponsemodel(BaseResponseModel):
    data: GetUserLogResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'id_user': '1',
                        'nama_user': 'alfan nurchamid',
                        'id_doc': '930070',
                        'jenis': 'po_add',
                        'tanggal': '2023-01-31 11:43:07.000',
                        'keterangan': "bla bla ",
                        'access': "admin"
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_user_logs(data: GetUserLogData, session=Depends(get_db_session)):
    data_post = jsonable_encoder(data)

    index: int = 0
    if 'index' in data_post and data_post['index']:
        index = data_post['index']

    awal = index * 5
    akhir = awal + 4

    awal = str(awal)
    akhir = str(akhir)

    part = ""
    range = ""
    # if data include "part"
    if "type" in data_post and data_post['type']:
        data_ytpe = data_post['type']
        part = f"WHERE jenis LIKE '{data_ytpe}%' "

    if "tanggal_awal" in data_post and data_post['tanggal_awal']:
        range = f"  created_at BETWEEN {data_post['tanggal_awal']} AND {data_post['tanggal_ahir']} "
        part = part + " AND " + range

    sql = f"SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY id_log DESC) AS R, id_log, id_user,created_at,keterangan,jenis,id_doc FROM user_log {part}) AS TR WHERE  R BETWEEN {awal} AND {akhir} ;"

    # sql = f"""SELECT * FROM user_log ORDER BY created_at DESC"""
    response = session.execute(
        sa.text(sql)
    ).all()
    datalist = []

    for Bara in response:

        data_user = session.execute(sa.select(User.full_name, User.access).where(
            User.id_user == Bara.id_user)).fetchone()
        accsess = "BC"
        if data_user[1] == 1:
            accsess = "admin"
        elif data_user[1] > 1:
            accsess = "super admin"

        a = {
            'id_user': '1',
            'id_log': Bara.id_log,
            'nama_user': data_user[0],
            'id_doc': Bara.id_doc,
            'jenis': Bara.jenis,
            'keterangan': Bara.keterangan,
            'tanggal': Bara.created_at,
            'access': accsess}
        datalist.append(a)

    return GetUserLogDataResponsemodel(data=GetUserLogResponseModel(
        data=datalist
    ))
