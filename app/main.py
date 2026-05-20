from fastapi import FastAPI, UploadFile, File
from app.classifier import predict_image
from app.utils import get_category, get_season, get_material, get_approx_color, get_gender, get_style, get_occasion
from app.gemini import generate_outfit_description

app = FastAPI(title="Clothing AI API")

@app.get("/")
def home():
    return {"message": "Clothing AI API Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()

    label, confidence = predict_image(image_bytes)
    color     = get_approx_color(image_bytes)
    category  = get_category(label)
    style     = get_style(label)
    season    = get_season(label)
    material  = get_material(label)

    occasions = get_occasion(label)
    occasion_strings = [f"{occ}: {reason}" for occ, reason in occasions]

    # LLM description — runs last so it never blocks classification
    description = generate_outfit_description(
        label=label,
        category=category,
        color=color,
        style=style,
        season=season,
        material=material,
    )

    return {
        "success": True,
        "prediction": {
            "label":       label,
            "confidence":  round(confidence, 2),
            "category":    category,
            "color":       color,
            "gender":      get_gender(label),
            "style":       style,
            "season":      season,
            "material":    material,
            "occasions":   occasion_strings,
            "description": description,   # None when Gemini key not set
        }
    }
