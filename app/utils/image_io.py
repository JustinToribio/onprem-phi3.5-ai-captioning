from PIL import Image

# If you're running into OOM issues, try resizing img down to 224x224 minimum
def load_image(image_file):
    img = Image.open(image_file).convert("RGB")
    return img