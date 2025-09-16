from PIL import Image

def load_image(path: str):
    try:
        return Image.open(path)
    except Exception:
        return None
