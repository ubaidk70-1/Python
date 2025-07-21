# Chronic Kidney Disease (CKD) - Data Cleaning & Preprocessing Project

## Project Goal

The primary objective of this project is to perform a comprehensive data cleaning and preprocessing pipeline on a raw dataset for Chronic Kidney Disease. The goal is to transform the initial messy, real-world data into a clean, well-structured, and model-ready format, suitable for training a predictive machine learning model. This project demonstrates the foundational and most critical skills in the data analysis workflow.

---

## About the Dataset

The dataset contains 400 records and 26 features, collected from patients to identify factors related to Chronic Kidney Disease. The raw data contains numerous issues, including missing values, incorrect data types, erroneous characters, and outliers, making it a perfect case study for a robust data preparation pipeline.

**Target Variable:**
* `classification`: This is the column a future model would aim to predict. It is a binary variable indicating whether a patient is classified as having **'ckd'** (Chronic Kidney Disease) or **'notckd'** (Not Chronic Kidney Disease).

---

## Project Workflow

The project follows a systematic approach to data preparation, broken down into two main phases:

#### 1. Data Cleaning
This phase focuses on fixing errors and inconsistencies in the raw data.
* **Correcting Data Types:** Identified and cleaned columns (`pcv`, `wc`, `rc`) that contained non-numeric characters (`?`, `\t`) and converted them to a proper numeric format.
* **Standardizing Values:** Fixed typos and removed leading/trailing whitespace from all categorical columns to ensure consistency (e.g., `'ckd\t'` was corrected to `'ckd'`).
* **Handling Missing Values:** Imputed missing data using appropriate statistical measures:
    * **Median** for numerical features to avoid skew from outliers.
    * **Mode** for categorical features to use the most frequent value.
* **Outlier Detection & Handling:** Used box plots to visualize distributions and identify outliers. Based on medical context, outliers were either kept (if they were a strong clinical signal, like in `bgr`, `sc`, `hemo`) or capped using the IQR method (for features like `bp`, `sod`, `pot`) to reduce statistical noise.

#### 2. Data Preprocessing
This phase prepares the clean data for machine learning models.
* **Encoding Categorical Features:** Converted all binary categorical columns (e.g., `'yes'`/`'no'`, `'normal'`/`'abnormal'`) into a numerical format (`1`/`0`) using mapping.
* **Feature Scaling:** Applied **Standardization** (`StandardScaler`) to all independent numerical features. This rescales the data to have a mean of 0 and a standard deviation of 1, ensuring that no single feature dominates a model's learning process due to its scale.

---

## Repository Structure

```
ckd-data-preprocessing-project/
│
├── data/
│   ├── kidney_disease.csv            # The original, raw dataset
│   └── kidney_disease_preprocessed.csv # The final, cleaned dataset
│
├──  Chronic_Kidney_disease.ipynb # Jupyter Notebook with step-by-step exploration
│
├── scripts/
│   └── preprocess.py                   # Final Python script to run the full pipeline
│
│
├── README.md                           # Project overview (this file)
│
└── requirements.txt                    # Required Python libraries

```
---

## How to Run

To replicate this project and run the preprocessing pipeline, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[Your-Username]/ckd-data-preprocessing-project.git
    cd ckd-data-preprocessing-project
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the preprocessing script:**
    ```bash
    python scripts/preprocess.py
    ```
    This will execute the full pipeline and generate the `kidney_disease_preprocessed.csv` file in the `data/` folder.

---

## Key Learnings

This project was a practical exercise in applying the core skills required for a data analyst role. Key takeaways include:

* **The Importance of Context:** The decision to handle outliers by capping them or keeping them depends entirely on their meaning in the context of the problem. A statistical outlier is not always a data error.
* **Systematic Workflow:** Following a structured workflow (Clean -> Preprocess -> Scale) is crucial for producing reliable and reproducible results.
* **Data Transformation:** Proficient use of `pandas` for data manipulation and `scikit-learn` for preprocessing are essential tools for preparing any dataset for analysis and machine learning.

