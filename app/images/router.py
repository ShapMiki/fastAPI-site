from fastapi import APIRouter, UploadFile, HTTPException, File, Request
from typing import List, Optional
from fastapi.responses import JSONResponse

import os
import json
from config import settings

from users.dependencies import get_current_user
from users.schemas import SUser
from users.dao import UsersDAO

from cars.dao import ActivCarsDAO

from fastapi import Depends

import shutil
from PIL import Image


router = APIRouter(
    prefix="/images",
    tags=["images"],
)

@router.post("/upload")
async def upload_image(name: str, file: UploadFile):
    with open(f"app/static/images/{name}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


@router.post("/upload_car_images/{car_id}")
async def upload_car_images(car_id: int, request: Request, user: SUser = Depends(get_current_user)):

    car = await ActivCarsDAO.find_by_id(car_id)

    if user.id != car.owner:
        return HTTPException(status_code=495, detail="You can't upload images for this car")

    form = await request.form()
    images = [form[key] for key in form if key.startswith('image')]

    localisation_directory = f"{settings.image_scr}/cars"

    image_names = []
    for i, image in enumerate(images):

        image_extension = image.filename.split('.')[-1]
        if image_extension not in ["jpg", "jpeg", "png"]:
            continue

        image_name = f"car_{car_id}_{i}.{image_extension}"
        image_names.append(image_name)

        file_path = f"{localisation_directory}/{image_name}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        with Image.open(file_path) as img:
            img.thumbnail((1400, 500), Image.LANCZOS)

            # Create a new image with the desired size and a white background
            new_img = Image.new("RGB", (1400, 500), (255, 255, 255))

            # Calculate the position to paste the resized image onto the new image
            paste_position = ((1400 - img.width) // 2, (500 - img.height) // 2)

            # Paste the resized image onto the new image
            new_img.paste(img, paste_position)

            # Save the new image
            new_img.save(file_path)

    car.images = json.dumps(image_names)
    await ActivCarsDAO.update_one_by_obj(car)

    return HTTPException(status_code=200, detail="Images uploaded")



@router.post("/upload_one_photo")
async def upload_one_image(image: UploadFile = File(), user: SUser = Depends(get_current_user)):
    if image.filename == "":
        return JSONResponse(status_code=200, content={"message": "No image"})

    localisation_directory = f"{settings.image_scr}/users"

    image_extension = image.filename.split('.')[-1]
    if image_extension not in ["jpg", "jpeg", "png", "JPEG", "JPG"]:
        raise HTTPException(status_code=400, detail="Image must be jpg, jpeg or png")

    image_name = f"user_{user.id}.{image_extension}"

    file_path = f"{localisation_directory}/{image_name}"

    if not user.image == "none_user_photo.jpg":
        os.remove(f"{localisation_directory}/{user.image}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    with Image.open(file_path) as img:
        img.thumbnail((300, 300), Image.LANCZOS)

        # Create a new image with the desired size and a white background
        new_img = Image.new("RGB", (300, 300), (255, 255, 255))

        # Calculate the position to paste the resized image onto the new image
        paste_position = ((300 - img.width) // 2, (300 - img.height) // 2)

        # Paste the resized image onto the new image
        new_img.paste(img, paste_position)

        # Save the new image
        new_img.save(file_path)

    await UsersDAO.update_one(user.id, image = image_name)

