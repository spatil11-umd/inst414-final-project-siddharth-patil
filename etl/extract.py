"""

This script prompts the user to select a CSV file using a GUI file picker (via Tkinter),
then copies the selected file into the 'data/extracted' directory while preserving the original filename.

This is used to streamline the import of raw EEOC CSV datasets into the project structure. Designed as a simple intake step in the EEOC workforce diversity data pipeline.
"""

import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def select_and_copy_file():
    # Suppress the root Tkinter window
    Tk().withdraw()

    # Prompt the user to select a CSV file
    print("Please select the CSV file to extract...")
    file_path = askopenfilename(
        title="Select the EEOC CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    # If no file was selected, exit early
    if not file_path:
        print("No file selected. Exiting.")
        return

    # Ensure the destination folder exists
    os.makedirs('data/extracted', exist_ok=True)

    # Get just the filename from the full path
    filename = os.path.basename(file_path)

    # Define the destination path
    dest_path = os.path.join('data', 'extracted', filename)

    # Copy the file to the destination
    shutil.copy(file_path, dest_path)

    # Confirm successful copy
    print(f"File copied to {dest_path}")

def main():
    select_and_copy_file()

if __name__ == "__main__":
    main()
