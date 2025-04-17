from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import v1
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Firebase 초기화
from core.firebase import initialize_firebase
initialize_firebase()

app = FastAPI(
    title="SoriVision Backend API",
    description="시각장애인을 위한 웨어러블 디바이스 백엔드 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(v1)

@app.get("/")
async def root():
    return {"message": "SoriVision Backend API 서버가 실행 중입니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)