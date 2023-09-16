from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.user_log import UserLog
from app.models.user import User
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddUserLogData(BaseModel):
    id_user: str
    keterangan: str
    jenis: str
    id_doc: Optional[str]


async def create_user_log(data: AddUserLogData, session=Depends(get_db_session)):
    datanya = jsonable_encoder(data)
    check_user = session.execute(
        sa.select(User.id_user).where(User.id_user ==
                                      data.id_user)
    ).scalar()
    if not check_user:
        raise HTTPException(
            400, detail='useer tidak terdaftar')

    user_log = UserLog(
        id_user=data.id_user, jenis=data.jenis, keterangan=data.keterangan
    )
    if "id_doc" in datanya and datanya["id_doc"]:
        barang = UserLog(
            id_user=data.id_user, jenis=data.jenis, keterangan=data.keterangan, id_doc=datanya[
                'id_doc']
        )

    with Session(db_engine) as session:

        session.add(user_log)
        session.commit()

        return Response(status_code=204)
