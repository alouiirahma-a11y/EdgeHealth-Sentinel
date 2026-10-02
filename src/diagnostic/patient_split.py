from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


MANIFEST_FILE = "data/processed/manifest.csv"
OUTPUT_FILE = "data/processed/patient_split.csv"

RANDOM_STATE = 42


def create_patient_split():

    df = pd.read_csv(MANIFEST_FILE)

    patients = list(
        df["patient_id"]
        .dropna()
        .astype(str)
        .unique()
    )

    print()
    print("=" * 60)
    print("EDGEHEALTH SENTINEL - PATIENT LEVEL SPLIT")
    print("=" * 60)
    print()

    print("TOTAL PATIENTS:", len(patients))
    print()

    train_patients, temp_patients = train_test_split(
        patients,
        test_size=0.30,
        random_state=RANDOM_STATE,
    )

    val_patients, test_patients = train_test_split(
        temp_patients,
        test_size=0.50,
        random_state=RANDOM_STATE,
    )

    split_map = {}

    for patient in train_patients:
        split_map[patient] = "train"

    for patient in val_patients:
        split_map[patient] = "validation"

    for patient in test_patients:
        split_map[patient] = "test"

    df["patient_id"] = df["patient_id"].astype(str)

    df["split"] = df["patient_id"].map(split_map)

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print("PATIENT SPLIT:")
    print(
        pd.Series(split_map.values())
        .value_counts()
        .sort_index()
    )

    print()
    print("IMAGE SPLIT:")
    print(
        df["split"]
        .value_counts()
        .sort_index()
    )

    print()
    print("PATIENTS PER SPLIT:")
    print(
        df.groupby("split")["patient_id"]
        .nunique()
        .sort_index()
    )

    print()
    print("CHECKING FOR PATIENT LEAKAGE...")

    train_set = set(train_patients)
    val_set = set(val_patients)
    test_set = set(test_patients)

    overlap_train_val = train_set & val_set
    overlap_train_test = train_set & test_set
    overlap_val_test = val_set & test_set

    print(
        "Train ∩ Validation:",
        len(overlap_train_val),
    )

    print(
        "Train ∩ Test:",
        len(overlap_train_test),
    )

    print(
        "Validation ∩ Test:",
        len(overlap_val_test),
    )

    print()

    if (
        len(overlap_train_val) == 0
        and len(overlap_train_test) == 0
        and len(overlap_val_test) == 0
    ):
        print("LEAKAGE CHECK: PASSED")
    else:
        print("LEAKAGE CHECK: FAILED")

    print()
    print("OUTPUT:")
    print(output_path)

    print()
    print("=" * 60)


if __name__ == "__main__":
    create_patient_split()