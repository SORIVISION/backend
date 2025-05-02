import os
import firebase_admin
import json
from firebase_admin import credentials, firestore, storage

#인증 키 경로 불러오기
cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
bucket_name = os.getenv("FIREBASE_BUCKET_NAME")
cred_dict = json.loads(cred_path.replace("\n","\\n"))

#앱 초기화 (한번만)
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        "storageBucket": os.getenv("FIREBASE_BUCKET_NAME")

    }) 

db = firestore.client()
bucket = storage.bucket()
