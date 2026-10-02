from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
    roc_auc_score,
)
import joblib


PATCH_MANIFEST = "data/processed/patch_manifest.csv"

MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "malaria_hog_logistic.joblib"

IMAGE_SIZE = (64, 64)

TRAIN_LIMIT = 30000

RANDOM_STATE = 42


def extract_hog_features(image_path):

    image = Image.open(
        image_path
    ).convert("L")

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

    return features


def select_training_data(df):

    train_df = df[
        df["split"] == "train"
    ].copy()

    if len(train_df) <= TRAIN_LIMIT:
        return train_df

    # Keep the two classes represented
    # in approximately the same proportion.
    selected_parts = []

    for label in [
        "Uninfected",
        "Parasitized",
    ]:

        label_df = train_df[
            train_df["label"] == label
        ]

        proportion = (
            len(label_df)
            / len(train_df)
        )

        n_samples = int(
            TRAIN_LIMIT * proportion
        )

        n_samples = max(
            n_samples,
            1,
        )

        selected_parts.append(
            label_df.sample(
                n=n_samples,
                random_state=RANDOM_STATE,
            )
        )

    selected = pd.concat(
        selected_parts
    )

    return selected.sample(
        frac=1,
        random_state=RANDOM_STATE,
    )


def load_features(df, split_name):

    subset = df[
        df["split"] == split_name
    ].copy()

    X = []
    y = []

    total = len(subset)

    print()
    print(
        f"Loading {split_name}: "
        f"{total} patches"
    )

    for index, (_, row) in enumerate(
        subset.iterrows(),
        start=1,
    ):

        X.append(
            extract_hog_features(
                row["patch_path"]
            )
        )

        y.append(
            1
            if row["label"] == "Parasitized"
            else 0
        )

        if index % 5000 == 0:
            print(
                f"  {index}/{total}"
            )

    return (
        np.asarray(
            X,
            dtype=np.float32,
        ),
        np.asarray(
            y,
            dtype=np.int64,
        ),
    )


def evaluate_model(
    model,
    X,
    y,
    split_name,
):

    probabilities = (
        model.predict_proba(X)[:, 1]
    )

    predictions = (
        probabilities >= 0.50
    ).astype(int)

    print()
    print("=" * 70)
    print(
        f"{split_name.upper()} RESULTS"
    )
    print("=" * 70)

    print()
    print("CONFUSION MATRIX:")

    print(
        confusion_matrix(
            y,
            predictions,
        )
    )

    print()
    print("CLASSIFICATION REPORT:")

    print(
        classification_report(
            y,
            predictions,
            target_names=[
                "Uninfected",
                "Parasitized",
            ],
            zero_division=0,
        )
    )

    print(
        "ROC-AUC:",
        round(
            roc_auc_score(
                y,
                probabilities,
            ),
            4,
        ),
    )

    print(
        "PR-AUC:",
        round(
            average_precision_score(
                y,
                probabilities,
            ),
            4,
        ),
    )


def main():

    print()
    print("=" * 70)
    print(
        "EDGEHEALTH SENTINEL"
    )
    print(
        "HOG + LOGISTIC REGRESSION BASELINE"
    )
    print("=" * 70)

    df = pd.read_csv(
        PATCH_MANIFEST
    )

    print()
    print(
        "TOTAL PATCHES:",
        len(df),
    )

    train_selected = select_training_data(
        df
    )

    print()
    print(
        "SELECTED TRAINING PATCHES:",
        len(train_selected),
    )

    print()
    print(
        "SELECTED TRAINING LABELS:"
    )

    print(
        train_selected[
            "label"
        ].value_counts()
    )

    train_df = train_selected.copy()

    validation_df = df[
        df["split"] == "validation"
    ].copy()

    test_df = df[
        df["split"] == "test"
    ].copy()

    # Temporarily combine the selected
    # training rows with validation/test
    # so load_features can process them.
    train_df["split"] = "train_selected"

    combined_train = train_df

    X_train = []
    y_train = []

    print()
    print(
        f"Loading train_selected: "
        f"{len(combined_train)} patches"
    )

    for index, (_, row) in enumerate(
        combined_train.iterrows(),
        start=1,
    ):

        X_train.append(
            extract_hog_features(
                row["patch_path"]
            )
        )

        y_train.append(
            1
            if row["label"] == "Parasitized"
            else 0
        )

        if index % 5000 == 0:
            print(
                f"  {index}/{len(combined_train)}"
            )

    X_train = np.asarray(
        X_train,
        dtype=np.float32,
    )

    y_train = np.asarray(
        y_train,
        dtype=np.int64,
    )

    validation_df["split"] = "validation"

    X_validation, y_validation = load_features(
        validation_df,
        "validation",
    )

    test_df["split"] = "test"

    X_test, y_test = load_features(
        test_df,
        "test",
    )

    print()
    print("=" * 70)
    print("FEATURE SHAPES")
    print("=" * 70)

    print(
        "X_train:",
        X_train.shape,
    )

    print(
        "X_validation:",
        X_validation.shape,
    )

    print(
        "X_test:",
        X_test.shape,
    )

    print()
    print("=" * 70)
    print("TRAINING MODEL")
    print("=" * 70)

    model = LogisticRegression(
        max_iter=300,
        class_weight="balanced",
        solver="liblinear",
        random_state=RANDOM_STATE,
    )

    model.fit(
        X_train,
        y_train,
    )

    print()
    print(
        "MODEL TRAINING COMPLETE"
    )

    evaluate_model(
        model,
        X_validation,
        y_validation,
        "validation",
    )

    evaluate_model(
        model,
        X_test,
        y_test,
        "test",
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_FILE,
    )

    print()
    print("=" * 70)
    print("MODEL SAVED")
    print("=" * 70)

    print(
        MODEL_FILE
    )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
