import math

def get_category(label):
    mapping = {
        "T-shirt/top": "T-shirt",
        "Trouser": "Jeans",
        "Pullover": "Hoodie",
        "Dress": "Dress",
        "Coat": "Jacket",
        "Sandal": "Sandal",
        "Shirt": "Shirt",
        "Sneaker": "Sneakers",
        "Bag": "Bag",
        "Ankle boot": "Boots"
    }
    return mapping.get(label, label)

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

def get_gender(label):
    if label in ["Dress"]: return "female"
    return "unisex"

def get_style(label):
    if label in ["Sneaker", "T-shirt/top", "Pullover"]:
        return "casual"
    elif label in ["Coat", "Shirt", "Ankle boot", "Dress"]:
        return "elegant"
    elif label in ["Sandal"]:
        return "summer"
    return "casual"

def get_approx_color(image_bytes):
    from PIL import Image
    import io
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        w, h = image.size

        # Sample the CENTER 40% of the image to avoid background edges
        x0 = int(w * 0.30)
        y0 = int(h * 0.30)
        x1 = int(w * 0.70)
        y1 = int(h * 0.70)
        center_crop = image.crop((x0, y0, x1, y1))

        # Downsample to a small grid and collect all pixel colors
        small = center_crop.resize((8, 8))
        pixels = list(small.getdata())

        # Filter out near-white and near-black pixels (background / shadow)
        filtered = [
            (r, g, b) for (r, g, b) in pixels
            if not (r > 220 and g > 220 and b > 220)   # skip near-white
            and not (r < 35 and g < 35 and b < 35)      # skip near-black
        ]

        if not filtered:
            filtered = pixels  # fallback if everything was filtered

        # Average the remaining pixels
        n = len(filtered)
        avg_r = sum(p[0] for p in filtered) // n
        avg_g = sum(p[1] for p in filtered) // n
        avg_b = sum(p[2] for p in filtered) // n

        return rgb_to_name(avg_r, avg_g, avg_b)
    except Exception:
        return "Unknown"


def _rgb_to_lab(r, g, b):
    """Convert RGB (0-255) to CIE Lab for perceptual color distance."""
    # Normalize to 0-1
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # Linearize
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = lin(r), lin(g), lin(b)

    # Convert to XYZ (D65 illuminant)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    x /= 0.95047
    y /= 1.00000
    z /= 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b_val = 200 * (fy - fz)
    return L, a, b_val


def rgb_to_name(r, g, b):
    """Match an RGB value to the nearest clothing color using perceptual Lab distance."""
    # Clothing-specific color palette (realistic, not just HTML primaries)
    colors = {
        "Black":        (20,  20,  20),
        "Charcoal":     (54,  54,  54),
        "Dark Gray":    (80,  80,  80),
        "Gray":         (128, 128, 128),
        "Light Gray":   (192, 192, 192),
        "White":        (245, 245, 245),
        "Cream":        (255, 253, 208),
        "Beige":        (245, 222, 179),
        "Khaki":        (195, 176, 131),
        "Tan":          (210, 180, 140),
        "Brown":        (139, 90,  43),
        "Dark Brown":   (92,  51,  23),
        "Navy Blue":    (20,  30,  80),
        "Denim Blue":   (93,  123, 166),
        "Blue":         (30,  90,  200),
        "Light Blue":   (135, 185, 235),
        "Sky Blue":     (87,  185, 240),
        "Teal":         (0,   128, 128),
        "Dark Green":   (1,   65,  36),
        "Green":        (34,  139, 34),
        "Olive":        (107, 110, 55),
        "Army Green":   (75,  83,  32),
        "Burgundy":     (128, 0,   32),
        "Red":          (200, 30,  30),
        "Coral":        (255, 127, 80),
        "Orange":       (230, 120, 20),
        "Yellow":       (240, 210, 30),
        "Mustard":      (210, 160, 40),
        "Pink":         (255, 182, 193),
        "Hot Pink":     (255, 100, 143),
        "Purple":       (128, 0,   128),
        "Lavender":     (180, 150, 220),
        "Mauve":        (180, 120, 140),
    }

    L1, a1, b1 = _rgb_to_lab(r, g, b)
    best_color = "Unknown"
    min_dist = float("inf")

    for name, (cr, cg, cb) in colors.items():
        L2, a2, b2 = _rgb_to_lab(cr, cg, cb)
        dist = math.sqrt((L1 - L2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2)
        if dist < min_dist:
            min_dist = dist
            best_color = name

    return best_color
