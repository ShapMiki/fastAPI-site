from fastapi import APIRouter, UploadFile
import shutil

router = APIRouter(
    prefix="/images",
    tags=["images"],
)

@router.post("/upload")
async def upload_image(name: str, file: UploadFile):
    with open(f"app/static/images/{name}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)