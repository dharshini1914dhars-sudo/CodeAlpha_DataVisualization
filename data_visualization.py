# ============================================================
# CodeAlpha Internship — Task 3: Data Visualization
# Dataset: COVID-19 Global Data
# Author: [Your Name]
# ============================================================

# Step 1: Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="darkgrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================
# Step 2: Create COVID-19 Dataset
# ============================================================
data = {
    'Country': ['USA', 'India', 'Brazil', 'France', 'Germany',
                'UK', 'Russia', 'South Korea', 'Italy', 'Australia',
                'Japan', 'Canada', 'Spain', 'Mexico', 'Indonesia'],
    'Total_Cases': [103436829, 44690078, 37519960, 38997490, 38249060,
                    24648327, 22072862, 30614833, 25880595, 11348321,
                    33803572, 4649373, 13797053, 7633355, 6812590],
    'Total_Deaths': [1127152, 530779, 702116, 167952, 174979,
                     232112, 385494, 34985, 192101, 19886,
                     74694, 51447, 121754, 334336, 160933],
    'Total_Recovered': [99000000, 44400000, 36700000, 38500000, 37900000,
                        23900000, 21500000, 30400000, 25500000, 11200000,
                        33500000, 4500000, 13600000, 7200000, 6600000],
    'Population_Million': [331, 1380, 213, 67, 83, 67, 144, 52, 60, 25, 126, 38, 47, 129, 273]
}

df = pd.DataFrame(data)

# Calculate additional metrics
df['Death_Rate'] = (df['Total_Deaths'] / df['Total_Cases'] * 100).round(2)
df['Recovery_Rate'] = (df['Total_Recovered'] / df['Total_Cases'] * 100).round(2)
df['Cases_Per_Million'] = (df['Total_Cases'] / df['Population_Million']).round(0)
df['Total_Cases_M'] = (df['Total_Cases'] / 1_000_000).round(2)
df['Total_Deaths_K'] = (df['Total_Deaths'] / 1_000).round(2)

print("=" * 60)
print("COVID-19 GLOBAL DATA - DATA VISUALIZATION")
print("=" * 60)
print(f"\n📌 Countries Analyzed: {len(df)}")
print("\n📌 Dataset Preview:")
print(df[['Country', 'Total_Cases_M', 'Total_Deaths_K', 'Death_Rate', 'Recovery_Rate']].to_string())

# ============================================================
# Step 3: Visualizations
# ============================================================

# Chart 1: Top 10 Countries by Total Cases
plt.figure(figsize=(12, 6))
df_sorted = df.sort_values('Total_Cases', ascending=True)
colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df)))
bars = plt.barh(df_sorted['Country'], df_sorted['Total_Cases_M'], color=colors)
plt.title('COVID-19 Total Cases by Country (in Millions)', fontsize=16, fontweight='bold')
plt.xlabel('Total Cases (Millions)')
plt.ylabel('Country')
for bar, val in zip(bars, df_sorted['Total_Cases_M']):
    plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}M', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('covid_total_cases.png', dpi=150)
plt.show()
print("✅ Saved: covid_total_cases.png")

# Chart 2: Death Rate by Country
plt.figure(figsize=(12, 6))
df_death = df.sort_values('Death_Rate', ascending=False)
colors2 = ['#e74c3c' if x > 2 else '#f39c12' if x > 1 else '#2ecc71' for x in df_death['Death_Rate']]
bars2 = plt.bar(df_death['Country'], df_death['Death_Rate'], color=colors2, edgecolor='black')
plt.title('COVID-19 Death Rate by Country (%)', fontsize=16, fontweight='bold')
plt.xlabel('Country')
plt.ylabel('Death Rate (%)')
plt.xticks(rotation=45, ha='right')
for bar, val in zip(bars2, df_death['Death_Rate']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val}%', ha='center', fontsize=9)
red = mpatches.Patch(color='#e74c3c', label='High (>2%)')
orange = mpatches.Patch(color='#f39c12', label='Medium (1-2%)')
green = mpatches.Patch(color='#2ecc71', label='Low (<1%)')
plt.legend(handles=[red, orange, green])
plt.tight_layout()
plt.savefig('covid_death_rate.png', dpi=150)
plt.show()
print("✅ Saved: covid_death_rate.png")

# Chart 3: Recovery Rate by Country
plt.figure(figsize=(12, 6))
df_rec = df.sort_values('Recovery_Rate', ascending=False)
sns.barplot(x='Country', y='Recovery_Rate', data=df_rec, palette='Greens_r')
plt.title('COVID-19 Recovery Rate by Country (%)', fontsize=16, fontweight='bold')
plt.xlabel('Country')
plt.ylabel('Recovery Rate (%)')
plt.xticks(rotation=45, ha='right')
plt.ylim(90, 100)
plt.tight_layout()
plt.savefig('covid_recovery_rate.png', dpi=150)
plt.show()
print("✅ Saved: covid_recovery_rate.png")

