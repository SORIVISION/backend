import asyncio

async def extract_text_from_image(image_url : str ) -> str:
    """
    Firebase에 업로드된 이미지 URL에서 텍스트 추출(더미)
    실제 CLOVA OCR API 연동 시 대체
    """

    await asyncio.sleep(0.1) # 고의로 지연 발생 (api 호출 느낌)
    return "더미 OCR 결과"