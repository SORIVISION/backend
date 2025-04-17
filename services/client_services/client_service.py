from datetime import datetime
from typing import Optional
from models.client_models import ClientCreate, ClientResponse
from firebase_admin import firestore
from core.firebase import db

class ClientService:
    def __init__(self):
        self.collection = db.collection('clients')

    async def register_device(self, client_data: ClientCreate) -> ClientResponse:
        """
        기기를 등록하거나 기존 기기로 로그인합니다.
        
        Args:
            client_data: 기기 정보 (device_id 포함)
            
        Returns:
            ClientResponse: 기기 정보와 상태
        """
        try:
            # 기존 기기 확인
            device_ref = self.collection.where('device_id', '==', client_data.device_id).get()
            
            if device_ref:
                # 기존 기기 정보 반환
                device_data = device_ref[0].to_dict()
                return ClientResponse(
                    device_id=device_data['device_id'],
                    status=device_data['status'],
                    created_at=device_data['created_at'],
                    updated_at=datetime.utcnow()
                )
            else:
                # 새 기기 등록
                device_doc = {
                    'device_id': client_data.device_id,
                    'status': 'active',
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                
                # Firestore에 추가
                doc_ref = self.collection.add(device_doc)
                device_doc['id'] = doc_ref[1].id
                
                return ClientResponse(**device_doc)
                
        except Exception as e:
            raise ValueError(f"기기 등록/로그인 실패: {str(e)}") 