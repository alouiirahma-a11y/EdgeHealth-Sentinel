from pathlib import Path
import pandas as pd
from PIL import Image


MANIFEST_FILE = "data/processed/download_manifest.csv"


df = pd.read_csv(MANIFEST_FILE)

valid_images = 0
valid_gt = 0
bad_images = []
missing_images = []
missing_gt = []


for _, row in df.iterrows():

    image_path = Path(row["image_path"])
    gt_path = Path(row["gt_path"])

    # Check image
    if image_path.exists() and image_path.stat().st_size > 0:
        try:
            with Image.open(image_path) as image:
                image.verify()
            valid_images += 1
        except Exception:
            bad_images.append(str(image_path))
    else:
        missing_images.append(str(image_path))

    # Check GT
    if gt_path.exists() and gt_path.stat().st_size > 0:
        valid_gt += 1
    else:
        missing_gt.append(str(gt_path))


print()
print("=" * 60)
print("EDGEHEALTH SENTINEL - DATASET VERIFICATION")
print("=" * 60)
print()

print("MANIFEST ROWS:", len(df))
print("VALID IMAGES:", valid_images)
print("VALID GT FILES:", valid_gt)
print("MISSING IMAGES:", len(missing_images))
print("MISSING GT:", len(missing_gt))
print("CORRUPTED IMAGES:", len(bad_images))

print()

if missing_images:
    print("FIRST MISSING IMAGE:")
    print(missing_images[0])
    print()

if missing_gt:
    print("FIRST MISSING GT:")
    print(missing_gt[0])
    print()

if bad_images:
    print("FIRST CORRUPTED IMAGE:")
    print(bad_images[0])
    print()

if (
    valid_images == 800
    and valid_gt == 800
    and len(missing_images) == 0
    and len(missing_gt) == 0
    and len(bad_images) == 0
):
    print("STATUS: DATASET READY")
else:
    print("STATUS: DATASET NEEDS REVIEW")

print()
print("=" * 60)
