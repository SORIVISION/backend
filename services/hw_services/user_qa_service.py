from services.hw_services.device_service import (
    get_device_by_id,
    create_user_qa_content,
    save_description_to_firestore,
)
from services.hw_services.gpt_service import generate_description_from_image
from services.hw_services.clova_tts_service import generate_tts
from services.hw_services.ocr_service import extract_text_from_image

async def handle_user_prompt(device_id: str, image_url : str, prompt: str) -> bytes:
    """
    사용자 프롬프트 기반 상황 설명 생성 흐름 ( 이게 맞나..?)
    1. device_id로 디바이스 확인
    2. OCR 실행하여 이미지 속 텍스트 추출
    3. contents 문서에 image_url + prompt + ocr_result 저장
    4. prompt + ocr_result로 GPT 호출
    5. contents 문서에 GPT 응답 저장
    6. GPT 응답을 TTS로 변환
    """

    #1. 디바이스 참조 획득
    device_ref = await get_device_by_id(device_id)

    #2. 이미지 Firebase Storage에 업로드
    ocr_result  = await extract_text_from_image(image_url)

    #3. Firestore contents 문서 생성
    content_ref = await create_user_qa_content(
        device_ref=device_ref,
        device_id=device_id,
        image_url=image_url,
        prompt=prompt,
        ocr_result=ocr_result,
    )

    # 4. GPT 생성
    gpt_input = f"{prompt}\n이미지에 포함된 텍스트는 다음과 같습니다:\n{ocr_result}"
    gpt_response = await generate_description_from_image(gpt_input)

    # 5. GPT 결과 저장
    await save_description_to_firestore(
        content_ref=content_ref,
        question_text=prompt,
        gpt_response=gpt_response,
        is_emergency=False
    )

    # 6. TTS 변환
    tts_binary = await generate_tts(gpt_response)

    return tts_binary