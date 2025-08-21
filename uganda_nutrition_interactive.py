"""
Uganda Nutrition Interactive Dashboard
=======================================
Enhanced interactive version of the nutrition analysis with intervention planning
Combines analysis capabilities with intervention simulation features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import base64

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Uganda Nutrition Intervention Dashboard",
    page_icon="🇺🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3d59;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #ff6e40;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTab {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load all required datasets"""
    nutrition_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/uganda-consumption-adequacy-all-nutrients.csv')
    health_facilities_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/ug2/national-health-facility-master-list-2018-health-facility-level-by-district.csv')
    population_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/ug2/uga_admpop_adm2_2023.csv')
    
    # Clean district names
    nutrition_df['District'] = nutrition_df['District'].str.upper().str.strip()
    population_df['District'] = population_df['ADM2_EN'].str.upper().str.strip()
    
    # Merge population data
    nutrition_df = nutrition_df.merge(
        population_df[['District', 'T_TL']], 
        on='District', 
        how='left'
    )
    nutrition_df.rename(columns={'T_TL': 'Population'}, inplace=True)
    nutrition_df['Population'].fillna(50000, inplace=True)  # Default for missing
    
    return nutrition_df, health_facilities_df, population_df

# Classification functions
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

def calculate_cnri(df, nutrients):
    """Calculate Composite Nutritional Risk Index"""
    df['Critical_Count'] = 0
    df['Severe_Count'] = 0
    df['Moderate_Count'] = 0
    
    for nutrient in nutrients:
        df['Critical_Count'] += (df[nutrient] < 30).astype(int)
        df['Severe_Count'] += ((df[nutrient] >= 30) & (df[nutrient] < 50)).astype(int)
        df['Moderate_Count'] += ((df[nutrient] >= 50) & (df[nutrient] < 70)).astype(int)
    
    df['CNRI'] = (
        (df['Critical_Count'] * 3) + 
        (df['Severe_Count'] * 2) + 
        (df['Moderate_Count'] * 1)
    ) / len(nutrients)
    
    return df

# Economic analysis functions
def calculate_intervention_cost(population, coverage, cost_per_person, duration_months):
    """Calculate total intervention cost"""
    target_population = population * (coverage / 100)
    monthly_cost = target_population * cost_per_person
    total_cost = monthly_cost * duration_months
    return total_cost, target_population

def calculate_roi(cost, health_benefit, economic_benefit):
    """Calculate Return on Investment"""
    total_benefit = health_benefit + economic_benefit
    roi = ((total_benefit - cost) / cost) * 100
    benefit_cost_ratio = total_benefit / cost
    return roi, benefit_cost_ratio

def estimate_health_impact(baseline_adequacy, target_adequacy, population, coverage):
    """Estimate health impact of intervention"""
    improvement = target_adequacy - baseline_adequacy
    affected_population = population * (coverage / 100)
    
    # Estimate DALYs averted (simplified model)
    dalys_per_point = 0.01  # DALYs averted per 1% improvement
    dalys_averted = improvement * dalys_per_point * affected_population / 1000
    
    # Economic value of health improvement
    value_per_daly = 1000  # USD per DALY averted
    health_benefit = dalys_averted * value_per_daly
    
    return {
        'improvement_points': improvement,
        'affected_population': affected_population,
        'dalys_averted': dalys_averted,
        'health_benefit_usd': health_benefit
    }

