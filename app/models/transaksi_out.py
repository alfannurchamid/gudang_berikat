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
    id_customer = sa.Column(sa.Integer, ForeignKey("Customer.id_customer"))
    customer = relationship("Customers")
    id_user = sa.Column(sa.Integer, sa.ForeignKey("User.id_user"))
    user = relationship("User")
    tanggal_sppb = sa.Column('tanggal_sppb', sa.Date)
    kode_barang = sa.Column(sa.Integer, ForeignKey("Barang.kode_barang"))
    no_sppb = sa.Column('no_sppb', sa.String)
    barang = relationship("Barang")
    jumlah = sa.Column('jumlah', sa.Integer)
    harga = sa.Column('harga', sa.Integer)
    tanggal = sa.Column('tanggal', sa.Date, default=datetime.datetime.now())
    saldo_jml = sa.Column('saldo_jml', sa.Integer)
    no_invoice = sa.Column('no_invoice', sa.String)
    tanggal_invoice = sa.Column('tanggal_invoice', sa.Date)
    vlauta = sa.Column('vlauta', sa.String)
    exchane_rate = sa.Column('exchange_rate', sa.Integer)
    total_harga_invoice = sa.Column('total_harga_invoice', sa.Integer)
    discount = sa.Column('discount', sa.Integer)
    ppn = sa.Column('ppn', sa.Integer)
    tanggal_jatuh_tempo = sa.Column('tanggal_jatuh_tempo', sa.Date)
    grad_total = sa.Column('grand_total', sa.Integer)
    jenis_dokumen = sa.Column('jenis_dokumen', sa.String)
