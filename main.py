"""
Full Pipeline Script: Extract, Transform, Analyze, Evaluate, Visualize

This script orchestrates the end-to-end data science pipeline for the EEOC dataset. 
Each stage is modularized into separate functions or modules:

- Extraction: Loads raw EEOC CSV files from `data/extracted/`.
- Transformation: Cleans and reshapes data into a consistent format.
- Analysis: Performs clustering and regression on demographic data.
- Evaluation: Computes model evaluation metrics and saves results.
- Visualization: Generates visualizations for analysis results.

Logging and error handling are included to improve robustness and traceability.
"""

import os
import sys
import logging
import csv

# Importing project modules organized by stage
from etl.extract import extract_eeoc_data
from etl.transform import transform_data
from analysis.model import run_analysis
from analysis.evaluate import evaluate_models
from vis.visualizations import visualize_all  # Visualization logic is wrapped in a single function


def save_data_dictionary(df, filename='data_dictionary_analyzed.csv'):
    """
    Generate a data dictionary CSV for a DataFrame.

    Columns in the CSV:
    - Column Name
    - Data Type
    - Description
    """
    ref_folder = os.path.join('data', 'reference-tables')
    os.makedirs(ref_folder, exist_ok=True)
    path = os.path.join(ref_folder, filename)

    # Custom descriptions for Part 3 columns
    part3_desc = {
        'Pct_White': 'Percentage of White employees (WHT10 / Total_Employees * 100)',
        'Pct_Black': 'Percentage of Black employees (BLKT10 / Total_Employees * 100)',
        'Pct_Hispanic': 'Percentage of Hispanic employees (HISPT10 / Total_Employees * 100)',
        'Pct_Asian': 'Percentage of Asian employees (ASIANT10 / Total_Employees * 100)',
        'Cluster': 'KMeans cluster assignment based on demographic percentages'
    }

    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Column Name', 'Data Type', 'Description'])
        for col in df.columns:
            dtype = str(df[col].dtype)
            desc = part3_desc.get(col, f"Auto-generated column for {col}")
            writer.writerow([col, dtype, desc])

    logging.info(f"Data dictionary saved to {path}")


def rename_extracted_files():
    """
    Rename extracted CSV files in `data/extracted/` to a consistent format.

    Each file is renamed to: data_dictionary_extracted_XXX.csv, 
    where XXX is a zero-padded index starting from 001.

    Logs warnings if the directory or CSV files are missing, and info messages
    for successful renames or skipped files.
    """
    extracted_dir = os.path.join('data', 'extracted')
    if not os.path.exists(extracted_dir):
        logging.warning(f"Directory {extracted_dir} does not exist.")
        return
    
    files = [f for f in os.listdir(extracted_dir) if f.endswith('.csv')]
    if not files:
        logging.warning("No CSV files found in data/extracted/")
        return
    
    for i, filename in enumerate(files, start=1):
        new_name = f"data_dictionary_extracted_{i:03}.csv"
        old_path = os.path.join(extracted_dir, filename)
        new_path = os.path.join(extracted_dir, new_name)
        
        if os.path.exists(new_path):
            logging.info(f"Skipping rename for {filename} because {new_name} already exists.")
            continue
        
        os.rename(old_path, new_path)
        logging.info(f"Renamed '{filename}' to '{new_name}'")

def main():
    """
    Main function to run the full EEOC data pipeline.

    Steps:
    1. Extract: Load raw EEOC data.
    2. Transform: Clean and reshape data.
    3. Analyze: Run clustering and regression analysis.
    4. Evaluate: Compute and save model evaluation metrics.
    5. Visualize: Generate visualizations for analysis results.

    Logging:
    - All pipeline stages log info and error messages to `pipeline.log`.
    - Errors at critical stages terminate the pipeline with sys.exit(1).
    """
    # Configure logging
    logging.basicConfig(
        filename='pipeline.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Pipeline started")

    # Step 1: Extract
    logging.info("=== Step 1: Extract ===")
    try:
        df_extracted = extract_eeoc_data()  # automatically grabs EEO1_2023_PUF.csv
        logging.info(f"Extraction completed. {len(df_extracted)} rows loaded.")
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        sys.exit(1)

    # Step 2: Transform
    logging.info("=== Step 2: Transform ===")
    try:
        df_transformed = transform_data()
        if df_transformed is None:
            raise ValueError("Transformation returned no data")
        logging.info(f"Transformation completed. {len(df_transformed)} rows processed.")
    except Exception as e:
        logging.error(f"Transformation failed: {e}")
        sys.exit(1)

    # Step 3: Analyze
    logging.info("=== Step 3: Analyze ===")
    try:
        df_analyzed = run_analysis()
        if df_analyzed is None:
            raise ValueError("Analysis returned no data")
        logging.info("Analysis completed successfully.")
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        sys.exit(1)

    # Step 3b: Save Data Dictionary for Analyzed Data
    try:
        save_data_dictionary(df_analyzed, filename='data_dictionary_analyzed.csv')
    except Exception as e:
        logging.error(f"Saving data dictionary failed: {e}")


    # Step 4: Evaluate
    logging.info("=== Step 4: Evaluate ===")
    try:
        evaluate_models()
        logging.info("Evaluation completed successfully.")
    except Exception as e:
        logging.error(f"Evaluation failed: {e}")

    # Step 5: Visualize
    logging.info("=== Step 5: Visualize ===")
    try:
        visualize_all()
        logging.info("Visualization completed successfully.")
    except Exception as e:
        logging.error(f"Visualization failed: {e}")

    logging.info("Pipeline complete!")

if __name__ == "__main__":
    main()
