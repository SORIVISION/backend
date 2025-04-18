from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

#응답 데이터
class AutoDescribeRequest(BaseModel):
    device_id : str
    # image는 basemodel로 못받아 라우터 함수에서 분리해서 담게 설계 

class AutoDescriveResponse(BaseModel):
    status : str
    tts: Optional[bytes] # 이부분 확인 부탁 