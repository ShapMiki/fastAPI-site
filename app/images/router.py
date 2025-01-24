from fastapi import APIRouter, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse

from users.dependencies import get_current_user
from users.schemas import SUser
from fastapi import Depends

import shutil

router = APIRouter(
    prefix="/images",
    tags=["images"],
)

@router.post("/upload")
async def upload_image(name: str, file: UploadFile):
    with open(f"app/static/images/{name}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)



@router.post("/upload_one_photo")
async def upload_one_image(
    #file,
    #user: SUser = Depends(get_current_user)
):
    print("ebat ti loh")