import base64
from config import settings

def get_image_base64(image_path):
    localisation_directory = f"{settings.image_scr}/{image_path}"
    try:
        with open(localisation_directory, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        return None