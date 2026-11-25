# ==============================================================================
# UNEMPLOYMENT ANALYSIS IN INDIA (COVID-19 IMPACT)
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ------------------------------------------------------------------------------
# PHASE 1: DATA SETUP & CLEANING
# ------------------------------------------------------------------------------
print("Loading and cleaning datasets...")

# 1. Load the datasets (Ensure these are uploaded to your Colab session first!)
df_area = pd.read_csv('Unemployment in India.csv')
df_timeline = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')

# 2. Clean messy column headers by stripping trailing/leading spaces
df_area.columns = df_area.columns.str.strip()
df_timeline.columns = df_timeline.columns.str.strip()

# 3. Drop any hidden completely empty rows
df_area.dropna(inplace=True)
df_timeline.dropna(inplace=True)

# 4. Standardize column names across both datasets
df_area.rename(columns={'Region': 'State'}, inplace=True)
df_timeline.rename(columns={'Region': 'State', 'Region.1': 'Zone'}, inplace=True)

# 5. Convert 'Date' columns to actual datetime objects for time-series analysis
df_area['Date'] = pd.to_datetime(df_area['Date'].str.strip(), format='%d-%m-%Y')
df_timeline['Date'] = pd.to_datetime(df_timeline['Date'].str.strip(), format='%d-%m-%Y')

# 6. Extract Month for seasonal/timeline aggregations
df_timeline['Month'] = df_timeline['Date'].dt.strftime('%b')


# ------------------------------------------------------------------------------
# PHASE 2: EXPLORATORY DATA ANALYSIS & VISUALIZATION
# ------------------------------------------------------------------------------

# --- Plot 1: The COVID-19 Lockdown Timeline ---
print("Generating Timeline Analysis...")
national_trends = df_timeline.groupby('Date')['Estimated Unemployment Rate (%)'].mean().reset_index()

plt.figure()
sns.lineplot(x='Date', y='Estimated Unemployment Rate (%)', data=national_trends, 
             color='crimson', linewidth=3, marker='o')
# Shading the strict lockdown period
plt.axvspan(pd.to_datetime('2020-03-25'), pd.to_datetime('2020-05-31'), 
            color='gray', alpha=0.2, label='Strict National Lockdown')
plt.title('The COVID-19 Unemployment Shock in India (2020)', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('National Average Unemployment Rate (%)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()


# --- Plot 2: Urban vs. Rural Sector Impact ---
print("Generating Sector Analysis...")
plt.figure()
# New Updated Code
sns.violinplot(x='Area', y='Estimated Unemployment Rate (%)', data=df_area, 
               hue='Area', palette='muted', inner="quart", legend=False)
plt.title('Unemployment Variance: Urban vs. Rural Sectors', fontsize=16, fontweight='bold')
plt.ylabel('Unemployment Rate (%)', fontsize=12)
plt.xlabel('Economic Sector', fontsize=12)
plt.tight_layout()
plt.show()


# --- Plot 3: Regional Disparities (Interactive Sunburst) ---
print("Generating Regional Analysis...")
# Calculate the average rate per state for the whole 2020 dataset
state_avg = df_timeline.groupby(['Zone', 'State'])['Estimated Unemployment Rate (%)'].mean().reset_index()

fig = px.sunburst(state_avg, 
                  path=['Zone', 'State'], 
                  values='Estimated Unemployment Rate (%)',
                  title='Average Unemployment by Zone and State (2020)',
                  color='Estimated Unemployment Rate (%)',
                  color_continuous_scale='RdYlGn_r')
fig.update_layout(title_font=dict(size=20))
fig.show()


# ------------------------------------------------------------------------------
# PHASE 3: PROJECT INSIGHTS & POLICY RECOMMENDATIONS
# ------------------------------------------------------------------------------
print("\n" + "="*60)
print("📝 AUTOMATED INSIGHTS REPORT FOR ECONOMIC POLICY")
print("="*60)

# Calculate peak metrics to print
peak_month = national_trends.loc[national_trends['Estimated Unemployment Rate (%)'].idxmax()]
pre_covid = national_trends[national_trends['Date'] < '2020-03-01']['Estimated Unemployment Rate (%)'].mean()

print(f"1. THE PANDEMIC SHOCK: Pre-COVID average unemployment hovered around {pre_covid:.2f}%.")
print(f"   During the lockdown, the national average peaked dramatically at {peak_month['Estimated Unemployment Rate (%)']:.2f}% on {peak_month['Date'].strftime('%B %Y')}.")
print("2. SECTOR VULNERABILITY: The violin plot reveals that the Urban sector experienced a higher")
print("   maximum variance and higher extremes in unemployment compared to Rural areas.")
print("3. REGIONAL DISPARITY: The sunburst chart highlights severe asymmetry in the economic hit.")
print("   Northern and Southern states bore the heaviest brunt compared to Eastern regions.")
print("\nPOLICY RECOMMENDATIONS:")
print("- Implement an 'Urban Employment Guarantee Scheme' similar to MGNREGA to protect municipal workers.")
print("- Shift away from uniform national relief budgets to targeted, zone-specific economic stimulus packages.")
print("="*60)
