"""
This module performs analysis on processed datasets saved in 'data/processed'.
Enhances insights for DEI initiatives by producing business-focused metrics and summaries.

model.py
"""

import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def run_analysis():
    # Setup paths for processed data and analysis outputs
    processed_folder = os.path.join('data', 'processed')
    analysis_folder = os.path.join('data', 'analysis')
    eval_folder = os.path.join('data', 'evaluation')
    os.makedirs(analysis_folder, exist_ok=True)
    os.makedirs(eval_folder, exist_ok=True)

    # Automatically select the first transformed CSV file
    files = [f for f in os.listdir(processed_folder) 
             if f.startswith("transformed_") and f.endswith(".csv")]
    if not files:
        print("No transformed CSV file found. Run transform first.")
        return

    filename = files[0]
    data_path = os.path.join(processed_folder, filename)
    print(f"Automatically selected {filename} for analysis.")

    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    # Identify the total employees column for percentage calculations
    total_col = next((c for c in ['Total_Employees', 'TOTAL10', 'TOTAL1'] if c in df.columns), None)
    if total_col is None:
        print("No total employees column found for percentage calculations.")
        return

    # Demographic count columns
    demo_cols = {
        'Pct_White': 'WHT10',
        'Pct_Black': 'BLKT10',
        'Pct_Hispanic': 'HISPT10',
        'Pct_Asian': 'ASIANT10',
    }

    # Calculate percentages
    df[total_col] = pd.to_numeric(df[total_col], errors='coerce')
    for pct_col, count_col in demo_cols.items():
        if count_col in df.columns:
            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df[pct_col] = df[count_col] / df[total_col] * 100
        else:
            df[pct_col] = None

    pct_cols = list(demo_cols.keys())
    df_clean = df.dropna(subset=pct_cols)
    if df_clean.empty:
        print("No rows with complete demographic percentages found.")
        return

    # Additional DEI metrics
    df_clean['Pct_Minority'] = 100 - df_clean['Pct_White']
    df_clean['Diversity_Index'] = df_clean[pct_cols].apply(lambda row: 1 - sum((row/100)**2), axis=1)

    # Descriptive stats
    desc_stats = df_clean[pct_cols + ['Pct_Minority','Diversity_Index']].describe().transpose()
    desc_stats.to_csv(os.path.join(analysis_folder, 'descriptive_stats.csv'))

    # Comparative analysis by Region
    if 'Region' in df_clean.columns:
        comp_region = df_clean.groupby('Region')[['Pct_White','Pct_Minority','Diversity_Index']].mean().reset_index()
        comp_region['Diversity_Rank'] = comp_region['Diversity_Index'].rank(ascending=False)
        comp_region.to_csv(os.path.join(analysis_folder, 'comparative_region_ranked.csv'), index=False)
        print("Comparative regional analysis saved with diversity ranking.")

    # KMeans clustering on demographic percentages
    try:
        X = df_clean[pct_cols]
        kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
        df_clean['Cluster'] = kmeans.fit_predict(X)

        cluster_summary = df_clean.groupby('Cluster')[pct_cols + ['Pct_Minority','Diversity_Index']].mean().round(1)
        cluster_summary.to_csv(os.path.join(analysis_folder,'cluster_summary.csv'))

        df_clean[['Cluster'] + pct_cols].to_csv(os.path.join(analysis_folder, 'clustered_employers.csv'), index=False)
        sil_score = silhouette_score(X, df_clean['Cluster'])
        with open(os.path.join(eval_folder, 'silhouette_score.txt'), 'w') as f:
            f.write(f"Silhouette Score: {sil_score:.3f}\n")
        print(f"KMeans clustering and evaluation saved. Silhouette: {sil_score:.3f}")
    except Exception as e:
        print(f"KMeans clustering failed: {e}")

    # Regression predicting percent white by Region + Industry
    if 'Region' in df_clean.columns:
        try:
            features_reg = ['Region']
            if 'Industry_Sector' in df_clean.columns:
                features_reg.append('Industry_Sector')
            df_reg = df_clean.dropna(subset=features_reg + ['Pct_White'])
            X_reg = pd.get_dummies(df_reg[features_reg], drop_first=True)
            y_reg = df_reg['Pct_White']

            X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            r2_score = model.score(X_test, y_test)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)

            df_reg['Predicted_Pct_White'] = model.predict(X_reg)
            df_reg.to_csv(os.path.join(analysis_folder,'predicted_diversity.csv'), index=False)

            with open(os.path.join(eval_folder,'regression_score.txt'),'w') as f:
                f.write(f"R^2 score: {r2_score:.3f}\nMSE: {mse:.3f}\n")

            print(f"Regression evaluation saved. R^2: {r2_score:.3f}, MSE: {mse:.3f}")
        except Exception as e:
            print(f"Regression failed: {e}")

    # Generate HR-friendly insights summary
    with open(os.path.join(analysis_folder,'insights.txt'),'w') as f:
        f.write("Key DEI Insights:\n")
        f.write(f"- Average % White: {df_clean['Pct_White'].mean():.1f}%\n")
        f.write(f"- Average % Minority: {df_clean['Pct_Minority'].mean():.1f}%\n")
        f.write(f"- Average Diversity Index: {df_clean['Diversity_Index'].mean():.2f}\n")
        f.write("- Cluster profiles saved in 'cluster_summary.csv'\n")
        if 'Region' in df_clean.columns:
            f.write("- Region diversity ranking saved in 'comparative_region_ranked.csv'\n")
        f.write("- Predicted vs actual diversity saved in 'predicted_diversity.csv'\n")
    print("HR-friendly insights report saved as 'insights.txt'")

    return df_clean

if __name__ == "__main__":
    run_analysis()
