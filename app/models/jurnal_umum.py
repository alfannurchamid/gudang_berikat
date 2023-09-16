import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime


from app.models.rejek import Rijek
from app.models.opname import Opname


from app.models import Base


class JurnalUmum(Base):
    __tablename__ = 'jurnal_umum'
    id_jurnal = sa.Column('id_jurnal', sa.Integer, primary_key=True)
    tanggal = sa.Column('tanggal', sa.DateTime(
        timezone=True), default=datetime.datetime.now())
    keterangan = sa.Column('keterangan', sa.String)
    id_akun = sa.Column('id_akun', sa.String)
    debet = sa.Column('debet', sa.Integer, default=0)
    kredit = sa.Column('kredit', sa.Integer, default=0)
    id_reg = sa.Column('id_reg', sa.Integer)
    current_saldo = sa.Column('current_saldo', sa.Integer)
