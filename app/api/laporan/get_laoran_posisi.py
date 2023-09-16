from fastapi import File, Response
from fastapi.responses import FileResponse


async def get_laporan_posisi_xl():
    return FileResponse('laporan/laporan_posisi.xlsx')
