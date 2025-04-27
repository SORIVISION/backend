
from firebase_admin import firestore
from core.firebase import db
from services.hw_services.device_service import get_device_by_id, create_content
from datetime import datetime
from fastapi import HTTPException

async def handle_emergency_image(device_id: str, emergency_id: str, image_url: str):
    # 디바이스 문서 찾기
    device_ref = await get_device_by_id(device_id)

    # 최신 location_id 찾기
    locations_ref = device_ref.collection("locations")
    latest_location_query = locations_ref.order_by("recorded_at", direction=firestore.Query.DESCENDING).limit(1)
    latest_location_docs = latest_location_query.stream()

    location_id = None
    for doc in latest_location_docs:
        location_id = doc.id
        break

    if not location_id:
        raise HTTPException(status_code=404, detail="최근 위치 정보 없음")

    # contents 문서 생성 (is_emergency=True)
    content_ref = await create_content(
        device_ref=device_ref,
        device_id=device_id,
        image_url=image_url,
        is_emergency=True
    )

    # emergency 문서에 contents_id 추가
    emergency_ref = device_ref.collection("emergency").document(emergency_id)
    emergency_doc = emergency_ref.get()

    if not emergency_doc.exists:
        raise HTTPException(status_code=404, detail="emergency_id 없음")

    emergency_ref.update({
        "contents_id": firestore.ArrayUnion([content_ref.id])
    })

    return emergency_id
