import asyncio

async def generate_description_from_image(image_url: str) -> str:
    """
    이미지 URL을 기반으로 상황 설명 텍스트를 생성.
    실제 GPT API 연동 전까지는 더미.
    """
    await asyncio.sleep(0.1)  # 테스트 중 비동기 처리 흉내
    return f"이미지({image_url})를 기반으로 생성된 더미 설명입니다."

async def generate_description_from_prompt(prompt: str, ocr_result: str) -> str:
    """
    사용자 프롬프트와 OCR 결과를 기반으로 GPT 응답 생성
    지금은 더미 문자열을 반환하고, 나중에 실제 GPT API로 대체 가능
    """
    await asyncio.sleep(0.1)  # API 호출 흉내
    return f"프롬프트: '{prompt}'\n이미지 인식 결과: '{ocr_result}'\n설명: 이것은 테스트."