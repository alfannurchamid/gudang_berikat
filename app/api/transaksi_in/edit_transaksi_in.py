from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.dependencies.get_db_session import get_db_session
from app.models.barang import Barang
from app.models.transaksi_in import Transaksi_in
from app.models.regulator_jurnal import RegulatorJurnal
from app.models.jurnal_umum import JurnalUmum
from app.models.akun import Akun


from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog
from app.models.purchase_order import Purchase_order


class EditTransaksiInData(BaseModel):
    no_daftar: str


async def edit_transaksi_in(data: EditTransaksiInData, payload=Depends(Autentication()), session=Depends(get_db_session)):

    id_payment = ""
    id_persediaan = ""

    # ambil data dokumen
    data_dok = session.execute(sa.select(Transaksi_in.grad_total, Transaksi_in.exchane_rate, Transaksi_in.jumlah,
                               Transaksi_in.kode_barang, Transaksi_in.administrasi_import, Transaksi_in.id_po).where(Transaksi_in.no_daftar == data.no_daftar)).fetchone()
    print(data_dok[0])

    # ambil id akun s dari barang
    ids = session.execute(sa.select(
        Barang.akun_persediaan
    ).where(Barang.kode_barang == data_dok[3])).scalar()

    id_persediaan = ids

    # ambil id akun payment
    id_payment = session.execute(sa.select(Purchase_order.id_akun_payment).where(
        Purchase_order.id_po == data_dok[5])).scalar()

    # print("----------------------", id_persediaan, id_payment)

    values_to_update = {'acc': True}

    result = session.execute(
        sa.update(Transaksi_in).values(
            **values_to_update).where(Transaksi_in.no_daftar == data.no_daftar)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Pengajuan not found')

    user_id = payload.get('uid', 0)
    user_log = UserLog(
        id_user=user_id, jenis='t_in_acc', keterangan=f"memberikan ACC dokumen pemasukan  no: -{data.no_daftar}", id_doc=data.no_daftar)
    reg_jurnal = RegulatorJurnal(
        jenis=True, deskripsi=f"dari pencatatan dokumen pemasukan  no: -{data.no_daftar}", id_transaksi=data.no_daftar)

    session.add(reg_jurnal)
    # session.commit()

    # ambil saldo barang
    saldoBarang = session.execute(
        sa.select(
            Barang.saldo
        ).where(Barang.kode_barang == data_dok[3])
    ).scalar()

    new_saldo = saldoBarang + data_dok[2]
    values_to_update = {'saldo': new_saldo}

    #  update stok
    result = session.execute(
        sa.update(Barang).values(
            **values_to_update).where(Barang.kode_barang == data_dok[3])
    )

    # get data akun
    data_akun_persediaan = session.execute(
        sa.select(Akun.saldo).where(Akun.id_akun == id_persediaan)).fetchone()

    new_saldo_persediaan = data_akun_persediaan[0] + data_dok[0] * data_dok[1]

    values_akun1 = {'saldo': new_saldo_persediaan}
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == id_persediaan)
    )

    # get data akun administrasi import
    data_akun_persediaan = session.execute(
        sa.select(Akun.saldo).where(Akun.id_akun == '2.1.4')).fetchone()

    new_saldo_hutang_admin_import = data_akun_persediaan[0] + data_dok[4]

    values_akun1 = {'saldo': new_saldo_hutang_admin_import}
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == '2.1.4')
    )

    # get data akun administrasi import
    data_akun_persediaan = session.execute(
        sa.select(Akun.saldo).where(Akun.id_akun == '5.1')).fetchone()
    new_saldo_admin_import = data_akun_persediaan[0] + data_dok[4]

    values_akun1 = {'saldo': new_saldo_admin_import}
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == '5.1')
    )

    id_reg = session.execute(sa.select(RegulatorJurnal.id_reg_jurnal).order_by(
        RegulatorJurnal.id_reg_jurnal)).scalar()
    Jurnal_Umum_perse = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pemasukan  no: -{data.no_daftar}", id_akun=id_persediaan, debet=data_dok[0] * data_dok[1], id_reg=id_reg, current_saldo=new_saldo_persediaan)

    # utang usaha(payment yang milih di po)
    # get data akun
    data_akun_hutang = session.execute(
        sa.select(Akun.saldo).where(Akun.id_akun == id_payment)).fetchone()
    new_saldo_hutang = data_akun_hutang[0] + data_dok[0] * data_dok[1]
    values_akun1 = {'saldo': new_saldo_hutang}
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == id_payment)
    )

    Jurnal_Umum_hutang = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pemasukan  no: -{data.no_daftar}", id_akun=id_payment, kredit=data_dok[0] * data_dok[1], id_reg=id_reg, current_saldo=new_saldo_hutang)

    Jurnal_Umum_beban_admin_import = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pemasukan  no: -{data.no_daftar}", id_akun='5.1', debet=data_dok[4], id_reg=id_reg, current_saldo=new_saldo_admin_import)

    Jurnal_Umum_hutang_admin_import = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pemasukan  no: -{data.no_daftar}", id_akun='2.1.4', kredit=data_dok[4], id_reg=id_reg, current_saldo=new_saldo_hutang_admin_import)

    session.add(user_log)
    session.add(Jurnal_Umum_perse)
    session.add(Jurnal_Umum_hutang)
    session.add(Jurnal_Umum_hutang_admin_import)
    session.add(Jurnal_Umum_beban_admin_import)

    session.commit()
    return Response(status_code=204)
