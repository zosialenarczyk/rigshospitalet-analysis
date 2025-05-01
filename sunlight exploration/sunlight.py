import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import glob
import os

from scipy.stats import zscore

# === Load disease data ===
def load_disease_data(filepath):
    df = pd.read_csv(filepath, low_memory=False)
    df.columns = df.columns.str.strip()

    diagnosis_col = 'Aktionsdiagnosekode'

    df['Kontakt startdato'] = df['Kontakt startdato'].astype(str).str.replace(',', '.', regex=False)
    df['Kontakt startdato'] = pd.to_datetime(df['Kontakt startdato'], errors='coerce')
    df.set_index('Kontakt startdato', inplace=True)

    df = df[[diagnosis_col]].dropna()
    df['count'] = 1
    disease_df = df.groupby([df.index.date, df[diagnosis_col]]).count().rename(columns={'count': 'cases'})
    disease_df.index = pd.MultiIndex.from_tuples([(pd.to_datetime(d), diag) for d, diag in disease_df.index], names=['date', 'diagnosis'])
    df_pivot = disease_df.reset_index().pivot(index='date', columns='diagnosis', values='cases')

    all_days = pd.date_range(df_pivot.index.min(), df_pivot.index.max(), freq='D')
    df_pivot = df_pivot.reindex(all_days)
    df_pivot = df_pivot.interpolate(method='linear', limit_direction='both')

    df_smoothed = df_pivot.rolling(window=5, center=True, min_periods=1).mean()
    return df_smoothed

# === Sunlight processing ===
def extract_copenhagen_region(ds):
    return ds.sel(
        latitude=slice(56.2, 55.5),
        longitude=slice(11.8, 13.0)
    )

def process_nc_file(filepath):
    ds = xr.open_dataset(filepath)
    ds_cph = extract_copenhagen_region(ds)
    ssrd = ds_cph['ssrd']
    ssrd_hourly_avg = ssrd.mean(dim=['latitude', 'longitude']).sortby('time')
    ssrd_daily = ssrd_hourly_avg.resample(time='1D').sum()
    df = ssrd_daily.to_dataframe().reset_index()
    df.columns = ['date', 'solar_radiation']
    df['date'] = df['date'].dt.date
    df.set_index('date', inplace=True)
    df = df.rolling(window=5, center=True, min_periods=1).mean()
    return df

def load_combined_sunlight_data(folder):
    files = glob.glob(os.path.join(folder, "*.nc"))
    all_dfs = []
    for file in files:
        try:
            df = process_nc_file(file)
            all_dfs.append(df)
        except Exception as e:
            print(f"Skipping {file}: {e}")
    return pd.concat(all_dfs).sort_index()

# === Visualization ===
def plot_disease_overlay(sunlight_df, disease_df, title):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Solar Radiation (W/m²)", color='tab:blue')
    ax1.plot(sunlight_df.index, sunlight_df['solar_radiation'], color='tab:blue', label='Solar Radiation', linewidth=2.5, alpha=0.8)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel("Number of Diagnoses", color='tab:red')

    total_counts = disease_df.sum()
    filtered_disease_df = disease_df.loc[:, total_counts[total_counts >= 10].index]

    correlations = filtered_disease_df.corrwith(sunlight_df['solar_radiation'])
    top_diagnoses = correlations.nsmallest(10).index

    for col in top_diagnoses:
        ax2.plot(filtered_disease_df.index, filtered_disease_df[col], label=col, linewidth=1.8, alpha=0.9)

    ax2.tick_params(axis='y')
    ax2.legend(loc='upper left', bbox_to_anchor=(1.01, 1))

    plt.title(title)
    fig.tight_layout()
    plt.show()

# === Main Runner ===
def main():
    disease_filepath = "/Users/jam/Downloads/Analytics to Action/Case_Rigshospitalet.csv"
    sunlight_folder = "/Users/jam/Downloads/Analytics to Action/sunlight exploration/new"

    disease_df = load_disease_data(disease_filepath)
    sunlight_df = load_combined_sunlight_data(sunlight_folder)

    merged_df = pd.merge(sunlight_df, disease_df, left_index=True, right_index=True, how='inner')

    for (year, month), group in merged_df.groupby([merged_df.index.year, merged_df.index.month]):
        month_name = pd.Timestamp(year=year, month=month, day=1).strftime('%B %Y')
        print(f"\n📅 Plotting disease overlay for {month_name}")
        plot_disease_overlay(group[['solar_radiation']], group.drop(columns='solar_radiation'), f"Solar Radiation vs Diagnoses – {month_name}")

if __name__ == '__main__':
    main()
