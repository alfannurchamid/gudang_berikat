import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models.akun import Akun
from app.models.barang import Barang
from app.models.suplier import Suplier

from app.models import Base


class Purchase_order(Base):
    __tablename__ = 'purchase_order'
    id_po = sa.Column('id_po', sa.Integer, primary_key=True)
    nomor_po = sa.Column('nomor_po', sa.Integer)
    tgl_po = sa.Column('tgl_po', sa.Date)
    id_suplier = sa.Column(sa.Integer, ForeignKey("suplier.id_suplier"))
    suplier = relationship('Suplier')
    kode_barang = sa.Column(sa.Integer, ForeignKey("baarang.kode_barang"))
    baarang = relationship('Barang')
    tgl_minta_kirim = sa.Column('tgl_minta_kirim', sa.Date)
    jumlah_order = sa.Column('jumlah_order', sa.Integer)
    harga_satuan = sa.Column('harga_satuan', sa.Float)
    remark = sa.Column('remark', sa.String)
    vlauta = sa.Column('vlauta', sa.String)
    id_akun_payment = sa.Column(sa.String, ForeignKey("akun.id_akun"))
    akun = relationship("Akun")
    discount = sa.Column('discount', sa.Float)
    ppn = sa.Column('ppn', sa.Float)
    exrate = sa.Column('exrate', sa.Float)
    grand_total = sa.Column('grand_total', sa.Float)
    done = sa.Column('done', sa.Boolean, default=False)
    acc = sa.Column('acc', sa.Boolean, default=False)
    administrasi_import = sa.Column('administrasi_import', sa.Float)
