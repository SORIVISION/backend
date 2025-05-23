from core.firebase import db
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

async def get_calendar_info(device_id: str, year: int, month: int) -> Dict[str, List[str]]:
    """
    device_id, year, month 기준으로
    contents를 day 기준으로 묶어 반환하는 API
    ex) {"3": ["id1", "id2"], "5": ["id3"]}
    """
    devices = db.collection("devices").where("device_id", "==",device_id).limit(1).stream()
    docs_list = list(devices)
    device_ref = docs_list[0].reference
    
    contents_ref = device_ref.collection("contents")
    docs = contents_ref.stream()

    contents_by_day = defaultdict(list)

    for doc in docs:
        data = doc.to_dict()
        created_at = data.get("created_at")
        is_emergency = data.get("is_emergency", False)

        if not created_at or is_emergency:
            continue

        dt = datetime.fromisoformat(str(created_at).split("T")[0])
        if dt.year == year and dt.month == month:
            contents_by_day[str(dt.day)].append(doc.id)

    return {
        "contents_by_day": dict(contents_by_day)
    }
