import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Customer(Base):
    __tablename__ = 'customer'
    id_customer = sa.Column('id_customer', sa.Integer, primary_key=True)
    nama_customer = sa.Column('nama_customer', sa.String)