# Main application
def main():
    st.markdown('<h1 class="main-header">🇺🇬 Uganda Nutrition Intervention Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    nutrition_df, health_facilities_df, population_df = load_data()
    nutrients = [col for col in nutrition_df.columns if col not in ['District', 'Population']]
    
    # Calculate CNRI
    nutrition_df = calculate_cnri(nutrition_df, nutrients)
    
    # Sidebar for user inputs
    st.sidebar.header("🎯 Intervention Parameters")
    
    # Budget input methods
    budget_method = st.sidebar.radio(
        "Budget Input Method",
        ["Simple Input", "Percentage of GDP", "Per Person Allocation"]
    )
    
    if budget_method == "Simple Input":
        total_budget = st.sidebar.number_input(
            "Total Budget (USD)",
            min_value=100000,
            max_value=100000000,
            value=10000000,
            step=100000,
            help="Enter the total budget available for interventions"
        )
    elif budget_method == "Percentage of GDP":
        gdp_percentage = st.sidebar.slider(
            "Percentage of Health Budget (%)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1
        )
        total_budget = 500000000 * (gdp_percentage / 100)  # Assuming $500M health budget
        st.sidebar.info(f"Calculated Budget: ${total_budget:,.0f}")
    else:
        per_person = st.sidebar.number_input(
            "Budget per Person (USD)",
            min_value=1,
            max_value=100,
            value=10,
            step=1
        )
        total_population = nutrition_df['Population'].sum()
        total_budget = per_person * total_population * 0.1  # Assume 10% coverage initially
        st.sidebar.info(f"Calculated Budget: ${total_budget:,.0f}")
    
    # Target population selection
    st.sidebar.subheader("Target Population")
    target_groups = st.sidebar.multiselect(
        "Select Target Groups",
        ["Children Under 5", "Pregnant Women", "Lactating Mothers", "Elderly", "General Population"],
        default=["Children Under 5", "Pregnant Women"]
    )
    
    coverage_target = st.sidebar.slider(
        "Coverage Target (%)",
        min_value=10,
        max_value=100,
        value=50,
        step=5,
        help="Percentage of target population to reach"
    )
    
    # Intervention mix
    st.sidebar.subheader("Intervention Mix")
    
    fortification_pct = st.sidebar.slider("Fortification (%)", 0, 100, 40)
    supplementation_pct = st.sidebar.slider("Supplementation (%)", 0, 100, 30)
    education_pct = st.sidebar.slider("Education (%)", 0, 100, 20)
    infrastructure_pct = 100 - fortification_pct - supplementation_pct - education_pct
    
    if infrastructure_pct < 0:
        st.sidebar.error("Total exceeds 100%. Please adjust.")
        infrastructure_pct = 0
    else:
        st.sidebar.info(f"Infrastructure: {infrastructure_pct}%")
    
    # Duration
    intervention_duration = st.sidebar.slider(
        "Intervention Duration (months)",
        min_value=3,
        max_value=60,
        value=12,
        step=3
    )
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Current Situation",
        "🎯 District Prioritization", 
        "💰 Budget Optimization",
        "📈 Impact Simulation",
        "🔄 Scenario Comparison",
        "📄 Generate Report"
    ])
    
    with tab1:
        st.header("Current Nutritional Status")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            critical_districts = len(nutrition_df[nutrition_df['Critical_Count'] > 3])
            st.metric("Critical Districts", critical_districts, delta="-5 vs last year", delta_color="inverse")
        
        with col2:
            avg_adequacy = nutrition_df[nutrients].mean().mean()
            st.metric("Average Adequacy", f"{avg_adequacy:.1f}%", delta="+2.3%")
        
        with col3:
            total_pop = nutrition_df['Population'].sum()
            st.metric("Total Population", f"{total_pop/1e6:.1f}M")
        
        with col4:
            worst_nutrient = nutrition_df[nutrients].mean().idxmin()
            worst_value = nutrition_df[nutrients].mean().min()
            st.metric("Most Deficient", worst_nutrient.split('_')[0], f"{worst_value:.1f}%")
        
        # Heatmap of top districts
        st.subheader("Nutritional Adequacy Heatmap - Top 30 Most Affected Districts")
        
        top_districts = nutrition_df.nlargest(30, 'CNRI')
        heatmap_data = top_districts.set_index('District')[nutrients].T
        
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="District", y="Nutrient", color="Adequacy %"),
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
            height=600
        )
        fig_heatmap.update_layout(
            xaxis_tickangle=-45,
            font=dict(size=10)
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Severity distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Severity Distribution by Nutrient")
            severity_data = []
            for nutrient in nutrients[:6]:  # Top 6 for visibility
                for _, row in nutrition_df.iterrows():
                    severity_data.append({
                        'Nutrient': nutrient.split('_')[0],
                        'Severity': classify_severity(row[nutrient])
                    })
            
            severity_df = pd.DataFrame(severity_data)
            fig_severity = px.histogram(
                severity_df,
                x='Nutrient',
                color='Severity',
                color_discrete_map={'Critical': '#d32f2f', 'Severe': '#f57c00', 
                                   'Moderate': '#fbc02d', 'Adequate': '#388e3c'},
                height=400
            )
            st.plotly_chart(fig_severity, use_container_width=True)
        
        with col2:
            st.subheader("Regional Risk Distribution")
            # Group districts by risk level
            risk_distribution = pd.DataFrame({
                'Risk Level': ['Critical', 'High', 'Medium', 'Low'],
                'Districts': [
                    len(nutrition_df[nutrition_df['CNRI'] > 2]),
                    len(nutrition_df[(nutrition_df['CNRI'] > 1.5) & (nutrition_df['CNRI'] <= 2)]),
                    len(nutrition_df[(nutrition_df['CNRI'] > 1) & (nutrition_df['CNRI'] <= 1.5)]),
                    len(nutrition_df[nutrition_df['CNRI'] <= 1])
                ]
            })
            
            fig_risk = px.pie(
                risk_distribution,
                values='Districts',
                names='Risk Level',
                color_discrete_map={'Critical': '#d32f2f', 'High': '#f57c00', 
                                   'Medium': '#fbc02d', 'Low': '#388e3c'},
                height=400
            )
            st.plotly_chart(fig_risk, use_container_width=True)
    
    with tab2:
        st.header("District Prioritization for Interventions")
        
        # Prioritization criteria
        col1, col2, col3 = st.columns(3)
        
        with col1:
            weight_severity = st.slider("Weight: Severity", 0.0, 1.0, 0.4, 0.1)
        with col2:
            weight_population = st.slider("Weight: Population", 0.0, 1.0, 0.3, 0.1)
        with col3:
            weight_feasibility = st.slider("Weight: Feasibility", 0.0, 1.0, 0.3, 0.1)
        
        # Normalize weights
        total_weight = weight_severity + weight_population + weight_feasibility
        if total_weight > 0:
            weight_severity /= total_weight
            weight_population /= total_weight
            weight_feasibility /= total_weight
        
        # Calculate priority score
        nutrition_df['Priority_Score'] = (
            nutrition_df['CNRI'] * weight_severity * 100 +
            (nutrition_df['Population'] / nutrition_df['Population'].max()) * weight_population * 100 +
            (1 - nutrition_df['CNRI']/nutrition_df['CNRI'].max()) * weight_feasibility * 100
        )
        
        # Show top priority districts
        priority_districts = nutrition_df.nlargest(20, 'Priority_Score')[
            ['District', 'Priority_Score', 'CNRI', 'Population', 'Critical_Count']
        ]
        
        st.subheader("Top 20 Priority Districts")
        
        # Interactive bar chart
        fig_priority = px.bar(
            priority_districts,
            x='Priority_Score',
            y='District',
            orientation='h',
            color='CNRI',
            color_continuous_scale='Reds',
            hover_data=['Population', 'Critical_Count'],
            height=600
        )
        fig_priority.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_priority, use_container_width=True)
        
        # Detailed table
        st.subheader("Detailed Priority Matrix")
        st.dataframe(
            priority_districts.style.background_gradient(subset=['Priority_Score', 'CNRI']),
            use_container_width=True
        )
    
    with tab3:
        st.header("Budget Optimization Analysis")
        
        # Cost parameters
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Cost per Intervention Type")
            cost_fortification = st.number_input("Fortification ($/person/month)", 0.5, 10.0, 2.0, 0.5)
            cost_supplementation = st.number_input("Supplementation ($/person/month)", 1.0, 20.0, 5.0, 1.0)
            cost_education = st.number_input("Education ($/person/month)", 0.1, 5.0, 1.0, 0.1)
            cost_infrastructure = st.number_input("Infrastructure ($/facility)", 1000, 100000, 10000, 1000)
        
        with col2:
            st.subheader("Budget Allocation")
            
            # Calculate allocations
            budget_fortification = total_budget * (fortification_pct / 100)
            budget_supplementation = total_budget * (supplementation_pct / 100)
            budget_education = total_budget * (education_pct / 100)
            budget_infrastructure = total_budget * (infrastructure_pct / 100)
            
            allocation_df = pd.DataFrame({
                'Intervention': ['Fortification', 'Supplementation', 'Education', 'Infrastructure'],
                'Budget': [budget_fortification, budget_supplementation, budget_education, budget_infrastructure],
                'Percentage': [fortification_pct, supplementation_pct, education_pct, infrastructure_pct]
            })
            
            fig_allocation = px.pie(
                allocation_df,
                values='Budget',
                names='Intervention',
                hole=0.4,
                height=400
            )
            fig_allocation.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_allocation, use_container_width=True)
        
        # Coverage analysis
        st.subheader("Coverage Analysis by Budget")
        
        # Calculate coverage for each intervention type
        total_target_pop = nutrition_df['Population'].sum() * 0.3  # Assume 30% are vulnerable
        
        coverage_fort = min(100, (budget_fortification / (cost_fortification * intervention_duration)) / total_target_pop * 100)
        coverage_supp = min(100, (budget_supplementation / (cost_supplementation * intervention_duration)) / total_target_pop * 100)
        coverage_edu = min(100, (budget_education / (cost_education * intervention_duration)) / total_target_pop * 100)
        
        coverage_data = pd.DataFrame({
            'Intervention': ['Fortification', 'Supplementation', 'Education'],
            'Coverage (%)': [coverage_fort, coverage_supp, coverage_edu],
            'People Reached': [
                total_target_pop * coverage_fort / 100,
                total_target_pop * coverage_supp / 100,
                total_target_pop * coverage_edu / 100
            ]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_coverage = px.bar(
                coverage_data,
                x='Intervention',
                y='Coverage (%)',
                color='Coverage (%)',
                color_continuous_scale='Viridis',
                height=350
            )
            st.plotly_chart(fig_coverage, use_container_width=True)
        
        with col2:
            fig_people = px.bar(
                coverage_data,
                x='Intervention',
                y='People Reached',
                color='People Reached',
                color_continuous_scale='Blues',
                height=350
            )
            st.plotly_chart(fig_people, use_container_width=True)
        
        # ROI Analysis
        st.subheader("Return on Investment Analysis")
        
        # Calculate ROI for each intervention
        roi_data = []
        for idx, row in coverage_data.iterrows():
            intervention = row['Intervention']
            people = row['People Reached']
            
            if intervention == 'Fortification':
                cost = max(1, budget_fortification)  # Avoid division by zero
                health_impact = estimate_health_impact(50, 75, people, 100)
            elif intervention == 'Supplementation':
                cost = max(1, budget_supplementation)
                health_impact = estimate_health_impact(50, 80, people, 100)
            else:
                cost = max(1, budget_education)
                health_impact = estimate_health_impact(50, 65, people, 100)
            
            roi, bcr = calculate_roi(cost, health_impact['health_benefit_usd'], 0)
            
            # Ensure valid values
            roi = min(1000, max(-100, roi)) if not np.isnan(roi) and not np.isinf(roi) else 0
            bcr = min(100, max(0, bcr)) if not np.isnan(bcr) and not np.isinf(bcr) else 0
            
            roi_data.append({
                'Intervention': intervention,
                'Cost': cost,
                'Health Benefit': health_impact['health_benefit_usd'],
                'ROI (%)': roi,
                'Benefit-Cost Ratio': bcr,
                'Size': abs(roi) + 10  # For bubble size
            })
        
        roi_df = pd.DataFrame(roi_data)
        
        fig_roi = px.scatter(
            roi_df,
            x='Cost',
            y='Health Benefit',
            size='Size',
            color='Intervention',
            hover_data=['ROI (%)', 'Benefit-Cost Ratio'],
            height=400,
            title="Cost-Benefit Analysis"
        )
        st.plotly_chart(fig_roi, use_container_width=True)
        
        st.dataframe(roi_df.style.format({
            'Cost': '${:,.0f}',
            'Health Benefit': '${:,.0f}',
            'ROI (%)': '{:.1f}%',
            'Benefit-Cost Ratio': '{:.2f}'
        }), use_container_width=True)
    
    with tab4:
        st.header("Impact Simulation")
        
        # Simulation parameters
        col1, col2 = st.columns(2)
        
        with col1:
            simulation_years = st.slider("Simulation Period (years)", 1, 5, 3)
            discount_rate = st.slider("Discount Rate (%)", 0, 10, 3)
        
        with col2:
            effectiveness_fort = st.slider("Fortification Effectiveness (%)", 50, 100, 75)
            effectiveness_supp = st.slider("Supplementation Effectiveness (%)", 50, 100, 85)
            effectiveness_edu = st.slider("Education Effectiveness (%)", 30, 80, 50)
        
        # Run simulation
        st.subheader("Projected Impact Over Time")
        
        # Create timeline data
        months = range(0, simulation_years * 12 + 1, 3)
        timeline_data = []
        
        for month in months:
            # Simple growth model
            coverage_growth = min(1.0, month / (simulation_years * 12))
            
            fort_impact = budget_fortification * effectiveness_fort / 100 * coverage_growth
            supp_impact = budget_supplementation * effectiveness_supp / 100 * coverage_growth
            edu_impact = budget_education * effectiveness_edu / 100 * coverage_growth
            
            # Estimate improvement in adequacy
            baseline = 50  # Average baseline adequacy
            improvement = (fort_impact + supp_impact + edu_impact) / total_budget * 20  # Max 20% improvement
            
            timeline_data.append({
                'Month': month,
                'Adequacy (%)': baseline + improvement * coverage_growth,
                'Coverage (%)': coverage_growth * 100,
                'DALYs Averted': improvement * coverage_growth * 1000
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        
        # Create subplots
        fig_timeline = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Nutritional Adequacy Improvement', 'Population Coverage',
                          'DALYs Averted', 'Cost-Effectiveness Over Time'),
            specs=[[{'secondary_y': False}, {'secondary_y': False}],
                   [{'secondary_y': False}, {'secondary_y': True}]]
        )
        
        # Adequacy improvement
        fig_timeline.add_trace(
            go.Scatter(x=timeline_df['Month'], y=timeline_df['Adequacy (%)'],
                      mode='lines+markers', name='Adequacy',
                      line=dict(color='green', width=2)),
            row=1, col=1
        )
        
        # Coverage
        fig_timeline.add_trace(
            go.Scatter(x=timeline_df['Month'], y=timeline_df['Coverage (%)'],
                      mode='lines+markers', name='Coverage',
                      line=dict(color='blue', width=2)),
            row=1, col=2
        )
        
        # DALYs averted
        fig_timeline.add_trace(
            go.Bar(x=timeline_df['Month'], y=timeline_df['DALYs Averted'],
                   name='DALYs Averted', marker_color='orange'),
            row=2, col=1
        )
        
        # Cost-effectiveness
        cumulative_cost = [(total_budget / (simulation_years * 12)) * m for m in timeline_df['Month']]
        cost_per_daly = [c / (d + 1) for c, d in zip(cumulative_cost, timeline_df['DALYs Averted'].cumsum())]
        
        fig_timeline.add_trace(
            go.Scatter(x=timeline_df['Month'], y=cost_per_daly,
                      mode='lines', name='Cost per DALY',
                      line=dict(color='red', width=2)),
            row=2, col=2
        )
        
        fig_timeline.update_layout(height=700, showlegend=True)
        fig_timeline.update_xaxes(title_text="Months", row=2)
        fig_timeline.update_yaxes(title_text="Percentage", row=1, col=1)
        fig_timeline.update_yaxes(title_text="Percentage", row=1, col=2)
        fig_timeline.update_yaxes(title_text="DALYs", row=2, col=1)
        fig_timeline.update_yaxes(title_text="USD per DALY", row=2, col=2)
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Impact summary
        st.subheader("Projected Impact Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        final_adequacy = timeline_df.iloc[-1]['Adequacy (%)']
        total_dalys = timeline_df['DALYs Averted'].sum()
        final_coverage = timeline_df.iloc[-1]['Coverage (%)']
        avg_cost_per_daly = np.mean(cost_per_daly)
        
        with col1:
            st.metric("Final Adequacy", f"{final_adequacy:.1f}%", 
                     f"+{final_adequacy - 50:.1f}%")
        
        with col2:
            st.metric("Total DALYs Averted", f"{total_dalys:,.0f}")
        
        with col3:
            st.metric("Population Coverage", f"{final_coverage:.1f}%")
        
        with col4:
            st.metric("Avg Cost per DALY", f"${avg_cost_per_daly:.2f}")
    
    with tab5:
        st.header("Scenario Comparison")
        
        # Define scenarios
        scenarios = {
            "Current Plan": {
                "budget": total_budget,
                "fortification": fortification_pct,
                "supplementation": supplementation_pct,
                "education": education_pct,
                "infrastructure": infrastructure_pct
            },
            "Fortification Focus": {
                "budget": total_budget,
                "fortification": 60,
                "supplementation": 20,
                "education": 10,
                "infrastructure": 10
            },
            "Balanced Approach": {
                "budget": total_budget,
                "fortification": 25,
                "supplementation": 25,
                "education": 25,
                "infrastructure": 25
            },
            "High Budget": {
                "budget": total_budget * 1.5,
                "fortification": fortification_pct,
                "supplementation": supplementation_pct,
                "education": education_pct,
                "infrastructure": infrastructure_pct
            }
        }
        
        # Calculate outcomes for each scenario
        scenario_results = []
        
        for scenario_name, params in scenarios.items():
            # Calculate coverage
            budget = params['budget']
            fort_budget = budget * params['fortification'] / 100
            supp_budget = budget * params['supplementation'] / 100
            edu_budget = budget * params['education'] / 100
            
            # Simple outcome calculation
            total_coverage = (
                (fort_budget / (cost_fortification * 12) / total_target_pop * 100 * 0.3) +
                (supp_budget / (cost_supplementation * 12) / total_target_pop * 100 * 0.4) +
                (edu_budget / (cost_education * 12) / total_target_pop * 100 * 0.3)
            )
            
            improvement = total_coverage * 0.3  # Simplified improvement calculation
            dalys = improvement * 1000
            cost_effectiveness = budget / (dalys + 1)
            
            scenario_results.append({
                'Scenario': scenario_name,
                'Budget': budget,
                'Coverage (%)': min(100, total_coverage),
                'Adequacy Improvement': improvement,
                'DALYs Averted': dalys,
                'Cost per DALY': cost_effectiveness
            })
        
        scenario_df = pd.DataFrame(scenario_results)
        
        # Comparison visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig_coverage = px.bar(
                scenario_df,
                x='Scenario',
                y='Coverage (%)',
                color='Coverage (%)',
                color_continuous_scale='Viridis',
                title='Coverage Comparison',
                height=350
            )
            st.plotly_chart(fig_coverage, use_container_width=True)
        
        with col2:
            fig_dalys = px.bar(
                scenario_df,
                x='Scenario',
                y='DALYs Averted',
                color='DALYs Averted',
                color_continuous_scale='Blues',
                title='Health Impact Comparison',
                height=350
            )
            st.plotly_chart(fig_dalys, use_container_width=True)
        
        # Radar chart for multi-dimensional comparison
        st.subheader("Multi-Dimensional Scenario Comparison")
        
        categories = ['Coverage', 'Health Impact', 'Cost-Effectiveness', 'Feasibility']
        
        fig_radar = go.Figure()
        
        for _, row in scenario_df.iterrows():
            values = [
                row['Coverage (%)'],
                row['DALYs Averted'] / scenario_df['DALYs Averted'].max() * 100,
                (1 / row['Cost per DALY']) * 1000,
                np.random.uniform(60, 90)  # Simulated feasibility score
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=row['Scenario']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Detailed comparison table
        st.subheader("Detailed Scenario Comparison")
        st.dataframe(
            scenario_df.style.format({
                'Budget': '${:,.0f}',
                'Coverage (%)': '{:.1f}%',
                'Adequacy Improvement': '{:.1f}',
                'DALYs Averted': '{:,.0f}',
                'Cost per DALY': '${:.2f}'
            }).background_gradient(subset=['Coverage (%)', 'DALYs Averted']),
            use_container_width=True
        )
        
        # Recommendation
        best_scenario = scenario_df.loc[scenario_df['DALYs Averted'].idxmax()]
        st.success(f"**Recommended Scenario:** {best_scenario['Scenario']} - "
                  f"Achieves {best_scenario['DALYs Averted']:,.0f} DALYs averted with "
                  f"{best_scenario['Coverage (%)']:.1f}% coverage")
    
    with tab6:
        st.header("Generate Comprehensive Report")
        
        report_type = st.radio(
            "Select Report Type",
            ["Executive Summary", "Technical Report", "Implementation Plan", "Full Report"]
        )
        
        include_sections = st.multiselect(
            "Include Sections",
            ["Current Situation", "District Prioritization", "Budget Analysis", 
             "Impact Projections", "Recommendations", "Appendices"],
            default=["Current Situation", "District Prioritization", "Budget Analysis", "Recommendations"]
        )
        
        if st.button("Generate PDF Report", type="primary"):
            # Generate PDF report
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1e3d59'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            # Build content
            story = []
            
            # Title page
            story.append(Paragraph("Uganda Nutrition Intervention Report", title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
            story.append(PageBreak())
            
            # Executive Summary
            if "Current Situation" in include_sections:
                story.append(Paragraph("Executive Summary", styles['Heading1']))
                summary_text = f"""
                <para>
                Uganda faces significant nutritional challenges across {len(nutrition_df)} districts, 
                with {len(nutrition_df[nutrition_df['Critical_Count'] > 3])} districts in critical condition. 
                The average nutritional adequacy stands at {nutrition_df[nutrients].mean().mean():.1f}%, 
                with {worst_nutrient.split('_')[0]} being the most deficient nutrient at {worst_value:.1f}% adequacy.
                </para>
                
                <para spaceBefore="12">
                With a budget of ${total_budget:,.0f}, the proposed intervention strategy allocates 
                {fortification_pct}% to fortification, {supplementation_pct}% to supplementation, 
                {education_pct}% to education, and {infrastructure_pct}% to infrastructure development.
                </para>
                
                <para spaceBefore="12">
                The intervention is projected to reach {coverage_target}% of the target population over 
                {intervention_duration} months, potentially averting {total_dalys:,.0f} DALYs and improving 
                nutritional adequacy by {final_adequacy - 50:.1f} percentage points.
                </para>
                """
                story.append(Paragraph(summary_text, styles['Normal']))
                story.append(PageBreak())
            
            # Priority Districts
            if "District Prioritization" in include_sections:
                story.append(Paragraph("Priority Districts for Intervention", styles['Heading1']))
                
                # Create table data
                priority_data = [['District', 'Priority Score', 'CNRI', 'Population']]
                for _, row in priority_districts.head(10).iterrows():
                    priority_data.append([
                        row['District'],
                        f"{row['Priority_Score']:.1f}",
                        f"{row['CNRI']:.2f}",
                        f"{row['Population']:,.0f}"
                    ])
                
                # Create table
                priority_table = Table(priority_data)
                priority_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3d59')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(priority_table)
                story.append(PageBreak())
            
            # Recommendations
            if "Recommendations" in include_sections:
                story.append(Paragraph("Key Recommendations", styles['Heading1']))
                recommendations = """
                <para>
                1. <b>Immediate Action:</b> Focus on the top 20 priority districts identified through the CNRI analysis, 
                particularly those with multiple critical nutrient deficiencies.
                </para>
                
                <para spaceBefore="12">
                2. <b>Intervention Mix:</b> Implement a balanced approach combining fortification for broad coverage, 
                supplementation for severe cases, and education for long-term behavioral change.
                </para>
                
                <para spaceBefore="12">
                3. <b>Monitoring:</b> Establish robust monitoring systems to track progress and adjust strategies 
                based on real-time data.
                </para>
                
                <para spaceBefore="12">
                4. <b>Partnerships:</b> Engage with international organizations, NGOs, and private sector partners 
                to maximize resources and expertise.
                </para>
                
                <para spaceBefore="12">
                5. <b>Sustainability:</b> Develop local capacity and infrastructure to ensure long-term sustainability 
                of nutrition improvements.
                </para>
                """
                story.append(Paragraph(recommendations, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            pdf_buffer.seek(0)
            
            # Provide download button
            b64 = base64.b64encode(pdf_buffer.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="uganda_nutrition_report.pdf">Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            st.success("Report generated successfully! Click the link above to download.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            Uganda Nutrition Intervention Dashboard v2.0 | 
            Data sources: Uganda Nutrition Survey 2024 | 
            Last updated: {date}
        </div>
        """.format(date=datetime.now().strftime('%Y-%m-%d')),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()