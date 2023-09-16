from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from sqlalchemy.orm import Session
from app.models.purchase_order import Purchase_order
from app.models.standar_doc import StandarDoc


class DeleteTransaksiIn(BaseModel):
    no_daftar: str


async def delete_T_in(data: DeleteTransaksiIn, session=Depends(get_db_session)):
    T_in = session.execute(sa.text(
        f"SELECT done, id_po from transaksi_in WHERE no_daftar = '{data.no_daftar}'")).fetchone()

    if T_in[0] != 0:
        raise HTTPException(
            400, detail='dokumen berkaitan dengan dokumen penjualan ,pencatatan dokumen penjualan telah ada !')

    values_to_update = {'done': False}

    result = session.execute(
        sa.update(Purchase_order).values(
            **values_to_update).where(Purchase_order.id_po == T_in[1])
    )

    result = session.execute(
        sa.update(StandarDoc).values(
            **values_to_update).where(StandarDoc.nomor == data.no_daftar)
    )

    result2 = session.execute(
        sa.text(f""" DELETE FROM transaksi_in WHERE no_daftar = '{data.no_daftar}' """))

    if result2.rowcount == 0:
        raise HTTPException(400, detail='T in not found')

    session.commit()
    return Response(status_code=204)
