from fastapi import FastAPI, UploadFile, File
from app.classifier import predict_image
from app.utils import get_category

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

    return {
        "success": True,
        "prediction": {
            "label": label,
            "confidence": round(confidence, 2),
            "category": get_category(label)
        }
    }