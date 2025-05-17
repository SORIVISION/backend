from core.firebase import db
from fastapi import HTTPException
from datetime import datetime, timedelta

async def save_gps_location(device_id: str, lat: float, lon: float):
    """
    주어진 device_id의 디바이스 문서 하위에 위치 정보 저장
    """

    # 1. 디바이스 존재 여부 확인
    docs = db.collection("devices").where("device_id", "==",device_id).limit(1).stream()
    docs_list = list(docs)

    if not docs_list:
        raise HTTPException(status_code=404, detail="디바이스가 존재하지 않습니다")

    device_ref = docs_list[0].reference

    #2. 위치 정보 저장
    location_ref = device_ref.collection("locations").document()
    location_ref.set({
        "device_id": device_id,
        "lat" : lat,
        "lng" : lon,
        "recorded_at": datetime.utcnow() + timedelta(hours=9)
    })

    return True
