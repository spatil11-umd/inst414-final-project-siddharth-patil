"""

This script prompts the user to select a CSV file using a GUI file picker (via Tkinter),
then copies the selected file into the 'data/extracted' directory while preserving the original filename.

This is used to streamline the import of raw EEOC CSV datasets into the project structure. Designed as a simple intake step in the EEOC workforce diversity data pipeline.

extract.py

"""

import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import os

def extract_eeoc_data():
    """
    Extracts the EEOC dataset from the /data folder and copies it to /data/extracted.
    Returns:
        DataFrame: Raw EEOC data for further processing.
    """
    source_path = os.path.join("data", "EEO1_2023_PUF.csv")
    extracted_dir = os.path.join("data", "extracted")
    extracted_path = os.path.join(extracted_dir, "eeoc_data.csv")

    # Check if source file exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source dataset not found at {source_path}")

    # Ensure extracted folder exists
    os.makedirs(extracted_dir, exist_ok=True)

    # Copy and rename
    shutil.copy(source_path, extracted_path)
    print(f"Copied dataset from {source_path} to {extracted_path}")

    # Load CSV into DataFrame
    df = pd.read_csv(extracted_path)
    print(f"Extraction complete. Loaded {len(df)} rows.")
    return df

if __name__ == "__main__":
    df = extract_eeoc_data()