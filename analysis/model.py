"""
THis module performs analysis on processed datasets saved in 'data/processed'.

"""

import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def run_analysis():
    # Setup paths for processed data and analysis outputs
    processed_folder = os.path.join('data', 'processed')
    analysis_folder = os.path.join('data', 'analysis')
    os.makedirs(analysis_folder, exist_ok=True)

    # List all CSV files in processed folder for user to choose from
    files = [f for f in os.listdir(processed_folder) if f.endswith('.csv')]
    if not files:
        print("No processed data found. Run ETL first.")
        return
    print("Available processed files:")
    for i, f in enumerate(files):
        print(f"{i+1}. {f}")
    choice = input(f"Select a file to analyze (1-{len(files)}): ")
    try:
        idx = int(choice) - 1
        filename = files[idx]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting.")
        return

    data_path = os.path.join(processed_folder, filename)
    df = pd.read_csv(data_path)

    # Identify the total employees column for percentage calculations
    total_col = None
    for col_candidate in ['Total_Employees', 'TOTAL10', 'TOTAL1']:
        if col_candidate in df.columns:
            total_col = col_candidate
            break
    if total_col is None:
        print("No total employees column found for percentage calculations.")
        return

    # Define demographic count columns for calculating percentages
    demo_cols = {
        'Pct_White': 'WHT10',
        'Pct_Black': 'BLKT10',
        'Pct_Hispanic': 'HISPT10',
        'Pct_Asian': 'ASIANT10',
        # Add more demographics if needed
    }

    # Convert relevant columns to numeric and calculate percentages
    df[total_col] = pd.to_numeric(df[total_col], errors='coerce')
    for pct_col, count_col in demo_cols.items():
        if count_col in df.columns:
            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df[pct_col] = df[count_col] / df[total_col] * 100
        else:
            df[pct_col] = None

    # Filter out rows missing any demographic percentage
    pct_cols = list(demo_cols.keys())
    df_clean = df.dropna(subset=pct_cols)

    if df_clean.empty:
        print("No rows with complete demographic percentages found.")
        return

    # Descriptive statistics for demographic percentages
    print("Descriptive stats for demographic percentages:")
    print(df_clean[pct_cols].describe())

    desc_stats = df_clean[pct_cols].describe().transpose()
    desc_stats.to_csv(os.path.join(analysis_folder, 'descriptive_stats.csv'))

    # Comparative analysis by Region for percent white employees
    if 'Region' in df_clean.columns and 'Pct_White' in df_clean.columns:
        comp_region = df_clean.groupby('Region')['Pct_White'].mean().reset_index()
        comp_region.to_csv(os.path.join(analysis_folder, 'comparative_region.csv'), index=False)
        print("Comparative analysis by Region saved.")

    # KMeans clustering on demographic percentages
    features = pct_cols
    X = df_clean[features]

    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    df_clean['Cluster'] = kmeans.fit_predict(X)

    df_clean[['Cluster'] + features].to_csv(os.path.join(analysis_folder, 'clustered_employers.csv'), index=False)
    print("KMeans clustering done and saved.")

    # Optional: Linear regression predicting percent white by Region
    if 'Region' in df_clean.columns and 'Pct_White' in df_clean.columns:
        df_reg = df_clean.dropna(subset=['Region', 'Pct_White'])
        X_reg = pd.get_dummies(df_reg['Region'], drop_first=True)
        y_reg = df_reg['Pct_White']

        X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)

        print(f"Linear regression R^2 score predicting Pct_White from Region: {score:.3f}")
        with open(os.path.join(analysis_folder, 'regression_score.txt'), 'w') as f:
            f.write(f"R^2 score: {score:.3f}\n")

    return df_clean

if __name__ == "__main__":
    run_analysis()
