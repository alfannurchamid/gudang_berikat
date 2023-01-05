
from getpass import getuser
from os import access
from fastapi import Depends, HTTPException, Response
from pydantic import BaseModel
from app.api_models import BaseResponseModel
import time
import sqlalchemy as sa

from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.utils.generate_access_token import generate_access_token

from fastapi.encoders import jsonable_encoder
from app.config import config

from app.models.user import User


class CheckVerifiData(BaseModel):
    verification_kode: str


class CheckVeriVicationModel(BaseModel):
    access_token: str
    expired_at: int


class CheckVerificationResponseModel(BaseResponseModel):
    data: CheckVeriVicationModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'access_token': 'abc.def.ghi',
                    'expired_at': 123456
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def check_verifi(data: CheckVerifiData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    # profile_data = jsonable_encoder(data)
    access_token = ""
    values_to_update = {}
    user_wa = payload.get('no_wa', 0)
    verifi = payload.get('verifi_kode', 0)
    username = payload.get('username', 0)
    filter = User.username == username

    def getUser(filter):
        user = session.execute(
            sa.select(
                User.id_user,
                User.access
            ).where(
                filter
            )
        ).fetchone()
        return user

    def updateAccess(user):
        useraccess = 0
        if user.access == 0:
            useraccess = 1
        if user.access == 3:
            useraccess = 4
        print(useraccess)
        values_to_update.update({'access': useraccess})
        result = session.execute(
            sa.update(User).values(
                **values_to_update).where(User.id_user == user.id)
        )

        print(user)
        print(user.id_user)
        print(user.access)
        print('updated')

        if result.rowcount == 0:
            raise HTTPException(400, detail='User not found')
        session.commit()
        return Response(status_code=204)

    print('verifikasi dari token', verifi)
    print(data.verification_kode)
    print(payload)

    if data.verification_kode != str(verifi):
        raise HTTPException(401, detail='kode verivikasi tidak sesuai')
    print('success')
    if username == "":
        # update access user
        filteres = User.noWa == user_wa
        user = getUser(filteres)
        updateAccess(user)
        return Response(status_code=204)
    else:
        filteres = User.username == username
        user = getUser(filteres)

        print(user)
        payload = {
            'uid': user.id_user,
            'username': username
        }
        print('payload kedua')
        print(payload)

        access_token, expired_at = generate_access_token(
            payload)  # type: ignore
        print(access_token)

        print(user_wa)
        print(verifi)

        return CheckVerificationResponseModel(data=CheckVeriVicationModel(
            access_token=access_token,
            expired_at=expired_at))
