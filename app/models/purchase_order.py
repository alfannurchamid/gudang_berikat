import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Purchase_order(Base):
    __tablename__ = 'purchase_order'
    id_po = sa.Column('id_po', sa.Integer, primary_key=True)
    tgl_po = sa.Column('tgl_po', sa.Date)
    id_suplier = sa.Column(sa.Integer, ForeignKey("suplier.id_suplier"))
    kode_barang = sa.Column(sa.Integer, ForeignKey("baarang.kode_barang"))
    tgl_minta_kirim = sa.Column('tgl_minta_kirim', sa.Date)
    jumlah_order = sa.Column('jumlah_order', sa.Integer)
    harga_satuan = sa.Column('harga_satuan', sa.Integer)
    remark = sa.Column('remark', sa.String)
    vlauta = sa.Column('vlauta', sa.String)
    id_akun_payment = sa.Column(sa.Integer, ForeignKey("akun.id_akun"))
    discount = sa.Column('discount', sa.Integer)
    ppn = sa.Column('ppn', sa.Integer)
