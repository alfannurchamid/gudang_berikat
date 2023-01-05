# import profile
# import sqlalchemy as sa
# from fastapi import Depends

# from app.api_models import BaseResponseModel
# from app.api_models.profile_model import ProfileModel
# from app.dependencies.autentication import Autentication
# from app.dependencies.get_db_session import get_db_session
# from app.models.user import User


# class GetsProfileResponseModel(BaseResponseModel):
#     data: [ProfileModel]

#     class Config:
#         schema_extra = {
#             'example': {
#                 'data': [{
#                     'id': 1000,
#                     'username': 'alpen',
#                     'access_token': 'alfan nurchamid',
#                     'email': 'alfannurchamid@gmial.com',
#                     'noWa': '089681709727',
#                     'access': '0',
#                     'path_foto': 'skjdalk.jpg',
#                     'alamat': 'rt1,rw2,ngalian,wadaslintang',
#                     'nik': '3307080409009990'
#                 }],
#                 'meta': {},
#                 'success': True,
#                 'message': 'Success',
#                 'code': 200
#             }
#         }


# async def gets_profile(payload=Depends(Autentication()), session=Depends(get_db_session)):
#     # #optimistik (aku yakin di payload ada 'uid')
#     # user_id = payload['uid']

#     # pesimistik (aku tdk yakin di payload ada 'uid' ,dikasih default 0)
#     user_id = payload.get('uid', 0)
#     profile = session.execute(
#         sa.select(
#             User.id,
#             User.username,
#             User.full_name,
#             User.email,
#             User.noWa,
#             User.nik,
#             User.alamat,
#             User.access,
#             User.path_foto
#         ).where(
#             User.access == 1
#         )
#     )
#     datanya = []
#     for us in profile:
#         datanya.append(ProfileModel(
#             id=us.id,
#             username=us.username,
#             full_name=us.full_name,
#             email=us.email,
#             noWa=us.noWa,
#             access=us.access,
#             nik=us.nik,
#             path_foto=us.path_foto,
#             alamat=us.alamat
#         ))

#     return GetsProfileResponseModel(data=datanya)
