"""

This module evaluates the performance of clustering and regression models
produced during the analysis phase.

evaluate.py

"""

import os
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

def evaluate_models():
    # Define path to analysis output folder
    analysis_folder = os.path.join('data', 'analysis')

    # Evaluate clustering performance if clustered data file exists
    clustered_file = os.path.join(analysis_folder, 'clustered_employers.csv')
    if os.path.exists(clustered_file):
        df = pd.read_csv(clustered_file)
        features = ['Pct_White', 'Pct_Black', 'Pct_Hispanic', 'Pct_Asian']
        X = df[features]

        kmeans = KMeans(n_clusters=3, random_state=42)
        labels = df['Cluster']
        score = silhouette_score(X, labels)
        print(f"Silhouette Score for KMeans clustering: {score:.3f}")

        # Save silhouette score to file
        with open(os.path.join(analysis_folder, 'cluster_evaluation.txt'), 'w') as f:
            f.write(f"Silhouette Score: {score:.3f}\n")
    else:
        print("Clustered data not found, run model.py first.")

    # Print regression evaluation if available
    reg_score_file = os.path.join(analysis_folder, 'regression_score.txt')
    if os.path.exists(reg_score_file):
        with open(reg_score_file, 'r') as f:
            reg_score = f.read()
        print("Regression evaluation:\n", reg_score)
    else:
        print("Regression results not found, run model.py first.")

if __name__ == "__main__":
    evaluate_models()