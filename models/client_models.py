from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    device_id: str = Field(..., description="기기 고유 식별자")

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    status: str = Field(..., description="기기 상태 (active/inactive)")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="마지막 업데이트 시간")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "device_id": "device-123",
                "status": "active",
                "created_at": "2024-04-17T01:14:00",
                "updated_at": "2024-04-17T01:14:00"
            }
        }