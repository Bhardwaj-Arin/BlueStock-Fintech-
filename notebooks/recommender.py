import pandas as pd
import numpy as np

def run_recommender():
    print("==================================================")
    print("   BLUESTOCK FINTECH - MUTUAL FUND RECOMMENDER    ")
    print("==================================================")

    perf_path = 'data-processed/cleaned_scheme_performance.csv'
    nav_path = 'data-processed/cleaned_nav_history.csv'

    try:
        df_scheme = pd.read_csv(perf_path)
        df_nav = pd.read_csv(nav_path)
    except Exception as e:
        print(f"Error loading system metrics: {e}")
        return

    # Dynamically find the correct risk column name (handles 'risk_grade' or 'risk_category')
    risk_col = 'risk_grade' if 'risk_grade' in df_scheme.columns else 'risk_category'
    if risk_col not in df_scheme.columns:
        # Fallback if it's named something else entirely
        risk_col = [c for c in df_scheme.columns if 'risk' in c or 'grade' in c][0]

    # Calculate global Sharpe Ratios for ranking metrics
    df_raw = pd.merge(df_nav, df_scheme[['amfi_code', 'scheme_name', risk_col]], on='amfi_code', how='inner')
    df_raw['daily_return'] = df_raw.groupby('scheme_name')['nav'].pct_change()

    metrics = df_raw.groupby(['scheme_name', risk_col])['daily_return'].agg(['mean', 'std']).reset_index()
    metrics['sharpe_ratio'] = (metrics['mean'] / metrics['std']) * np.sqrt(252)
    metrics = metrics.dropna().sort_values(by='sharpe_ratio', ascending=False)

    user_input = input("\nEnter your risk appetite (Low / Moderate / High): ").strip().lower()

    # Map inputs to standard risk labels found in datasets
    if user_input == 'low':
        target_categories = ['Low', 'Low to Moderate', 'Moderate']
    elif user_input == 'moderate':
        target_categories = ['Moderate', 'Moderately High', 'Medium', 'High']
    elif user_input == 'high':
        target_categories = ['High', 'Very High']
    else:
        print("Invalid option. Defaulting to 'Moderate' risk mapping profile.")
        target_categories = ['Moderate', 'Moderately High', 'Medium']

    recommendations = metrics[metrics[risk_col].isin(target_categories)].head(3)

    print(f"\nTop 3 Recommended Funds for a '{user_input.upper()}' Risk Appetite Profile:")
    print("--------------------------------------------------------------------------------")
    print(recommendations[['scheme_name', risk_col, 'sharpe_ratio']].to_string(index=False))
    print("--------------------------------------------------------------------------------")

if __name__ == "__main__":
    run_recommender()
