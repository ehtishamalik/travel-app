import uuid
from PIL import Image


def generate_unique_key():
    unique_key = str(uuid.uuid4())
    return unique_key


def save_compressed_image(path: str, img):
    base_width = 480
    image = Image.open(img)
    image = image.convert("RGB")
    if image.size[0] <= base_width:
        image.save(path, optimize=True, format="JPEG")
    else:
        width_percent = base_width / float(image.size[0])
        hsize = int((float(image.size[1]) * float(width_percent)))
        image = image.resize((base_width, hsize), Image.LANCZOS)
        image.save(path, optimize=True, format="JPEG")
