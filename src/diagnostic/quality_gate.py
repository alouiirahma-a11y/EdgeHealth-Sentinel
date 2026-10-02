from PIL import Image, ImageStat, ImageFilter


def extract_image_features(image_path):
    """
    Extract basic image-quality features.

    This is a research prototype.
    It is NOT a validated medical image-quality model.
    """

    image = Image.open(image_path).convert("L")

    # Brightness
    brightness = ImageStat.Stat(image).mean[0]

    # Contrast
    contrast = ImageStat.Stat(image).stddev[0]

    # Sharpness proxy
    edges = image.filter(ImageFilter.FIND_EDGES)
    sharpness = ImageStat.Stat(edges).mean[0]

    return {
        "brightness": brightness,
        "contrast": contrast,
        "sharpness": sharpness,
    }


def check_image_quality(
    brightness,
    contrast,
    sharpness,
):
    """
    Evaluate whether an image has sufficient quality
    for further AI analysis.

    This is a synthetic research prototype.
    It is NOT a validated medical image-quality model.
    """

    issues = []

    if brightness < 40:
        issues.append("LOW_BRIGHTNESS")

    if contrast < 30:
        issues.append("LOW_CONTRAST")

    if sharpness < 0.5:
        issues.append("LOW_SHARPNESS")

    if issues:
        return {
            "quality_status": "INSUFFICIENT",
            "decision": "RETAKE_IMAGE",
            "issues": issues,
        }

    return {
        "quality_status": "SUFFICIENT",
        "decision": "PROCEED",
        "issues": [],
    }