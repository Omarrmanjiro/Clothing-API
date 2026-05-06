import math

def get_category(label):
    mapping = {
        "T-shirt/top": "Topwear",
        "Trouser": "Bottomwear",
        "Pullover": "Topwear",
        "Dress": "Full Body",
        "Coat": "Outerwear",
        "Sandal": "Footwear",
        "Shirt": "Topwear",
        "Sneaker": "Footwear",
        "Bag": "Accessory",
        "Ankle boot": "Footwear"
    }
    return mapping.get(label, "Fashion Item")

def get_season(label):
    if label in ["Coat", "Pullover", "Ankle boot"]:
        return "Winter / Fall"
    elif label in ["T-shirt/top", "Sandal", "Dress"]:
        return "Summer / Spring"
    else:
        return "All Seasons"

def get_material(label):
    if label == "Trouser": return "Denim or Cotton"
    if label in ["Coat", "Pullover"]: return "Wool or Fleece"
    if label in ["T-shirt/top", "Shirt", "Dress"]: return "Cotton or Blend"
    if label in ["Sneaker", "Sandal", "Ankle boot"]: return "Leather or Synthetic"
    if label == "Bag": return "Canvas or Leather"
    return "Mixed materials"

def get_approx_color(image_bytes):
    from PIL import Image
    import io
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((1, 1))
        r, g, b = image.getpixel((0, 0))
        return rgb_to_name(r, g, b)
    except:
        return "Unknown"

def rgb_to_name(r, g, b):
    # Simple color bucketing
    colors = {
        "Black": (0, 0, 0), "White": (255, 255, 255), "Red": (255, 0, 0),
        "Green": (0, 255, 0), "Blue": (0, 0, 255), "Yellow": (255, 255, 0),
        "Cyan": (0, 255, 255), "Magenta": (255, 0, 255), "Gray": (128, 128, 128),
        "Navy": (0, 0, 128), "Maroon": (128, 0, 0), "Olive": (128, 128, 0),
        "Brown": (139, 69, 19), "Orange": (255, 140, 0), "Pink": (255, 192, 203)
    }
    best_color = "Unknown"
    min_dist = float("inf")
    for name, (cr, cg, cb) in colors.items():
        dist = math.sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        if dist < min_dist:
            min_dist = dist
            best_color = name
    return best_color