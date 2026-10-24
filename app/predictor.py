import json
from pathlib import Path
import numpy as np
from PIL import Image

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = MODEL_DIR / "disease_model.h5"
# Class order saved by train.py (falls back to the 4 default classes, alphabetical)
_classes = MODEL_DIR / "classes.json"
DISEASES = (json.loads(_classes.read_text()) if _classes.exists()
            else ["Bacterial Blight", "Leaf Spot", "Mosaic Viruses", "Powdery Mildew"])


def load_model():
    """Load the local Keras model (no internet needed)."""
    from tensorflow.keras.models import load_model
    return load_model(MODEL_PATH)


def preprocess_image(image):
    image = image.convert("RGB").resize((224, 224))
    arr = np.array(image, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def predict(image, model, regional_diseases=None):
    """Classify locally. If regional data is stored, restrict to those diseases."""
    probs = model.predict(preprocess_image(image), verbose=0)[0]
    if regional_diseases:
        mask = np.array([d in regional_diseases for d in DISEASES], dtype=np.float32)
        if mask.sum() > 0:
            probs = probs * mask
            probs = probs / probs.sum() if probs.sum() > 0 else mask / mask.sum()
    idx = int(np.argmax(probs))
    return {"disease": DISEASES[idx], "confidence": float(probs[idx])}
