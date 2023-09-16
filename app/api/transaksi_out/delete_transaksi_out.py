from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from sqlalchemy.orm import Session
from app.models.transaksi_in import Transaksi_in
from app.models.standar_doc import StandarDoc


class DeleteTransaksiOut(BaseModel):
    no_daftar: str


async def delete_T_out(data: DeleteTransaksiOut, session=Depends(get_db_session)):
    T_out = session.execute(sa.text(
        f"SELECT acc, nomor_daftar_in from transaksi_out WHERE no_daftar = '{data.no_daftar}'")).fetchone()

    if T_out[0] != 0:
        raise HTTPException(
            400, detail='dokumen berkaitan dengan dokumen penjualan ,pencatatan dokumen penjualan telah ada !')

    values_to_update = {'done': False}

    result = session.execute(
        sa.update(Transaksi_in).values(
            **values_to_update).where(Transaksi_in.no_daftar == T_out[1])
    )

    result = session.execute(
        sa.update(StandarDoc).values(
            **values_to_update).where(StandarDoc.nomor == data.no_daftar)
    )

    result2 = session.execute(
        sa.text(f""" DELETE FROM transaksi_out WHERE no_daftar = '{data.no_daftar}' """))

    if result2.rowcount == 0:
        raise HTTPException(400, detail='T out not found')

    session.commit()
    return Response(status_code=204)
