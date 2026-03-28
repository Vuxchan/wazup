import cloudinary
import cloudinary.uploader
from src.core.config import settings
from fastapi import UploadFile
from typing import Any
from uuid import UUID

cloudinary.config( 
    cloud_name = settings.CLOUDINARY_CLOUD_NAME, 
    api_key = settings.CLOUDINARY_API_KEY, 
    api_secret = settings.CLOUDINARY_API_SECRET,
    secure=True
)

async def upload_img(file: UploadFile, user_id: UUID) -> Any:
    result = cloudinary.uploader.upload(file.file, transformation=[
        {"width": 200, "height": 200, "crop": "fill"},
        {"quality": "auto"}
    ], folder="chat_app/avatars", resource_type="image", public_id=f"{str(user_id)}")
    return result