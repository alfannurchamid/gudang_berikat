import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class Rijek(Base):
    __tablename__ = 'rijek'
    id_rijek = sa.Column('id_rijek', sa.Integer, primary_key=True)
    kode_barang = sa.Column(sa.Integer, ForeignKey("baarang.kode_barang"))
    jumlah_rijek = sa.Column('jumlah_rijek', sa.Integer)
    tgl_rijek = sa.Column('tgl_rijek', sa.Date,
                          default=datetime.datetime.now())
