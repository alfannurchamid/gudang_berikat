import sqlalchemy as sa
import datetime


from app.models import Base


class Akun(Base):
    __tablename__ = 'akun'
    id_akun = sa.Column('id_akun', sa.Integer, primary_key=True)
    nama_akun = sa.Column('nama_akun', sa.String)
    pos_akun_debit = sa.Column('pos_akun_debit', sa.Boolean)
    saldo = sa.Column('saldo', sa.Integer, default=0)
