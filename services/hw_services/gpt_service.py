import asyncio

async def generate_description_from_image_url(image_url: str) -> str:
    """
    이미지 URL을 기반으로 상황 설명문 생성 (auto_describe 전용)
    """
    await asyncio.sleep(0.1)
    return f"이미지({image_url})를 기반으로 생성된 설명문."

async def generate_description_from_prompt(prompt_text: str) -> str:
    """
    사용자 프롬프트 + OCR 결과를 기반으로 설명문 생성 (user_qa 전용)
    """
    await asyncio.sleep(0.1)
    return f"프롬프트 기반 설명문: {prompt_text}"
