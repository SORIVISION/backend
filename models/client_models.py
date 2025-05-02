from pydantic import BaseModel
from datetime import datetime
from typing import List


class ContentDetailResponse(BaseModel):
    lat: float
    lon: float
    question: str
    gpt_response: str
    created_at: datetime

class DeviceInfoResponse(BaseModel):
    user_name: str
    guardian_name: str
    guardian_phone: str

class GPSItem(BaseModel):
    lat : float 
    lon : float
    timestamp: datetime

class GPSTraceResponse(BaseModel):
    gps : List[GPSItem]

class PreviewImageItem(BaseModel):
    id: str
    image_url: str

class PreviewImageResponse(BaseModel):
    contents_list_image: List[PreviewImageItem]
