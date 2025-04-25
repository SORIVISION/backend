from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io
from services.hw_services.device_service import get_device_by_id, create_content, save_description_to_firestore
from services.hw_services.storage_service import upload_image_to_firebase
from services.hw_services.auto_describe_service import generate_auto_description

from services.hw_services.user_qa_service import handle_user_prompt

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
    
    #6. 응답 반환
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
    사용자 프롬프트 기반 질문 응답 및 음성 생성
    """

    # Firebase Storage에 업로드하여 url 받기
    image_url = await upload_image_to_firebase(image)

    tts_binary = await handle_user_prompt(device_id, image_url, prompt)

    return StreamingResponse(
        content=io.BytesIO(tts_binary),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=description.mp3"}
    )