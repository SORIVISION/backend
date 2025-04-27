from services.hw_services.gpt_service import generate_description_from_image_url
from services.hw_services.clova_tts_service import generate_tts
from services.hw_services.device_service import (
    create_content,
    save_description_to_firestore,
)

async def generate_auto_description(content_ref, image_url : str ) -> bytes:

    """
    상황 설명문 기능
    """
    #1. GPT에 설명 생성 요청
    description = await generate_description_from_image_url(image_url)

    #2. Firestore의 contents 문서에 설명 업데이트
    await save_description_to_firestore(     
        content_ref,
        question_text="이 이미지에 대한 설명을 생성해주세요.",
        gpt_response=description,
        is_emergency=False  # 현재 단계에서는 고정
    )

    #3. 설명을 mp3 binary로 반환
    tts_binary =  await generate_tts(description)

    return tts_binary