# Dataset — EdgeHealth Sentinel

## Dataset Used

**NIH-NLM-ThinBloodSmearsPf — Point Set**

Source: U.S. National Library of Medicine (NLM), National Institutes of Health (NIH).

Official dataset source:

https://data.lhncbc.nlm.nih.gov/public/Malaria/NIH-NLM-ThinBloodSmearsPf/Point%20Set/

## Description

The dataset contains thin blood smear microscopy images and expert annotations for malaria-related cell analysis.

The official NLM documentation describes two annotation collections: Point Set and Polygon Set. EdgeHealth Sentinel uses the Point Set collection.

## Data Used in This Prototype

For this hackathon prototype, a subset of the Point Set data was processed locally.

Project manifest:
- 807 manifest records
- 160 patients
- 800 source images available for processing
- 162,249 image patches of 128 × 128 pixels
- Training patches: 112,661
- Validation patches: 24,002
- Test patches: 25,586

Labels:
- Parasitized: 6,801
- Uninfected: 155,448

The train/validation/test split was performed at patient level to avoid patient leakage.

## Processing

The source images were processed into smaller image patches for the malaria classification prototype.

The diagnostic baseline uses:
- Image quality assessment
- HOG (Histogram of Oriented Gradients) feature extraction
- Logistic Regression classification

The resulting model is used only as a research prototype and is not clinically validated.

## Data Availability

The original dataset is **not redistributed inside this GitHub repository**.

Users should obtain the dataset directly from the official NLM source and follow the applicable dataset documentation and terms.

Official source:

https://data.lhncbc.nlm.nih.gov/public/Malaria/NIH-NLM-ThinBloodSmearsPf/

## Reproducibility Note

The repository contains the code and documentation needed to understand the processing and modeling workflow.

Large raw datasets and generated image collections are excluded from the repository to keep the project lightweight and avoid unnecessary redistribution of the original dataset.

## Citation / Attribution

Source: U.S. National Library of Medicine (NLM), National Institutes of Health (NIH).

Dataset:
NIH-NLM-ThinBloodSmearsPf — Thin Blood Smears Pf, Point Set.

Official source:
https://data.lhncbc.nlm.nih.gov/public/Malaria/NIH-NLM-ThinBloodSmearsPf/Point%20Set/
