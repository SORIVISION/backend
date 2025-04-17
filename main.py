from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import v1
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

app = FastAPI(
    title="SoriVision Backend API",
    description="시각장애인을 위한 웨어러블 디바이스 백엔드 API",
    version="1.0.0"
)

# "/ap1/v1" 아래 모든 라우터 등록
app.include_router(v1, prefix="/api/v1")

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)