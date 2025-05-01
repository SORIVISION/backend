from fastapi import APIRouter, Query
from services.client_services.emergency_service import get_emergency_image_urls
from typing import List

router = APIRouter(tags=["Client"])

@router.get("/get_emergency_imglist")
async def get_emergency_imglist(
    device_id: str = Query(..., description="디바이스 ID"),
    emergency_id: str = Query(..., description="비상 상황 ID")
):
    """
    비상 상황의 이미지 URL 목록을 조회하는 API
    """
    try:
        image_urls = await get_emergency_image_urls(device_id, emergency_id)
        return {
            "image_urls": image_urls
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

