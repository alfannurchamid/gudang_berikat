from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.dependencies.get_db_session import get_db_session
from app.models.transaksi_out import Transaksi_out


class EditTransaksi_outData(BaseModel):
    no_daftar: str


async def edit_Transaksi_out(data: EditTransaksi_outData, session=Depends(get_db_session)):
    values_to_update = {'ajukan_penyesuaian': True}

    result = session.execute(
        sa.update(Transaksi_out).values(
            **values_to_update).where(Transaksi_out.no_daftar == data.no_daftar)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Dokumen not found')

    session.commit()
    return Response(status_code=204)
