from fastapi import APIRouter, Query
from models.client_models import ContentDetailResponse
from services.client_services.content_detail_service import get_content_detail

router = APIRouter(tags=["Client"])

@router.get("/get_content_byid", response_model=ContentDetailResponse)
async def get_content_by_id_api(
    device_id: str = Query(..., description="디바이스 ID"),
    contents_id: str = Query(..., description="콘텐츠 ID")
):
    result = await get_content_detail(device_id, contents_id)

    return ContentDetailResponse(**result)
