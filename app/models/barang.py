import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime


from app.models.rejek import Rijek
from app.models.opname import Opname


from app.models import Base


class Barang(Base):
    __tablename__ = 'baarang'
    kode_barang = sa.Column('kode_barang', sa.String, primary_key=True)
    nama_barang = sa.Column('nama_barang', sa.String)
    satuan = sa.Column('satuan', sa.String)
    akun_persediaan = sa.Column('akun_persediaan', sa.String)
    akun_beban = sa.Column('akun_beban', sa.String)
    harga = sa.Column('harga', sa.Integer)
    saldo = sa.Column('saldo', sa.Float, default=0)
    bm = sa.Column('bm', sa.Float, default=5)
    ppn = sa.Column('ppn', sa.Float, default=11)
    pph = sa.Column('pph', sa.Float, default=2.5)
    aktif = sa.Column('aktif', sa.Boolean, default=True)
