from core.firebase import db
from typing import List

async def get_total_contents(device_id : str, date : str) -> List :
    devices = db.collection("devices").where("device_id", "==",device_id).limit(1).stream()
    docs_list = list(devices)
    device_ref = docs_list[0].reference
    
    contents_ref = device_ref.collection("contents")
    docs = contents_ref.stream()

    ids = []
    urls = []
    
    out = []

    for doc in docs:
        data = doc.to_dict()
        created_at = data.get("created_at")

        out_dict = {
            
        }

        if not created_at:
            continue
        
        c_split = str(created_at).split("T")

        content_date = c_split[0]

        if content_date != date:
            continue

        out_dict["content_id"] = doc.id
        out_dict["image_url"] = data.get("image_url", "")
        out_dict["question_text"] = data.get("question_text", "")
        out_dict["gpt_response"] = data.get("gpt_response", "")
        out_dict["created_at"] = c_split[1]
        out.append(out_dict)
        
    return out