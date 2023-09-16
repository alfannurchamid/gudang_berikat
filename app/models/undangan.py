import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class Undangan(Base):
    __tablename__ = 'undangan'
    id = sa.Column('id', sa.Integer, primary_key=True)
    nama = sa.Column('nama', sa.String)
    no_wa = sa.Column('no_wa', sa.String)
    kata = sa.Column('kata', sa.String)
