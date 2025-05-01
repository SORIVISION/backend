from fastapi import APIRouter
from . import hw, client

v1 = APIRouter()
v1.include_router(hw.router, prefix="/hw")
v1.include_router(client.router, prefix="/client")