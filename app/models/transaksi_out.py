import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models.user import User
from app.models.barang import Barang
from app.models.customer import Customer
from app.models import Base


class Transaksi_out(Base):
    __tablename__ = "transaksi_out"
    no_pengajuan = sa.Column('no_pengajuan', sa.String)
    no_daftar = sa.Column('no_daftar', sa.String, primary_key=True)
    tanggal_daftar = sa.Column('tanggal_daftar', sa.Date)
    id_customer = sa.Column(sa.Integer, ForeignKey("customer.id_customer"))
    customer = relationship("Customer")
    id_user = sa.Column(sa.Integer, sa.ForeignKey("user.id_user"))
    user = relationship("User")
    kode_barang = sa.Column(sa.Integer, ForeignKey("baarang.kode_barang"))
    tanggal_sppb = sa.Column('tanggal_sppb', sa.Date)
    baarang = relationship("Barang")
    no_sppb = sa.Column('no_sppb', sa.String)
    jumlah = sa.Column('jumlah', sa.Integer)
    harga_satuan = sa.Column('harga_satuan', sa.Float)
    tanggal = sa.Column('tanggal', sa.Date, default=datetime.datetime.now())
    saldo_jml = sa.Column('saldo_jml', sa.Integer)
    nomor_invoice = sa.Column('nomor_invoice', sa.String)
    tanggal_invoice = sa.Column('tanggal_invoice', sa.Date)
    vlauta = sa.Column('vlauta', sa.String)
    exchane_rate = sa.Column('exchange_rate', sa.Float)
    total_harga_invoice = sa.Column('total_harga_invoice', sa.Float)
    discount = sa.Column('discount', sa.Float)
    ppn = sa.Column('ppn', sa.Float)
    tanggal_jatuh_tempo = sa.Column('tanggal_jatuh_tempo', sa.Date)
    grand_total = sa.Column('grand_total', sa.Float)
    jenis = sa.Column('jenis', sa.String)
    nomor_daftar_in = sa.Column('nomor_daftar_in', sa.String)
    lokasi = sa.Column('lokasi', sa.String)
    acc = sa.Column('acc', sa.Boolean, default=False)
    ajukan_penyesuaian = sa.Column(
        'ajukan_penyesuaian', sa.Boolean, default=False)
