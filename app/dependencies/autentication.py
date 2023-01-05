from typing import Optional

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.get_payload import get_payload


class Autentication(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        authorization = await super().__call__(request)

        if not authorization.credentials:
            return {}

        try:
            payload = get_payload(authorization.credentials)

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
