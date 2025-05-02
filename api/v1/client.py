from fastapi import APIRouter, Query
from models.client_models import ContentDetailResponse
from services.client_services.content_detail_service import get_content_detail
from models.client_models import DeviceInfoResponse
from models.client_models import GPSTraceResponse
from services.client_services.device_info_service import get_device_info
from services.client_services.gps_trace_service import get_recent_gps_trace

router = APIRouter(tags=["Client"])

@router.get("/get_content_byid", response_model=ContentDetailResponse)
async def get_content_by_id_api(
    device_id: str = Query(..., description="디바이스 ID"),
    contents_id: str = Query(..., description="콘텐츠 ID")
):
    result = await get_content_detail(device_id, contents_id)

    return ContentDetailResponse(**result)

@router.get("/device_info", response_model=DeviceInfoResponse)
async def device_info(device_id: str = Query(..., description="디바이스 ID")):
    """
    기기 ID를 기준으로 사용자 정보를 반환하는 API
    """
    result = await get_device_info(device_id)

    return DeviceInfoResponse(**result)

@router.get("/gps_trace", response_model= GPSTraceResponse)
async def gps_trace(device_id: str = Query(..., description="조회할 디바이스 ID")):
    """
    보호자가 특정 device_id에 대해 최근 1시간 이내 GPS 위치 타임라인을 조회
    """
    gps_data =  await get_recent_gps_trace(device_id)
    return {"gps": gps_data}
