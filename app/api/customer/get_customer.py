from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.customer import Customer
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetCustomerData(BaseModel):
    id_customer: str


class GetCustomerResponseModel(BaseModel):
    id_customer: str
    nama_customer: str


class GetCustomerDataResponsemodel(BaseResponseModel):
    data: GetCustomerResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id_customer': '2',
                    'nama_customer': 'PT.Berkah Abadi',
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_customer(data: GetCustomerData, session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Customer.nama_customer
        ).where(Customer.id_customer == data.id_customer)
    ).fetchone()

    return GetCustomerDataResponsemodel(data=GetCustomerResponseModel(

        id_customer=data.id_customer,
        nama_customer=response.nama_customer
    ))
