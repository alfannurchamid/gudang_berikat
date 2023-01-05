from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.standar_doc import StandarDoc
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddStandarDocData(BaseModel):
    id_doc: str
    nomor: str


async def add_standar_doc(data: AddStandarDocData, session=Depends(get_db_session)):

    with Session(db_engine) as session:
        standar_doc = StandarDoc(
            id_doc=data.id_doc,
            nomor=data.nomor
        )
        session.add(standar_doc)
        session.commit()

        return Response(status_code=204)
