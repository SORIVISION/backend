import uuid
from core.firebase import bucket

async def upload_image_to_firebase(image_file) -> str:
    """
    이미지 파일을 firebase Storage에 업로드하고 공개 URL로 변환
    """
    filename = f"images/{uuid.uuid4()}.png"
    blob = bucket.blob(filename)

    # 이미지 파일의 내용을 읽어서 업로드
    blob.upload_from_file(
        image_file.file,
        content_type="image/png"
    )

    # URL 접근 허용
    blob.make_public()

    return blob.public_url

## --> 수정 예정