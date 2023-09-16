import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class UserLog(Base):
    __tablename__ = 'user_log'

    id_log = sa.Column('id_log', sa.Integer, primary_key=True)
    id_user = sa.Column('id_user', sa.Integer)
    created_at = sa.Column('created_at', sa.DateTime,
                           default=datetime.datetime.now())
    keterangan = sa.Column('keterangan', sa.String)
    jenis = sa.Column('jenis', sa.String)
    id_doc = sa.Column('id_doc', sa.String)
