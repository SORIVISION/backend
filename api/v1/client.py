from fastapi import APIRouter, HTTPException
from models.client_models import ClientCreate, ClientResponse
from services.client_services import ClientService

router = APIRouter(tags=["client"])

@router.post("/login", 
    response_model=ClientResponse,
    summary="기기 등록/로그인",
    description="기기를 등록하거나 기존 기기로 로그인합니다."
)
async def register_device(client_data: ClientCreate):
    """
    기기를 등록하거나 기존 기기로 로그인합니다.
    
    Args:
        client_data: 기기 정보 (device_id 포함)
    
    Returns:
        ClientResponse: 기기 정보와 상태
    """
    client_service = ClientService()
    try:
        result = await client_service.register_device(client_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")