from pathlib import Path

import numpy as np
from PIL import Image
from skimage.feature import hog
import joblib


MODEL_PATH = Path(
    "models/malaria_hog_logistic.joblib"
)

IMAGE_SIZE = (64, 64)


def load_model():
    """
    Load the trained HOG + Logistic Regression baseline.

    Research prototype only.
    Not a clinically validated diagnostic model.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def extract_hog_features(image):
    """
    Convert a cell image into the same HOG representation
    used during model training.
    """

    image = image.convert("L")

    image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.asarray(
        image,
        dtype=np.float32,
    ) / 255.0

    features = hog(
        image_array,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
    )

    return features.reshape(1, -1)


def analyze_image(image_path):
    """
    Run the trained malaria patch classifier.

    Returns a model probability and prediction.

    This is a research prototype.
    It is NOT a clinical diagnostic system.
    """

    model = load_model()

    image = Image.open(
        image_path
    )

    features = extract_hog_features(
        image
    )

    probability = float(
        model.predict_proba(
            features
        )[0][1]
    )

    prediction = (
        "Parasitized"
        if probability >= 0.50
        else "Uninfected"
    )

    confidence = (
        probability
        if prediction == "Parasitized"
        else 1.0 - probability
    )

    return {
        "prediction": prediction,
        "parasitized_probability": probability,
        "confidence": confidence,
        "status": "MODEL_INFERENCE",
        "model": "HOG + Logistic Regression",
        "model_path": str(MODEL_PATH),
        "threshold": 0.50,
    }


if __name__ == "__main__":

    print()
    print("=" * 70)
    print("EDGEHEALTH SENTINEL")
    print("MALARIA MODEL INFERENCE TEST")
    print("=" * 70)

    print()
    print(
        "Model:",
        MODEL_PATH,
    )

    print()
    print(
        "Model loaded successfully."
    )

    print()
    print(
        "This module is ready for integration "
        "with the safety pipeline."
    )

    print()
    print("=" * 70)
