from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from sqlalchemy.orm import Session


class DeletePurchaseOrderData(BaseModel):
    id_po: str


async def delete_po(data: DeletePurchaseOrderData, session=Depends(get_db_session)):

    result2 = session.execute(
        sa.text(f""" DELETE FROM purchase_order WHERE id_po = '{data.id_po}' """))

    if result2.rowcount == 0:
        raise HTTPException(400, detail='po not found')

    session.commit()
    return Response(status_code=204)
