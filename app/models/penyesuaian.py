import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class Penyesuaian(Base):
    __tablename__ = 'pengajuan_penyesuaian'
    id_pengajuan = sa.Column('id_pengajuan', sa.Integer, primary_key=True)
    no_daftar = sa.Column('no_daftar', sa.String)
    jenis = sa.Column('jenis', sa.Boolean)
    tanggal = sa.Column('tanggal', sa.DateTime,
                        default=datetime.datetime.now())
    done = sa.Column('done', sa.Boolean, default=False)
    id_user = sa.Column('id_user', sa.Integer)
