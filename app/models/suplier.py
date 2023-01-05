import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class Suplier(Base):
    __tablename__ = 'suplier'
    id_suplier = sa.Column('id_suplier', sa.Integer, primary_key=True)
    nama_suplier = sa.Column('nama_suplier', sa.String)
    asal_negara = sa.Column('asal_negara', sa.String)
