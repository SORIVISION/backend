import io
import asyncio
from core.tts import get_tts

async def generate_tts(text: str) -> bytes:
    """
    입력된 텍스트를 TTS로 변환하여 mp3 바이너리를 반환.
    실제 CLOVA TTS 연동 전까지는 더미 mp3 바이너리.
    """
    await asyncio.sleep(0.1)
    dummy_mp3 = io.BytesIO()
    dummy_mp3.write(b"This is a dummy mp3 file generated from text: " + text.encode())
    
    #status, mp3 = get_tts(text)
    
    return dummy_mp3.getvalue()
