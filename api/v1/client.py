from fastapi import APIRouter, Query
from models.client_models import DeviceInfoResponse
from services.client_services.device_info_service import get_device_info

router = APIRouter(tags=["Client"])

@router.get("/device_info", response_model=DeviceInfoResponse)
async def device_info(device_id: str = Query(..., description="디바이스 ID")):
    """
    기기 ID를 기준으로 사용자 정보를 반환하는 API
    """
    result = await get_device_info(device_id)

    return DeviceInfoResponse(**result)
