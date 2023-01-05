from app.api_models import BaseResponseModel
from app.utils.generate_verification_token import generate_verification_token
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from pydantic import BaseModel
# from heyoo import WhatsApp
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, Response
from app.utils.send_whatsapp_massage import WhatsApp
import sqlalchemy as sa
from typing import Optional

import random

err = {'error':
       {'message': '(#131009) Parameter value is not valid',
        'type': 'OAuthException',
        'code': 131009,
        'error_data': {
            'messaging_product': 'whatsapp',
            'details': 'Parameter Invalid'},
        'error_subcode': 2494010,
        'fbtrace_id': 'ABXMXo-YQdjkpNKjSN4KL4n'}
       }
err = {"error":
       {"message":
        "(#131009) Parameter value is not valid",
        "type": "OAuthException",
        "code": 131009,
        "error_data": {
            "messaging_product": "whatsapp",
            "details": "Parameter Invalid"},
        "error_subcode": 2494010,
        "fbtrace_id": "AJdqDQ_yaXjAHzA1Ba2NKrt"}
       }

messenger = WhatsApp()
# messenger = WhatsApp('EAALIAfYZASCQBAGY6MUo8jZAd6qAJbhE1EZCX0Af8x6lwwQUxmX6dGZA2GMrAe2JZBPZC3vzVzZAXFRCgC5Qr5dYOY9VtenpCgpZC3cUW7a8fbqT3KhgMG3c0ZAawfz971LJMpjX7ojZB62FnL7A4hTvF9oGTtcyFqvHu39LUtKbLwAfrhgzdENwgO', phone_number_id='113756431518535')


class CreateVerifiData(BaseModel):
    username: Optional[str]
    no_wa: Optional[str]


class CreateVerifiModel(BaseModel):
    verifi_token: str
    expired_at: int
    no_wa: str


class SendVerifiResponseModel(BaseResponseModel):
    data: CreateVerifiModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'verifi_token': 'jkl,nmo.pqr',
                    'expired_at': 123456,
                    'no_wa': "089763652863"
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


def sendWa(data: CreateVerifiData, session=Depends(get_db_session)):
    profile_data = jsonable_encoder(data)
    no_wa = ""
    username = ""

    if 'username' in profile_data and profile_data['username']:
        username = profile_data['username']
        # select noWa user by username
        profile = session.execute(
            sa.select(
                User.noWa
            ).where(User.username == profile_data['username'])
        ).scalar()

        if profile == None:
            print("Username tidak terdaftar")
            raise HTTPException(400, 'Username tidak terdaftar')
        if profile == sa.null or profile == 'NULL':
            print("nomor whatsapp tidak tercantum")
            raise HTTPException(
                400, 'nomor whatsapp tidak tercantum dalam akun anda')
        # print(profile)
        no_wa = profile
        print(no_wa)

    if 'no_wa' in profile_data and profile_data['no_wa']:
        no_wa = profile_data['no_wa']

    random_number = random.randint(1000, 9999)
    print(random_number)

    payload = {
        'no_wa': no_wa,
        'verifi_kode': random_number,
        'username': username
    }

    verifi_token, expired_at = generate_verification_token(
        payload)  # type: ignore
    # print(verifi_token)
    # N: raise http > "username tidak terdaftar "
    # Y: - buat kode verivy
    # Y: - tambah ke db
    # Y: - kirim kode ke wa
    if no_wa.startswith("0"):
        # s
        xlice = no_wa[1:len(no_wa)]
        no_wa = '62'+xlice
    print(no_wa)
    mengirim = messenger.send_message(no_wa, random_number)

    if 'error' in mengirim and mengirim['error']['code'] == 131009:
        print('erroooorrrr')
        raise HTTPException(
            400, f'nomor anda {no_wa} tidak terdaftar ke akun Whatsapp')
    if 'error' in mengirim and mengirim['error']['code'] == 100:
        print('erroooorrrr')
        raise HTTPException(
            400, f'Waktu habis')
    if mengirim:
        return SendVerifiResponseModel(data=CreateVerifiModel(
            verifi_token=verifi_token,
            expired_at=expired_at,
            no_wa=no_wa
        ))
