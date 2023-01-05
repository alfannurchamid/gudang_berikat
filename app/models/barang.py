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
    harga = sa.Column('harga', sa.Integer)
    saldo = sa.Column('saldo', sa.Integer, default=0)
    lokasi = sa.Column('lokasi', sa.String)
    aktif = sa.Column('aktif', sa.Boolean, default=True)
