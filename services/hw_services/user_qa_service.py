from services.hw_services.device_service import (
    get_device_by_id,
    create_content,
    save_description_to_firestore,
)
from services.hw_services.gpt_service import generate_description_from_image
from services.hw_services.clova_tts_service import generate_tts
from services.hw_services.ocr_service import extract_text_from_image

async def handle_user_prompt(device_id: str, image_url : str, prompt: str) -> bytes:
    """
    사용자 프롬프트 기반 상황 설명 생성 흐름
    1. device_id로 디바이스 확인
    2. OCR 실행하여 이미지 속 텍스트 추출
    3. contents 문서에 (prompt + ocr 텍스트로 구현된 question_text 저장)
    4. GPT 응답 생성 및 저장
    5. TTS 변환 및 반환
    """

    #1. 디바이스 참조 획득
    device_ref = await get_device_by_id(device_id)

    #2. 이미지 Firebase Storage에 업로드
    ocr_result  = await extract_text_from_image(image_url)  # OCR용    

    # 3. Firestore에 콘텐츠 문서 생성
    question_text = f"{prompt}\n이미지 내 텍스트: {ocr_result}"
    content_ref = await create_content(
        device_ref=device_ref,
        device_id=device_id,
        image_url=image_url,
        question_text=question_text,
    )

    # 4. GPT 생성
    gpt_response = await generate_description_from_image(question_text)

    # 5. GPT 결과 저장
    await save_description_to_firestore(
        content_ref=content_ref,
        question_text=question_text,
        gpt_response=gpt_response,
        is_emergency=False
    )
    
    # 6. TTS 변환
    tts_binary = await generate_tts(gpt_response)

    return tts_binary