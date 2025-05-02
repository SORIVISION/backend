from core.firebase import db
from fastapi import HTTPException

async def get_content_detail(device_id: str, contents_id: str) -> dict:
    doc_ref = db.collection("devices").document(device_id).collection("contents").document(contents_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="해당 콘텐츠를 찾을 수 없습니다")

    data = doc.to_dict()

    return {
        "lat": data.get("lat", 0.0),
        "lon": data.get("lon", 0.0),
        "question": data.get("question_text", ""),
        "gpt_response": data.get("gpt_response", ""),
        "created_at": data.get("created_at")
    }
