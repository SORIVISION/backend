from datetime import datetime, timedelta
from typing import List, Dict
from core.firebase import db

async def get_recent_gps_trace(device_id: str) -> List[Dict]:
    """
    주어진 device_id에 대한 최근 1시간 이내 GPS 위치 데이터를 반환
    """
    
    docs = db.collection("devices").where("device_id", "==",device_id).limit(1).stream()
    docs_list = list(docs)
    device_ref = docs_list[0].reference
    
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    gps_ref = device_ref.collection("locations")

    query = gps_ref.where("timestamp", ">=", one_hour_ago).order_by("timestamp").limit(120)
    docs = query.stream()

    gps_list = []
    for doc in docs:
        data = doc.to_dict()
        gps_list.append({
            "lat" : data.get("lat"),
            "lon" : data.get("lon"),
            "timestamp" : str(data.get("timestamp") + timedelta(hours=9))
        })

    return gps_list