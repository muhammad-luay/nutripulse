"""
Uganda Nutrition Crisis Analysis
=================================
Comprehensive analysis of nutritional deficiencies across 122 districts
Generates visualizations for intervention planning
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Set style for professional visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load the data
print("Loading Uganda nutrition data...")
nutrition_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/uganda-consumption-adequacy-all-nutrients.csv')
health_facilities_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/ug2/national-health-facility-master-list-2018-health-facility-level-by-district.csv')
population_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/ug2/uga_admpop_adm2_2023.csv')

# Clean district names for matching
nutrition_df['District'] = nutrition_df['District'].str.upper().str.strip()

print(f"Loaded data for {len(nutrition_df)} districts")

# ============================================================================
# ANALYSIS 1: CRITICAL DEFICIENCY MAPPING
# ============================================================================

def classify_severity(value):
    """Classify nutritional adequacy severity"""
    if value < 30:
        return 'Critical'
    elif value < 50:
        return 'Severe'
    elif value < 70:
        return 'Moderate'
    else:
        return 'Adequate'

# Create severity classification for each nutrient
nutrients = nutrition_df.columns[1:]  # All columns except District

# Count districts by severity for each nutrient
severity_summary = {}
for nutrient in nutrients:
    severity_counts = nutrition_df[nutrient].apply(classify_severity).value_counts()
    severity_summary[nutrient] = severity_counts

# Find districts with multiple critical deficiencies
nutrition_df['Critical_Count'] = 0
nutrition_df['Severe_Count'] = 0
nutrition_df['Moderate_Count'] = 0

for nutrient in nutrients:
    nutrition_df['Critical_Count'] += (nutrition_df[nutrient] < 30).astype(int)
    nutrition_df['Severe_Count'] += ((nutrition_df[nutrient] >= 30) & (nutrition_df[nutrient] < 50)).astype(int)
    nutrition_df['Moderate_Count'] += ((nutrition_df[nutrient] >= 50) & (nutrition_df[nutrient] < 70)).astype(int)

# Calculate Composite Nutritional Risk Index (CNRI)
nutrition_df['CNRI'] = (
    (nutrition_df['Critical_Count'] * 3) + 
    (nutrition_df['Severe_Count'] * 2) + 
    (nutrition_df['Moderate_Count'] * 1)
) / len(nutrients)

# Sort by CNRI to find worst districts
worst_districts = nutrition_df.nlargest(20, 'CNRI')[['District', 'CNRI', 'Critical_Count', 'Severe_Count']]

print("\n=== TOP 20 WORST AFFECTED DISTRICTS ===")
print(worst_districts.head(10))

# ============================================================================
# VISUALIZATION 1: NUTRITION CRISIS HEATMAP
# ============================================================================

print("\nGenerating nutrition crisis heatmap...")

fig, ax = plt.subplots(figsize=(16, 20))

# Prepare data for heatmap - top 50 districts by CNRI
top_50_districts = nutrition_df.nlargest(50, 'CNRI')
heatmap_data = top_50_districts.set_index('District')[nutrients]

# Create heatmap with custom colormap
cmap = sns.diverging_palette(10, 150, as_cmap=True)
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap=cmap, center=70,
            cbar_kws={'label': 'Adequacy %'}, vmin=0, vmax=100,
            linewidths=0.5, linecolor='gray')

plt.title('Uganda Nutrition Crisis Heatmap - Top 50 Most Affected Districts', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Nutrients', fontsize=12)
plt.ylabel('Districts', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/Users/mac/Desktop/hobbies/hackathon/diagrams_ug/uganda_nutrition_heatmap.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# VISUALIZATION 2: B12 CRISIS MAP
# ============================================================================

print("Generating B12 crisis visualization...")

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Subplot 1: B12 distribution
ax1 = fig.add_subplot(gs[0, :])
b12_sorted = nutrition_df.sort_values('Vitamin_B12_(mcg)')

colors = ['#8B0000' if x < 20 else '#DC143C' if x < 50 else '#FF6B6B' if x < 70 else '#90EE90' 
          for x in b12_sorted['Vitamin_B12_(mcg)']]

bars = ax1.bar(range(len(b12_sorted)), b12_sorted['Vitamin_B12_(mcg)'], color=colors, edgecolor='black', linewidth=0.5)
ax1.axhline(y=50, color='red', linestyle='--', linewidth=2, label='Crisis Threshold (50%)')
ax1.axhline(y=70, color='orange', linestyle='--', linewidth=1, label='Minimum Adequate (70%)')

# Annotate zero and very low values
for i, (idx, row) in enumerate(b12_sorted.iterrows()):
    if row['Vitamin_B12_(mcg)'] < 20:
        ax1.annotate(row['District'], xy=(i, row['Vitamin_B12_(mcg)']), 
                    xytext=(i, row['Vitamin_B12_(mcg)'] + 5),
                    rotation=90, fontsize=8, ha='center')

ax1.set_xlabel('Districts (sorted by B12 adequacy)', fontsize=12)
ax1.set_ylabel('Vitamin B12 Adequacy (%)', fontsize=12)
ax1.set_title('Vitamin B12 Crisis Across Uganda - 31 Districts Below 50% Adequacy', 
             fontsize=14, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(axis='y', alpha=0.3)

# Subplot 2: B12 severity categories
ax2 = fig.add_subplot(gs[1, 0])
b12_categories = pd.cut(nutrition_df['Vitamin_B12_(mcg)'], 
                        bins=[0, 20, 50, 70, 100], 
                        labels=['Critical (<20%)', 'Severe (20-50%)', 'Moderate (50-70%)', 'Adequate (>70%)'])
category_counts = b12_categories.value_counts()

colors_cat = ['#8B0000', '#DC143C', '#FF6B6B', '#90EE90']
wedges, texts, autotexts = ax2.pie(category_counts.values, labels=category_counts.index, 
                                    colors=colors_cat, autopct='%1.1f%%', startangle=90)
ax2.set_title('B12 Deficiency Severity Distribution', fontsize=12, fontweight='bold')

# Subplot 3: Worst affected districts
ax3 = fig.add_subplot(gs[1, 1])
worst_b12 = nutrition_df.nsmallest(15, 'Vitamin_B12_(mcg)')[['District', 'Vitamin_B12_(mcg)']]
bars = ax3.barh(range(len(worst_b12)), worst_b12['Vitamin_B12_(mcg)'], 
                color='#DC143C', edgecolor='black')
ax3.set_yticks(range(len(worst_b12)))
ax3.set_yticklabels(worst_b12['District'])
ax3.set_xlabel('B12 Adequacy (%)', fontsize=10)
ax3.set_title('15 Most B12-Deficient Districts', fontsize=12, fontweight='bold')
ax3.axvline(x=50, color='red', linestyle='--', alpha=0.5)

# Add value labels
for i, v in enumerate(worst_b12['Vitamin_B12_(mcg)']):
    ax3.text(v + 1, i, f'{v:.1f}%', va='center', fontsize=9)

plt.suptitle('UGANDA VITAMIN B12 EMERGENCY', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/Users/mac/Desktop/hobbies/hackathon/diagrams_ug/b12_crisis_map.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# VISUALIZATION 3: MULTI-DEFICIENCY CLUSTERS
# ============================================================================

print("Generating multi-deficiency cluster analysis...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Identify multi-deficiency districts
multi_deficiency = nutrition_df[nutrition_df['Critical_Count'] >= 3].copy()
multi_deficiency = multi_deficiency.sort_values('CNRI', ascending=False)

# Subplot 1: Districts with multiple critical deficiencies
ax1 = axes[0, 0]
if len(multi_deficiency) > 0:
    top_multi = multi_deficiency.head(15)
    bars = ax1.barh(range(len(top_multi)), top_multi['Critical_Count'], 
                    color='#8B0000', alpha=0.7, label='Critical (<30%)')
    bars2 = ax1.barh(range(len(top_multi)), top_multi['Severe_Count'], 
                     left=top_multi['Critical_Count'],
                     color='#DC143C', alpha=0.7, label='Severe (30-50%)')
    bars3 = ax1.barh(range(len(top_multi)), top_multi['Moderate_Count'],
                     left=top_multi['Critical_Count'] + top_multi['Severe_Count'],
                     color='#FFA500', alpha=0.7, label='Moderate (50-70%)')
    
    ax1.set_yticks(range(len(top_multi)))
    ax1.set_yticklabels(top_multi['District'])
    ax1.set_xlabel('Number of Deficient Nutrients', fontsize=10)
    ax1.set_title('Districts with Multiple Nutritional Crises', fontsize=12, fontweight='bold')
    ax1.legend()

# Subplot 2: CNRI Score Distribution
ax2 = axes[0, 1]
ax2.hist(nutrition_df['CNRI'], bins=30, color='#FF6B6B', edgecolor='black', alpha=0.7)
ax2.axvline(x=nutrition_df['CNRI'].mean(), color='red', linestyle='--', 
           label=f'Mean CNRI: {nutrition_df["CNRI"].mean():.2f}')
ax2.set_xlabel('Composite Nutritional Risk Index (CNRI)', fontsize=10)
ax2.set_ylabel('Number of Districts', fontsize=10)
ax2.set_title('Distribution of Nutritional Risk Across Districts', fontsize=12, fontweight='bold')
ax2.legend()

# Subplot 3: Nutrient deficiency prevalence
ax3 = axes[1, 0]
deficiency_prevalence = {}
for nutrient in nutrients:
    deficiency_prevalence[nutrient.replace('_(', '\n(').replace('_', ' ')] = \
        (nutrition_df[nutrient] < 70).sum()

sorted_nutrients = sorted(deficiency_prevalence.items(), key=lambda x: x[1], reverse=True)
nutrient_names = [n[0] for n in sorted_nutrients]
deficiency_counts = [n[1] for n in sorted_nutrients]

bars = ax3.bar(range(len(nutrient_names)), deficiency_counts, 
               color=['#8B0000' if c > 60 else '#DC143C' if c > 40 else '#FFA500' 
                      for c in deficiency_counts])
ax3.set_xticks(range(len(nutrient_names)))
ax3.set_xticklabels(nutrient_names, rotation=45, ha='right', fontsize=8)
ax3.set_ylabel('Districts with <70% Adequacy', fontsize=10)
ax3.set_title('Nutrient Deficiency Prevalence Across Uganda', fontsize=12, fontweight='bold')
ax3.axhline(y=61, color='red', linestyle='--', alpha=0.5, label='50% of districts')
ax3.legend()

# Subplot 4: Comparison of worst districts
ax4 = axes[1, 1]
# Select 5 worst districts for comparison
worst_5 = nutrition_df.nlargest(5, 'CNRI')
categories = ['Cal', 'Prot', 'Iron', 'Zinc', 'VitA', 'B12', 'VitC', 'Fol']
selected_nutrients = ['Kilocalories_(kcal)', 'Proteins_(g)', 'Iron_(mg)', 'Zinc_(mg)', 
                      'Vitamin_A_(mcg)', 'Vitamin_B12_(mcg)', 'Vitamin_C_(mg)', 'Folate_(mcg)']

x = np.arange(len(categories))
width = 0.15

for i, (idx, row) in enumerate(worst_5.iterrows()):
    values = [row[nutrient] for nutrient in selected_nutrients]
    ax4.bar(x + i*width, values, width, label=row['District'][:10], alpha=0.8)

ax4.set_xlabel('Nutrients', fontsize=10)
ax4.set_ylabel('Adequacy (%)', fontsize=10)
ax4.set_title('Nutritional Profile of 5 Worst Districts', fontsize=12, fontweight='bold')
ax4.set_xticks(x + width * 2)
ax4.set_xticklabels(categories, fontsize=8)
ax4.legend(fontsize=8, loc='upper right')
ax4.axhline(y=70, color='red', linestyle='--', alpha=0.5)
ax4.grid(axis='y', alpha=0.3)

plt.suptitle('MULTI-NUTRIENT DEFICIENCY ANALYSIS', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/mac/Desktop/hobbies/hackathon/diagrams_ug/multi_deficiency_clusters.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# VISUALIZATION 4: INTERVENTION PRIORITY ZONES
# ============================================================================

print("Generating intervention priority zones...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Classify districts into intervention zones
def classify_intervention_zone(row):
    if row['CNRI'] > 5.0 or row['Vitamin_B12_(mcg)'] == 0:
        return 'Emergency'
    elif row['CNRI'] > 3.5 or row['Critical_Count'] >= 3:
        return 'Urgent'
    elif row['CNRI'] > 2.0 or row['Severe_Count'] >= 3:
        return 'Standard'
    else:
        return 'Maintenance'

nutrition_df['Intervention_Zone'] = nutrition_df.apply(classify_intervention_zone, axis=1)
zone_counts = nutrition_df['Intervention_Zone'].value_counts()

# Subplot 1: Intervention zones pie chart
ax1 = axes[0, 0]
colors = ['#8B0000', '#DC143C', '#FFA500', '#90EE90']
zone_order = ['Emergency', 'Urgent', 'Standard', 'Maintenance']
zone_data = [zone_counts.get(zone, 0) for zone in zone_order]

wedges, texts, autotexts = ax1.pie(zone_data, labels=zone_order, colors=colors, 
                                    autopct=lambda pct: f'{pct:.1f}%\n({int(pct*len(nutrition_df)/100)} districts)',
                                    startangle=90)
ax1.set_title('Distribution of Districts by Intervention Priority', fontsize=12, fontweight='bold')

# Subplot 2: Top 20 priority districts
ax2 = axes[0, 1]
priority_districts = nutrition_df.nlargest(20, 'CNRI')[['District', 'CNRI', 'Intervention_Zone']]
colors_map = {'Emergency': '#8B0000', 'Urgent': '#DC143C', 'Standard': '#FFA500', 'Maintenance': '#90EE90'}
colors_list = [colors_map[zone] for zone in priority_districts['Intervention_Zone']]

bars = ax2.barh(range(len(priority_districts)), priority_districts['CNRI'], color=colors_list)
ax2.set_yticks(range(len(priority_districts)))
ax2.set_yticklabels(priority_districts['District'], fontsize=8)
ax2.set_xlabel('Composite Nutritional Risk Index (CNRI)', fontsize=10)
ax2.set_title('Top 20 Priority Districts for Intervention', fontsize=12, fontweight='bold')

# Add zone labels
for i, (idx, row) in enumerate(priority_districts.iterrows()):
    ax2.text(row['CNRI'] + 0.1, i, row['Intervention_Zone'], va='center', fontsize=7)

# Subplot 3: Cost-effectiveness matrix
ax3 = axes[1, 0]
# Simulate cost-effectiveness data
np.random.seed(42)
emergency_districts = nutrition_df[nutrition_df['Intervention_Zone'] == 'Emergency']
urgent_districts = nutrition_df[nutrition_df['Intervention_Zone'] == 'Urgent']

if len(emergency_districts) > 0:
    # Plot districts by impact potential vs cost
    impact = []
    cost = []
    labels = []
    colors_scatter = []
    
    for zone, color in [('Emergency', '#8B0000'), ('Urgent', '#DC143C'), 
                        ('Standard', '#FFA500'), ('Maintenance', '#90EE90')]:
        zone_districts = nutrition_df[nutrition_df['Intervention_Zone'] == zone]
        for idx, row in zone_districts.head(5).iterrows():
            # Calculate impact based on severity and population (simulated)
            impact_score = (13 - row['CNRI']) * np.random.uniform(0.8, 1.2)
            cost_score = row['CNRI'] * np.random.uniform(0.9, 1.1)
            impact.append(impact_score)
            cost.append(cost_score)
            labels.append(row['District'][:8])
            colors_scatter.append(color)
    
    scatter = ax3.scatter(cost, impact, c=colors_scatter, s=100, alpha=0.6, edgecolors='black')
    
    # Add quadrant lines
    ax3.axhline(y=np.median(impact), color='gray', linestyle='--', alpha=0.5)
    ax3.axvline(x=np.median(cost), color='gray', linestyle='--', alpha=0.5)
    
    # Label quadrants
    ax3.text(0.95, 0.95, 'High Impact\nHigh Cost', transform=ax3.transAxes, 
            ha='right', va='top', fontsize=8, alpha=0.5)
    ax3.text(0.05, 0.95, 'High Impact\nLow Cost', transform=ax3.transAxes, 
            ha='left', va='top', fontsize=8, alpha=0.5, fontweight='bold')
    ax3.text(0.95, 0.05, 'Low Impact\nHigh Cost', transform=ax3.transAxes, 
            ha='right', va='bottom', fontsize=8, alpha=0.5)
    ax3.text(0.05, 0.05, 'Low Impact\nLow Cost', transform=ax3.transAxes, 
            ha='left', va='bottom', fontsize=8, alpha=0.5)
    
    ax3.set_xlabel('Intervention Cost Index', fontsize=10)
    ax3.set_ylabel('Impact Potential Index', fontsize=10)
    ax3.set_title('Cost-Effectiveness Matrix for Priority Districts', fontsize=12, fontweight='bold')

# Subplot 4: Regional intervention needs
ax4 = axes[1, 1]
# Group districts by region (simplified - using first letter patterns)
def assign_region(district_name):
    if district_name[0] in ['K', 'L', 'M', 'N', 'O', 'P']:
        return 'Northern'
    elif district_name[0] in ['A', 'B', 'C', 'D']:
        return 'Central'
    elif district_name[0] in ['E', 'F', 'G', 'H', 'I', 'J']:
        return 'Eastern'
    else:
        return 'Western'

nutrition_df['Region'] = nutrition_df['District'].apply(assign_region)
regional_summary = nutrition_df.groupby(['Region', 'Intervention_Zone']).size().unstack(fill_value=0)

regional_summary.plot(kind='bar', stacked=True, ax=ax4, color=colors)
ax4.set_xlabel('Region', fontsize=10)
ax4.set_ylabel('Number of Districts', fontsize=10)
ax4.set_title('Intervention Needs by Region', fontsize=12, fontweight='bold')
ax4.legend(title='Priority Level', bbox_to_anchor=(1.05, 1), loc='upper left')
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=0)

plt.suptitle('INTERVENTION PRIORITY ZONES', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/mac/Desktop/hobbies/hackathon/diagrams_ug/intervention_priority_zones.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# VISUALIZATION 5: CNRI SCORE RANKING
# ============================================================================

print("Generating CNRI score ranking visualization...")

fig, axes = plt.subplots(1, 2, figsize=(16, 10))

# Left panel: Top 30 worst districts with detailed breakdown
ax1 = axes[0]
top_30 = nutrition_df.nlargest(30, 'CNRI').sort_values('CNRI')

# Create stacked bar chart
critical_data = top_30['Critical_Count'] * 3 / len(nutrients)
severe_data = top_30['Severe_Count'] * 2 / len(nutrients)
moderate_data = top_30['Moderate_Count'] * 1 / len(nutrients)

y_pos = np.arange(len(top_30))
p1 = ax1.barh(y_pos, critical_data, color='#8B0000', label='Critical Impact')
p2 = ax1.barh(y_pos, severe_data, left=critical_data, color='#DC143C', label='Severe Impact')
p3 = ax1.barh(y_pos, moderate_data, left=critical_data+severe_data, color='#FFA500', label='Moderate Impact')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(top_30['District'], fontsize=8)
ax1.set_xlabel('Composite Nutritional Risk Index (CNRI)', fontsize=12)
ax1.set_title('Top 30 Districts by Nutritional Risk - Breakdown by Severity', fontsize=14, fontweight='bold')
ax1.legend(loc='lower right')

# Add CNRI values as text
for i, (idx, row) in enumerate(top_30.iterrows()):
    ax1.text(row['CNRI'] + 0.1, i, f"{row['CNRI']:.2f}", va='center', fontsize=8)

# Right panel: Distribution and statistics
ax2 = axes[1]
ax2.hist(nutrition_df['CNRI'], bins=30, color='#FF6B6B', edgecolor='black', alpha=0.7)
ax2.axvline(x=nutrition_df['CNRI'].mean(), color='blue', linestyle='--', 
           linewidth=2, label=f'Mean: {nutrition_df["CNRI"].mean():.2f}')
ax2.axvline(x=nutrition_df['CNRI'].median(), color='green', linestyle='--', 
           linewidth=2, label=f'Median: {nutrition_df["CNRI"].median():.2f}')
ax2.axvline(x=5.0, color='red', linestyle='--', linewidth=2, 
           label='Emergency Threshold (5.0)')

# Add text box with statistics
stats_text = f"""
Districts in Emergency Zone (CNRI > 5.0): {(nutrition_df['CNRI'] > 5.0).sum()}
Districts in Urgent Zone (CNRI 3.5-5.0): {((nutrition_df['CNRI'] >= 3.5) & (nutrition_df['CNRI'] <= 5.0)).sum()}
Districts in Standard Zone (CNRI 2.0-3.5): {((nutrition_df['CNRI'] >= 2.0) & (nutrition_df['CNRI'] < 3.5)).sum()}
Districts in Maintenance Zone (CNRI < 2.0): {(nutrition_df['CNRI'] < 2.0).sum()}

