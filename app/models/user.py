
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship


from app.models import Base


class User(Base):
    __tablename__ = 'user'
    id_user = sa.Column('id_user', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String)
    password = sa.Column('password', sa.String)
    full_name = sa.Column('full_name', sa.String)
    noWa = sa.Column('noWa', sa.String)
    jabatan = sa.Column('jabatan', sa.String)
    access = sa.Column('access', sa.Integer, default=0)
    path_foto = sa.Column('path_foto', sa.String, default=sa.null)
    created_at = sa.Column('created_at', sa.DateTime(
        timezone=True), default=datetime.datetime.now())
    modifed_at = sa.Column('modifed_at', sa.DateTime(timezone=True),
                           default=datetime.datetime.now(), onupdate=datetime.datetime.now())
