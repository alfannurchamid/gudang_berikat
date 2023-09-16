from pydantic import BaseModel
from fastapi import HTTPException, Response, Depends
import sqlalchemy as sa
from app.dependencies.get_db_session import get_db_session
from app.models.transaksi_out import Transaksi_out

from app.dependencies.autentication import Autentication
from app.models.user_log import UserLog
from app.models.barang import Barang
from app.models.regulator_jurnal import RegulatorJurnal
from app.models.akun import Akun
from app.models.jurnal_umum import JurnalUmum
from app.models.transaksi_in import Transaksi_in


class EditTransaksiInData(BaseModel):
    no_daftar: str


async def edit_Transaksi_out_acc(data: EditTransaksiInData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    saldo_hpp = 0
    saldo_persediaan = 0
    saldo_piutang = 0
    saldo_pendapatan = 0

    id_beban = ""
    id_persediaan = ""

    # ambil data dokumen
    data_dok = session.execute(sa.select(Transaksi_out.grand_total, Transaksi_out.exchane_rate, Transaksi_out.jumlah,
                               Transaksi_out.kode_barang, Transaksi_out.nomor_daftar_in).where(Transaksi_out.no_daftar == data.no_daftar)).fetchone()

    ids = session.execute(sa.select(Barang.akun_beban, Barang.akun_persediaan).where(
        Barang.kode_barang == data_dok[3])).fetchone()

    id_beban = ids[0]
    id_persediaan = ids[1]

    print("==========================", id_beban, id_persediaan)

    list_id = [id_beban, id_persediaan, '1.1.9', '4.1']

    for id_saldo in list_id:
        saldo = session.execute(sa.select(Akun.saldo).where(
            Akun.id_akun == id_saldo)).fetchone()
        match id_saldo:
            case '1.1.9':
                saldo_piutang = saldo[0]
            case '4.1':
                saldo_pendapatan = saldo[0]

        if id_saldo == id_beban:
            saldo_hpp = saldo[0]
            print("masokkk saldo hpp")
        if id_saldo == id_persediaan:
            saldo_persediaan = saldo[0]
            print("masokkk saldo persediaaan")

    values_to_update = {'acc': True}

    result = session.execute(
        sa.update(Transaksi_out).values(
            **values_to_update).where(Transaksi_out.no_daftar == data.no_daftar)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Pengajuan not found')

    user_id = payload.get('uid', 0)
    user_log = UserLog(
        id_user=user_id, jenis='t_out_acc', keterangan=f"memberikan ACC dokumen pengeluaran  no: -{data.no_daftar}", id_doc=data.no_daftar)
    # BUAT REGULATOR JURNAL
    reg_jurnal = RegulatorJurnal(
        jenis=False, deskripsi=f"dari pencatatan dokumen pemasukan  no: -{data.no_daftar}", id_transaksi=data.no_daftar)
    session.add(reg_jurnal)
    session.commit()
    session.delete(reg_jurnal)

    no_daftar_in = data_dok[4]
    data_dok_in = session.execute(sa.text(
        f"""SELECT grand_total,jumlah, exchange_rate FROM transaksi_in WHERE no_daftar = '{no_daftar_in}'""")).fetchone()

    # print(data_dok_in)

    # data baranhg
    barang = session.execute(
        sa.select(Barang.bm, Barang.ppn, Barang.pph)).fetchone()
    bm = barang[0] / 100
    ppn = barang[1] / 100
    pph = barang[2] / 100

    nilai_pabean = 0

    # nilai_saldo hpp transaksi
    # nilai_hpp transaksi ini
    nilai_hpp = (data_dok_in[0] * data_dok_in[2] /
                 data_dok_in[1]) * data_dok[2]
    # update hpp
    values_akun1 = {'saldo': nilai_hpp + saldo_hpp}

    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == id_beban)
    )

    # ambil saldo barang
    saldoBarang = session.execute(
        sa.select(
            Barang.saldo
        ).where(Barang.kode_barang == data_dok[3])
    ).scalar()

    new_saldo = saldoBarang - data_dok[2]
    values_to_update = {'saldo': new_saldo}

    #  update stok
    result = session.execute(
        sa.update(Barang).values(
            **values_to_update).where(Barang.kode_barang == data_dok[3])
    )

    #  update saldo akun

    new_saldo_persediaan = saldo_persediaan - nilai_hpp

    # persediaan
    #  PR cari nilai beli per barang dan hitung dg jmlah penjualan
    values_akun1 = {'saldo': new_saldo_persediaan}
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == id_persediaan)
    )
    id_reg = session.execute(sa.select(RegulatorJurnal.id_reg_jurnal).order_by(
        RegulatorJurnal.id_reg_jurnal.desc())).scalar()

    Jurnal_Umum_perse = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pengeluaran  no: -{data.no_daftar}", id_akun=id_persediaan, kredit=nilai_hpp, id_reg=id_reg, current_saldo=new_saldo_persediaan)
    Jurnal_Umum_hpp = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pengeluaran  no: -{data.no_daftar}", id_akun=id_beban, debet=nilai_hpp, id_reg=id_reg, current_saldo=nilai_hpp + saldo_hpp)

    # piutang
    values_akun1 = {'saldo': saldo_piutang + data_dok[0]}
    print(saldo_piutang + data_dok[0])
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == '1.1.9')
    )

    # pendapatan
    values_akun1 = {'saldo': saldo_pendapatan + data_dok[0] * data_dok[1]}
    result_akun = session.execute(
        sa.update(Akun).values(
            **values_akun1).where(Akun.id_akun == '4.1')
    )

    Jurnal_Umum_piutang = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pengeluaran  no: -{data.no_daftar}", id_akun='1.1.9', debet=data_dok[0] * data_dok[1], id_reg=id_reg, current_saldo=saldo_piutang + data_dok[0])
    Jurnal_Umum_pendapatan = JurnalUmum(
        keterangan=f"dari pencatatan dokumen pengeluaran  no: -{data.no_daftar}", id_akun='4.1', kredit=data_dok[0] * data_dok[1], id_reg=id_reg, current_saldo=data_dok[0] + saldo_pendapatan)

    session.add(user_log)
    session.add(Jurnal_Umum_perse)
    session.add(Jurnal_Umum_piutang)
    session.add(Jurnal_Umum_hpp)
    session.add(Jurnal_Umum_pendapatan)

    session.commit()
    return Response(status_code=204)
