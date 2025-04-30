from pydantic import BaseModel
from typing import List
from datetime import datetime

class GPSItem(BaseModel):
    lat : float 
    lon : float
    timestamp: datetime

class GPSTraceResponse(BaseModel):
    gps : List[GPSItem]