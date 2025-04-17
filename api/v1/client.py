from fastapi import APIRouter, HTTPException
from models.client_models import ClientCreate, ClientResponse
from services.client_services import ClientService

router = APIRouter(tags=["client"])

@router.post("/login", 
    response_model=ClientResponse,
    summary="기기 로그인",
    description="""
    보호자가 디바이스에서 디바이스 아이디를 입력하여 로그인을 시도합니다.

    - master 컬렉션의 devices_id 배열에 해당 device_id가 존재하는 경우: 로그인 성공 (status: 200)
    - master 컬렉션의 devices_id 배열에 해당 device_id가 없는 경우: 로그인 실패 (status: 401)
    """,
    responses={
        200: {
            "description": "로그인 성공",
            "content": {
                "application/json": {
                    "example": {
                        "status": 200
                    }
                }
            }
        },
        401: {
            "description": "로그인 실패 (인증되지 않은 기기)",
            "content": {
                "application/json": {
                    "example": {
                        "status": 401
                    }
                }
            }
        },
        400: {
            "description": "잘못된 요청",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "기기 로그인 처리 중 오류 발생: [오류 메시지]"
                    }
                }
            }
        },
        500: {
            "description": "서버 오류",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "서버 오류: [오류 메시지]"
                    }
                }
            }
        }
    }
)
def register_device(client_data: ClientCreate):
    """
    master 컬렉션의 devices_id 배열을 확인하여 기기 로그인을 처리합니다.

    Args:
        client_data: 기기 정보 (device_id 포함)

    Returns:
        ClientResponse: HTTP 상태 코드 (200: 성공, 401: 인증 실패)
    """
    client_service = ClientService()
    try:
        result = client_service.register_device(client_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
