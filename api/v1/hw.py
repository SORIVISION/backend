from fastapi import APIRouter, UploadFile, File, Form, Body
from fastapi.responses import StreamingResponse
import io
from services.hw_services.device_service import get_device_by_id, create_content, save_description_to_firestore
from services.hw_services.storage_service import upload_image_to_firebase
from services.hw_services.auto_describe_service import generate_auto_description
from services.hw_services.emergency_service import create_emergency
from typing import Dict
from services.hw_services.emergency_img_service import handle_emergency_image


router = APIRouter(tags=["Hardware"])

@router.post("/auto_describe")
async def auto_describe(device_id : str = Form(...), image : UploadFile = File(...)):
    
    #1. 디바이스 확인
    device_ref = await get_device_by_id(device_id)

    #2. 이미지 Firebase에 업로드
    image_url = await upload_image_to_firebase(image)

    #3. contents 하위 문서 생성 (image_url 포함)
    content_ref = await create_content(device_ref, device_id, image_url)

    #4. GPT 질문 생성 및 답변 저장 (지금은 더미)
    question = " 이 이미지는 무엇인가요?"
    gpt_response = "이 이미지는 예시 이미지입니다" # <<-- 실제 gpt 연결 시 대체
    await save_description_to_firestore(content_ref, question, gpt_response, is_emergency=False)

    
    #5. TTS 생성( 더미 )
    tts_binary = await generate_auto_description(device_ref, device_id, image_url)

    print(f"[DEBUG] tts_binary type: {type(tts_binary)}")
    print(f"[DEBUG] tts_binary preview: {tts_binary[:10] if isinstance(tts_binary, bytes) else tts_binary}")

    #6. 응답 반환
    return StreamingResponse(
        content = io.BytesIO(tts_binary),
        media_type="audio/mpeg",
        headers={"Content-Disposition" : "inline; filename = description.mp3"}
    )

@router.post("/get_emergency_id")
async def get_emergency_id(request: Dict[str, str] = Body(...)):
    device_id = request.get("device_id")
    if not device_id:
        return {"status": "error", "message": "device_id is required"}
    
    try:
        emergency_id = await create_emergency(device_id)
        return {
            "status": "success",
            "emergency_id": emergency_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/emergency_img")
async def emergency_img(
    device_id: str = Form(...),
    emergency_id: str = Form(...),
    image: UploadFile = File(...)
):
    """
    비상 상황 이미지 전송 및 contents 저장 API
    """
    image_url = await upload_image_to_firebase(image)

    final_emergency_id = await handle_emergency_image(device_id, emergency_id, image_url)

    return {
        "status": "success",
        "emergency_id": final_emergency_id
    }
        
        