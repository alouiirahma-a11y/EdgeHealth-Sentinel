from pathlib import Path
from PIL import Image
import numpy as np


LABELS = {
    "Uninfected": 0,
    "Parasitized": 1,
}


def load_cell_dataset(
    dataset_dir="data/processed/cell_patches",
):
    """
    Load extracted cell patches into arrays.

    This is a research prototype.
    It is NOT a clinically validated dataset pipeline.
    """

    dataset_path = Path(dataset_dir)

    images = []
    labels = []
    paths = []

    for class_name, label in LABELS.items():

        class_dir = dataset_path / class_name

        if not class_dir.exists():
            continue

        for image_path in sorted(
            class_dir.glob("*.jpg")
        ):
            image = Image.open(
                image_path
            ).convert("RGB")

            image_array = np.asarray(
                image,
                dtype=np.float32,
            )

            # Normalize pixels from 0–255 to 0–1.
            image_array = image_array / 255.0

            images.append(image_array)
            labels.append(label)
            paths.append(str(image_path))

    if not images:
        raise ValueError(
            "No cell patches were found."
        )

    X = np.stack(images)
    y = np.array(labels, dtype=np.int64)

    return X, y, paths


if __name__ == "__main__":

    X, y, paths = load_cell_dataset()

    print("DATASET LOADED")
    print("X shape:", X.shape)
    print("y shape:", y.shape)

    print()
    print("LABEL COUNTS:")

    print(
        "Uninfected:",
        int(np.sum(y == 0)),
    )

    print(
        "Parasitized:",
        int(np.sum(y == 1)),
    )

    print()
    print("FIRST IMAGE SHAPE:")
    print(X[0].shape)

    print()
    print("PIXEL RANGE:")
    print(
        "min =",
        X.min(),
        "max =",
        X.max(),
    )