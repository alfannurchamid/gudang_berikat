import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime


from app.models.rejek import Rijek
from app.models.opname import Opname


from app.models import Base


class RegulatorJurnal(Base):
    __tablename__ = 'regulator_jurnal'
    id_reg_jurnal = sa.Column('id_reg_jurnal', sa.Integer, primary_key=True)
    created_at = sa.Column('created_at', sa.DateTime(
        timezone=True), default=datetime.datetime.now())
    id_transaksi = sa.Column('id_transaksi', sa.String, default=sa.null)
    jenis = sa.Column('jenis', sa.Boolean, default=False)

    deskripsi = sa.Column('deskripsi', sa.String)
