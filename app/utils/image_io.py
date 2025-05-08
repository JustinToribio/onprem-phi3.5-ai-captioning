from PIL import Image
from io import BytesIO

# If you're running into OOM issues, try resizing img down to 224x224 minimum
def load_image_from_bytes(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    return img