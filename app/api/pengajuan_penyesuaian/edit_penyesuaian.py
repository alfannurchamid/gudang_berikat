from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.dependencies.get_db_session import get_db_session
from app.models.penyesuaian import Penyesuaian


from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog


class EditPenyesuaianData(BaseModel):
    id_pengajuan: str


async def edit_penyesuaian(data: EditPenyesuaianData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    values_to_update = {'done': True}

    result = session.execute(
        sa.update(Penyesuaian).values(
            **values_to_update).where(Penyesuaian.id_pengajuan == data.id_pengajuan)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Pengajuan not found')

    no_daftar = ""

    data_dok = session.execute(sa.select(Penyesuaian.no_daftar, Penyesuaian.jenis).where(
        Penyesuaian.id_pengajuan == data.id_pengajuan)).fetchone()

    jenis_nya = "t_out_put_peny"
    jenis_dokumen = "penjualan"
    if data_dok.jenis:
        jenis_dokumen = "pemasukan"
        jenis_nya = "t_in_put_peny"

    user_id = payload.get('uid', 0)
    user_log = UserLog(
        id_user=user_id, jenis='jenis_nya', keterangan=f"melakukan penyesuaian {jenis_dokumen},dokumen  no: {data_dok.no_daftar}", id_doc=data_dok.no_daftar)

    session.add(user_log)

    session.commit()
    return Response(status_code=204)
