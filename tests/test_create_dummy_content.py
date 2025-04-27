import pytest
from datetime import datetime

# 🔥 core/firebase.py를 import 해서 초기화된 db를 사용
import core.firebase

db = core.firebase.db  # core에서 생성한 Firestore 클라이언트 사용

def create_dummy_content():
    contents_ref = db.collection("devices").document("yR74URDoRqdg2xvrLhiV").collection("contents")
    dummy_data = {
        "created_at": datetime.utcnow(),
        "gpt_response": "that is sakura tree",
        "image_url": "2525",
        "is_emergency": False, # 더미 데이터 생성 시 False/True 설정 / 
        "location_id": "jAtxAVZwkikJXbWC9LXV",
        "question_text": "what is that tree?"
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
    assert data["gpt_response"] == "that is sakura tree"
    assert data["image_url"] == "2525"
    assert data["is_emergency"] is False # 더미 데이터 생성 시 False/True 설정 / 위의 함수와 동일하게 설정
    assert data["location_id"] == "jAtxAVZwkikJXbWC9LXV"
    assert data["question_text"] == "what is that tree?"