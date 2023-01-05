from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.customer import Customer
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetCustomersResponseModel(BaseModel):
    data: List[object]


class GetCustomersDataResponsemodel(BaseResponseModel):
    data: GetCustomersResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'nama_customer': 'Contoh Nama customer',
                        'asal_negara': 'CN'
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


async def get_data_customers(session=Depends(get_db_session)):
    response = session.execute(
        sa.select(
            Customer.id_customer,
            Customer.nama_customer
        )
    ).all()
    datalist = []

    for Custome in response:
        datalist.append(Custome)

    return GetCustomersDataResponsemodel(data=GetCustomersResponseModel(
        data=datalist
    ))
