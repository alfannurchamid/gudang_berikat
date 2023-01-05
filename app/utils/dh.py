from typing import Optional

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from app.utils.get_payload import get_payload


def Dh(key: str):
    authorization = key

    if not authorization:
        return {}  # type: ignore

    try:
        payload = get_payload(authorization)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            401,
            detail={
                'message': 'Token expired',
                'code': 40100
            }
        )

    except jwt.DecodeError:
        raise HTTPException(
            401,
            detail={
                'message': 'Token infalid',
                'code': 40101
            }
        )

    return payload  # type: ignore