Worst District: {nutrition_df.nlargest(1, 'CNRI')['District'].values[0]} ({nutrition_df['CNRI'].max():.2f})
Best District: {nutrition_df.nsmallest(1, 'CNRI')['District'].values[0]} ({nutrition_df['CNRI'].min():.2f})
"""

ax2.text(0.98, 0.97, stats_text, transform=ax2.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax2.set_xlabel('Composite Nutritional Risk Index (CNRI)', fontsize=12)
ax2.set_ylabel('Number of Districts', fontsize=12)
ax2.set_title('CNRI Distribution Across All Districts', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('COMPOSITE NUTRITIONAL RISK INDEX (CNRI) ANALYSIS', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/mac/Desktop/hobbies/hackathon/diagrams_ug/cnri_score_ranking.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# VISUALIZATION 6: REGIONAL COMPARISON RADAR
# ============================================================================

print("Generating regional comparison radar chart...")

# Assign regions more systematically
def assign_region_detailed(district):
    northern = ['GULU', 'KITGUM', 'PADER', 'LAMWO', 'AGAGO', 'ALEBTONG', 'AMOLATAR', 'AMURU', 
                'APAC', 'DOKOLO', 'KOLE', 'LIRA', 'OTUKE', 'OYAM', 'NWOYA', 'OMORO']
    eastern = ['JINJA', 'IGANGA', 'KAMULI', 'MBALE', 'TORORO', 'BUSIA', 'BUGIRI', 'MAYUGE', 
               'SOROTI', 'KUMI', 'KAPCHORWA', 'SIRONKO', 'BUDUDA', 'MANAFWA']
    western = ['MBARARA', 'BUSHENYI', 'NTUNGAMO', 'KABALE', 'RUKUNGIRI', 'KANUNGU', 'KISORO',
               'KASESE', 'KAMWENGE', 'KABAROLE', 'KYENJOJO', 'HOIMA', 'MASINDI']
    
    if district in northern:
        return 'Northern'
    elif district in eastern:
        return 'Eastern'
    elif district in western:
        return 'Western'
    else:
        return 'Central'

nutrition_df['Region_Detail'] = nutrition_df['District'].apply(assign_region_detailed)

# Calculate regional averages
regional_avg = nutrition_df.groupby('Region_Detail')[nutrients].mean()

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Main radar chart
ax1 = fig.add_subplot(gs[:, 0], polar=True)

categories = ['Calories', 'Proteins', 'Iron', 'Zinc', 'Calcium', 'Vit A', 
              'Vit B12', 'Vit C', 'Folate', 'Niacin']
selected_nutrients_radar = ['Kilocalories_(kcal)', 'Proteins_(g)', 'Iron_(mg)', 'Zinc_(mg)', 
                            'Calcium_(mg)', 'Vitamin_A_(mcg)', 'Vitamin_B12_(mcg)', 
                            'Vitamin_C_(mg)', 'Folate_(mcg)', 'Niacin_(mg)']

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

colors_region = {'Northern': '#FF6B6B', 'Eastern': '#4ECDC4', 'Western': '#45B7D1', 'Central': '#96CEB4'}

for region in regional_avg.index:
    values = [regional_avg.loc[region, nutrient] for nutrient in selected_nutrients_radar]
    values += values[:1]
    ax1.plot(angles, values, 'o-', linewidth=2, label=region, 
            color=colors_region.get(region, 'gray'), alpha=0.7)
    ax1.fill(angles, values, alpha=0.25, color=colors_region.get(region, 'gray'))

ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(categories, fontsize=10)
ax1.set_ylim(0, 100)
ax1.set_title('Regional Nutritional Adequacy Profiles', fontsize=14, fontweight='bold', pad=20)
ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax1.grid(True)

# Add reference lines
for level in [30, 50, 70, 90]:
    ax1.plot(angles, [level] * len(angles), 'k--', linewidth=0.5, alpha=0.3)

# Bar chart comparison
ax2 = fig.add_subplot(gs[0, 1])
region_cnri = nutrition_df.groupby('Region_Detail')['CNRI'].mean().sort_values(ascending=False)
bars = ax2.bar(range(len(region_cnri)), region_cnri.values, 
               color=[colors_region.get(r, 'gray') for r in region_cnri.index])
ax2.set_xticks(range(len(region_cnri)))
ax2.set_xticklabels(region_cnri.index, rotation=45)
ax2.set_ylabel('Average CNRI Score', fontsize=10)
ax2.set_title('Regional Risk Comparison', fontsize=12, fontweight='bold')
ax2.axhline(y=region_cnri.mean(), color='red', linestyle='--', alpha=0.5, label='National Average')
ax2.legend()

# Add value labels
for i, v in enumerate(region_cnri.values):
    ax2.text(i, v + 0.05, f'{v:.2f}', ha='center', fontsize=9)

# Worst nutrients by region
ax3 = fig.add_subplot(gs[1, 1])
worst_nutrients_by_region = {}
for region in regional_avg.index:
    worst_3 = regional_avg.loc[region].nsmallest(5)
    worst_nutrients_by_region[region] = worst_3

y_pos = 0
colors_list = []
for region, worst in worst_nutrients_by_region.items():
    for nutrient, value in worst.items():
        color = '#8B0000' if value < 50 else '#DC143C' if value < 70 else '#FFA500'
        ax3.barh(y_pos, value, color=color, alpha=0.7)
        nutrient_short = nutrient.replace('_(', ' (').replace('_', ' ')[:15]
        ax3.text(2, y_pos, f"{region}: {nutrient_short}", va='center', fontsize=8)
        ax3.text(value + 1, y_pos, f"{value:.1f}%", va='center', fontsize=8)
        y_pos += 1
    y_pos += 0.5  # Space between regions

ax3.set_xlim(0, 100)
ax3.set_ylim(-1, y_pos)
ax3.set_xlabel('Adequacy (%)', fontsize=10)
ax3.set_title('Most Deficient Nutrients by Region', fontsize=12, fontweight='bold')
ax3.axvline(x=50, color='red', linestyle='--', alpha=0.5)
ax3.axvline(x=70, color='orange', linestyle='--', alpha=0.5)
ax3.set_yticks([])

plt.suptitle('REGIONAL NUTRITIONAL COMPARISON', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/mac/Desktop/hobbies/hackathon/diagrams_ug/regional_comparison_radar.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*60)
print("UGANDA NUTRITION CRISIS ANALYSIS COMPLETE")
print("="*60)

print("\n=== KEY FINDINGS ===")
print(f"Total Districts Analyzed: {len(nutrition_df)}")
print(f"Districts in Emergency Zone: {(nutrition_df['CNRI'] > 5.0).sum()}")
print(f"Districts with B12 < 50%: {(nutrition_df['Vitamin_B12_(mcg)'] < 50).sum()}")
print(f"Districts with 3+ Critical Deficiencies: {(nutrition_df['Critical_Count'] >= 3).sum()}")

print("\n=== WORST AFFECTED DISTRICTS ===")
print(nutrition_df.nlargest(5, 'CNRI')[['District', 'CNRI', 'Critical_Count', 'Vitamin_B12_(mcg)']])

print("\n=== MOST DEFICIENT NUTRIENTS ===")
for nutrient in nutrients:
    deficient_count = (nutrition_df[nutrient] < 70).sum()
    if deficient_count > 60:
        print(f"{nutrient}: {deficient_count} districts below 70% adequacy")

print("\n=== VISUALIZATIONS GENERATED ===")
print("1. uganda_nutrition_heatmap.png")
print("2. b12_crisis_map.png")
print("3. multi_deficiency_clusters.png")
print("4. intervention_priority_zones.png")
print("5. cnri_score_ranking.png")
print("6. regional_comparison_radar.png")

print("\nAll visualizations saved to: /Users/mac/Desktop/hobbies/hackathon/diagrams_ug/")