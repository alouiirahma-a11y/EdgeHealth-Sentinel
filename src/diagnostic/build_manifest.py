from pathlib import Path
import pandas as pd


INPUT_FILE = "data/raw/Dataset_statistics.xlsx"
OUTPUT_FILE = "data/processed/manifest.csv"


def extract_patient_id(file_path):
    """
    Extract the patient ID from the official NLM GT path.
    """
    path = str(file_path).strip("'")
    parts = path.split("\\")

    if len(parts) >= 5:
        return parts[2]

    return "UNKNOWN"


def build_manifest():
    """
    Build a clean image-level manifest from the
    NIH-NLM-ThinBloodSmearsPf Point Set statistics.
    """

    df = pd.read_excel(
        INPUT_FILE,
        sheet_name="Point Set",
        header=1,
    )

    # Keep only the actual image-statistics columns.
    df = df[
        [
            "File path",
            "WBC",
            "Infected RBC",
            "Uninfected RBC",
        ]
    ].copy()

    # Remove summary rows that do not contain a GT file path.
    df = df[
        df["File path"].notna()
    ].copy()

    # Remove rows that are not actual GT paths.
    df["File path"] = (
        df["File path"]
        .astype(str)
        .str.strip("'")
    )

    df = df[
        df["File path"].str.contains(
            r"\\GT\\",
            regex=True,
        )
    ].copy()

    # Extract patient ID.
    df["patient_id"] = df["File path"].apply(
        extract_patient_id
    )

    # Extract GT filename.
    df["gt_filename"] = (
        df["File path"]
        .str.split("\\")
        .str[-1]
    )

    # Convert GT filename to image filename.
    df["image_filename"] = (
        df["gt_filename"]
        .str.replace(
            ".txt",
            ".jpg",
            regex=False,
        )
    )

    # Dataset-management label.
    #
    # This indicates whether the image has at least
    # one annotated infected RBC.
    #
    # It is NOT a clinical diagnosis.
    df["image_label"] = df["Infected RBC"].apply(
        lambda x: "infected"
        if x > 0
        else "uninfected"
    )

    # Rename the official path column.
    df = df.rename(
        columns={
            "File path": "gt_path"
        }
    )

    # Reorder columns.
    df = df[
        [
            "patient_id",
            "image_filename",
            "gt_filename",
            "WBC",
            "Infected RBC",
            "Uninfected RBC",
            "image_label",
            "gt_path",
        ]
    ]

    # Create output directory.
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save manifest.
    df.to_csv(
        output_path,
        index=False,
    )

    # Verification.
    print()
    print("=" * 60)
    print("EDGEHEALTH SENTINEL - CLEAN MANIFEST")
    print("=" * 60)
    print()

    print("ROWS:", len(df))
    print("UNIQUE PATIENTS:", df["patient_id"].nunique())
    print()

    print("IMAGES PER PATIENT:")
    print(
        df.groupby("patient_id")
        .size()
        .value_counts()
        .sort_index()
    )
    print()

    print("IMAGE LABEL COUNTS:")
    print(
        df["image_label"]
        .value_counts()
    )
    print()

    print("INFECTED RBC TOTAL:")
    print(
        int(df["Infected RBC"].sum())
    )
    print()

    print("UNINFECTED RBC TOTAL:")
    print(
        int(df["Uninfected RBC"].sum())
    )
    print()

    print("WBC TOTAL:")
    print(
        int(df["WBC"].sum())
    )
    print()

    print("UNKNOWN PATIENTS:")
    print(
        int(
            (df["patient_id"] == "UNKNOWN")
            .sum()
        )
    )
    print()

    print("OUTPUT:")
    print(output_path)
    print()

    print("=" * 60)
    print("CLEAN MANIFEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    build_manifest()
