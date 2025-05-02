from firebase_admin import firestore
from fastapi import HTTPException
from typing import List

async def get_emergency_image_urls(device_id: str, emergency_id: str) -> List[str]:
    """
    비상 상황의 모든 이미지 URL을 조회합니다.
    
    Args:
        device_id (str): 디바이스 ID
        emergency_id (str): 비상 상황 ID
    
    Returns:
        List[str]: 이미지 URL 목록
    """
    db = firestore.client()
    
    # 1. device_id 필드로 devices 문서 검색
    query = db.collection('devices').where('device_id', '==', device_id).limit(1)
    docs = query.stream()
    
    device_doc = None
    for doc in docs:
        device_doc = doc
        break
    
    if not device_doc:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device_ref = device_doc.reference  # 디바이스 문서 참조
    
    # 2. emergency 문서 참조
    emergency_ref = device_ref.collection('emergency').document(emergency_id)
    emergency_doc = emergency_ref.get()
    
    if not emergency_doc.exists:
        raise HTTPException(status_code=404, detail="Emergency not found")
    
    emergency_data = emergency_doc.to_dict()
    contents_ids = emergency_data.get('contents_id', [])
    
    # 3. 각 contents_id에 대한 이미지 URL 조회
    image_urls = []
    for content_id in contents_ids:
        content_doc = device_ref.collection('contents').document(content_id).get()
        if content_doc.exists:
            content_data = content_doc.to_dict()
            image_url = content_data.get('image_url')
            if image_url:
                image_urls.append(image_url)
    
    return image_urls 