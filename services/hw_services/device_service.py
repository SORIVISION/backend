from core.firebase import db
from fastapi import HTTPException
from datetime import datetime
from typing import Optional

#1. 디바이스 문서 참조 얻기
async def get_device_by_id(device_id : str):
    docs = db.collection("devices").where("device_id", "==", device_id).limit(1).stream()
    docs_list =  list(docs)

    if not docs_list:
        raise HTTPException(status_code=404, detail="디바이스 없음")
    
    return docs_list[0].reference

#2. contents 문서 생성 (상황설명문/ 사용자 프롬프트 공통 )
async def create_content(
        device_ref, 
        device_id : str, 
        image_url :str,
        question_text : Optional[str] = "",
        gpt_response : Optional[str] = "",
        is_emergency : bool = False
):
    content_ref = device_ref.collection("contents").document()
    content_ref.set({
        "device_id": device_id,
        "image_url": image_url,
        "created_at": datetime.utcnow().isoformat(),
        "question_text": question_text,
        "gpt_response": gpt_response,
        "is_emergency": is_emergency
    })      
    print(f"[DEBUG] Writing to: {device_ref.path}/contents")
    print(f"[DEBUG] Data: {image_url}, {question_text}")
    return content_ref

#3. GPT 응답을 Firebase로 저장
async def save_description_to_firestore(
        content_ref, 
        question_text: str, 
        gpt_response: str, 
        is_emergency: bool
):
    content_ref.update({
        "question_text": question_text,
        "gpt_response": gpt_response,
        "is_emergency": is_emergency,
        "updated_at": datetime.utcnow().isoformat()
    })