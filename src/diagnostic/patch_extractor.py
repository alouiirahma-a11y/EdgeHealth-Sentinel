from pathlib import Path
from PIL import Image


def load_annotations(gt_path):
    """
    Read point-based Ground Truth annotations.

    Returns a list of cell annotations.
    """

    annotations = []

    lines = Path(gt_path).read_text().splitlines()

    for line in lines[1:]:
        parts = line.split(",")

        if len(parts) < 7:
            continue

        cell_id = parts[0]
        label = parts[1]
        annotation_type = parts[3]

        if annotation_type != "Point":
            continue

        x = float(parts[5])
        y = float(parts[6])

        annotations.append(
            {
                "id": cell_id,
                "label": label,
                "x": x,
                "y": y,
            }
        )

    return annotations


def extract_patches(
    image_path,
    gt_path,
    output_dir,
    patch_size=128,
):
    """
    Extract cell-centered image patches.

    This is a research prototype.
    It is NOT a clinically validated preprocessing pipeline.
    """

    image = Image.open(image_path).convert("RGB")

    annotations = load_annotations(gt_path)

    output_dir = Path(output_dir)

    for label in ["Parasitized", "Uninfected"]:

        label_dir = output_dir / label
        label_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    half = patch_size // 2

    extracted = 0

    for annotation in annotations:

        x = int(round(annotation["x"]))
        y = int(round(annotation["y"]))

        left = x - half
        top = y - half
        right = x + half
        bottom = y + half

        # Skip annotations too close to image boundaries.
        if left < 0:
            continue

        if top < 0:
            continue

        if right > image.width:
            continue

        if bottom > image.height:
            continue

        patch = image.crop(
            (
                left,
                top,
                right,
                bottom,
            )
        )

        label = annotation["label"]

        output_path = (
            output_dir
            / label
            / f'{annotation["id"]}.jpg'
        )

        patch.save(
            output_path,
            quality=95,
        )

        extracted += 1

    return extracted


if __name__ == "__main__":

    image_path = (
        "data/sample/malaria_sample_01.jpg"
    )

    gt_path = (
        "data/raw/IMG_20150818_142948.txt"
    )

    output_dir = (
        "data/processed/cell_patches"
    )

    count = extract_patches(
        image_path=image_path,
        gt_path=gt_path,
        output_dir=output_dir,
        patch_size=128,
    )

    print(
        f"Extracted patches: {count}"
    )