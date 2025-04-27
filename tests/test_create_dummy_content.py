import pytest
from datetime import datetime

# 🔥 core/firebase.py를 import 해서 초기화된 db를 사용
import core.firebase

db = core.firebase.db  # core에서 생성한 Firestore 클라이언트 사용

def create_dummy_content():
    contents_ref = db.collection("devices").document("yR74URDoRqdg2xvrLhiV").collection("contents")
    dummy_data = {
        "device_id": "test_device",
        "guardian_name": "홍길동",
        "guardian_phone": "010-1234-5678",
        "user_name": "테스트유저",
        "created_at": datetime.utcnow(),
    }
    doc_ref = contents_ref.document()
    doc_ref.set(dummy_data)
    return doc_ref.id

# ✅ 유닛 테스트 함수
def test_create_dummy_content():
    content_id = create_dummy_content()
    assert content_id is not None
    doc = db.collection("devices").document("yR74URDoRqdg2xvrLhiV").collection("contents").document(content_id).get()
    assert doc.exists
    data = doc.to_dict()
    assert data["device_id"] == "test_device"
    assert data["guardian_name"] == "홍길동"
    assert data["guardian_phone"] == "010-1234-5678"
    assert data["user_name"] == "테스트유저"
