from fastapi import FastAPI
from api.v1 import v1

app = FastAPI()

# "/ap1/v1" 아래 모든 라우터 등록
app.include_router(v1, prefix="/api/v1")

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
