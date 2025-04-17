from datetime import datetime
from typing import Optional
from models.client_models import ClientCreate, ClientResponse
from firebase_admin import firestore
from core.firebase import db

class ClientService:
    def __init__(self):
        if db is None:
            raise ValueError("Firebase가 초기화되지 않았습니다.")
        self.master_collection = db.collection('master')

    def register_device(self, client_data: ClientCreate) -> ClientResponse:
        try:
            master_docs = self.master_collection.get()
            
            for master_doc in master_docs:
                master_data = master_doc.to_dict()
                if 'devices_id' in master_data and client_data.device_id in master_data['devices_id']:
                    return ClientResponse(status=200)
            
            return ClientResponse(status=401)
                
        except Exception as e:
            raise ValueError(f"기기 로그인 처리 중 오류 발생: {str(e)}")