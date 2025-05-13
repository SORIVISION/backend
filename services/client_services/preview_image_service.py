from core.firebase import db
from typing import List

async def get_preview_images(device_id: str, date: str) -> dict:
    """"
    id_list 기반으로 컨텐츠 이미지 url 가져오기 (이중 리스트 형태로 반환)
    """
    devices = db.collection("devices").where("device_id", "==",device_id).limit(1).stream()
    docs_list = list(devices)
    device_ref = docs_list[0].reference
    
    contents_ref = device_ref.collection("contents")
    docs = contents_ref.stream()

    ids = []
    urls = []

    for doc in docs:
        data = doc.to_dict()
        created_at = data.get("created_at")

        if not created_at:
            continue

        content_date = str(created_at).split("T")[0]

        if content_date != date:
            continue

        ids.append(doc.id)
        urls.append(data.get("image_url", ""))
        
    return {
        "contents_list_image": [ids, urls]
    }



