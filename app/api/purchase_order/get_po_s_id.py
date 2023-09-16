from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from typing import List


from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.models.purchase_order import Purchase_order
from app.models.barang import Barang
from app.models.suplier import Suplier
from sqlalchemy.orm import Session
from app.utils.db import db_engine


class GetPurchaseOrdersIdResponseModel(BaseModel):
    data: List[object]


class GetPurchaseOrdersIdDataResponsemodel(BaseResponseModel):
    data: GetPurchaseOrdersIdResponseModel

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'data': [{
                        'id_po': 1,
                        "nomorpo": "7239417"
                    }],
                },
                'meta': {},
                'success': True,
                'message': 'Success',
                'code': 200
            }
        }


NOW = datetime.now()

today = NOW.strftime("%Y-%m-%d")

print(today)

sql = f"SELECT id_po,nomor_po ,tgl_minta_kirim FROM purchase_order where tgl_minta_kirim > {today} AND done = false"


async def get_data_purchase_orders_id(session=Depends(get_db_session)):
    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:

        datalist.append(Custome)

    return GetPurchaseOrdersIdDataResponsemodel(data=GetPurchaseOrdersIdResponseModel(
        data=datalist
    ))
