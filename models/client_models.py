from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    device_id: str = Field(..., description="기기 고유 식별자")

class ClientCreate(ClientBase):
    pass

class ClientResponse(BaseModel):
    status: int = Field(..., description="HTTP 상태 코드 (200: 성공, 401: 인증 실패)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "status": 200
            }
        }