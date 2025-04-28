from fastapi import APIRouter, UploadFile, File, Form, Body
from typing import Dict
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
import io
from datetime import datetime

from services.hw_services.device_service import get_device_by_id, create_content, save_description_to_firestore
from services.hw_services.storage_service import upload_image_to_firebase
from services.hw_services.auto_describe_service import generate_auto_description
from services.hw_services.user_qa_service import handle_user_prompt
from services.hw_services.gps_service import save_gps_location
from services.hw_services.emergency_service import create_emergency
from services.hw_services.emergency_img_service import handle_emergency_image

router = APIRouter(tags=["Hardware"])

@router.post("/auto_describe")
async def auto_describe(device_id : str = Form(...), image : UploadFile = File(...)):
    """
    상황 설명문 생성 API
    1. 디바이스 확인
    2. 이미지 Firebase 업로드
    3. GPT로 설명 생성 및 Firestore 저장
    4. 설명 TTS 변환 후 반환
    """

    device_ref = await get_device_by_id(device_id)
    image_url =await upload_image_to_firebase(image)

    content_ref = await create_content(
    device_ref=device_ref,
    device_id=device_id,
    image_url=image_url,
)
    tts_binary = await generate_auto_description(content_ref, image_url)
    
    return StreamingResponse(
        content = io.BytesIO(tts_binary),
        media_type="audio/mpeg",
        headers={"Content-Disposition" : "inline; filename = description.mp3"}
    )


@router.post("/user_qa")
async def user_prompt_qa(
    device_id: str = Form(...),
    prompt: str = Form(...),
    image: UploadFile = File(...)
):
    """
    사용자 프롬프트 기반 질문 응답 및 음성 생성 API
    1. 디바이스 확인
    2. 이미지 Firebase 업로드
    3. 사용자 질문 + OCR 결과로 GPT 호출
    4. 설명문 Firestore 저장 및 TTS 반환
    """
    image_url = await upload_image_to_firebase(image)

    tts_binary = await handle_user_prompt(device_id, image_url, prompt)

    return StreamingResponse(
        content=io.BytesIO(tts_binary),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=description.mp3"}
    )

@router.post("/gps")
async def post_gps_location(
    device_id : str = Form(...),
    lat : float = Form(...),
    lon : float = Form(...)
):
    """
    GPS 위치정보 저장 API
    디바이스 하위 locations 컬렉션에 저장
    """
    await save_gps_location(device_id, lat, lon)

    return JSONResponse(content={"status": "success"}, headers={"Content-Disposition" : "inline; filename = description.mp3"})

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
        