# Chart 4: Cases vs Deaths Scatter Plot
plt.figure(figsize=(12, 7))
scatter = plt.scatter(df['Total_Cases_M'], df['Total_Deaths_K'],
                      s=df['Population_Million']*3,
                      c=df['Death_Rate'], cmap='RdYlGn_r',
                      alpha=0.7, edgecolors='black')
plt.colorbar(scatter, label='Death Rate (%)')
for i, row in df.iterrows():
    plt.annotate(row['Country'],
                 (row['Total_Cases_M'], row['Total_Deaths_K']),
                 textcoords="offset points", xytext=(5, 5), fontsize=9)
plt.title('Total Cases vs Total Deaths (Bubble size = Population)', fontsize=16, fontweight='bold')
plt.xlabel('Total Cases (Millions)')
plt.ylabel('Total Deaths (Thousands)')
plt.tight_layout()
plt.savefig('covid_cases_vs_deaths.png', dpi=150)
plt.show()
print("✅ Saved: covid_cases_vs_deaths.png")

# Chart 5: Cases Per Million Population
plt.figure(figsize=(12, 6))
df_cpm = df.sort_values('Cases_Per_Million', ascending=False)
sns.barplot(x='Country', y='Cases_Per_Million', data=df_cpm, palette='Blues_r')
plt.title('COVID-19 Cases Per Million Population', fontsize=16, fontweight='bold')
plt.xlabel('Country')
plt.ylabel('Cases Per Million')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('covid_cases_per_million.png', dpi=150)
plt.show()
print("✅ Saved: covid_cases_per_million.png")

# Chart 6: Stacked Bar - Cases, Recovered, Deaths
plt.figure(figsize=(14, 7))
x = np.arange(len(df['Country']))
width = 0.6
df_plot = df.sort_values('Total_Cases', ascending=False)
active = df_plot['Total_Cases'] - df_plot['Total_Recovered'] - df_plot['Total_Deaths']
p1 = plt.bar(x, df_plot['Total_Recovered']/1e6, width, label='Recovered', color='#2ecc71')
p2 = plt.bar(x, active/1e6, width, bottom=df_plot['Total_Recovered']/1e6, label='Active', color='#f39c12')
p3 = plt.bar(x, df_plot['Total_Deaths']/1e6, width,
             bottom=(df_plot['Total_Recovered']+active)/1e6, label='Deaths', color='#e74c3c')
plt.title('COVID-19 Cases Breakdown by Country (Millions)', fontsize=16, fontweight='bold')
plt.xlabel('Country')
plt.ylabel('Cases (Millions)')
plt.xticks(x, df_plot['Country'], rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('covid_stacked_bar.png', dpi=150)
plt.show()
print("✅ Saved: covid_stacked_bar.png")

# Chart 7: Correlation Heatmap
plt.figure(figsize=(10, 7))
numeric_cols = ['Total_Cases', 'Total_Deaths', 'Total_Recovered',
                'Death_Rate', 'Recovery_Rate', 'Cases_Per_Million']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            linewidths=0.5, square=True)
plt.title('Correlation Heatmap - COVID-19 Metrics', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('covid_correlation_heatmap.png', dpi=150)
plt.show()
print("✅ Saved: covid_correlation_heatmap.png")

# ============================================================
# Step 4: Key Insights
# ============================================================
print("\n" + "=" * 60)
print("📊 KEY INSIGHTS FROM DATA VISUALIZATION")
print("=" * 60)

print(f"\n1. Highest Cases: {df.loc[df['Total_Cases'].idxmax(), 'Country']} ({df['Total_Cases_M'].max():.1f}M)")
print(f"2. Highest Death Rate: {df.loc[df['Death_Rate'].idxmax(), 'Country']} ({df['Death_Rate'].max():.2f}%)")
print(f"3. Highest Recovery Rate: {df.loc[df['Recovery_Rate'].idxmax(), 'Country']} ({df['Recovery_Rate'].max():.2f}%)")
print(f"4. Most Cases Per Million: {df.loc[df['Cases_Per_Million'].idxmax(), 'Country']}")
print(f"5. Global Average Death Rate: {df['Death_Rate'].mean():.2f}%")
print(f"6. Global Average Recovery Rate: {df['Recovery_Rate'].mean():.2f}%")

print("\n" + "=" * 60)
print("✅ Data Visualization Complete! All 7 charts saved as PNG.")
print("=" * 60)
print("\n📌 Next Steps:")
print("  1. Upload to GitHub repo: CodeAlpha_DataVisualization")
print("  2. Record a video explanation")
print("  3. Post on LinkedIn tagging @CodeAlpha")
print("  4. Submit via WhatsApp group Submission Form")
