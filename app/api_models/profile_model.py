from datetime import datetime
from typing import List
from pydantic import BaseModel


class ProfileModel(BaseModel):
    id: int
    username: str
    full_name: str
    jabatan: str
    noWa: str
    access: int
    path_foto: str
    tanggal_daftar: datetime
