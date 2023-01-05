import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.models.suplier import Suplier
from app.models.user import User
from app.models.barang import Barang
from app.models.purchase_order import Purchase_order

from app.models import Base


class Transaksi_in(Base):
    __tablename__ = "transaksi_in"
    no_daftar = sa.Column('no_daftar', sa.String, primary_key=True)
    tanggal_daftar = sa.Column('tanggal_daftar', sa.Date)
    id_user = sa.Column(sa.Integer, sa.ForeignKey("User.id_user"))
    user = relationship("User")
    id_suplier = sa.Column(sa.Integer, ForeignKey("Suplier.id_suplier"))
    suplier = relationship("Suplier")
    kode_barang = sa.Column(sa.Integer, ForeignKey("Barang.kode_barang"))
    barang = relationship("Barang")
    id_po = sa.Column(sa.Integer, ForeignKey('Purchase_order.id_po'))
    purchase_order = relationship("Purchase_order")
    jumlah = sa.Column('jumlah', sa.Integer)
    tanggal = sa.Column('tanggal', sa.Date, default=datetime.datetime.now())
    saldo_jml = sa.Column('saldo_jml', sa.Integer)
    no_sppb = sa.Column('no_sppb', sa.String)
    tanggal_sppb = sa.Column('tanggal_sppb', sa.Date)
    no_invoice = sa.Column('no_invoice', sa.String)
    tanggal_invoice = sa.Column('tanggal_invoice', sa.Date)
    jenis = sa.Column('jenis', sa.String)
    vlauta = sa.Column('vlauta', sa.String)
    exchane_rate = sa.Column('exchange_rate', sa.Integer)
    total_harga_invoice = sa.Column('total_harga_invoice', sa.Integer)
    discount = sa.Column('discount', sa.Integer)
    freight = sa.Column('freight', sa.Integer)
    tanggal_jatuh_tempo = sa.Column('tanggal_jatuh_tempo', sa.Date)
    grad_total = sa.Column('grand_total', sa.Integer)
