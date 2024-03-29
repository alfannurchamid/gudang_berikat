import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class StandarDoc(Base):
    __tablename__ = 'standar_doc'
    id_doc = sa.Column('id_doc', sa.Integer, primary_key=True)
    nomor = sa.Column('nomor', sa.String)
    jenis_dokumen = sa.Column('jenis_dokumen', sa.String)
    jenis = sa.Column('jenis', sa.Boolean)
    done = sa.Column('done', sa.Boolean, default=False)
    tanggal = sa.Column('tanggal', sa.Date)
