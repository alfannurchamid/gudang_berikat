import datetime
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


class Akuns(BaseModel):
    catatan: str
    debet: int
    kredit: int
    id_akun: str
    saldo: int
    type: bool


class AddJurnalData(BaseModel):
    list_akun: List[Akuns]
    tanggal: datetime.date
    keterangan: str

# , payload=Depends(Autentication())


async def add_jurnal_umum(data: AddJurnalData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    reg_jurnal = RegulatorJurnal(
        jenis=True, deskripsi=data.keterangan, id_transaksi="0")
    ket = ""
    list_absen = ""
    list_value = {}

    session.add(reg_jurnal)
    session.commit()
    # session.delete(reg_jurnal)
    id_reg = session.execute(sa.select(RegulatorJurnal.id_reg_jurnal).order_by(
        RegulatorJurnal.id_reg_jurnal.desc())).scalar()

    for data_akun in data.list_akun:

        ket += "=" + data_akun.id_akun + " d: " + \
            str(data_akun.debet) + ",k: " + str(data_akun.kredit)
        catatan = ""
        if data_akun.catatan == "":
            catatan = data.keterangan

        old_saldo = data_akun.saldo

        print('list absen', list_absen, '|', data_akun.id_akun)
        print('list value', list_value, '|')
        x = list_absen.find(f"-{data_akun.id_akun};")
        if x != -1:
            print("sudah ada ", data_akun.id_akun, '|', list_value)
            old_saldo = list_value[data_akun.id_akun]

        new_saldo = old_saldo - data_akun.debet + data_akun.kredit

        if data_akun.type:
            new_saldo = old_saldo + data_akun.debet - data_akun.kredit
        print('new saldoo', new_saldo)

        Jurnal_Umum = JurnalUmum(
            tanggal=data.tanggal, keterangan=f"{catatan}", id_akun=data_akun.id_akun, debet=data_akun.debet, kredit=data_akun.kredit, id_reg=id_reg, current_saldo=new_saldo)
        session.add(Jurnal_Umum)
        values_akun1 = {"saldo": new_saldo}
        result_akun = session.execute(
            sa.update(Akun).values(
                **values_akun1).where(Akun.id_akun == data_akun.id_akun)
        )

        list_value[data_akun.id_akun] = new_saldo
        list_absen += '-' + data_akun.id_akun+';'

    user_id = payload.get('uid', 0)
    # user_id = "1"
    user_log = UserLog(
        id_user=user_id, jenis='jur_u_add', keterangan=f"mencatat jurnal umum == {ket}", id_doc=id_reg)
    session.add(user_log)
    session.commit()

    return Response(status_code=204)
