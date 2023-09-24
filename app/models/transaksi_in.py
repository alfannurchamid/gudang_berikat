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
    no_pengajuan = sa.Column('no_pengajuan', sa.String)
    tanggal_daftar = sa.Column('tanggal_daftar', sa.Date)
    id_user = sa.Column(sa.Integer, ForeignKey("user.id_user"))
    user = relationship('User')
    id_suplier = sa.Column(sa.Integer, ForeignKey("suplier.id_suplier"))
    suplier = relationship("Suplier")
    kode_barang = sa.Column(sa.Integer, ForeignKey("baarang.kode_barang"))
    baarang = relationship("Barang")
    id_po = sa.Column(sa.Integer, ForeignKey('purchase_order.id_po'))
    purchase_order = relationship("Purchase_order")
    jumlah = sa.Column('jumlah', sa.Integer)
    harga_satuan = sa.Column('harga_satuan', sa.Float)
    tanggal = sa.Column('tanggal', sa.Date, default=datetime.datetime.now())
    saldo_jml = sa.Column('saldo_jml', sa.Integer)
    no_sppb = sa.Column('no_sppb', sa.String)
    tanggal_sppb = sa.Column('tanggal_sppb', sa.Date)
    nomor_invoice = sa.Column('nomor_invoice', sa.String)
    tanggal_invoice = sa.Column('tanggal_invoice', sa.Date)
    jenis = sa.Column('jenis', sa.String)
    vlauta = sa.Column('vlauta', sa.String)
    exchane_rate = sa.Column('exchange_rate', sa.Float)
    total_harga_invoice = sa.Column('total_harga_invoice', sa.Float)
    discount = sa.Column('discount', sa.Float)
    freight = sa.Column('freight', sa.DECIMAL)
    tanggal_jatuh_tempo = sa.Column('tanggal_jatuh_tempo', sa.Date)
    grad_total = sa.Column('grand_total', sa.Float)
    done = sa.Column('done', sa.Boolean, default=False)
    acc = sa.Column('acc', sa.Boolean, default=False)
    out = sa.Column('out', sa.Boolean, default=False)
    lokasi = sa.Column('lokasi', sa.String)
    administrasi_import = sa.Column('administrasi_import', sa.Float)
    pabean = sa.Column('pabean', sa.Float)
