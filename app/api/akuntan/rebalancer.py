from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.dependencies.get_db_session import get_db_session
from typing import List


from app.models.regulator_jurnal import RegulatorJurnal
from app.models.jurnal_umum import JurnalUmum
from app.models.akun import Akun


from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog


class ReBalancerJurnalData(BaseModel):
    id_reg: str


async def rebalancer(data: ReBalancerJurnalData, session=Depends(get_db_session)):

    sql = f"""SELECT id_akun,id_jurnal FROM jurnal_umum WHERE id_reg = '{data.id_reg}' """

    akun_list_jurnal = session.execute(sa.text(sql)).all()

    for akun in akun_list_jurnal:
        sql2 = f"""SELECT current_saldo FROM jurnal_umum WHERE id_akun = '{akun['id_akun']}'  AND  id_jurnal < {akun['id_jurnal']} ORDER BY id_jurnal DESC"""
        saldo_lama_1 = session.execute(sa.text(sql2)).scalar()
        print(akun['id_akun'], '|', akun['id_jurnal'], '|', saldo_lama_1)

        values_to_update = {'saldo': 0}
        if saldo_lama_1 != None:
            values_to_update = {'saldo': saldo_lama_1}
        result = session.execute(
            sa.update(Akun).values(
                **values_to_update).where(Akun.id_akun == akun['id_akun'])
        )

        result2 = session.execute(
            sa.text(f""" DELETE FROM jurnal_umum WHERE id_jurnal = '{akun['id_jurnal']}' """))

        if result2.rowcount == 0:
            raise HTTPException(400, detail='User not found')

    # ===========================

    session.commit()
