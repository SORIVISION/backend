from fastapi import APIRouter, Query
from models.client_models import GPSTraceResponse
from services.client_services.gps_trace_service import get_recent_gps_trace

router = APIRouter(tags=["Client"])

@router.get("/gps_trace", response_model= GPSTraceResponse)
async def gps_trace(device_id: str = Query(..., description="조회할 디바이스 ID")):
    """
    보호자가 특정 device_id에 대해 최근 1시간 이내 GPS 위치 타임라인을 조회
    """

    gps_data =  await get_recent_gps_trace(device_id)
    return {"gps": gps_data}