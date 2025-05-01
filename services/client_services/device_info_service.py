from core.firebase import db
from fastapi import HTTPException

async def get_device_info(device_id: str) -> dict:
    docs =  db.collection("devices").where("device_id","==", device_id).limit(1).stream()
    docs_list =  list(docs)

    if not docs_list:
        raise HTTPException(status_code=404, detail="해당 디바이스를 찾을 수 없습니다")
    
    data =  docs_list[0].to_dict()

    return {
        "user_name": data.get("user_name"),
        "guardian_name": data.get("guardian_name"),
        "guardian_phone": data.get("guardian_phone")
    }