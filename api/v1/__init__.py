from fastapi import APIRouter
from . import hw

v1 = APIRouter()
v1.include_router(hw.router, prefix="/hw")
