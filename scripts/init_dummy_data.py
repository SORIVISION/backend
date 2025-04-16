import sys
import os

# 루트 디렉토리 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from core.firebase import db
from datetime import datetime

def insert_dummy_device():
    device_data = {
        "device_id": "1",
        "guardian_name": "강성은",
        "guardian_phone": "01032375605",
        "user_name": "김진",
        "created_at": datetime.utcnow().isoformat()
    }

    doc_ref = db.collection("devices").document("1")
    doc_ref.set(device_data)

    print("✅ 더미 디바이스 데이터 삽입 완료!")

# 호출
insert_dummy_device()
