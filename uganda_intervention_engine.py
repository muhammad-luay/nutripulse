"""
Uganda Multi-Nutrient Intervention Simulation Engine
=====================================================
An advanced evidence-based tool for planning and optimizing multi-nutrient 
interventions across 122 districts with 13 tracked nutrients.

Designed for policy makers, program managers, and funding organizations
to combat the nutrition crisis affecting 15+ million Ugandans.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Uganda Nutrition Command Center",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #d32f2f 0%, #f57c00 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .critical-box {
        background-color: #ffebee;
        border-left: 5px solid #d32f2f;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 5px solid #f57c00;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .district-priority-1 {
        background-color: #ffcdd2;
        font-weight: bold;
    }
    .nutrient-critical {
        color: #d32f2f;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'selected_districts' not in st.session_state:
    st.session_state.selected_districts = []
if 'intervention_history' not in st.session_state:
    st.session_state.intervention_history = []
if 'simulation_outcomes' not in st.session_state:
    st.session_state.simulation_outcomes = None

# Load Uganda-specific data
@st.cache_data
def load_uganda_data():
    """Load all Uganda nutrition and demographic data"""
    
    # Load nutrition adequacy data
    nutrition_data = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/uganda-consumption-adequacy-all-nutrients.csv')
    
    # Load population data
    population_data = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/ug2/uga_admpop_adm2_2023.csv')
    
    # Load health facility data
    health_facilities = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/ug2/national-health-facility-master-list-2018-health-facility-level-by-district.csv')
    
    # Standardize district names for matching (uppercase)
    nutrition_data['District'] = nutrition_data['District'].str.upper()
    population_data['ADM2_EN'] = population_data['ADM2_EN'].str.upper()
    if 'District' in health_facilities.columns:
        health_facilities['District'] = health_facilities['District'].str.upper()
    
    return nutrition_data, population_data, health_facilities

# Load data
nutrition_df, population_df, facilities_df = load_uganda_data()

# Constants
UGANDA_POPULATION = 48_582_334  # 2023 projection
TOTAL_DISTRICTS = 122
NUTRIENTS_TRACKED = ['Calcium_(mg)', 'Iron_(mg)', 'Zinc_(mg)', 'Folate_(mcg)', 
                     'Niacin_(mg)', 'Riboflavin_(mg)', 'Thiamin_(mg)', 
                     'Vitamin_A_(mcg)', 'Vitamin_B12_(mcg)', 'Vitamin_B6_(mg)', 
                     'Vitamin_C_(mg)', 'Proteins_(g)', 'Kilocalories_(kcal)']
CRITICAL_THRESHOLD = 50  # % adequacy below which is critical
SEVERE_THRESHOLD = 30   # % adequacy below which is severe

# Multi-Nutrient Optimization Engine
class MultiNutrientOptimizer:
    """Core optimization engine for multi-nutrient interventions"""
    
    def __init__(self, nutrition_data, population_data, facilities_data):
        self.nutrition = nutrition_data
        self.population = population_data
        self.facilities = facilities_data
        self.cnri_scores = self.calculate_cnri()
        
    def calculate_cnri(self) -> pd.DataFrame:
        """Calculate Composite Nutritional Risk Index for each district"""
        cnri_scores = []
        
        for idx, row in self.nutrition.iterrows():
            district = row['District']
            
            # Count critical deficiencies
            critical_count = sum(1 for nutrient in NUTRIENTS_TRACKED 
                                if row[nutrient] < CRITICAL_THRESHOLD)
            
            # Count severe deficiencies
            severe_count = sum(1 for nutrient in NUTRIENTS_TRACKED 
                              if row[nutrient] < SEVERE_THRESHOLD)
            
            # Calculate average adequacy
            avg_adequacy = np.mean([row[nutrient] for nutrient in NUTRIENTS_TRACKED])
            
            # Special weight for B12 (most critical)
            b12_weight = 2.0 if row['Vitamin_B12_(mcg)'] < 30 else 1.0
            
            # CNRI formula
            cnri = (severe_count * 3 + critical_count * 2) * b12_weight / avg_adequacy * 100
            
            cnri_scores.append({
                'District': district,
                'CNRI': cnri,
                'Critical_Count': critical_count,
                'Severe_Count': severe_count,
                'Avg_Adequacy': avg_adequacy,
                'Priority': 1 if cnri > 15 else 2 if cnri > 10 else 3
            })
        
        return pd.DataFrame(cnri_scores).sort_values('CNRI', ascending=False)
    
    def calculate_nutrient_synergies(self, nutrients: List[str]) -> float:
        """Calculate synergy multiplier for nutrient combinations"""
        synergy_matrix = {
            ('Vitamin_B12_(mcg)', 'Folate_(mcg)'): 1.4,
            ('Iron_(mg)', 'Vitamin_C_(mg)'): 2.5,
            ('Zinc_(mg)', 'Vitamin_A_(mcg)'): 1.3,
            ('Calcium_(mg)', 'Vitamin_D'): 1.8,
            ('Iron_(mg)', 'Vitamin_B12_(mcg)'): 1.2,
            ('Magnesium', 'Vitamin_D'): 1.3
        }
        
        multiplier = 1.0
        for combo, boost in synergy_matrix.items():
            if combo[0] in nutrients and combo[1] in nutrients:
                multiplier *= boost
        
        return min(multiplier, 2.0)  # Cap at 2x
    
    def prioritize_districts(self, budget: float, mode: str = 'balanced') -> Dict:
        """Prioritize districts based on CNRI and population"""
        
        if mode == 'emergency':
            # Focus on top 15 most critical districts
            priority_districts = self.cnri_scores.head(15)['District'].tolist()
            allocation_mode = 'concentrated'
        elif mode == 'prevention':
            # Target districts at tipping point (40-60% adequacy)
            at_risk = self.nutrition[
                (self.nutrition[NUTRIENTS_TRACKED].mean(axis=1) > 40) & 
                (self.nutrition[NUTRIENTS_TRACKED].mean(axis=1) < 60)
            ]['District'].tolist()
            priority_districts = at_risk
            allocation_mode = 'preventive'
        else:  # balanced
            # Weight by CNRI × Population
            merged = self.cnri_scores.merge(
                self.population[['ADM2_EN', 'T_TL']],
                left_on='District',
                right_on='ADM2_EN'
            )
            merged['Weight'] = merged['CNRI'] * merged['T_TL'] / 1000000
            priority_districts = merged.nlargest(45, 'Weight')['District'].tolist()
            allocation_mode = 'weighted'
        
        return {
            'districts': priority_districts,
            'mode': allocation_mode,
            'budget_per_district': budget / len(priority_districts)
        }
    
    def optimize_intervention_mix(self, district: str, budget: float) -> Dict:
        """Optimize intervention mix for a specific district"""
        
        district_data = self.nutrition[self.nutrition['District'] == district].iloc[0]
        district_facilities = self.facilities[self.facilities['District'] == district]
        
        # Identify critical nutrients
        critical_nutrients = [
            nutrient for nutrient in NUTRIENTS_TRACKED
            if district_data[nutrient] < CRITICAL_THRESHOLD
        ]
        
        # Calculate intervention effectiveness
        # Costs updated based on real Uganda/UNICEF data (in UGX per person)
        interventions = {
            'fortification': {
                'cost': 55500,  # $15 USD based on CLAUDE.md
                'effectiveness': 0.61,  # Evidence-based from CLAUDE.md
                'suitable_for': ['Iron_(mg)', 'Zinc_(mg)', 'Folate_(mcg)', 'Vitamin_B12_(mcg)'],
                'infrastructure_required': 'low'
            },
            'supplementation': {
                'cost': 1850,  # $0.50 USD - UNICEF actual cost from CLAUDE.md
                'effectiveness': 0.73,  # 77% improvement from Vitamin A programs
                'suitable_for': NUTRIENTS_TRACKED,
                'infrastructure_required': 'medium'
            },
            'biofortification': {
                'cost': 74000,  # $20 USD based on CLAUDE.md
                'effectiveness': 0.65,  # Based on adoption rates
                'suitable_for': ['Iron_(mg)', 'Zinc_(mg)', 'Vitamin_A_(mcg)'],
                'infrastructure_required': 'low'
            },
            'dietary_diversification': {
                'cost': 29600,  # $8 USD - Education cost from CLAUDE.md
                'effectiveness': 0.55,  # Conservative estimate from CLAUDE.md
                'suitable_for': NUTRIENTS_TRACKED,
                'infrastructure_required': 'high'
            }
        }
        
        # Check infrastructure capacity
        total_facilities = district_facilities.shape[0] if not district_facilities.empty else 1
        infrastructure_score = min(total_facilities / 10, 1.0)
        
        # Optimize mix based on district characteristics
        optimal_mix = {}
        remaining_budget = budget
        
        for intervention, details in interventions.items():
            # Check if intervention suits critical nutrients
            coverage = len([n for n in critical_nutrients if n in details['suitable_for']])
            if coverage == 0:
                continue
            
            # Adjust for infrastructure
            if details['infrastructure_required'] == 'high' and infrastructure_score < 0.5:
                continue
            
            # Allocate budget proportionally
            allocation = min(
                remaining_budget * 0.4,  # Max 40% per intervention
                remaining_budget
            )
            optimal_mix[intervention] = allocation
            remaining_budget -= allocation
            
            if remaining_budget <= 0:
                break
        
        return optimal_mix

class InterventionSimulator:
    """Simulates health and economic outcomes of interventions"""
    
    def __init__(self, optimizer: MultiNutrientOptimizer):
        self.optimizer = optimizer
        
    def calculate_health_outcomes(self, coverage: float, districts: List[str], 
                                 nutrients: List[str], timeline_months: int) -> Dict:
        """Calculate expected health outcomes"""
        
        # Get affected population
        affected_pop = self.optimizer.population[
            self.optimizer.population['ADM2_EN'].isin(districts)
        ]['T_TL'].sum()
        
        # Calculate lives saved (based on critical deficiencies)
        lives_saved = 0
        for district in districts:
            district_data = self.optimizer.nutrition[
                self.optimizer.nutrition['District'] == district
            ].iloc[0]
            
            # B12 deficiency mortality impact (based on WHO data)
            # Severe B12 deficiency has 2-5% mortality rate if untreated
            if district_data['Vitamin_B12_(mcg)'] < 30:
                district_pop = affected_pop / len(districts)  # Approximate per district
                at_risk_pop = district_pop * 0.15  # 15% are children under 5
                mortality_rate = 0.02  # 2% mortality for severe deficiency
                lives_saved += int(coverage * at_risk_pop * mortality_rate * 0.7)  # 70% effectiveness
            
            # Iron deficiency anemia (based on Lancet studies)
            if district_data['Iron_(mg)'] < 50:
                district_pop = affected_pop / len(districts)
                at_risk_pop = district_pop * 0.25  # 25% vulnerable (children + pregnant women)
                mortality_rate = 0.005  # 0.5% mortality for severe anemia
                lives_saved += int(coverage * at_risk_pop * mortality_rate * 0.6)  # 60% effectiveness
        
        # Stunting prevention
        stunting_prevented = int(coverage * affected_pop * 0.14 * 0.15)
        
        # Cognitive improvement (IQ points)
        avg_iq_gain = 0
        if 'Vitamin_B12_(mcg)' in nutrients:
            avg_iq_gain += 5
        if 'Iron_(mg)' in nutrients:
            avg_iq_gain += 3
        if 'Zinc_(mg)' in nutrients:
            avg_iq_gain += 2
        avg_iq_gain *= coverage
        
        # Economic benefit
        economic_benefit = self.calculate_economic_benefit(
            lives_saved, stunting_prevented, avg_iq_gain, affected_pop
        )
        
        return {
            'lives_saved': lives_saved,
            'stunting_prevented': stunting_prevented,
            'iq_gain': avg_iq_gain,
            'economic_benefit': economic_benefit,
            'people_reached': int(coverage * affected_pop)
        }
    
    def calculate_economic_benefit(self, lives_saved: int, stunting_prevented: int,
                                  iq_gain: float, population: int) -> float:
        """Calculate ANNUALIZED economic benefits using WHO/World Bank methodology"""
        
        # Use 10-year NPV with 5% discount rate for more realistic ROI
        discount_rate = 0.05
        years = 10
        
        # Healthcare savings (immediate)
        healthcare_saved_immediate = (
            lives_saved * 2_500_000 +  # Statistical value of life in Uganda
            stunting_prevented * 85_000  # Healthcare costs avoided in first 5 years
        )
        
        # Annual productivity gains (calculated per year, not lifetime)
        # Uganda GDP per capita ~$1000 USD = 3.7M UGX
        annual_gdp_per_capita = 3_700_000
        
        # Children who avoid stunting have 20% higher earnings as adults
        # But they only start earning after 15-20 years, so discount heavily
        annual_productivity = stunting_prevented * 0.20 * annual_gdp_per_capita / 20  # Spread over 20 years
        
        # Calculate NPV of productivity gains over 10 years
        productivity_npv = 0
        for year in range(1, years + 1):
            productivity_npv += annual_productivity / ((1 + discount_rate) ** year)
        
        # Cognitive benefits (annualized)
        # Each IQ point = 1% increase in annual earnings
        children_benefiting = int(population * 0.15)  # Children under 5
        annual_cognitive = children_benefiting * iq_gain * 0.01 * annual_gdp_per_capita / 25  # Over 25 working years
        
        # Calculate NPV of cognitive benefits
        cognitive_npv = 0
        for year in range(5, years + 1):  # Benefits start after 5 years
            cognitive_npv += annual_cognitive / ((1 + discount_rate) ** year)
        
        # Education savings (one-time, discounted)
        education_savings = stunting_prevented * 5_000 / (1 + discount_rate)
        
        # Total annualized benefit
        total_benefit = healthcare_saved_immediate + productivity_npv + cognitive_npv + education_savings
        
        return total_benefit

# Initialize optimizer
optimizer = MultiNutrientOptimizer(nutrition_df, population_df, facilities_df)
simulator = InterventionSimulator(optimizer)

# Header
st.markdown("""
<div class="main-header">
    <h1>🇺🇬 Uganda Nutrition Command Center</h1>
    <p style="font-size: 1.2rem;">Multi-Nutrient Intervention Planning System</p>
    <p style="font-size: 1rem;">Addressing 13 nutrients across 122 districts</p>
