from core.firebase import db
from fastapi import HTTPException
from typing import List

async def get_preview_images(device_id: str, id_list: List[str]) -> List[dict]:
    """
    선택한 id_list를 기반으로 콘텐츠 이미지 url 가져오기
    """
    result = []

    for content_id in id_list:
        doc_ref = db.collection("devices").document(device_id).collection("contents").document(content_id)
        doc = doc_ref.get()

        if not doc.exists:
            continue  # 존재하지 않는 콘텐츠는 skip

        data = doc.to_dict()
        result.append({
            "id": content_id,
            "image_url": data.get("image_url", "")
        })

    return result
