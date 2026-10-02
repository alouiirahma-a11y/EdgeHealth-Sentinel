from pathlib import Path
import pandas as pd
from PIL import Image


MANIFEST_FILE = "data/processed/patient_split.csv"
OUTPUT_DIR = "data/processed/all_cell_patches"
PATCH_MANIFEST = "data/processed/patch_manifest.csv"

PATCH_SIZE = 128


def load_annotations(gt_path):
    annotations = []

    lines = Path(gt_path).read_text(
        encoding="utf-8"
    ).splitlines()

    for line in lines[1:]:
        parts = line.split(",")

        if len(parts) < 7:
            continue

        cell_id = parts[0]
        label = parts[1]
        annotation_type = parts[3]

        if annotation_type != "Point":
            continue

        if label not in ["Parasitized", "Uninfected"]:
            continue

        x = float(parts[5])
        y = float(parts[6])

        annotations.append(
            {
                "cell_id": cell_id,
                "label": label,
                "x": x,
                "y": y,
            }
        )

    return annotations


def extract_patch(image, x, y, patch_size):
    half = patch_size // 2

    x = int(round(x))
    y = int(round(y))

    left = x - half
    top = y - half
    right = x + half
    bottom = y + half

    if left < 0 or top < 0:
        return None

    if right > image.width or bottom > image.height:
        return None

    return image.crop(
        (
            left,
            top,
            right,
            bottom,
        )
    )


def main():

    df = pd.read_csv(MANIFEST_FILE)

    output_dir = Path(OUTPUT_DIR)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    patch_records = []

    total_images = len(df)
    total_patches = 0
    skipped_patches = 0

    print()
    print("=" * 70)
    print("EDGEHEALTH SENTINEL - FULL CELL PATCH EXTRACTION")
    print("=" * 70)
    print()

    print("IMAGES:", total_images)
    print("PATCH SIZE:", PATCH_SIZE)
    print()

    for index, row in df.iterrows():

        patient_id = str(row["patient_id"])
        image_filename = str(row["image_filename"])
        gt_filename = str(row["gt_filename"])
        split = str(row["split"])

        image_path = (
            Path("data/raw/Point_Set")
            / patient_id
            / "Img"
            / image_filename
        )

        gt_path = (
            Path("data/raw/Point_Set")
            / patient_id
            / "GT"
            / gt_filename
        )

        if not image_path.exists():
            print("MISSING IMAGE:", image_path)
            continue

        if not gt_path.exists():
            print("MISSING GT:", gt_path)
            continue

        annotations = load_annotations(gt_path)

        with Image.open(image_path) as image:

            image = image.convert("RGB")

            image_stem = Path(
                image_filename
            ).stem

            for annotation in annotations:

                patch = extract_patch(
                    image,
                    annotation["x"],
                    annotation["y"],
                    PATCH_SIZE,
                )

                if patch is None:
                    skipped_patches += 1
                    continue

                label = annotation["label"]

                label_dir = (
                    output_dir
                    / split
                    / label
                )

                label_dir.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                patch_filename = (
                    f"{patient_id}__"
                    f"{image_stem}__"
                    f"{annotation['cell_id']}.jpg"
                )

                patch_path = (
                    label_dir
                    / patch_filename
                )

                patch.save(
                    patch_path,
                    quality=95,
                )

                patch_records.append(
                    {
                        "patch_path": str(patch_path),
                        "patient_id": patient_id,
                        "image_filename": image_filename,
                        "split": split,
                        "label": label,
                        "cell_id": annotation["cell_id"],
                        "x": annotation["x"],
                        "y": annotation["y"],
                    }
                )

                total_patches += 1

        if (index + 1) % 25 == 0:
            print(
                f"[{index + 1}/{total_images}] "
                f"images processed | "
                f"patches: {total_patches}"
            )

    patch_df = pd.DataFrame(patch_records)

    patch_df.to_csv(
        PATCH_MANIFEST,
        index=False,
    )

    print()
    print("=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)

    print()
    print("TOTAL PATCHES:", total_patches)
    print("SKIPPED PATCHES:", skipped_patches)

    print()
    print("PATCHES BY SPLIT:")
    print(
        patch_df["split"]
        .value_counts()
        .sort_index()
    )

    print()
    print("PATCHES BY LABEL:")
    print(
        patch_df["label"]
        .value_counts()
        .sort_index()
    )

    print()
    print("PATCHES BY SPLIT AND LABEL:")
    print(
        pd.crosstab(
            patch_df["split"],
            patch_df["label"],
        )
    )

    print()
    print("UNIQUE PATIENTS BY SPLIT:")
    print(
        patch_df.groupby("split")[
            "patient_id"
        ].nunique()
    )

    print()
    print("OUTPUT DIRECTORY:")
    print(output_dir)

    print()
    print("PATCH MANIFEST:")
    print(PATCH_MANIFEST)

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
