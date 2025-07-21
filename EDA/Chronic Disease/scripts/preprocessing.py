# =============================================================================
# PREPROCESSING SCRIPT FOR CHRONIC KIDNEY DISEASE (CKD) DATASET
#
# Author: [Your Name]
# Date: July 22, 2025
#
# Description:
# This script takes the raw 'kidney_disease.csv' dataset and performs a
# full cleaning and preprocessing pipeline. The steps include:
# 1.  Dropping irrelevant columns.
# 2.  Correcting data types and cleaning erroneous characters.
# 3.  Standardizing categorical values.
# 4.  Imputing missing values using appropriate strategies (median/mode).
# 5.  Handling outliers using the capping method (IQR).
# 6.  Encoding all categorical features into a numerical format.
# 7.  Applying feature scaling (Standardization) to all independent features.
#
# The final output is a clean, model-ready dataset saved as
# 'kidney_disease_preprocessed.csv'.
# =============================================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings

# Suppress warnings for a cleaner output
warnings.filterwarnings('ignore')

def preprocess_ckd_data(input_filepath, output_filepath):
    """
    Loads, cleans, preprocesses the CKD dataset and saves the result.

    Args:
        input_filepath (str): The path to the raw CSV file.
        output_filepath (str): The path to save the preprocessed CSV file.
    """
    print("--- Starting Data Preprocessing Pipeline ---")

    # 1. Load the raw dataset
    try:
        df = pd.read_csv(input_filepath)
        print("1. Dataset loaded successfully.")
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_filepath}'")
        return

    # 2. Drop the 'id' column as it is irrelevant
    df.drop('id', axis=1, inplace=True)

    # 3. Correct data types and clean erroneous characters in specific numeric columns
    dirty_numeric_cols = ['pcv', 'wc', 'rc']
    for col in dirty_numeric_cols:
        df[col] = pd.to_numeric(df[col].str.extract('(\d+\.?\d*)', expand=False), errors='coerce')
    print("2. Corrected data types for 'pcv', 'wc', 'rc'.")

    # 4. Standardize categorical values (strip whitespace and fix known typos)
    # This loop handles all text-based columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
        df[col] = df[col].replace({
            r'\tno': 'no', r'\tyes': 'yes', r' yes': 'yes',
            r'ckd\t': 'ckd', r'\t?': np.nan
        }, regex=True)
    print("3. Standardized categorical text values.")

    # 5. Impute (Fill) Missing Values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)
    print("4. Imputed all missing values using median/mode.")

    # 6. Handle Outliers by Capping (based on our EDA)
    cols_to_cap = ['bp', 'sod', 'pot', 'wc', 'rc']
    for col in cols_to_cap:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_fence = Q1 - 1.5 * IQR
        upper_fence = Q3 + 1.5 * IQR
        df[col] = np.clip(df[col], lower_fence, upper_fence)
    print("5. Handled outliers using capping for specific columns.")

    # 7. Encode all categorical features into numerical format
    categorical_cols = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane', 'classification']
    mapping_dict = {
        'normal': 1, 'abnormal': 0, 'present': 1, 'notpresent': 0,
        'yes': 1, 'no': 0, 'good': 1, 'poor': 0, 'ckd': 1, 'notckd': 0
    }
    for col in categorical_cols:
        df[col] = df[col].map(mapping_dict)
    print("6. Encoded all categorical features to numerical format.")

    # 8. Feature Scaling
    X = df.drop('classification', axis=1)
    y = df['classification']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    print("7. Applied feature scaling (Standardization).")

    # 9. Combine scaled features and target into a final DataFrame
    final_df = pd.concat([X_scaled_df, y.reset_index(drop=True)], axis=1)

    # 10. Save the final preprocessed data
    try:
        final_df.to_csv(output_filepath, index=False)
        print(f"\n--- Pipeline Complete! ---")
        print(f"Preprocessed data saved successfully to '{output_filepath}'")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == '__main__':
    # Define the input and output file paths
    # Assumes the script is in a 'scripts' folder and data is in a 'data' folder
    # at the same level as 'scripts'.
    INPUT_FILE = '../data/kidney_disease.csv'
    OUTPUT_FILE = '../data/kidney_disease_preprocessed.csv'
    
    preprocess_ckd_data(INPUT_FILE, OUTPUT_FILE)
