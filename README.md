# =============================================================================
# Project Title: Racial Composition Cluster Analysis
# Siddharth Patil
# 8/13/2025
# =============================================================================

# =============================================================================
# Project Overview
# =============================================================================
# This project explores racial composition across U.S. regions by performing a cluster analysis based on the percentage of different racial groups (White, Black, Hispanic, Asian). The goal is to uncover underlying groupings in the data and compare them with regional averages to derive sociological and geographic insights.
#
# Part 3 Updates:
# - Automatic file selection: The pipeline now automatically selects the first transformed CSV in `data/processed`.
# - Logging: Added `pipeline.log` to track pipeline execution and errors across Extract, Transform, Analyze, Evaluate, and Visualize stages.
# - Evaluation Metrics: Added `data/evaluation/` folder to save model evaluation outputs, including silhouette score for clustering and R² for regression.
#
# Datasets Used:
# - data/processed/transformed_eeoc_data.csv
# - data/analysis/clustered_employers.csv
# - data/analysis/comparative_region.csv
# - data/evaluation/silhouette_score.txt
# - data/evaluation/regression_score.txt

# Techniques Employed:
# - KMeans Clustering
# - Linear Regression
# - Exploratory Data Analysis (EDA)
# - Comparative bar chart visualizations
# - Pipeline logging and error handling

# Expected Outputs:
# - Cluster groupings for racial demographic data
# - Comparative analysis of clusters and U.S. regional demographics
# - Evaluation metrics for clustering and regression

# =============================================================================
# Setup Instructions
# =============================================================================
# 1. Clone the repository:
#    git clone <your-github-repo-url>
#
# 2. Navigate to the project directory:
#    cd your-project-name
#
# 3. Create a virtual environment:
#    python -m venv venv
#
# 4. Activate the virtual environment:
#    - On Windows:
#        venv\Scripts\activate
#    - On Mac/Linux:
#        source venv/bin/activate
#
# 5. Install required dependencies:
#    pip install -r requirements.txt

# =============================================================================
# Running the Project
# =============================================================================
# To run the full pipeline with logging and evaluation metrics:
# python main.py
#
# To run the clustering and comparison visualizations separately:
# python code/cluster_and_compare.py
#
# To open the full EDA notebook:
# notebooks/eda_clusters.ipynb
#
# Reference tables and data dictionaries are stored in:
# data/reference-tables/

# =============================================================================
# Code Package Structure
# =============================================================================
# ├── code/
# │   ├── cluster_and_compare.py     
# │   └── __init__.py               
# ├── data/
# │   ├── processed/
# │   │   └── transformed_eeoc_data.csv
# │   ├── analysis/
# │   │   ├── clustered_employers.csv     
# │   │   └── comparative_region.csv    
# │   ├── evaluation/
# │   │   ├── silhouette_score.txt
# │   │   └── regression_score.txt
# │   └── reference-tables/
# │       ├── data_dictionary_clustered_employers.csv
# │       └── data_dictionary_comparative_region.csv
# ├── notebooks/
# │   └── eda_clusters.ipynb         
# ├── requirements.txt              
# └── README.md                      
