import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class Opname(Base):
    __tablename__ = 'opname'
    id_opname = sa.Column('id_opname', sa.Integer, primary_key=True)
    kode_barang = sa.Column(sa.Integer, ForeignKey("baarang.kode_barang"))
    jml_opname = sa.Column('jml_opname', sa.Integer)
    keterangan = sa.Column('keterangan', sa.String)
    tgl_opname = sa.Column('tgl_opname', sa.Date,
                           default=datetime.datetime.now())
