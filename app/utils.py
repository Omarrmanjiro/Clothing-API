def get_category(label):
    mapping = {
        "T-shirt/top": "Topwear",
        "Trouser": "Bottomwear",
        "Sneaker": "Footwear",
        "Bag": "Accessory"
    }

    return mapping.get(label, "Fashion Item")