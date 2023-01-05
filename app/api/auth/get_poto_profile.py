from fastapi import File, Response
from fastapi.responses import FileResponse


async def get_foto_profile(file: str):
    return FileResponse('foto_profile/'+file)
