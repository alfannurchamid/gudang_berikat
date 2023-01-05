from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.customer import Customer
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class AddCustomerData(BaseModel):
    nama_customer: str


async def add_customer(data: AddCustomerData, session=Depends(get_db_session)):

    with Session(db_engine) as session:
        customer = Customer(
            nama_customer=data.nama_customer
        )
        session.add(customer)
        session.commit()

        return Response(status_code=204)
