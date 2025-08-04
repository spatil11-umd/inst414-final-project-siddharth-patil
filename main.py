"""
This script runs the full pipeline:
Extract, Transform, Analyze, Evaluate, Visualize

Each step is modularized
"""

import os
import sys

# Importing project modules organized by stage
from etl.extract import select_and_copy_file
from etl.transform import transform_data
from analysis.model import run_analysis
from analysis.evaluate import evaluate_models
from vis.visualizations import visualize_all  # Visualization logic is wrapped in a single function

def rename_extracted_files():
    extracted_dir = os.path.join('data', 'extracted')
    if not os.path.exists(extracted_dir):
        print(f"Directory {extracted_dir} does not exist.")
        return
    
    files = [f for f in os.listdir(extracted_dir) if f.endswith('.csv')]
    if not files:
        print("No CSV files found in data/extracted/")
        return
    
    for i, filename in enumerate(files, start=1):
        new_name = f"data_dictionary_extracted_{i:03}.csv"
        old_path = os.path.join(extracted_dir, filename)
        new_path = os.path.join(extracted_dir, new_name)
        
        if os.path.exists(new_path):
            print(f"Skipping rename for {filename} because {new_name} already exists.")
            continue
        
        os.rename(old_path, new_path)
        print(f"Renamed '{filename}' to '{new_name}'")

"""
def main():
    print("\n=== Step 1: Extract ===")
    # Copy the selected raw data file into the working directory
    select_and_copy_file()

    print("\nRenaming extracted files to data dictionary format...")
    rename_extracted_files()
    
    print("\n=== Step 2: Transform ===")
    # Clean and prepare the dataset for analysis
    df_transformed = transform_data()
    if df_transformed is None:
        print("Transformation failed or returned no data. Exiting.")
        sys.exit(1)
    
    print("\n=== Step 3: Analyze ===")
    # Apply clustering and regression models to the data
    df_analyzed = run_analysis()
    if df_analyzed is None:
        print("Analysis failed. Exiting.")
        sys.exit(1)
    
    print("\n=== Step 4: Evaluate ===")
    # Generate evaluation metrics for model performance
    evaluate_models()
    
    print("\n=== Step 5: Visualize ===")
    # Produce visualizations based on analysis results
    visualize_all()

    print("\nPipeline complete!")

if __name__ == "__main__":
    main()
"""

rename_extracted_files()