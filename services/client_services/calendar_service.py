from core.firebase_utils import get_contents_ref
from datetime import datetime
from typing import Dict

async def get_calendar_info(device_id: str, year: int, month: int) -> Dict:
    contents_ref = get_contents_ref(device_id)
    docs = contents_ref.stream()

    id_list= []
    day_list = []

    for doc in docs:
        data =  doc.to_dict()
        created_at = data.get("created_at")
        is_emergency = data.get("is_emergency", False)

        if not created_at or is_emergency:
            continue

        dt = datetime.fromisoformat(created_at)
        if dt.year == year and dt.month == month:
            id_list.append(doc.id)
            day_list.append(dt.day)

    return {
        "contents_list_day" : [
            id_list,
            day_list
        ]
    }