import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class Regulator(Base):
    __tablename__ = "regulator"
    id_regulator = sa.Column('id_regulator', sa.Integer, primary_key=True)
    id_akun = sa.Column(sa.Integer, ForeignKey("akun.id_akun"))
    akun = relationship("Akun")
    jenis = sa.Column("jenis", sa.String)
    id_transaksi = sa.Column('id_transaksi', sa.Integer)
    is_debet = sa.Column('is_debet', sa.Boolean)
    nominal = sa.Column('nominal', sa.Float)
