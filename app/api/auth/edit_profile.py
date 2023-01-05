
from typing import Optional

import sqlalchemy as sa
from fastapi import Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, root_validator
from werkzeug.security import generate_password_hash

from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session

from app.models.user import User


class EditProfileData(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    password: Optional[str]
    confirm_password: Optional[str]
    path_foto: Optional[str]
    noWa: Optional[str]

    @root_validator
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password and confirm_password != password:
            raise HTTPException(
                400, 'katasandi tidak sama ,ulangi dengan  benar !')

        return values


async def edit_profile(data: EditProfileData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    profile_data = jsonable_encoder(data)
    user_id = payload.get('uid', 0)

    # TODO:
    values_to_update = {}

    if 'username' in profile_data and profile_data['username']:
        # check username exist
        check_username = session.execute(
            sa.select(User.id_user).where(
                sa.and_(
                    User.username == profile_data['username'],
                    User.id_user != user_id
                )
            )
        ).fetchone()

        if check_username:
            raise HTTPException(400, 'Username telah digunakan akun lain')

        values_to_update.update({'username': profile_data['username']})

    if 'full_name' in profile_data and profile_data['full_name']:
        values_to_update.update({'full_name': profile_data['full_name']})

    if 'password' in profile_data and profile_data['password']:
        password = generate_password_hash(profile_data['password'])
        values_to_update.update({'password': password})

    if 'noWa' in profile_data and profile_data['noWa']:
        check_noWa = session.execute(
            sa.select(User.id_user).where(
                sa.and_(
                    User.noWa == profile_data['noWa'],
                    User.id_user != user_id
                )
            )
        ).fetchone()

        if check_noWa:
            raise HTTPException(
                400, 'nomor whatsapp telah digunakan akun lain')
        values_to_update.update({'noWa': profile_data['noWa']})

    if 'path_foto' in profile_data and profile_data['path_foto']:
        values_to_update.update({'path_foto': profile_data['path_foto']})

    result = session.execute(
        sa.update(User).values(
            **values_to_update).where(User.id_user == user_id)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='User not found')

    session.commit()
    return Response(status_code=204)
