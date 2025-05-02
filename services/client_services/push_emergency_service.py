import os
import json
import aiohttp
from fastapi import HTTPException
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# 서비스 계정 JSON 경로
SERVICE_ACCOUNT_FILE = os.getenv("FIREBASE_CREDENTIAL_PATH")
CLIENT_FCM_TOKEN = os.getenv("CLIENT_FCM_TOKEN") # ???
PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")  # 예: "sorivision-50058"

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]


def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials.token


async def send_emergency_push(device_id: str, emergency_id: str):
    if not CLIENT_FCM_TOKEN or not PROJECT_ID:
        raise HTTPException(status_code=500, detail="필수 환경변수가 누락되었습니다.")

    access_token = get_access_token()
    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    message = {
        "message": {
            "token": CLIENT_FCM_TOKEN,
            "notification": {
                "title": "🚨 비상 상황 발생",
                "body": f"디바이스 {device_id}에서 긴급 상황이 발생했습니다."
            },
            "data": {
                "device_id": device_id,
                "emergency_id": emergency_id
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(message)) as resp:
            if resp.status != 200:
                error = await resp.text()
                raise HTTPException(status_code=resp.status, detail=f"FCM Error: {error}")
            return {"status": "success"}
