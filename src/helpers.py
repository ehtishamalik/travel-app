import uuid
from PIL import Image
from os import path
from sqlalchemy.inspection import inspect
from src.constants import IMAGES_FOLDER


def generate_unique_key():
    unique_key = str(uuid.uuid4())
    return unique_key


def save_compressed_image(img_name: str, img):
    base_width = 480
    image = Image.open(img)
    image = image.convert("RGB")
    if image.size[0] <= base_width:
        image.save(path.join(IMAGES_FOLDER, img_name), optimize=True, format="JPEG")
    else:
        width_percent = base_width / float(image.size[0])
        hsize = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((base_width, hsize), Image.LANCZOS)
        image.save(path.join(IMAGES_FOLDER, img_name), optimize=True, format="JPEG")


def sqlalchemy_to_tuple(instance):
    return tuple(
        getattr(instance, column.key)
        for column in inspect(instance).mapper.column_attrs
    )


def valid_image(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]
