import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, storage

load_dotenv()

#인증 키 경로 불러오기
cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
if not cred_path:
    raise ValueError("FIREBASE_CREDENTIAL_PATH 환경 변수가 설정되지 않았습니다.")

bucket_name = os.getenv("FIREBASE_BUCKET_NAME")
if not bucket_name:
    raise ValueError("FIREBASE_BUCKET_NAME 환경 변수가 설정되지 않았습니다.")

#앱 초기화 (한번만)
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "storageBucket": os.getenv("FIREBASE_BUCKET_NAME")

    }) 

# Firestore 클라이언트 초기화
try:
    db = firestore.client()
    bucket = storage.bucket()
except Exception as e:
    raise ValueError(f"Firebase 클라이언트 초기화 실패: {str(e)}")