import asyncio

async def generate_description_from_image(image_url: str) -> str:
    """
    이미지 URL을 기반으로 상황 설명 텍스트를 생성.
    실제 GPT API 연동 전까지는 더미.
    """
    await asyncio.sleep(0.1)  # 테스트 중 비동기 처리 흉내
    return f"이미지({image_url})를 기반으로 생성된 더미 설명입니다."
