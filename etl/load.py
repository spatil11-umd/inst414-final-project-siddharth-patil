"""

This script lists CSV files in the 'data/processed' directory,
prompts the user to select one of the files, and loads the selected
file into a pandas DataFrame for further analysis.

load.py

"""

import os
import pandas as pd

def list_processed_files():
    # List all CSV files in 'data/processed' directory
    processed_dir = os.path.join('data', 'processed')
    files = [f for f in os.listdir(processed_dir) if f.endswith('.csv')]
    return files

def select_file(files):
    # Display available files and prompt user to select one
    print("Available cleaned CSV files in data/processed/:")
    for i, f in enumerate(files):
        print(f"{i + 1}: {f}")
    while True:
        choice = input(f"Select a file to load (1-{len(files)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        else:
            print("Invalid choice. Try again.")

def load_data():
    # List CSV files in processed folder
    processed_dir = os.path.join('data', 'processed')
    files = [f for f in os.listdir(processed_dir) if f.endswith('.csv')]
    
    if not files:
        print("No processed CSV files found in data/processed/. Please run transform first.")
        return None

    # Automatically pick the first file
    filename = files[0]
    print(f"Automatically loading file: {filename}")
    
    file_path = os.path.join(processed_dir, filename)
    df = pd.read_csv(file_path)
    print(f"\nLoaded data from {file_path} - shape: {df.shape}")
    return df


if __name__ == "__main__":
    load_data()
