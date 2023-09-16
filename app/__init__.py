import time
from concurrent.futures import process

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import api_router

app = FastAPI(
    title='bspn_indika',
    version='1.0.0'
)

app.include_router(api_router)


# midlewware
class MyMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)

        return response


# origin = ["http://localhost:8000", "http://202.149.70.68","http://localhost", "http://localhost:80",
#           "http://127.0.0.1:3000", "202.149.70.68"]

# origin = ["https://localhost:8000",
#           "https://bspnwonosobo.com", "https://bspnwonosobo.com/", "https://localhost:3000"]


origin = ["http://localhost:8000", "http://89.116.179.69:3060", "http://89.116.179.69:80", "http://localhost:3001",
          "https://lestariberkahsae.com", "http://127.0.0.1:3001"]
app.add_middleware(MyMiddleWare)
app.add_middleware(CORSMiddleware, allow_origins=origin,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)
