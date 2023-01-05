import sqlalchemy as sa
import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class StandarDoc(Base):
    __tablename__ = 'standar_doc'
    id_doc = sa.Column('id_doc', sa.String, primary_key=True)
    nomor = sa.Column('nomor', sa.String)
