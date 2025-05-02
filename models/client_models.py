from pydantic import BaseModel
from typing import List
from datetime import datetime

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
