import os
import random
import shutil

import sqlalchemy as sa
from fastapi import Depends, File, UploadFile
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.get_db_session import get_db_session
from app.models.user import User


class UploadPpDataResponseModel(BaseModel):
    file_name: str


class UploadPpResponseModel(BaseResponseModel):
    data: UploadPpDataResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'file_name': 'asasda.jpg'
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def upload_pp(file: UploadFile, session=Depends(get_db_session)):

    userya = session.execute(
        sa.select(
            User.path_foto
        ).where(User.username == file.filename)
    ).fetchone()

    print(userya[0])
    if userya[0] != "NULL":
        os.remove("foto_profile/"+userya[0])
    print(file.filename)
    print(file.content_type)
    type = file.content_type.split('/')
    rand = random.randint(1000, 9999)
    filename = file.filename+str(rand)+'.'+type[1]

    with open(f'foto_profile/{filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        return UploadPpResponseModel(
            data=UploadPpDataResponseModel(
                file_name=filename
            )
        )
