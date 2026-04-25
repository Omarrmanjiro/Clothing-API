import tensorflow as tf
import numpy as np
from PIL import Image
import io
from app.labels import LABELS

model = tf.keras.models.load_model("model/fashion_model.h5")

def preprocess(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((96, 96))
    img = np.array(image) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_image(image_bytes):
    img = preprocess(image_bytes)
    pred = model.predict(img, verbose=0)

    index = int(np.argmax(pred))
    confidence = float(np.max(pred)) * 100

    return LABELS[index], confidence