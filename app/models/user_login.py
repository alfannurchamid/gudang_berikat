import datetime
from email.policy import default

import sqlalchemy as sa

from app.models import Base


class UserLogin(Base):
    __tablename__ = 'userLogin'

    id = sa.Column('id', sa.Integer, primary_key=True)
    user_id = sa.Column('user_id', sa.Integer)
    refresh_token = sa.Column('refresh_token', sa.String)
    expired_at = sa.Column('expired_at', sa.DateTime,
                           default=datetime.datetime.now())
    created_at = sa.Column('created_at', sa.DateTime,
                           default=datetime.datetime.now())
    modified_at = sa.Column('modified_at', sa.DateTime,
                            default=datetime.datetime.now(), onupdate=datetime.datetime.now())
