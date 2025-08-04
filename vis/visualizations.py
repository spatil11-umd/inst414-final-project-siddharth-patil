"""
visualize_all.py

This script generates visualizations based on pre-computed analysis files. The figures include:
1. A scatter plot of employer clusters colored by demographic composition.
2. A bar chart comparing the average percentage of White employees across U.S. regions.
3. A bar chart showing mean demographic percentages with standard deviations.

Input files are expected to be located in the /data/analysis/ directory:
- clustered_employers.csv
- comparative_region.csv
- descriptive_stats.csv

"""




import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def visualize_all():
    # Ensure consistent styling
    sns.set(style="whitegrid")

    # Paths
    analysis_path = os.path.join("data", "analysis")
    output_path = os.path.join("data", "outputs")
    os.makedirs(output_path, exist_ok=True)

    # Visualization 1: Clustered Employers
    cluster_file = os.path.join(analysis_path, "clustered_employers.csv")
    if os.path.exists(cluster_file):
        df_cluster = pd.read_csv(cluster_file)
        plt.figure(figsize=(10, 6))
        # Use two demographic columns for x and y
        sns.scatterplot(
            data=df_cluster,
            x="Pct_White",
            y="Pct_Black",
            hue="Cluster",
            palette="tab10"
        )
        plt.title("Employer Clusters (White vs Black %)")
        plt.xlabel("Percent White Employees")
        plt.ylabel("Percent Black Employees")
        plt.legend(title="Cluster")
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, "clustered_employers_plot.png"))
        plt.close()
    else:
        print("clustered_employers.csv not found")

    # You can keep your other visualizations unchanged


    # Visualization 2: Comparative Region Analysis
    region_file = os.path.join(analysis_path, "comparative_region.csv")
    if os.path.exists(region_file):
        df_region = pd.read_csv(region_file)
        print("Columns in comparative_region.csv:", df_region.columns.tolist())  # Optional debug print

        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_region, x="Region", y="Pct_White", palette="pastel")
        plt.title("Mean % White Employees by Region")
        plt.xticks(rotation=45)
        plt.ylabel("Percent White")
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, "comparative_region_plot.png"))
        plt.close()
    else:
        print("comparative_region.csv not found")


    # Visualization 3: Descriptive Stats
    desc_file = os.path.join(analysis_path, "descriptive_stats.csv")
    if os.path.exists(desc_file):
        df_desc = pd.read_csv(desc_file, index_col=0)
        
        # Extract means and std deviations
        means = df_desc['mean']
        stds = df_desc['std']
        
        plt.figure(figsize=(8, 6))
        plt.bar(means.index, means, yerr=stds, capsize=5, color='skyblue')
        plt.ylabel('Percentage (%)')
        plt.title('Mean Demographic Percentages with Standard Deviation')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_path, "descriptive_stats_barplot.png"))
        plt.close()
    else:
        print("descriptive_stats.csv not found")
    