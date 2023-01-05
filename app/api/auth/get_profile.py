from typing import List
from fastapi import Depends
import sqlalchemy as sa

from app.api_models import BaseResponseModel
from app.api_models.profile_model import ProfileModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session


from app.models.user import User


class Tugasy():
    rw: str
    rt: List[str]


class GetProfileResponseModel(BaseResponseModel):
    data: ProfileModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id': 1000,
                    'username': 'alpen',
                    'access_token': 'alfan nurchamid',
                    'email': 'alfannurchamid@gmial.com',
                    'noWa': '089681709727',
                    'access': '0',
                    'path_foto': 'skjdalk.jpg',
                    'alamat': 'rt1,rw2,ngalian,wadaslintang',
                    'nik': '3307080409009990',
                    'data_penduduk': {
                                'nama': 'nama lengkap',
                                'desa': 'nama desa',
                                'rw': '2',
                                'rt': '1',
                                'tgl_lh': '12/12/1999',
                                'kot_lh': 'wonosobo',
                                'kawin': 'b'
                    },
                    'anggal_daftar': '12-20-2022'
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_profile(payload=Depends(Autentication()), session=Depends(get_db_session)):
    # #optimistik (aku yakin di payload ada 'uid')
    # user_id = payload['uid']

    # pesimistik (aku tdk yakin di payload ada 'uid' ,dikasih default 0)
    user_id = payload.get('uid', 0)
    dataPengguna = False
    profile = session.execute(
        sa.select(
            User.id_user,
            User.username,
            User.full_name,
            User.noWa,
            User.access,
            User.path_foto,
            User.created_at
        ).where(
            User.id_user == user_id
        )
    ).fetchone()

    return GetProfileResponseModel(data=ProfileModel(
        id=profile.id_user,
        username=profile.username,
        full_name=profile.full_name,
        noWa=profile.noWa,
        access=profile.access,
        path_foto=profile.path_foto,
        tanggal_daftar=profile.created_at,
        jabatan=""
    ))
