from core.firebase import db
from fastapi import HTTPException

async def get_content_detail(device_id: str, contents_id: str) -> dict:
    docs = db.collection("devices").where("device_id", "==",device_id).limit(1).stream()
    docs_list = list(docs)

    if not docs_list:
        raise HTTPException(status_code=404, detail="디바이스가 존재하지 않습니다")
    device_ref = docs_list[0].reference
    
    doc = device_ref.collection("contents").document(contents_id)
    
    data = doc.get().to_dict()

    return {
        "lat": data.get("lat", 0.0),
        "lon": data.get("lon", 0.0),
        "question": data.get("question_text", ""),
        "gpt_response": data.get("gpt_response", ""),
        "created_at": data.get("created_at")
    }
