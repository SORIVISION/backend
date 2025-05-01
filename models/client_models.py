from pydantic import BaseModel

class DeviceInfoResponse(BaseModel):
    user_name: str
    guardian_name: str
    guardian_phone: str