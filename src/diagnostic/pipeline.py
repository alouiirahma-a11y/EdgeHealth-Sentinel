from src.diagnostic.malaria_model import analyze_image
from src.diagnostic.quality_gate import (
    extract_image_features,
    check_image_quality,
)
from src.diagnostic.uncertainty import assess_uncertainty
from src.safety.governor import safety_decision


def run_diagnostic_pipeline(
    image_path,
    ood_detected=False,
):
    """
    Run the complete EdgeHealth Sentinel
    diagnostic safety pipeline.

    Pipeline:

    Image
        ↓
    Quality Gate
        ↓
    Trained ML Model
        ↓
    Uncertainty Assessment
        ↓
    Safety Governor
        ↓
    Final Decision

    This is a research prototype.
    It is NOT a clinically validated diagnostic system.
    """

    # -------------------------------------------------
    # 1. IMAGE QUALITY
    # -------------------------------------------------

    features = extract_image_features(
        image_path
    )

    quality = check_image_quality(
        **features
    )

    if quality["decision"] == "RETAKE_IMAGE":

        return {
            "image": image_path,
            "features": features,
            "quality": quality,
            "model": None,
            "uncertainty": None,
            "safety": {
                "decision": "RETAKE_IMAGE",
                "reason": "IMAGE_QUALITY_INSUFFICIENT",
            },
            "final_decision": "RETAKE_IMAGE",
        }

    # -------------------------------------------------
    # 2. REAL MODEL INFERENCE
    # -------------------------------------------------

    model_result = analyze_image(
        image_path
    )

    probability = model_result[
        "parasitized_probability"
    ]

    # -------------------------------------------------
    # 3. UNCERTAINTY
    # -------------------------------------------------

    uncertainty = assess_uncertainty(
        model_result["confidence"]
    )

    # -------------------------------------------------
    # 4. SAFETY GOVERNOR
    # -------------------------------------------------

    safety = safety_decision(
        quality_status=quality[
            "quality_status"
        ],
        confidence=model_result[
            "confidence"
        ],
        ood_detected=ood_detected,
    )

    # -------------------------------------------------
    # 5. FINAL RESULT
    # -------------------------------------------------

    return {
        "image": image_path,
        "features": features,
        "quality": quality,
        "model": {
            "prediction": model_result[
                "prediction"
            ],
            "parasitized_probability": probability,
            "confidence": model_result[
                "confidence"
            ],
            "model_name": model_result[
                "model"
            ],
        },
        "uncertainty": uncertainty,
        "safety": safety,
        "final_decision": safety[
            "decision"
        ],
    }


if __name__ == "__main__":

    print()
    print("=" * 70)
    print("EDGEHEALTH SENTINEL")
    print("COMPLETE DIAGNOSTIC SAFETY PIPELINE")
    print("=" * 70)

    print()
    print(
        "Pipeline module loaded successfully."
    )

    print()
    print(
        "Architecture:"
    )

    print(
        "Image"
        " -> Quality Gate"
        " -> ML Model"
        " -> Uncertainty"
        " -> Safety Governor"
        " -> Decision"
    )

    print()
    print(
        "The pipeline is ready for image-level testing."
    )

    print()
    print("=" * 70)
