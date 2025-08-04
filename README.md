# =============================================================================
# Project Title: Racial Composition Cluster Analysis
# Siddharth Patil
# 8/3/2025
# =============================================================================

# =============================================================================
# Project Overview
# =============================================================================
# This project explores racial composition across U.S. regions by performing a cluster analysis based on the percentage of different racial groups (White, Black, Hispanic, Asian). The goal is to uncover underlying groupings in the data and compare them with regional averages to derive sociological and geographic insights.

# Datasets Used:
# - data/analysis/clustered_race_data.csv
# - data/analysis/comparative_region.csv

# Techniques Employed:
# - KMeans Clustering
# - Exploratory Data Analysis (EDA)
# - Comparative bar chart visualizations

# Expected Outputs:
# - Cluster groupings for racial demographic data
# - Comparison of clusters to U.S. regional race demographics

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
# To run the clustering and comparison visualizations:
# python code/cluster_and_compare.py

# To run the full EDA notebook, open:
# notebooks/eda_clusters.ipynb

# To generate reference tables or update data dictionaries, refer to:
# data/reference-tables/ and data/reference-tables/data_dictionary_[dataset name].csv

# =============================================================================
# Code Package Structure
# =============================================================================
# ├── code/
# │   ├── cluster_and_compare.py     
# │   └── __init__.py               
# ├── data/
# │   ├── analysis/
# │   │   ├── clustered_race_data.csv     
# │   │   └── comparative_region.csv    
# │   └── reference-tables/
# │       ├── data_dictionary_clustered_race_data.csv
# │       └── data_dictionary_comparative_region.csv
# ├── notebooks/
# │   └── eda_clusters.ipynb         
# ├── requirements.txt              
# └── README.md                      

