from firebase_admin import firestore
from client_services.push_emergency_service import send_emergency_push
from datetime import datetime

async def create_emergency(device_id: str) -> str:
    db = firestore.client()

    # 1. device_id 필드로 devices 문서 검색
    query = db.collection('devices').where('device_id', '==', device_id).limit(1)
    docs = query.stream()

    device_doc = None
    for doc in docs:
        device_doc = doc
        break

    if not device_doc:
        raise ValueError(f"Device with ID {device_id} not found")

    device_ref = device_doc.reference  # <- 디바이스 문서

    # 2. locations에서 최신 recorded_at 문서 찾기
    locations_ref = device_ref.collection("locations")
    latest_location_query = locations_ref.order_by("recorded_at", direction=firestore.Query.DESCENDING).limit(1)
    latest_location_docs = latest_location_query.stream()

    location_id = None
    for doc in latest_location_docs:
        location_id = doc.id
        break

    if not location_id:
        raise ValueError("최근 위치 정보가 존재하지 않습니다.")

    # 3. emergency 서브컬렉션에 저장 (← 여기 핵심)
    emergency_data = {
        "triggered_at": datetime.utcnow(),
        "contents_id": [],
        "location_id": location_id
    }

    emergency_ref = device_ref.collection("emergency").document()
    emergency_ref.set(emergency_data)
    
    emergency_id = emergency_ref.id
    
    res = await send_emergency_push(device_id=device_id, emergency_id=emergency_id)

    return emergency_id
