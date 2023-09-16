from fastapi import File, Response
from fastapi.responses import FileResponse


async def get_laporan():
    return FileResponse('laporan/laporan.xlsx')
