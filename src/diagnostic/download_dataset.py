from pathlib import Path
import pandas as pd
import requests
import time


BASE_URL = (
    "https://data.lhncbc.nlm.nih.gov/public/"
    "Malaria/NIH-NLM-ThinBloodSmearsPf/"
    "Point%20Set/"
)

MANIFEST_FILE = "data/processed/manifest.csv"
OUTPUT_DIR = Path("data/raw/Point_Set")
DOWNLOAD_LOG = Path("data/processed/download_manifest.csv")


def download_file(url, output_path):
    """
    Download one file if it does not already exist.
    """
    if output_path.exists() and output_path.stat().st_size > 0:
        return "EXISTS"

    try:
        response = requests.get(
            url,
            stream=True,
            timeout=120,
        )

        if response.status_code != 200:
            return f"HTTP_{response.status_code}"

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):
                if chunk:
                    file.write(chunk)

        return "DOWNLOADED"

    except Exception as error:
        return f"ERROR: {error}"


def build_url(patient_id, folder, filename):
    return (
        BASE_URL
        + patient_id
        + "/"
        + folder
        + "/"
        + filename
    )


def main():

    print()
    print("=" * 70)
    print("EDGEHEALTH SENTINEL - NLM DATASET DOWNLOADER")
    print("=" * 70)
    print()

    df = pd.read_csv(MANIFEST_FILE)

    print("Manifest rows:", len(df))
    print("Patients:", df["patient_id"].nunique())
    print()

    results = []

    for index, row in df.iterrows():

        patient_id = row["patient_id"]
        image_filename = row["image_filename"]
        gt_filename = row["gt_filename"]

        patient_dir = OUTPUT_DIR / patient_id

        image_path = (
            patient_dir
            / "Img"
            / image_filename
        )

        gt_path = (
            patient_dir
            / "GT"
            / gt_filename
        )

        image_url = build_url(
            patient_id,
            "Img",
            image_filename,
        )

        gt_url = build_url(
            patient_id,
            "GT",
            gt_filename,
        )

        image_status = download_file(
            image_url,
            image_path,
        )

        gt_status = download_file(
            gt_url,
            gt_path,
        )

        results.append(
            {
                "patient_id": patient_id,
                "image_filename": image_filename,
                "gt_filename": gt_filename,
                "image_path": str(image_path),
                "gt_path": str(gt_path),
                "image_status": image_status,
                "gt_status": gt_status,
            }
        )

        completed = index + 1

        print(
            f"[{completed}/{len(df)}] "
            f"{patient_id} | "
            f"{image_filename} | "
            f"IMAGE={image_status} | "
            f"GT={gt_status}"
        )

        time.sleep(0.05)

    results_df = pd.DataFrame(results)

    DOWNLOAD_LOG.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df.to_csv(
        DOWNLOAD_LOG,
        index=False,
    )

    print()
    print("=" * 70)
    print("DOWNLOAD COMPLETE")
    print("=" * 70)
    print()

    print("IMAGE STATUS:")
    print(
        results_df["image_status"]
        .value_counts()
        .to_string()
    )

    print()
    print("GT STATUS:")
    print(
        results_df["gt_status"]
        .value_counts()
        .to_string()
    )

    print()
    print("Download log:")
    print(DOWNLOAD_LOG)

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