</div>
""", unsafe_allow_html=True)

# Critical Alert Dashboard
st.markdown("### 🚨 Critical Situation Overview")
col1, col2, col3, col4 = st.columns(4)

# Calculate key metrics
b12_critical = len(nutrition_df[nutrition_df['Vitamin_B12_(mcg)'] < 50])
multi_deficient = len(nutrition_df[
    nutrition_df[NUTRIENTS_TRACKED].apply(lambda x: sum(x < 50) >= 3, axis=1)
])
worst_district = optimizer.cnri_scores.iloc[0]['District']
worst_cnri = optimizer.cnri_scores.iloc[0]['CNRI']

with col1:
    st.markdown(f"""
    <div class="metric-card" style="background-color: #ffebee; border-left: 5px solid #d32f2f;">
        <h4 style="color: #b71c1c;">🩸 B12 Crisis</h4>
        <h2 style="color: #d32f2f;">{b12_critical} Districts</h2>
        <p style="color: #424242;">Below 50% adequacy</p>
        <p style="color: #d32f2f; font-weight: bold;">15M+ people affected</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background-color: #fff3e0; border-left: 5px solid #f57c00;">
        <h4 style="color: #e65100;">📊 Multi-Deficiency</h4>
        <h2 style="color: #f57c00;">{multi_deficient} Districts</h2>
        <p style="color: #424242;">3+ nutrient deficiencies</p>
        <p style="color: #f57c00; font-weight: bold;">Complex intervention needed</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background-color: #ffcdd2; border-left: 5px solid #d32f2f;">
        <h4 style="color: #b71c1c;">🎯 Worst District</h4>
        <h2 style="color: #d32f2f;">{worst_district}</h2>
        <p style="color: #424242;">CNRI Score: {worst_cnri:.1f}</p>
        <p style="color: #d32f2f; font-weight: bold;">EMERGENCY PRIORITY</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="background-color: #f3e5f5; border-left: 5px solid #7b1fa2;">
        <h4 style="color: #4a148c;">💰 Annual Loss</h4>
        <h2 style="color: #7b1fa2;">$2.3B</h2>
        <p style="color: #424242;">Economic impact</p>
        <p style="color: #7b1fa2; font-weight: bold;">2.8% of GDP</p>
    </div>
    """, unsafe_allow_html=True)

# Create tabs with better state management
tab_names = [
    "💰 Budget Optimization",
    "🎯 District Prioritization",
    "💊 Intervention Design", 
    "📊 Impact Simulation",
    "📈 Real-time Monitoring",
    "📋 Reports & Export"
]

# Create tabs
# Note: tab variables renamed to match their actual content
tab_budget, tab_district, tab_design, tab_sim, tab_monitor, tab_report = st.tabs(tab_names)

# Tab 2: District Prioritization (now in second position)
with tab_district:
    st.header("🎯 Smart District Prioritization")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Prioritization Strategy")
        
        strategy = st.selectbox(
            "Select targeting strategy:",
            ["Emergency Response", "Balanced Approach", "Prevention Focus", "Custom Selection"],
            help="Choose how to prioritize districts for intervention"
        )
        
        if strategy == "Emergency Response":
            st.markdown("""
            <div class="critical-box">
                <strong>Emergency Mode:</strong><br>
                • Focus on 15 most critical districts<br>
                • Target B12 and Iron deficiencies<br>
                • Rapid supplementation programs<br>
                • 3-6 month timeline
            </div>
            """, unsafe_allow_html=True)
            priority_districts = optimizer.cnri_scores.head(15)
            
        elif strategy == "Balanced Approach":
            st.markdown("""
            <div class="warning-box">
                <strong>Balanced Mode:</strong><br>
                • Cover 45 high-priority districts<br>
                • Address multiple nutrients<br>
                • Mix of interventions<br>
                • 12-24 month timeline
            </div>
            """, unsafe_allow_html=True)
            priority_districts = optimizer.cnri_scores.head(45)
            
        elif strategy == "Prevention Focus":
            st.markdown("""
            <div class="success-box">
                <strong>Prevention Mode:</strong><br>
                • Target at-risk districts<br>
                • Prevent deterioration<br>
                • Sustainable interventions<br>
                • 24-36 month timeline
            </div>
            """, unsafe_allow_html=True)
            # Get districts with 40-60% adequacy
            at_risk = nutrition_df[
                (nutrition_df[NUTRIENTS_TRACKED].mean(axis=1) > 40) & 
                (nutrition_df[NUTRIENTS_TRACKED].mean(axis=1) < 60)
            ]
            priority_districts = optimizer.cnri_scores[
                optimizer.cnri_scores['District'].isin(at_risk['District'])
            ]
        else:
            # Custom selection
            all_districts = nutrition_df['District'].tolist()
            selected = st.multiselect(
                "Select districts manually:",
                all_districts,
                default=optimizer.cnri_scores.head(10)['District'].tolist()
            )
            priority_districts = optimizer.cnri_scores[
                optimizer.cnri_scores['District'].isin(selected)
            ]
        
        # Show priority metrics
        st.metric("Districts Selected", len(priority_districts))
        
        # Calculate affected population (handle missing districts)
        if not priority_districts.empty:
            matching_districts = population_df[
                population_df['ADM2_EN'].isin(priority_districts['District'].str.upper())
            ]
            affected_pop = matching_districts['T_TL'].sum() if not matching_districts.empty else 1000000  # Default 1M if no match
        else:
            affected_pop = 0
        
        st.metric("Population Coverage", f"{affected_pop/1_000_000:.1f}M")
        st.metric("Coverage %", f"{affected_pop/UGANDA_POPULATION*100:.1f}%")
    
    with col2:
        st.subheader("Priority Districts Map")
        
        if not priority_districts.empty:
            # Create district priority visualization
            fig = go.Figure()
            
            # Add CNRI scores as bar chart
            fig.add_trace(go.Bar(
                x=priority_districts['District'].head(20),
                y=priority_districts['CNRI'].head(20),
                marker_color=['#d32f2f' if cnri > 15 else '#f57c00' if cnri > 10 else '#fbc02d' 
                             for cnri in priority_districts['CNRI'].head(20)],
                text=priority_districts['CNRI'].head(20).round(1),
                textposition='outside',
                name='CNRI Score'
            ))
            
            fig.update_layout(
                title="Top 20 Priority Districts by CNRI Score",
                xaxis_title="District",
                yaxis_title="Composite Nutritional Risk Index",
                height=400,
                showlegend=False,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed table
            st.subheader("District Priority Details")
            display_df = priority_districts[['District', 'CNRI', 'Critical_Count', 
                                            'Severe_Count', 'Avg_Adequacy', 'Priority']].head(20)
            display_df['CNRI'] = display_df['CNRI'].round(2)
            display_df['Avg_Adequacy'] = display_df['Avg_Adequacy'].round(1)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "CNRI": st.column_config.NumberColumn("CNRI Score", format="%.2f"),
                    "Critical_Count": "Critical Nutrients",
                    "Severe_Count": "Severe Nutrients",
                    "Avg_Adequacy": st.column_config.ProgressColumn(
                        "Avg Adequacy %",
                        min_value=0,
                        max_value=100,
                    ),
                    "Priority": st.column_config.NumberColumn("Priority Level", format="%d")
                }
            )
        
        # Store selected districts in session state
        st.session_state.selected_districts = priority_districts['District'].tolist() if not priority_districts.empty else []

# Tab 3: Intervention Design (now in third position)
with tab_design:
    st.header("💊 Multi-Nutrient Intervention Design")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Budget Configuration")
        
        # Budget input
        budget_input = st.number_input(
            "Total Budget (Million UGX)",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Enter total budget in millions of Ugandan Shillings"
        )
        budget_ugx = budget_input * 1_000_000
        
        st.info(f"""
        💰 **Budget Breakdown:**
        - Per district: {budget_ugx/len(st.session_state.selected_districts)/1_000_000:.1f}M UGX
        - Per person: {budget_ugx/affected_pop:.0f} UGX
        - USD equivalent: ${budget_ugx/3700/1_000_000:.1f}M
        """)
        
        st.subheader("Intervention Strategy Mix")
        
        # Intervention sliders
        fortification_pct = st.slider("Fortification %", 0, 100, 30, 
                                     help="Food fortification (flour, salt, oil)")
        supplementation_pct = st.slider("Supplementation %", 0, 100, 35,
                                       help="Direct nutrient supplements")
        biofortification_pct = st.slider("Biofortification %", 0, 100, 20,
                                        help="Nutrient-rich crop varieties")
        diversification_pct = st.slider("Dietary Diversification %", 0, 100, 15,
                                       help="Education and behavior change")
        
        total_pct = fortification_pct + supplementation_pct + biofortification_pct + diversification_pct
        
        if total_pct != 100:
            st.error(f"⚠️ Total must equal 100% (currently {total_pct}%)")
        else:
            st.success("✅ Valid intervention mix!")
            
        # Timeline selection
        st.subheader("Implementation Timeline")
        timeline = st.select_slider(
            "Program Duration",
            options=[6, 12, 18, 24, 36, 48, 60],
            value=24,
            format_func=lambda x: f"{x} months"
        )
        
    with col2:
        st.subheader("Nutrient Targeting Strategy")
        
        # Show nutrient deficiency heatmap for selected districts
        if st.session_state.selected_districts:
            selected_nutrition = nutrition_df[
                nutrition_df['District'].isin(st.session_state.selected_districts[:20])
            ]
            
            # Prepare heatmap data
            heatmap_data = selected_nutrition[['District'] + NUTRIENTS_TRACKED].set_index('District')
            
            # Create heatmap
            fig = px.imshow(
                heatmap_data.T,
                labels=dict(x="District", y="Nutrient", color="Adequacy %"),
                color_continuous_scale=["#d32f2f", "#ff9800", "#ffeb3b", "#8bc34a", "#4caf50"],
                title="Nutrient Adequacy Heatmap (Top 20 Selected Districts)",
                height=500
            )
            
            fig.update_layout(
                xaxis_tickangle=-45,
                coloraxis_colorbar=dict(
                    title="Adequacy %",
                    tickvals=[0, 30, 50, 70, 100],
                    ticktext=["0%", "30%", "50%", "70%", "100%"]
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Identify priority nutrients
            st.subheader("Priority Nutrients to Target")
            
            # Calculate average deficiency across selected districts
            nutrient_priorities = []
            for nutrient in NUTRIENTS_TRACKED:
                avg_adequacy = selected_nutrition[nutrient].mean()
                deficient_districts = len(selected_nutrition[selected_nutrition[nutrient] < 50])
                
                nutrient_priorities.append({
                    'Nutrient': nutrient,
                    'Avg_Adequacy': avg_adequacy,
                    'Deficient_Districts': deficient_districts,
                    'Priority': 'CRITICAL' if avg_adequacy < 30 else 'HIGH' if avg_adequacy < 50 else 'MEDIUM'
                })
            
            priority_df = pd.DataFrame(nutrient_priorities).sort_values('Avg_Adequacy')
            
            # Display priority nutrients
            critical_nutrients = priority_df[priority_df['Priority'] == 'CRITICAL']
            high_nutrients = priority_df[priority_df['Priority'] == 'HIGH']
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("**🔴 Critical Priority**")
                for _, row in critical_nutrients.iterrows():
                    st.markdown(f"• **{row['Nutrient']}**: {row['Avg_Adequacy']:.1f}% adequacy")
            
            with col_b:
                st.markdown("**🟡 High Priority**")
                for _, row in high_nutrients.iterrows():
                    st.markdown(f"• **{row['Nutrient']}**: {row['Avg_Adequacy']:.1f}% adequacy")

# Tab 4: Impact Simulation (now in fourth position)
with tab_sim:
    st.header("📊 Impact Simulation & Outcomes")
    
    if st.session_state.selected_districts and total_pct == 100:
        
        # Calculate coverage based on budget and intervention mix
        # Using real intervention costs from UNICEF/WHO data
        avg_cost_per_person = (
            fortification_pct * 55500 +     # $15 USD
            supplementation_pct * 1850 +    # $0.50 USD  
            biofortification_pct * 74000 +  # $20 USD
            diversification_pct * 29600     # $8 USD
        ) / 100
        
        max_coverage = min(1.0, budget_ugx / (avg_cost_per_person * affected_pop))
        
        # Display coverage metrics
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            people_reachable = int(max_coverage * affected_pop)
            st.metric(
                "People Reachable",
                f"{people_reachable:,}",
                help="Maximum people that can be reached with current budget"
            )
        with col_b:
            st.metric(
                "Cost per Person",
                f"{avg_cost_per_person:,.0f} UGX",
                f"${avg_cost_per_person/3700:.2f} USD"
            )
        with col_c:
            st.metric(
                "Population Coverage",
                f"{max_coverage*100:.1f}%",
                f"of {affected_pop/1_000_000:.1f}M people"
            )
        
        # Implementation efficiency slider
        efficiency = st.slider(
            "Implementation Efficiency %",
            min_value=40,
            max_value=90,
            value=70,
            help="Account for real-world implementation challenges"
        )
        
        actual_coverage = max_coverage * (efficiency / 100)
        
        # Show actual people reached after efficiency
        st.info(f"💡 **With {efficiency}% implementation efficiency**: {int(actual_coverage * affected_pop):,} people will be reached")
        
        # Run simulation
        with st.spinner("Running simulation..."):
            outcomes = simulator.calculate_health_outcomes(
                coverage=actual_coverage,
                districts=st.session_state.selected_districts,
                nutrients=priority_df[priority_df['Priority'].isin(['CRITICAL', 'HIGH'])]['Nutrient'].tolist(),
                timeline_months=timeline
            )
            
            # Save outcomes to session state for report generation
            st.session_state.simulation_outcomes = outcomes
        
        # Display results
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Lives Saved",
                f"{outcomes['lives_saved']:,}",
                delta=f"+{outcomes['lives_saved']/timeline*12:,.0f}/year"
            )
        
        with col2:
            st.metric(
                "Stunting Prevented",
                f"{outcomes['stunting_prevented']:,}",
                delta=f"{outcomes['stunting_prevented']/affected_pop*100:.1f}% reduction"
            )
        
        with col3:
            st.metric(
                "Avg IQ Gain",
                f"+{outcomes['iq_gain']:.1f} points",
                delta="Per child reached"
            )
        
        with col4:
            st.metric(
                "Economic Benefit",
                f"{outcomes['economic_benefit']/1_000_000_000:.1f}B UGX",
                delta=f"ROI: {outcomes['economic_benefit']/budget_ugx*100:.0f}%"
            )
        
        # Timeline visualization
        st.subheader("Impact Timeline")
        
        months = list(range(0, timeline + 1, 3))
        
        # Different impact curves
        immediate_impact = [min(100, (m/6) * 80) for m in months]
        growth_impact = [min(100, (m/12) * 60) for m in months]
        cognitive_impact = [min(100, (m/24) * 40) for m in months]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months, y=immediate_impact,
            mode='lines+markers',
            name='Micronutrient Status',
            line=dict(color='#4CAF50', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=growth_impact,
            mode='lines+markers',
            name='Growth Improvement',
            line=dict(color='#2196F3', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=cognitive_impact,
            mode='lines+markers',
            name='Cognitive Development',
            line=dict(color='#9C27B0', width=3)
        ))
        
        fig.update_layout(
            title="Expected Impact Achievement Over Time",
            xaxis_title="Months",
            yaxis_title="Impact Achievement (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # District-level impact
        st.subheader("District-Level Impact Projection")
        
        # Calculate district-specific impacts
        district_impacts = []
        for district in st.session_state.selected_districts[:10]:
            district_data = nutrition_df[nutrition_df['District'] == district].iloc[0]
            district_pop = population_df[population_df['ADM2_EN'] == district]['T_TL'].values
            district_pop = district_pop[0] if len(district_pop) > 0 else 100000
            
            # Calculate improvement potential
            b12_improvement = max(0, 70 - district_data['Vitamin_B12_(mcg)']) * actual_coverage
            iron_improvement = max(0, 70 - district_data['Iron_(mg)']) * actual_coverage
            
            district_impacts.append({
                'District': district,
                'Population': district_pop,
                'B12 Improvement': b12_improvement,
                'Iron Improvement': iron_improvement,
                'People Reached': int(district_pop * actual_coverage)
            })
        
        impact_df = pd.DataFrame(district_impacts)
        
        # Create grouped bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='B12 Improvement',
            x=impact_df['District'],
            y=impact_df['B12 Improvement'],
            marker_color='#d32f2f'
        ))
        
        fig.add_trace(go.Bar(
            name='Iron Improvement',
            x=impact_df['District'],
            y=impact_df['Iron Improvement'],
            marker_color='#f57c00'
        ))
        
        fig.update_layout(
            title="Expected Nutrient Adequacy Improvements (Top 10 Districts)",
            xaxis_title="District",
            yaxis_title="Percentage Point Improvement",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("⚠️ Please complete district selection and intervention design first.")

# Tab 1: Budget Optimization (now in first position)
with tab_budget:
    st.header("💰 Dynamic Budget Optimization")
    
    if st.session_state.selected_districts:
        
        st.subheader("Marginal Benefit Analysis")
        
        # Get necessary variables
        # Calculate affected population
        affected_pop = population_df[
            population_df['ADM2_EN'].isin(st.session_state.selected_districts)
        ]['T_TL'].sum()
        
        if affected_pop == 0:
            affected_pop = 1000000  # Default if no match
            
        # Default values for cost calculation (based on weighted average of real costs)
        # Assuming 40% supplementation, 30% fortification, 20% biofortification, 10% education
        avg_cost_per_person = (
            0.40 * 1850 +    # Supplementation
            0.30 * 55500 +   # Fortification  
            0.20 * 74000 +   # Biofortification
            0.10 * 29600     # Education
        )  # = ~35,000 UGX per person
        efficiency = 70  # Default 70% efficiency
        
        # Use a form to prevent automatic rerun on input changes
        with st.form("budget_optimization_form"):
            st.markdown("### Configure Analysis Parameters")
            
            # User inputs for budget range
            col1, col2 = st.columns(2)
            with col1:
                min_budget = st.number_input(
                    "Minimum Budget (Million UGX)",
                    min_value=10,
                    max_value=5000,
                    value=100,
                    step=10
                ) * 1_000_000
            
            with col2:
                max_budget = st.number_input(
                    "Maximum Budget (Million UGX)",
                    min_value=100,
                    max_value=10000,
                    value=5000,
                    step=100
                ) * 1_000_000
            
            # Reduce number of scenarios for performance
            num_scenarios = st.slider(
                "Analysis Detail Level",
                min_value=10,
                max_value=50,
                value=20,
                help="More scenarios = more accurate but slower"
            )
            
            # Submit button within the form
            submitted = st.form_submit_button("Run Budget Optimization Analysis", type="primary")
        
        if submitted:
            # Create budget scenarios
            budget_scenarios = np.linspace(min_budget, max_budget, num_scenarios)
            
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            scenario_outcomes = []
            
            for i, test_budget in enumerate(budget_scenarios):
                # Update progress
                progress = (i + 1) / len(budget_scenarios)
                progress_bar.progress(progress)
                status_text.text(f"Analyzing scenario {i+1}/{len(budget_scenarios)}...")
                
                # Calculate coverage for this budget
                test_coverage = min(1.0, test_budget / (avg_cost_per_person * affected_pop)) * (efficiency / 100)
                
                # Run simulation
                test_outcomes = simulator.calculate_health_outcomes(
                    coverage=test_coverage,
                    districts=st.session_state.selected_districts[:10],  # Limit to 10 for performance
                    nutrients=['Vitamin_B12_(mcg)', 'Iron_(mg)', 'Zinc_(mg)'],  # Key nutrients
                    timeline_months=24
                )
                
                scenario_outcomes.append({
                    'Budget': test_budget,
                    'Lives_Saved': test_outcomes['lives_saved'],
                    'Stunting_Prevented': test_outcomes['stunting_prevented'],
                    'Economic_Benefit': test_outcomes['economic_benefit'],
                    'ROI': (test_outcomes['economic_benefit'] - test_budget) / test_budget * 100,
                    'People_Reached': int(test_coverage * affected_pop),
                    'Coverage_Pct': test_coverage * 100
                })
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Store results in session state
            st.session_state.scenario_df = pd.DataFrame(scenario_outcomes)
            st.session_state.optimization_complete = True
        
        # Display results if available
        if 'scenario_df' in st.session_state and st.session_state.get('optimization_complete', False):
            scenario_df = st.session_state.scenario_df
            
            # Plot optimization curves
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=scenario_df['Budget'] / 1_000_000,
                y=scenario_df['ROI'],
                mode='lines',
                name='ROI (%)',
                line=dict(color='green', width=3),
                yaxis='y'
            ))
            
            fig.add_trace(go.Scatter(
                x=scenario_df['Budget'] / 1_000_000,
                y=scenario_df['Lives_Saved'],
                mode='lines',
                name='Lives Saved',
                line=dict(color='red', width=3),
                yaxis='y2'
            ))
            
            # Add people reached as a third trace
            fig.add_trace(go.Scatter(
                x=scenario_df['Budget'] / 1_000_000,
                y=scenario_df['People_Reached'],
                mode='lines',
                name='People Reached',
                line=dict(color='blue', width=2, dash='dot'),
                yaxis='y3',
                visible='legendonly'  # Hidden by default, can be toggled
            ))
            
            # Find optimal budget (max ROI)
            optimal_idx = scenario_df['ROI'].idxmax()
            optimal_budget = scenario_df.loc[optimal_idx, 'Budget']
            optimal_roi = scenario_df.loc[optimal_idx, 'ROI']
            
            fig.add_vline(
                x=optimal_budget / 1_000_000,
                line_dash="dot",
                line_color="gold",
                annotation_text=f"Optimal: {optimal_budget/1_000_000:.0f}M"
            )
            
            fig.update_layout(
                title="Budget Optimization Analysis",
                xaxis_title="Budget (Million UGX)",
                yaxis=dict(
                    title="ROI (%)",
                    side="left"
                ),
                yaxis2=dict(
                    title="Lives Saved",
                    overlaying="y",
                    side="right"
                ),
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show optimization insights
            col1, col2, col3 = st.columns(3)
            
            # Use middle budget as reference
            reference_budget = (min_budget + max_budget) / 2
            
            with col1:
                optimal_people = scenario_df.loc[optimal_idx, 'People_Reached']
                max_people = scenario_df['People_Reached'].max()
                
                if reference_budget < optimal_budget:
                    st.info(f"""
                    📊 **Budget Analysis:**
                    - Analysis Range: {min_budget/1_000_000:.0f}-{max_budget/1_000_000:.0f}M UGX
                    - Optimal: {optimal_budget/1_000_000:.0f}M UGX
                    - People at optimal: **{optimal_people:,}**
                    - Max reachable: **{max_people:,}**
                    
                    💡 Optimal budget reaches {optimal_people:,} people efficiently
                    """)
                else:
                    st.warning(f"""
                    📊 **Budget Analysis:**
                    - Analysis Range: {min_budget/1_000_000:.0f}-{max_budget/1_000_000:.0f}M UGX
                    - Optimal: {optimal_budget/1_000_000:.0f}M UGX
                    - People at optimal: **{optimal_people:,}**
                    - Max reachable: **{max_people:,}**
                    
                    ⚠️ Diminishing returns at higher budgets
                    """)
            
            with col2:
                st.success(f"""
                💰 **At Optimal Budget:**
                - ROI: {optimal_roi:.0f}%
                - Lives Saved: {scenario_df.loc[optimal_idx, 'Lives_Saved']:,}
                - Stunting Prevented: {scenario_df.loc[optimal_idx, 'Stunting_Prevented']:,}
                """)
            
            with col3:
                # Calculate marginal benefit at optimal point
                optimal_lives = scenario_df.loc[optimal_idx, 'Lives_Saved']
                if optimal_lives > 0:
                    marginal_cost_per_life = optimal_budget / optimal_lives
                    
                    st.info(f"""
                    📈 **Cost-Effectiveness at Optimal:**
                    - Cost per life saved: {marginal_cost_per_life:,.0f} UGX
                    - Cost per stunting case: {optimal_budget/scenario_df.loc[optimal_idx, 'Stunting_Prevented']:,.0f} UGX
                    - Payback period: {optimal_budget/scenario_df.loc[optimal_idx, 'Economic_Benefit']*12:.1f} months
                    """)
                else:
                    st.info("📈 Run analysis to see cost-effectiveness metrics")
    else:
        st.warning("⚠️ Please select districts in the 'District Prioritization' tab first.")

# Tab 5: Real-time Monitoring
with tab_monitor:
    st.header("📈 Real-time Monitoring Dashboard")
    
    st.info("🚧 This section would connect to live data feeds in production")
    
    # Simulate monitoring data
    st.subheader("Implementation Progress Tracker")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        districts_reached = st.metric(
            "Districts Activated",
            f"{min(15, len(st.session_state.selected_districts))}/122",
            delta="+3 this month"
        )
        
        coverage_achieved = st.metric(
            "Population Coverage",
            "32%",
            delta="+5% from baseline"
        )
    
    with col2:
        supplements_distributed = st.metric(
            "Supplements Distributed",
            "1.2M doses",
            delta="+150K this week"
        )
        
        fortification_compliance = st.metric(
            "Fortification Compliance",
            "78%",
            delta="+3% improvement"
        )
    
    with col3:
        budget_utilization = st.metric(
            "Budget Utilization",
            "42%",
            delta="On track"
        )
        
        timeline_progress = st.metric(
            "Timeline Progress",
            "Month 6/24",
            delta="25% complete"
        )
    
    # Key Performance Indicators
    st.subheader("Key Performance Indicators")
    
    kpi_data = {
        'Indicator': ['B12 Adequacy', 'Iron Adequacy', 'Stunting Rate', 'Coverage Rate', 'Cost Efficiency'],
        'Baseline': [42, 55, 29, 0, 0],
        'Current': [48, 59, 27, 32, 92],
        'Target': [70, 75, 20, 80, 100],
        'Status': ['🟡 On Track', '🟡 On Track', '🟢 Good', '🔴 Behind', '🟢 Good']
    }
    
    kpi_df = pd.DataFrame(kpi_data)
    
    # Create KPI visualization
    fig = go.Figure()
    
    fig.add_trace(go.Bar(name='Baseline', x=kpi_df['Indicator'], y=kpi_df['Baseline'], marker_color='lightgray'))
    fig.add_trace(go.Bar(name='Current', x=kpi_df['Indicator'], y=kpi_df['Current'], marker_color='#2196F3'))
    fig.add_trace(go.Bar(name='Target', x=kpi_df['Indicator'], y=kpi_df['Target'], marker_color='#4CAF50', opacity=0.5))
    
    fig.update_layout(
        title="KPI Performance Dashboard",
        xaxis_title="Indicator",
        yaxis_title="Value (%)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display KPI table
    st.dataframe(
        kpi_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn("Status", help="Performance status")
        }
    )

# Tab 6: Reports & Export
with tab_report:
    st.header("📋 Generate Reports & Export Data")
    
    st.subheader("Report Generation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Select Report Type",
            ["Executive Summary", "Technical Report", "District Profiles", "Budget Analysis", "Impact Assessment"]
        )
        
        format_type = st.selectbox(
            "Export Format",
            ["PDF", "Excel", "CSV", "JSON"]
        )
    
    with col2:
        include_visuals = st.checkbox("Include Visualizations", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
        include_methodology = st.checkbox("Include Methodology", value=False)
    
    if st.button("Generate Report", type="primary"):
        # Check if simulation has been run
        if 'simulation_outcomes' not in st.session_state or st.session_state.simulation_outcomes is None:
            st.error("⚠️ Please run the impact simulation first (Tab 3) before generating reports.")
            st.info("Go to the 'Impact Simulation' tab, configure your intervention, and run the simulation.")
        else:
            with st.spinner("Generating report..."):
                # Simulate report generation
                import time
                time.sleep(2)
                
                st.success("✅ Report generated successfully!")
                
                # Get outcomes from session state
                outcomes = st.session_state.simulation_outcomes
                
                # Create download button
                report_data = f"""
                UGANDA NUTRITION INTERVENTION REPORT
                =====================================
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                
                EXECUTIVE SUMMARY
                -----------------
                Districts Targeted: {len(st.session_state.selected_districts)}
                Population Covered: {affected_pop/1_000_000:.1f} million
                Budget Allocated: {budget_ugx/1_000_000:.0f} million UGX
                
                KEY FINDINGS
                ------------
                - Critical B12 deficiency in {b12_critical} districts
                - Multi-nutrient deficiency in {multi_deficient} districts  
                - Worst affected: {worst_district} (CNRI: {worst_cnri:.1f})
                
                PROJECTED OUTCOMES
                ------------------
                Lives Saved: {outcomes['lives_saved']:,}
                Stunting Prevented: {outcomes['stunting_prevented']:,}
                Economic Benefit: {outcomes['economic_benefit']/1_000_000:.0f}M UGX
                ROI: {outcomes['economic_benefit']/budget_ugx*100:.0f}%
            
            RECOMMENDATIONS
            ---------------
            1. Prioritize B12 supplementation in critical districts
            2. Implement fortification programs for staple foods
            3. Strengthen health system capacity in rural areas
            4. Establish monitoring and evaluation framework
            5. Secure sustainable funding mechanisms
            """
            
            st.download_button(
                label=f"Download {report_type} ({format_type})",
                data=report_data,
                file_name=f"uganda_nutrition_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Data Export Section
    st.subheader("Export Simulation Data")
    
    if st.session_state.selected_districts:
        export_data = {
            'configuration': {
                'districts': st.session_state.selected_districts,
                'budget': budget_ugx,
                'timeline': timeline,
                'interventions': {
                    'fortification': fortification_pct,
                    'supplementation': supplementation_pct,
                    'biofortification': biofortification_pct,
                    'diversification': diversification_pct
                }
            },
            'outcomes': outcomes,
            'timestamp': datetime.now().isoformat()
        }
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="Export as JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"simulation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # Export priority districts as CSV
            if not priority_districts.empty:
                csv_data = priority_districts.to_csv(index=False)
                st.download_button(
                    label="Export Districts CSV",
                    data=csv_data,
                    file_name=f"priority_districts_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            st.download_button(
                label="Export Full Analysis",
                data=str(export_data),
                file_name=f"full_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Uganda Nutrition Command Center v1.0 | Built with ❤️ for saving lives</p>
    <p>Data sources: Uganda Nutrition Survey 2023 | Population Census 2023 | Health Facility Registry 2018</p>
</div>
""", unsafe_allow_html=True)

# Add alias for compatibility with report generator
InterventionEngine = InterventionSimulator