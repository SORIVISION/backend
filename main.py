from fastapi import FastAPI
from api.v1 import v1
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(v1, prefix="/api/v1")

if __name__ == "__main__" :
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)