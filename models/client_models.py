from pydantic import BaseModel
from datetime import datetime

class ContentDetailResponse(BaseModel):
    lat: float
    lon: float
    question: str
    gpt_response: str
    created_at: datetime
