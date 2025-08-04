"""
transform.py

This module handles data transformation and cleaning on raw CSV files
extracted into the 'data/extracted' folder.

"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def transform_data():
    # List CSV files in the extracted data folder
    extracted_folder = os.path.join('data', 'extracted')
    files = [f for f in os.listdir(extracted_folder) if f.endswith('.csv')]
    
    if not files:
        print("No CSV files found in data/extracted/. Please run extract first.")
        return
    
    # Prompt user to select a file for transformation
    print("Available files to transform:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    
    choice = input(f"Select a file number (1-{len(files)}): ")
    try:
        idx = int(choice) - 1
        filename = files[idx]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        return
    
    raw_path = os.path.join(extracted_folder, filename)
    df = pd.read_csv(raw_path)

    # Display basic dataset info
    print("\n--- Dataset Inspection ---")
    print(f"File: {filename}")
    print(f"Shape: {df.shape}")
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    missing_df = pd.DataFrame({'MissingCount': missing, 'MissingPercent': missing_percent})
    print(missing_df)
    print("\nDuplicate rows count:")
    print(df.duplicated().sum())
    
    # Save missing values summary for review
    missing_df.to_csv('data/processed/missing_values_summary.csv')
    print("Saved missing values summary to data/processed/missing_values_summary.csv")

    # Remove duplicates
    df = df.drop_duplicates()

    # Drop rows with missing values (customize if needed)
    df = df.dropna()

    # Clean string columns by stripping whitespace
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # Convert specific columns to categorical dtype if present
    categorical_cols = ['Nation', 'Region', 'Division', 'State']  # expand list as needed
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')

    # Rename columns for clarity and consistency
    rename_map = {
        'NAICS2_Name': 'Industry_Sector',
        'TOTAL10': 'Total_Employees',
        # add more renames here as needed
    }
    df = df.rename(columns=rename_map)

    # Create new percentage variable for White employees if data present
    if 'WHT10' in df.columns and 'TOTAL10' in df.columns:
        df['Pct_White'] = df['WHT10'] / df['TOTAL10'] * 100

    # Display and save summary statistics for numeric columns
    print("\nSummary statistics for numeric columns:")
    num_summary = df.describe()
    print(num_summary)
    num_summary.to_csv('data/processed/numeric_summary_stats.csv')
    print("Saved numeric summary statistics to data/processed/numeric_summary_stats.csv")

    # Output value counts for categorical columns and save to CSV
    print("\nValue counts for categorical columns:")
    for col in categorical_cols:
        if col in df.columns:
            print(f"\nColumn: {col}")
            counts = df[col].value_counts()
            print(counts.head(10))  # show top 10
            counts.to_csv(f'data/processed/value_counts_{col}.csv')
            print(f"Saved value counts for {col} to data/processed/value_counts_{col}.csv")

    # Generate histograms for numeric columns and save plots
    numeric_cols = df.select_dtypes(include='number').columns
    hist_folder = 'data/processed/histograms'
    os.makedirs(hist_folder, exist_ok=True)
    for col in numeric_cols:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], kde=False, bins=30)
        plt.title(f'Histogram of {col}')
        plt.tight_layout()
        plt.savefig(os.path.join(hist_folder, f'hist_{col}.png'))
        plt.close()
    print(f"Saved histograms for numeric columns to {hist_folder}/")

    # Save the cleaned and transformed data for downstream use
    processed_path = os.path.join('data', 'processed', f'transformed_{filename}')
    df.to_csv(processed_path, index=False)
    print(f"Cleaned data saved to {processed_path}")

    return df

if __name__ == "__main__":
    transform_data()
