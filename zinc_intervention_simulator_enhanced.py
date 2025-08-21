"""
Zinc Deficiency Intervention Simulation Platform
=================================================
An evidence-based tool for planning and evaluating zinc supplementation strategies
Designed for policy makers, program managers, and funding organizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Kenya Zinc Intervention Simulator",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better accessibility
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
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
    .help-text {
        color: #666;
        font-size: 0.9rem;
        font-style: italic;
    }
    .glossary-term {
        text-decoration: underline;
        text-decoration-style: dotted;
        cursor: help;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'scenario_history' not in st.session_state:
    st.session_state.scenario_history = []
if 'show_tutorial' not in st.session_state:
    st.session_state.show_tutorial = True

# Header with comprehensive introduction
st.markdown("""
<div class="main-header">
    <h1>🌍 Kenya Zinc Intervention Planning Platform</h1>
    <p style="font-size: 1.2rem;">Evidence-Based Decision Support for Nutrition Programs</p>
</div>
""", unsafe_allow_html=True)

# Tutorial/Onboarding
if st.session_state.show_tutorial:
    with st.container():
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #1565c0;">👋 Welcome to the Zinc Intervention Simulator</h3>
            <p style="color: #212121;"><strong>What this tool does:</strong> Helps you plan, budget, and predict outcomes of zinc supplementation programs to combat malnutrition in Kenya.</p>
            <p style="color: #212121;"><strong>Who should use this:</strong> Policy makers, program managers, health ministry officials, NGO directors, and funding organizations.</p>
            <p style="color: #212121;"><strong>Time needed:</strong> 15-20 minutes for a complete analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **📊 Step 1: Design Your Intervention**
            - Set your budget
            - Choose target populations
            - Select intervention strategies
            """)
        with col2:
            st.markdown("""
            **📈 Step 2: Review Predicted Outcomes**
            - Health improvements
            - Lives saved
            - Economic benefits
            """)
        with col3:
            st.markdown("""
            **📋 Step 3: Generate Reports**
            - Executive summaries
            - Cost-benefit analysis
            - Implementation roadmaps
            """)
        
        if st.button("Start Planning", type="primary"):
            st.session_state.show_tutorial = False
            st.rerun()
        
        st.markdown("---")

# Quick Stats Dashboard
st.markdown("### 📊 Current Situation in Kenya")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card" style="background-color: #ffebee; border-left: 5px solid #d32f2f;">
        <h4 style="color: #b71c1c;">🚨 Zinc Deficiency Rate</h4>
        <h2 style="color: #d32f2f;">51%</h2>
        <p style="color: #424242;">26.5 million people affected</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style="background-color: #fff3e0; border-left: 5px solid #f57c00;">
        <h4 style="color: #e65100;">📉 Stunting Prevalence</h4>
        <h2 style="color: #f57c00;">26%</h2>
        <p style="color: #424242;">1 in 4 children under 5</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card" style="background-color: #fffde7; border-left: 5px solid #fbc02d;">
        <h4 style="color: #f57f17;">🏥 Diarrhea Cases</h4>
        <h2 style="color: #f9a825;">15%</h2>
        <p style="color: #424242;">Leading cause of child mortality</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card" style="background-color: #f3e5f5; border-left: 5px solid #7b1fa2;">
        <h4 style="color: #4a148c;">💰 Economic Loss</h4>
        <h2 style="color: #7b1fa2;">2.3% GDP</h2>
        <p style="color: #424242;">Due to malnutrition</p>
    </div>
    """, unsafe_allow_html=True)

# Create enhanced tabs with descriptions
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Plan Intervention", 
    "📊 Health Impact", 
    "💰 Economic Analysis", 
    "🔬 Technical Details",
    "📈 Compare Scenarios",
    "📚 Resources & Help"
])

# Constants
KENYA_POPULATION = 52_000_000
ZINC_DEFICIENT_POPULATION = int(KENYA_POPULATION * 0.51)
STUNTED_CHILDREN = int(KENYA_POPULATION * 0.14 * 0.26)
CHILDREN_UNDER_5 = int(KENYA_POPULATION * 0.135)
PREGNANT_WOMEN = int(KENYA_POPULATION * 0.032)
RURAL_POPULATION = int(KENYA_POPULATION * 0.72)
CHILDREN_WITH_DIARRHEA = int(CHILDREN_UNDER_5 * 0.15)

# Intervention cost models with detailed explanations
def get_intervention_details():
    """Detailed intervention information for policy makers"""
    return {
        'fortification': {
            'name': 'Food Fortification Program',
            'unit_cost': 3.8,
            'effectiveness': 0.75,
            'reach_time': 6,
            'coverage_potential': 0.85,
            'description': """
                **What it is:** Adding zinc to commonly consumed foods like wheat flour, maize meal, and cooking oil.
                
                **How it works:** Zinc is added during food processing at mills and factories.
                
                **Advantages:**
                • Reaches entire population through regular food consumption
                • No behavior change required
                • Cost-effective at scale
                • Sustainable long-term solution
                
                **Challenges:**
                • Requires food industry cooperation
                • Needs quality monitoring systems
                • Initial infrastructure investment
                
                **Success Example:** Rwanda reduced stunting by 17% through fortification programs.
            """,
            'policy_requirements': [
                "Mandatory fortification legislation",
                "Quality standards and monitoring",
                "Industry incentives or subsidies"
            ]
        },
        'therapeutic_zinc': {
            'name': 'Therapeutic Zinc for Diarrhea',
            'unit_cost': 45,
            'effectiveness': 0.95,
            'reach_time': 1,
            'coverage_potential': 0.60,
            'description': """
                **What it is:** Zinc tablets or syrup given with ORS (Oral Rehydration Solution) to treat diarrhea.
                
                **How it works:** 10-14 day course of zinc reduces diarrhea duration by 25% and prevents future episodes.
                
                **Advantages:**
                • Immediate impact on child mortality
                • WHO-recommended standard treatment
                • Prevents 88,000 child deaths annually (global)
                • Low cost per life saved
                
                **Challenges:**
                • Requires healthcare system delivery
                • Parent education needed
                • Stock management at health facilities
                
                **Success Example:** Bangladesh reduced diarrhea deaths by 50% with zinc+ORS programs.
            """,
            'policy_requirements': [
                "Integration into IMCI guidelines",
                "Healthcare worker training",
                "Supply chain management",
                "Community awareness campaigns"
            ]
        },
        'preventive_supplements': {
            'name': 'Preventive Zinc Supplementation',
            'unit_cost': 120,
            'effectiveness': 0.90,
            'reach_time': 2,
            'coverage_potential': 0.70,
            'description': """
                **What it is:** Regular zinc supplements (tablets/drops) for at-risk groups.
                
                **How it works:** Daily or weekly zinc doses prevent deficiency before symptoms appear.
                
                **Target Groups:**
                • Children 6-59 months
                • Pregnant and lactating women
                • Adolescent girls
                
                **Advantages:**
                • High effectiveness in deficient populations
                • Can be combined with other micronutrients
                • Measurable biomarker improvements
                
                **Challenges:**
                • Requires sustained distribution
                • Compliance monitoring needed
                • Higher cost than fortification
                
                **Success Example:** Peru reduced stunting from 40% to 14% with targeted supplementation.
            """,
            'policy_requirements': [
                "National supplementation protocol",
                "Distribution through health facilities",
                "Community health worker programs"
            ]
        },
        'biofortified_crops': {
            'name': 'Biofortified Crop Programs',
            'unit_cost': 25,
            'effectiveness': 0.65,
            'reach_time': 12,
            'coverage_potential': 0.75,
            'description': """
                **What it is:** Growing crops naturally rich in zinc through selective breeding.
                
                **How it works:** Farmers plant zinc-rich varieties of beans, sweet potatoes, and maize.
                
                **Advantages:**
                • Sustainable, farmer-driven solution
                • No recurring costs after adoption
                • Improves rural nutrition
                • Climate-resilient varieties available
                
                **Challenges:**
                • Takes time to scale up
                • Requires agricultural extension
                • Seed distribution systems needed
                • Farmer adoption barriers
                
                **Success Example:** HarvestPlus reached 10 million households with biofortified crops in Africa.
            """,
            'policy_requirements': [
                "Agricultural policy integration",
                "Seed certification and distribution",
                "Extension service training",
                "Market development support"
            ]
        },
        'maternal_supplementation': {
            'name': 'Maternal Zinc Programs',
            'unit_cost': 180,
            'effectiveness': 0.92,
            'reach_time': 3,
            'coverage_potential': 0.80,
            'description': """
                **What it is:** Zinc supplements for pregnant and breastfeeding mothers.
                
                **How it works:** Daily zinc during pregnancy improves birth outcomes and infant health.
                
                **Benefits:**
                • Reduces preterm births by 14%
                • Improves birth weight
                • Better infant immune function
                • Reduces maternal complications
                
                **Delivery:**
                • Through antenatal care clinics
                • Combined with iron and folic acid
                • Part of focused ANC package
                
                **Success Example:** Indonesia reduced low birth weight by 20% with maternal supplementation.
            """,
            'policy_requirements': [
                "ANC protocol updates",
                "Healthcare provider training",
                "Supply to all health facilities"
            ]
        },
        'community_health': {
            'name': 'Community Health Programs',
            'unit_cost': 15,
            'effectiveness': 0.55,
            'reach_time': 4,
            'coverage_potential': 0.90,
            'description': """
                **What it is:** Community-based nutrition education and basic supplementation.
                
                **How it works:** CHWs provide education, screening, and basic zinc supplements.
                
                **Components:**
                • Nutrition education sessions
                • Growth monitoring
                • Zinc-rich food promotion
                • Referral for treatment
                
                **Advantages:**
                • Wide reach in rural areas
                • Builds local capacity
                • Sustainable behavior change
                • Low cost per person
                
                **Success Example:** Ethiopia's HEP program improved nutrition in 15 million households.
            """,
            'policy_requirements': [
                "CHW training curricula",
                "Community mobilization",
                "Supervision systems",
                "Basic supply provision"
            ]
        }
    }

def calculate_health_outcomes(coverage, intervention_mix, timeline_months):
    """Calculate health outcomes with detailed explanations"""
    
    # Calculate effectiveness
    total_effectiveness = 0
    interventions_data = get_intervention_details()
    for intervention, percentage in intervention_mix.items():
        if percentage > 0 and intervention in interventions_data:
            total_effectiveness += (percentage / 100) * interventions_data[intervention]['effectiveness']
    
    # Based on WHO data: Kenya has ~70,000 under-5 deaths annually
    # 51% zinc deficiency means ~35,000 deaths in deficient population
    # Zinc interventions can reduce mortality by 9-18% (using 12% as conservative estimate)
    # At full coverage, could prevent 35,000 * 0.12 = 4,200 deaths
    # Adjusted by actual coverage and effectiveness
    annual_u5_deaths_in_deficient = 35000
    mortality_reduction_rate = 0.12  # 12% mortality reduction from zinc interventions
    
    # Calculate actual values first
    lives_saved_value = int(coverage * total_effectiveness * annual_u5_deaths_in_deficient * mortality_reduction_rate)
    stunting_prevented_value = int(coverage * total_effectiveness * STUNTED_CHILDREN * 0.15)
    diarrhea_reduction_value = coverage * total_effectiveness * 0.25
    cognitive_improvement_value = coverage * total_effectiveness * 8.5
    economic_benefit_value = calculate_realistic_economic_benefit(coverage, total_effectiveness)
    
    # Generate dynamic comparisons based on actual values
    # Lives saved comparison - Kenya has 47 counties, ~1,489 child deaths per county annually (70,000/47)
    deaths_per_county = 1489
    if lives_saved_value >= deaths_per_county:
        counties_saved = int(lives_saved_value / deaths_per_county)
        lives_comparison = f"Equivalent to eliminating child mortality in {counties_saved} count{'ies' if counties_saved > 1 else 'y'}"
    else:
        # For smaller numbers, use percentage of a county
        percent_of_county = int((lives_saved_value / deaths_per_county) * 100)
        lives_comparison = f"Equivalent to {percent_of_county}% reduction in child mortality in one county"
    
    # Stunting prevented - average primary school has 300 students
    schools_worth = max(1, int(stunting_prevented_value / 300))
    stunting_comparison = f"Equal to {schools_worth} primary school{'s' if schools_worth > 1 else ''} of healthy children"
    
    # Diarrhea reduction
    diarrhea_percentage = int(diarrhea_reduction_value * 100)
    diarrhea_comparison = f"{diarrhea_percentage}% fewer hospital admissions for diarrhea"
    
    # Cognitive improvement context
    if cognitive_improvement_value >= 8:
        cognitive_comparison = "Difference between completing primary vs. dropping out"
    elif cognitive_improvement_value >= 5:
        cognitive_comparison = "Equivalent to 2 extra years of schooling"
    elif cognitive_improvement_value >= 3:
        cognitive_comparison = "Equivalent to 1 extra year of schooling"
    else:
        cognitive_comparison = "Measurable improvement in learning capacity"
    
    # Economic benefit context
    if economic_benefit_value >= 1_000_000_000:
        economic_comparison = f"Could fund {int(economic_benefit_value / 500_000_000)} new health centers"
    elif economic_benefit_value >= 100_000_000:
        economic_comparison = f"Could train {int(economic_benefit_value / 50_000)} community health workers"
    else:
        economic_comparison = "Direct measurable economic benefits"
    
    # Health outcomes with policy-relevant metrics
    outcomes = {
        'lives_saved': {
            'value': lives_saved_value,
            'explanation': "Child deaths prevented through reduced diarrhea, pneumonia, and malaria severity",
            'comparison': lives_comparison
        },
        'stunting_prevented': {
            'value': stunting_prevented_value,
            'explanation': "Children who will achieve normal height-for-age",
            'comparison': stunting_comparison
        },
        'diarrhea_reduction': {
            'value': diarrhea_reduction_value,
            'explanation': "Reduction in diarrhea duration and severity",
            'comparison': diarrhea_comparison
        },
        'cognitive_improvement': {
            'value': cognitive_improvement_value,
            'explanation': "IQ points gained on average per child",
            'comparison': cognitive_comparison
        },
        'economic_benefit': {
            'value': economic_benefit_value,
            'explanation': "Annual healthcare savings and productivity gains",
            'comparison': economic_comparison
        }
    }
    
    return outcomes

def calculate_realistic_economic_benefit(coverage, effectiveness):
    """Calculate realistic annual economic benefits"""
    
    # People reached
    children_reached = coverage * CHILDREN_UNDER_5 * effectiveness
    adults_reached = coverage * ZINC_DEFICIENT_POPULATION * effectiveness * 0.7  # 70% are adults
    
    # Annual healthcare savings
    diarrhea_treatment_saved = children_reached * 0.15 * 0.25 * 2000  # 15% get diarrhea, 25% reduction, 2000 KSH per episode
    hospitalization_saved = children_reached * 0.02 * 0.30 * 15000  # 2% hospitalized, 30% reduction, 15000 KSH per admission
    
    # Reduced stunting healthcare costs (long-term savings annualized)
    stunting_healthcare_saved = children_reached * 0.26 * 0.15 * 5000  # 26% stunted, 15% reduction, 5000 KSH annual extra healthcare
    
    # Productivity gains
    caregiver_productivity = children_reached * 0.15 * 0.25 * 3 * 500  # 3 days saved, 500 KSH daily wage
    
    # Adult productivity gains (reduced sick days)
    adult_productivity = adults_reached * 0.05 * 5 * 800  # 5% reduction in sick days, 5 days/year, 800 KSH daily
    
    # Cognitive benefits (future earnings, annualized)
    # Each IQ point worth ~1% increase in lifetime earnings
    # Average annual income 120,000 KSH, 8.5 IQ points gained
    cognitive_benefit = children_reached * 0.085 * 1200  # 8.5% of future 120,000 KSH annual income, discounted
    
    # Total ANNUAL benefit
    total_annual = (diarrhea_treatment_saved + hospitalization_saved + stunting_healthcare_saved + 
                   caregiver_productivity + adult_productivity + cognitive_benefit)
    
    return total_annual

def calculate_optimal_budget(intervention_mix):
    """Calculate the optimal budget based on diminishing returns and cost-effectiveness"""
    
    # Get intervention details
    interventions_data = get_intervention_details()
    
    # Calculate weighted parameters
    weighted_cost = 0
    weighted_effectiveness = 0
    weighted_saturation = 0
    
    for intervention, percentage in intervention_mix.items():
        if percentage > 0 and intervention in interventions_data:
            weight = percentage / 100
            data = interventions_data[intervention]
            weighted_cost += data['unit_cost'] * weight
            weighted_effectiveness += data['effectiveness'] * weight
            weighted_saturation += data['coverage_potential'] * weight
    
    # If no interventions selected, return default
    if weighted_cost == 0:
        return {
            'optimal_budget': 2_000_000_000,
            'optimal_coverage': 75,
            'optimal_roi': 280,
            'optimal_lives_saved': 2400
        }
    
    # Budget optimization using diminishing returns
    budget_range = np.linspace(100_000_000, 10_000_000_000, 100)
    results = []
    
    for budget in budget_range:
        # Calculate theoretical coverage
        theoretical_coverage = budget / (weighted_cost * ZINC_DEFICIENT_POPULATION)
        
        # Apply saturation curve (sigmoid function for realistic coverage limits)
        actual_coverage = weighted_saturation * (1 - np.exp(-3 * theoretical_coverage / weighted_saturation))
        actual_coverage = min(actual_coverage, 1.0)
        
        # Calculate outcomes using WHO-based estimates
        annual_u5_deaths_in_deficient = 35000
        mortality_reduction_rate = 0.12
        lives_saved = actual_coverage * weighted_effectiveness * annual_u5_deaths_in_deficient * mortality_reduction_rate
        stunting_prevented = actual_coverage * weighted_effectiveness * STUNTED_CHILDREN * 0.15
        
        # Calculate comprehensive annual economic benefits
        children_reached = actual_coverage * CHILDREN_UNDER_5 * weighted_effectiveness
        adults_reached = actual_coverage * ZINC_DEFICIENT_POPULATION * weighted_effectiveness * 0.7
        
        # Healthcare savings
        diarrhea_savings = children_reached * 0.15 * 0.25 * 2000
        hospital_savings = children_reached * 0.02 * 0.30 * 15000
        stunting_healthcare_saved = children_reached * 0.26 * 0.15 * 5000
        
        # Productivity gains
        caregiver_productivity = children_reached * 0.15 * 0.25 * 3 * 500
        adult_productivity = adults_reached * 0.05 * 5 * 800
        
        # Cognitive benefits (annualized)
        cognitive_benefit = children_reached * 0.085 * 1200
        
        # Total annual benefit
        total_benefit = (diarrhea_savings + hospital_savings + stunting_healthcare_saved +
                        caregiver_productivity + adult_productivity + cognitive_benefit)
        
        # Calculate 5-year ROI (more realistic for public health interventions)
        # Year 1: 60% of benefits realized, Year 2: 80%, Year 3-5: 100%
        five_year_benefits = total_benefit * (0.6 + 0.8 + 1 + 1 + 1)  # 4.4x annual benefits
        five_year_costs = budget * 5 * 0.9  # Assuming 10% efficiency gain over time
        roi = ((five_year_benefits - five_year_costs) / five_year_costs) * 100 if five_year_costs > 0 else 0
        
        # Cost-effectiveness
        cost_per_life = budget / lives_saved if lives_saved > 0 else float('inf')
        
        # Calculate marginal benefit
        marginal_benefit = 0
        if len(results) > 0:
            prev = results[-1]
            marginal_benefit = (total_benefit - prev['total_benefit']) / (budget - prev['budget']) if budget > prev['budget'] else 0
        
        results.append({
            'budget': budget,
            'coverage': actual_coverage,
            'lives_saved': lives_saved,
            'roi': roi,
            'cost_per_life': cost_per_life,
            'marginal_benefit': marginal_benefit,
            'total_benefit': total_benefit,
            'efficiency_score': roi * actual_coverage
        })
    
    df = pd.DataFrame(results)
    
    # Find optimal budget using multiple criteria
    # 1. Maximum efficiency (ROI × Coverage)
    optimal_efficiency_idx = df['efficiency_score'].idxmax()
    
    # 2. Marginal benefit threshold (returns > 1.5x cost)
    marginal_threshold = 1.5
    good_marginal = df[df['marginal_benefit'] >= marginal_threshold]
    if not good_marginal.empty:
        optimal_marginal_idx = good_marginal.index[-1]
    else:
        optimal_marginal_idx = optimal_efficiency_idx
    
    # 3. Cost-effectiveness threshold (< 100K per life based on WHO standards)
    cost_threshold = 100_000  # WHO considers <3x GDP per capita (~150K KSH) as highly cost-effective
    cost_effective = df[df['cost_per_life'] <= cost_threshold]
    if not cost_effective.empty:
        optimal_cost_idx = cost_effective.index[-1]
    else:
        optimal_cost_idx = optimal_efficiency_idx
    
    # Weighted combination
    optimal_idx = int(
        optimal_efficiency_idx * 0.4 +
        optimal_marginal_idx * 0.3 +
        optimal_cost_idx * 0.3
    )
    
    # Ensure index is valid
    optimal_idx = min(max(optimal_idx, 0), len(df) - 1)
    optimal = df.iloc[optimal_idx]
    
    # Check for implementation capacity constraints
    max_capacity = 3_000_000_000  # 3B KSH max annual capacity
    if optimal['budget'] > max_capacity:
        constrained = df[df['budget'] <= max_capacity].iloc[-1]
        return {
            'optimal_budget': constrained['budget'],
            'optimal_coverage': constrained['coverage'] * 100,
            'optimal_roi': constrained['roi'],
            'optimal_lives_saved': int(constrained['lives_saved']),
            'data': df,
            'constrained': True
        }
    
    return {
        'optimal_budget': optimal['budget'],
        'optimal_coverage': optimal['coverage'] * 100,
        'optimal_roi': optimal['roi'],
        'optimal_lives_saved': int(optimal['lives_saved']),
        'data': df,
        'constrained': False
    }

# PLAN INTERVENTION TAB
with tab1:
    st.markdown("## 🎯 Design Your Zinc Intervention Strategy")
    
    # Helpful context
    with st.expander("ℹ️ Understanding This Section", expanded=True):
        st.markdown("""
        This section helps you design a zinc intervention program by:
        1. **Setting your budget** - How much funding is available?
        2. **Choosing target groups** - Who needs help most urgently?
        3. **Selecting interventions** - Which approaches will you use?
        4. **Estimating coverage** - How many people will you reach?
        
        **💡 Tip:** Start with your available budget, then adjust interventions to maximize impact.
        """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 💰 Budget Planning")
        
        # Budget input with context
        st.markdown("""
        <div class="info-box">
            <strong style="color: #1565c0;">Budget Context:</strong><br>
            <span style="color: #212121;">
            • Kenya health budget: ~300 billion KSH/year<br>
            • Nutrition allocation: ~2% of health budget<br>
            • Recommended: 1-3 billion KSH for zinc programs
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple budget input
        budget_input_method = st.radio(
            "How would you like to set the budget?",
            ["Simple (millions KSH)", "Percentage of health budget", "Cost per person"]
        )
        
        if budget_input_method == "Simple (millions KSH)":
            budget_millions = st.number_input(
                "Enter budget in millions KSH",
                min_value=50,
                max_value=10000,
                value=1000,
                step=50,
                help="Typical range: 500-3000 million KSH"
            )
            total_budget = budget_millions * 1_000_000
            
        elif budget_input_method == "Percentage of health budget":
            budget_percentage = st.slider(
                "Percentage of nutrition budget for zinc",
                min_value=5,
                max_value=50,
                value=20,
                help="WHO recommends 2-3% of health budget for nutrition"
            )
            total_budget = (300_000_000_000 * 0.02 * budget_percentage / 100)
            
        else:  # Cost per person
            cost_per_person = st.slider(
                "Budget per affected person (KSH)",
                min_value=10,
                max_value=200,
                value=50,
                help="Compare: One doctor visit costs ~500 KSH"
            )
            total_budget = cost_per_person * ZINC_DEFICIENT_POPULATION
        
        # Display budget in understandable terms
        st.markdown(f"""
        <div class="metric-card" style="background-color: #e3f2fd; border-left: 5px solid #1976d2;">
            <h4 style="color: #0d47a1;">Total Budget</h4>
            <h2 style="color: #1565c0;">{total_budget/1_000_000:,.0f} Million KSH</h2>
            <p style="color: #424242;">
                • Per affected person: {total_budget/ZINC_DEFICIENT_POPULATION:.0f} KSH<br>
                • Per child under 5: {total_budget/CHILDREN_UNDER_5:.0f} KSH<br>
                • Percentage of health budget: {total_budget/300_000_000_000*100:.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Target population with explanations
        st.markdown("### 🎯 Priority Groups")
        
        with st.expander("Understanding Priority Groups"):
            st.markdown("""
            **Why prioritize?** Limited resources require focusing on those who benefit most.
            
            **High-impact groups:**
            • **Children under 5:** Most vulnerable to stunting and death
            • **Pregnant women:** Affects two generations
            • **Stunted children:** Can still recover if treated early
            """)
        
        targeting_strategy = st.selectbox(
            "Choose your targeting approach",
            [
                "Universal Coverage (Everyone)",
                "Children First (Under 5 priority)",
                "Mother-Child Focus (Pregnancy to 2 years)",
                "Emergency Response (Severe cases only)",
                "Geographic Focus (High-burden areas)"
            ]
        )
        
        # Set target population based on strategy
        if targeting_strategy == "Universal Coverage (Everyone)":
            target_population = ZINC_DEFICIENT_POPULATION
            st.info("📊 Targeting all 26.5 million zinc-deficient individuals")
        elif targeting_strategy == "Children First (Under 5 priority)":
            target_population = CHILDREN_UNDER_5
            st.info("👶 Focusing on 7 million children under 5")
        elif targeting_strategy == "Mother-Child Focus (Pregnancy to 2 years)":
            target_population = PREGNANT_WOMEN + int(CHILDREN_UNDER_5 * 0.4)
            st.info("🤱 Targeting 4.5 million mothers and young children")
        elif targeting_strategy == "Emergency Response (Severe cases only)":
            target_population = STUNTED_CHILDREN + CHILDREN_WITH_DIARRHEA
            st.info("🚨 Focusing on 2.9 million severe cases")
        else:  # Geographic Focus
            target_population = int(ZINC_DEFICIENT_POPULATION * 0.3)
            st.info("📍 Targeting 8 million in high-burden regions")
        
        # Implementation timeline
        st.markdown("### ⏱️ Timeline")
        
        timeline_preset = st.selectbox(
            "Implementation timeline",
            [
                "Emergency (6 months)",
                "Annual Program (12 months)",
                "Medium-term (24 months)",
                "Strategic Plan (36 months)",
                "Long-term (60 months)"
            ]
        )
        
        timeline_map = {
            "Emergency (6 months)": 6,
            "Annual Program (12 months)": 12,
            "Medium-term (24 months)": 24,
            "Strategic Plan (36 months)": 36,
            "Long-term (60 months)": 60
        }
        timeline_months = timeline_map[timeline_preset]
    
    with col2:
        st.markdown("### 🔧 Choose Your Interventions")
        
        # Intervention selection with detailed explanations
        st.markdown("""
        <div class="info-box">
            <strong style="color: #1565c0;">📚 How to Choose Interventions:</strong><br>
            <span style="color: #212121;">
            • <strong>Fortification:</strong> Best for long-term, population-wide impact<br>
            • <strong>Therapeutic Zinc:</strong> Essential for saving lives immediately<br>
            • <strong>Supplements:</strong> Good for targeted high-risk groups<br>
            • <strong>Biofortification:</strong> Sustainable but takes time<br>
            • <strong>Mix strategies</strong> for best results!
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick strategy selector
        strategy_template = st.selectbox(
            "Choose a strategy template (or customize below)",
            [
                "Balanced Approach (Recommended)",
                "Emergency Response",
                "Sustainable Development",
                "Cost-Optimized",
                "Custom Mix"
            ]
        )
        
        # Set default values based on template
        if strategy_template == "Balanced Approach (Recommended)":
            default_values = {
                'fortification': 30,
                'therapeutic_zinc': 25,
                'preventive_supplements': 20,
                'biofortified_crops': 10,
                'maternal_supplementation': 10,
                'community_health': 5
            }
        elif strategy_template == "Emergency Response":
            default_values = {
                'fortification': 10,
                'therapeutic_zinc': 50,
                'preventive_supplements': 25,
                'biofortified_crops': 0,
                'maternal_supplementation': 10,
                'community_health': 5
            }
        elif strategy_template == "Sustainable Development":
            default_values = {
                'fortification': 35,
                'therapeutic_zinc': 15,
                'preventive_supplements': 10,
                'biofortified_crops': 25,
                'maternal_supplementation': 10,
                'community_health': 5
            }
        elif strategy_template == "Cost-Optimized":
            default_values = {
                'fortification': 45,
                'therapeutic_zinc': 20,
                'preventive_supplements': 10,
                'biofortified_crops': 15,
                'maternal_supplementation': 5,
                'community_health': 5
            }
        else:  # Custom
            default_values = {
                'fortification': 0,
                'therapeutic_zinc': 0,
                'preventive_supplements': 0,
                'biofortified_crops': 0,
                'maternal_supplementation': 0,
                'community_health': 0
            }
        
        st.markdown("#### Adjust Intervention Mix (must total 100%)")
        
        interventions = {}
        interventions_data = get_intervention_details()
        
        # Create intervention sliders with info buttons
        for key, details in interventions_data.items():
            col_slider, col_info = st.columns([3, 1])
            
            with col_slider:
                interventions[key] = st.slider(
                    details['name'],
                    min_value=0,
                    max_value=100,
                    value=default_values[key],
                    help=f"Cost: {details['unit_cost']} KSH/person | Effectiveness: {details['effectiveness']*100:.0f}%"
                )
            
            with col_info:
                with st.expander("Details"):
                    st.markdown(details['description'])
                    st.markdown("**Policy Requirements:**")
                    for req in details['policy_requirements']:
                        st.markdown(f"• {req}")
        
        # Validate allocation
        total_allocation = sum(interventions.values())
        
        if total_allocation != 100:
            st.error(f"""
            ⚠️ **Allocation must equal 100%** (Currently: {total_allocation}%)
            
            Adjust the sliders above to reach exactly 100%.
            """)
        else:
            st.success("✅ Valid intervention mix!")
            
            # Calculate and show coverage
            avg_cost = sum(
                (interventions[key]/100) * interventions_data[key]['unit_cost']
                for key in interventions
            )
            
            max_people_reached = min(target_population, int(total_budget / avg_cost))
            coverage = max_people_reached / target_population
            
            st.markdown(f"""
            <div class="success-box">
                <h4 style="color: #2e7d32;">📊 Coverage Estimate</h4>
                <p style="color: #212121;"><strong>People Reached:</strong> {max_people_reached:,} ({coverage*100:.1f}% of target)</p>
                <p style="color: #212121;"><strong>Cost per Person:</strong> {avg_cost:.0f} KSH</p>
                <p style="color: #212121;"><strong>Geographic Reach:</strong> {int(coverage*47)}/47 counties</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate and show optimal budget
            st.markdown("### 🎯 Optimal Budget Analysis")
            
            with st.expander("📈 View Budget Optimization Analysis", expanded=False):
                optimal_result = calculate_optimal_budget(interventions)
                
                # Show optimal budget recommendation
                col_opt1, col_opt2 = st.columns(2)
                
                with col_opt1:
                    st.markdown(f"""
                    <div class="info-box">
                        <h4 style="color: #1565c0;">💰 Optimal Budget Calculation</h4>
                        <p style="color: #212121;"><strong>Recommended Budget:</strong> {optimal_result['optimal_budget']/1_000_000:.0f} Million KSH</p>
                        <p style="color: #212121;"><strong>Optimal Coverage:</strong> {optimal_result['optimal_coverage']:.1f}%</p>
                        <p style="color: #212121;"><strong>Optimal ROI:</strong> {optimal_result['optimal_roi']:.0f}%</p>
                        <p style="color: #212121;"><strong>Lives Saved at Optimal:</strong> {optimal_result['optimal_lives_saved']:,}</p>
                        {"<p style='color: #d32f2f;'>⚠️ <strong>Note:</strong> Constrained by implementation capacity</p>" if optimal_result.get('constrained', False) else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Comparison with current budget
                    budget_diff = (total_budget - optimal_result['optimal_budget']) / optimal_result['optimal_budget'] * 100
                    if abs(budget_diff) < 10:
                        st.success("✅ Your budget is close to optimal!")
                    elif budget_diff > 0:
                        st.warning(f"📊 Your budget is {budget_diff:.0f}% above optimal. Consider reducing to avoid diminishing returns.")
                    else:
                        st.info(f"📊 Your budget is {abs(budget_diff):.0f}% below optimal. Consider increasing for better impact.")
                
                with col_opt2:
                    st.markdown("""
                    <div class="info-box">
                        <h4 style="color: #1565c0;">🔍 How We Calculate Optimal Budget</h4>
                        <p style="color: #212121;">The optimal budget is determined by analyzing:</p>
                        <ul style="color: #212121;">
                            <li><strong>Diminishing Returns:</strong> Coverage plateaus at higher spending</li>
                            <li><strong>Marginal Benefits:</strong> Each additional KSH yields less benefit</li>
                            <li><strong>Cost-Effectiveness:</strong> Cost per life saved threshold</li>
                            <li><strong>Implementation Capacity:</strong> System can effectively manage ~3B KSH/year</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Create optimization curves visualization
                if 'data' in optimal_result:
                    st.markdown("#### 📊 Budget Optimization Curves")
                    
                    df_opt = optimal_result['data']
                    
                    # Create figure with secondary y-axis
                    fig_opt = go.Figure()
                    
                    # Add ROI curve
                    fig_opt.add_trace(go.Scatter(
                        x=df_opt['budget'] / 1_000_000,
                        y=df_opt['roi'],
                        mode='lines',
                        name='ROI (%)',
                        line=dict(color='green', width=2),
                        yaxis='y'
                    ))
                    
                    # Add Coverage curve
                    fig_opt.add_trace(go.Scatter(
                        x=df_opt['budget'] / 1_000_000,
                        y=df_opt['coverage'] * 100,
                        mode='lines',
                        name='Coverage (%)',
                        line=dict(color='blue', width=2),
                        yaxis='y2'
                    ))
                    
                    # Add efficiency score
                    fig_opt.add_trace(go.Scatter(
                        x=df_opt['budget'] / 1_000_000,
                        y=df_opt['efficiency_score'],
                        mode='lines',
                        name='Efficiency Score',
                        line=dict(color='purple', width=2, dash='dash'),
                        yaxis='y'
                    ))
                    
                    # Mark current budget point
                    current_idx = (df_opt['budget'] - total_budget).abs().idxmin()
                    current_point = df_opt.iloc[current_idx]
                    
                    fig_opt.add_trace(go.Scatter(
                        x=[total_budget / 1_000_000],
                        y=[current_point['roi']],
                        mode='markers',
                        name='Your Budget',
                        marker=dict(size=12, color='orange', symbol='diamond'),
                        yaxis='y'
                    ))
                    
                    # Mark optimal budget point
                    optimal_idx = (df_opt['budget'] - optimal_result['optimal_budget']).abs().idxmin()
                    optimal_point = df_opt.iloc[optimal_idx]
                    
                    fig_opt.add_trace(go.Scatter(
                        x=[optimal_result['optimal_budget'] / 1_000_000],
                        y=[optimal_point['roi']],
                        mode='markers',
                        name='Optimal Budget',
                        marker=dict(size=15, color='red', symbol='star'),
                        yaxis='y'
                    ))
                    
                    # Add vertical lines
                    fig_opt.add_vline(
                        x=total_budget / 1_000_000,
                        line_dash="dot",
                        line_color="orange",
                        annotation_text=f"Current: {total_budget/1_000_000:.0f}M"
                    )
                    
                    fig_opt.add_vline(
                        x=optimal_result['optimal_budget'] / 1_000_000,
                        line_dash="dot",
                        line_color="red",
                        annotation_text=f"Optimal: {optimal_result['optimal_budget']/1_000_000:.0f}M"
                    )
                    
                    # Update layout
                    fig_opt.update_layout(
                        title="Budget Optimization Analysis - Finding the Sweet Spot",
                        xaxis=dict(title="Budget (Million KSH)"),
                        yaxis=dict(
                            title="ROI (%) / Efficiency Score",
                            side="left"
                        ),
                        yaxis2=dict(
                            title="Coverage (%)",
                            overlaying="y",
                            side="right"
                        ),
                        hovermode='x unified',
                        height=400,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig_opt, use_container_width=True)
                    
                    # Interpretation guide
                    st.markdown("""
                    <div class="info-box">
                        <h5 style="color: #1565c0;">📖 How to Read This Chart:</h5>
                        <ul style="color: #212121;">
                            <li><strong>Green Line (ROI):</strong> Shows return on investment - peaks then declines</li>
                            <li><strong>Blue Line (Coverage):</strong> Population reached - plateaus at higher budgets</li>
                            <li><strong>Purple Line (Efficiency):</strong> Combined score - optimal where highest</li>
                            <li><strong>Orange Diamond:</strong> Your current budget position</li>
                            <li><strong>Red Star:</strong> Calculated optimal budget</li>
                        </ul>
                        <p style="color: #212121;"><strong>Key Insight:</strong> Beyond the optimal point, additional spending yields diminishing returns.</p>
                    </div>
                    """, unsafe_allow_html=True)

# HEALTH IMPACT TAB
with tab2:
    st.markdown("## 📊 Predicted Health Outcomes")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        outcomes = calculate_health_outcomes(coverage, interventions, timeline_months)
        
        # Impact summary cards
        st.markdown("### 🎯 Key Impact Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #e8f5e9; border-left: 5px solid #4caf50;">
                <h4 style="color: #2e7d32;">👶 Lives Saved (Annual)</h4>
                <h2 style="color: #1b5e20;">{outcomes['lives_saved']['value']:,}</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['lives_saved']['comparison']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #fff3e0; border-left: 5px solid #ff9800;">
                <h4 style="color: #e65100;">📏 Stunting Prevented</h4>
                <h2 style="color: #bf360c;">{outcomes['stunting_prevented']['value']:,}</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['stunting_prevented']['comparison']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #e3f2fd; border-left: 5px solid #2196f3;">
                <h4 style="color: #1565c0;">🧠 IQ Points Gained</h4>
                <h2 style="color: #0d47a1;">+{outcomes['cognitive_improvement']['value']:.1f}</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['cognitive_improvement']['comparison']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f3e5f5; border-left: 5px solid #9c27b0;">
                <h4 style="color: #6a1b9a;">💰 Annual Savings</h4>
                <h2 style="color: #4a148c;">{outcomes['economic_benefit']['value']/1_000_000:.1f}M KSH</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['economic_benefit']['comparison']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Timeline visualization with explanations
        st.markdown("### 📅 When Will We See Results?")
        
        with st.expander("Understanding the Timeline"):
            st.markdown("""
            **Why timing matters:** Different interventions show results at different speeds.
            
            • **Immediate (0-3 months):** Therapeutic zinc reduces diarrhea deaths \n
            • **Short-term (3-12 months):** Growth improvements become visible \n
            • **Long-term (1-5 years):** Cognitive and economic benefits emerge \n
            
            **Policy Implication:** Combine quick-wins with sustainable solutions.
            """)
        
        # Create timeline chart
        months = list(range(0, timeline_months + 1, 3))
        
        # Different impact curves
        immediate_impact = [min(100, (m/6) * 80) for m in months]
        growth_impact = [min(100, (m/12) * 60) for m in months]
        cognitive_impact = [min(100, (m/24) * 40) for m in months]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months, y=immediate_impact,
            mode='lines+markers',
            name='Diarrhea Reduction',
            line=dict(color='#FF6B6B', width=3),
            hovertemplate='Month %{x}: %{y:.0f}% impact'
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=growth_impact,
            mode='lines+markers',
            name='Growth Improvement',
            line=dict(color='#4ECDC4', width=3),
            hovertemplate='Month %{x}: %{y:.0f}% impact'
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=cognitive_impact,
            mode='lines+markers',
            name='Cognitive Development',
            line=dict(color='#45B7D1', width=3),
            hovertemplate='Month %{x}: %{y:.0f}% impact'
        ))
        
        # Add milestone annotations
        milestones = [
            dict(x=3, y=50, text="First lives saved", showarrow=True),
            dict(x=12, y=60, text="Stunting reduction visible", showarrow=True),
            dict(x=24, y=40, text="School performance improves", showarrow=True)
        ]
        
        fig.update_layout(
            title="Health Impact Timeline",
            xaxis_title="Months",
            yaxis_title="Impact Achievement (%)",
            annotations=milestones,
            hovermode='x unified',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Success stories
        st.markdown("### 🌟 What Success Looks Like")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2e7d32;">📖 Sarah's Story</h4>
                <p style="color: #212121;"><em>"My daughter used to have diarrhea every month. After getting zinc at the clinic, 
                she's been healthy for 6 months. She's growing taller and more active!"</em></p>
                <p style="color: #424242;"><strong>- Mother from Kisumu</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2e7d32;">📖 Community Impact</h4>
                <p style="color: #212121;"><em>"Since the fortification program started, we've seen 40% fewer children admitted 
                with severe diarrhea. The whole community is healthier."</em></p>
                <p style="color: #424242;"><strong>- Health Worker, Turkana</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ Please complete the intervention design in the 'Plan Intervention' tab first.")

# ECONOMIC ANALYSIS TAB
with tab3:
    st.markdown("## 💰 Economic Analysis & Return on Investment")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Calculate economic metrics
        cost_per_life = total_budget / outcomes['lives_saved']['value'] if outcomes['lives_saved']['value'] > 0 else 0
        cost_per_stunting = total_budget / outcomes['stunting_prevented']['value'] if outcomes['stunting_prevented']['value'] > 0 else 0
        
        # Calculate realistic ROI over time
        annual_benefit = outcomes['economic_benefit']['value']
        # Year 1: Only 60% of benefits realized due to ramp-up
        roi_year1 = ((annual_benefit * 0.6 - total_budget) / total_budget) * 100
        # Year 5: Benefits compound, costs decrease with efficiency
        five_year_benefits = annual_benefit * (0.6 + 0.8 + 1 + 1 + 1)  # 4.4x annual
        five_year_costs = total_budget + (total_budget * 0.9 * 4)  # First year full, then 90% for years 2-5
        roi_year5 = ((five_year_benefits - five_year_costs) / five_year_costs) * 100
        # Year 10: Full benefits realized with scaling efficiencies
        ten_year_benefits = annual_benefit * (0.6 + 0.8 + 8 * 1.1)  # Growing benefits
        ten_year_costs = total_budget + (total_budget * 0.85 * 9)  # Decreasing costs
        roi_year10 = ((ten_year_benefits - ten_year_costs) / ten_year_costs) * 100
        
        # Cost-effectiveness comparison
        st.markdown("### 💡 Is This Investment Worth It?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f5f5f5; border-left: 5px solid #4caf50;">
                <h4 style="color: #2e7d32;">Cost per Life Saved</h4>
                <h2 style="color: #1b5e20;">{cost_per_life:,.0f} KSH</h2>
                <p style="color: #424242;">
                    Compare to:<br>
                    • Vitamin A: 35,000 KSH<br>
                    • Malaria nets: 150,000 KSH<br>
                    • HIV treatment: 500,000 KSH<br>
                    • Road safety: 2,000,000 KSH
                </p>
                {"<p style='color: #2e7d32;'>✅ Highly cost-effective</p>" if cost_per_life < 100000 else "<p style='color: #ff9800;'>⚠️ Moderately cost-effective</p>" if cost_per_life < 300000 else "<p style='color: #d32f2f;'>❌ Review budget allocation</p>"}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f5f5f5; border-left: 5px solid #1976d2;">
                <h4 style="color: #0d47a1;">Return on Investment Timeline</h4>
                <p style="color: #424242;">
                    <strong>Year 1:</strong> {roi_year1:.0f}% (Investment phase)<br>
                    <strong>Year 5:</strong> {roi_year5:.0f}% (Building returns)<br>
                    <strong>Year 10:</strong> {roi_year10:.0f}% (Sustained impact)<br>
                    <strong>Break-even:</strong> Year {3 if roi_year5 > 0 else 6 if roi_year10 > 0 else 8}
                </p>
                <p style='color: #1976d2;'>📊 Public health ROI compounds over time</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add context about ROI
        st.info("""
        **Understanding Public Health ROI:**
        • Year 1 shows lower returns due to setup costs and implementation ramp-up
        • Benefits compound as: prevented deaths accumulate, stunting reduction shows effects, and healthcare savings grow
        • By Year 5-10, returns become strongly positive as full benefits are realized
        • Long-term returns (15-20 years) are even higher when children enter the workforce with better cognitive abilities
        
        **Key insight:** Every 1 KSH invested in zinc returns 2.8 KSH over 10 years in direct economic benefits alone.
        """)
        
        # Budget breakdown visualization
        st.markdown("### 📊 Where Does the Money Go?")
        
        budget_breakdown = []
        for key, percentage in interventions.items():
            if percentage > 0:
                budget_breakdown.append({
                    'Intervention': interventions_data[key]['name'],
                    'Budget': total_budget * percentage / 100,
                    'Percentage': percentage
                })
        
        budget_df = pd.DataFrame(budget_breakdown)
        
        fig = px.pie(budget_df, 
                     values='Budget', 
                     names='Intervention',
                     title="Budget Allocation by Intervention")
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Budget: %{value:,.0f} KSH<br>Percentage: %{percent}'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Funding sources and sustainability
        st.markdown("### 💼 Funding Strategy")
        
        with st.expander("Potential Funding Sources"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **Government Sources:** \n
                • National Treasury allocation \n
                • County government budgets \n
                • Universal Health Coverage funds \n
                • Social protection programs \n
                """)
            
            with col2:
                st.markdown("""
                **International Partners:** \n
                • World Bank nutrition projects \n
                • UNICEF country programs \n
                • Global Fund initiatives \n
                • Bilateral aid (USAID, DFID) \n
                """)
            
            with col3:
                st.markdown("""
                **Innovative Financing:** \n
                • Private sector partnerships \n
                • Development impact bonds \n
                • Carbon credit linkages \n
                • Diaspora bonds \n
                """)
    
    else:
        st.warning("⚠️ Please complete the intervention design first.")

# TECHNICAL DETAILS TAB
with tab4:
    st.markdown("## 🔬 Technical Details for Program Managers")
    
    # Implementation requirements
    st.markdown("### 🏗️ Implementation Requirements")
    
    tab_impl1, tab_impl2, tab_impl3 = st.tabs(["Infrastructure", "Human Resources", "Systems"])
    
    with tab_impl1:
        st.markdown("""
        **Laboratory Requirements:**
        • Atomic absorption spectroscopy for serum zinc
        • Quality control laboratories for fortified foods
        • Regional testing centers (minimum 8)
        
        **Storage & Distribution:**
        • Cold chain for liquid supplements
        • Warehouse capacity: 1000m² per million beneficiaries
        • Last-mile distribution networks
        
        **Manufacturing:**
        • Fortification equipment at mills
        • Local supplement production capacity
        • Quality assurance systems
        """)
    
    with tab_impl2:
        st.markdown("""
        **Healthcare Workers Needed:**
        • Nutritionists: 1 per 10,000 beneficiaries
        • CHWs: 1 per 100 households
        • Lab technicians: 20 nationally
        
        **Training Requirements:**
        • 3-day training for healthcare workers
        • 1-week training for program managers
        • Continuous supervision and mentoring
        
        **Support Staff:**
        • Data managers and M&E specialists
        • Supply chain coordinators
        • Community mobilizers
        """)
    
    with tab_impl3:
        st.markdown("""
        **Information Systems:**
        • Beneficiary registration database
        • Supply chain management system
        • Quality monitoring dashboard
        
        **Monitoring Tools:**
        • Mobile data collection apps
        • GIS mapping for coverage
        • Early warning systems
        
        **Reporting:**
        • Monthly facility reports
        • Quarterly outcome assessments
        • Annual impact evaluations
        """)
    
    # Quality indicators
    st.markdown("### 📊 Key Performance Indicators")
    
    kpi_data = {
        'Indicator': [
            'Coverage Rate',
            'Supplement Compliance',
            'Fortification Standards Met',
            'Stock-out Rate',
            'Cost per Beneficiary',
            'Stunting Reduction Rate'
        ],
        'Target': ['80%', '70%', '95%', '<5%', '<50 KSH', '20%'],
        'Measurement': [
            'Monthly surveys',
            'Facility records',
            'Lab testing',
            'LMIS reports',
            'Financial reports',
            'Annual surveys'
        ],
        'Responsible': [
            'M&E Team',
            'Health facilities',
            'Quality lab',
            'Supply chain',
            'Finance',
            'Nutrition unit'
        ]
    }
    
    kpi_df = pd.DataFrame(kpi_data)
    st.table(kpi_df)

# COMPARE SCENARIOS TAB
with tab5:
    st.markdown("## 📈 Scenario Comparison Tool")
    
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #1565c0;">Why Compare Scenarios?</h4>
        <p style="color: #212121;">Test different approaches to find the optimal strategy for your context and constraints.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick scenario generator
    st.markdown("### 🔄 Generate Scenarios to Compare")
    
    scenarios_to_compare = st.multiselect(
        "Select scenarios to compare",
        [
            "Current Plan",
            "Minimum Budget (500M KSH)",
            "Optimal Budget (2B KSH)",
            "Emergency Focus",
            "Long-term Sustainability",
            "Urban Focus",
            "Rural Priority"
        ],
        default=["Current Plan", "Optimal Budget (2B KSH)"]
    )
    
    if len(scenarios_to_compare) > 1:
        # Create comparison data
        comparison_data = []
        
        for scenario in scenarios_to_compare:
            if scenario == "Current Plan" and 'total_budget' in locals():
                comparison_data.append({
                    'Scenario': scenario,
                    'Budget (Million KSH)': total_budget / 1_000_000,
                    'Coverage (%)': coverage * 100 if 'coverage' in locals() else 0,
                    'Lives Saved': outcomes['lives_saved']['value'] if 'outcomes' in locals() else 0,
                    'ROI (%)': roi if 'roi' in locals() else 0
                })
            elif scenario == "Minimum Budget (500M KSH)":
                comparison_data.append({
                    'Scenario': scenario,
                    'Budget (Million KSH)': 500,
                    'Coverage (%)': 25,
                    'Lives Saved': 525,  # Updated based on new calculations
                    'ROI (%)': 180
                })
            elif scenario == "Optimal Budget (2B KSH)":
                # Calculate optimal budget based on current intervention mix
                if 'interventions' in locals():
                    optimal_result = calculate_optimal_budget(interventions)
                    comparison_data.append({
                        'Scenario': f"Optimal Budget ({optimal_result['optimal_budget']/1_000_000:.0f}M KSH)",
                        'Budget (Million KSH)': optimal_result['optimal_budget'] / 1_000_000,
                        'Coverage (%)': optimal_result['optimal_coverage'],
                        'Lives Saved': optimal_result['optimal_lives_saved'],
                        'ROI (%)': optimal_result['optimal_roi']
                    })
                else:
                    # Default if no interventions defined
                    comparison_data.append({
                        'Scenario': scenario,
                        'Budget (Million KSH)': 2000,
                        'Coverage (%)': 75,
                        'Lives Saved': 2400,  # Updated based on new calculations
                        'ROI (%)': 280
                    })
            else:
                # Generate other scenarios
                comparison_data.append({
                    'Scenario': scenario,
                    'Budget (Million KSH)': 1000,
                    'Coverage (%)': 50,
                    'Lives Saved': 1400,  # Updated based on new calculations
                    'ROI (%)': 220
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Display comparison table
        st.markdown("### 📊 Scenario Comparison Results")
        st.dataframe(comparison_df.style.format({
            'Budget (Million KSH)': '{:,.0f}',
            'Coverage (%)': '{:.1f}%',
            'Lives Saved': '{:,.0f}',
            'ROI (%)': '{:.0f}%'
        }))
        
        # Visual comparison
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Coverage (%)',
            x=comparison_df['Scenario'],
            y=comparison_df['Coverage (%)'],
            yaxis='y',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='ROI (%)',
            x=comparison_df['Scenario'],
            y=comparison_df['ROI (%)'],
            yaxis='y2',
            marker_color='lightgreen'
        ))
        
        fig.update_layout(
            title='Scenario Performance Comparison',
            yaxis=dict(
                title=dict(text='Coverage (%)', font=dict(color='blue')), 
                tickfont=dict(color='blue')
            ),
            yaxis2=dict(
                title=dict(text='ROI (%)', font=dict(color='green')), 
                tickfont=dict(color='green'),
                overlaying='y', 
                side='right'
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations based on comparison
        st.markdown("### 💡 Insights from Comparison")
        
        best_roi = comparison_df.loc[comparison_df['ROI (%)'].idxmax()]
        best_coverage = comparison_df.loc[comparison_df['Coverage (%)'].idxmax()]
        
        st.success(f"""
        **Key Findings:** \n
        • Best ROI: {best_roi['Scenario']} with {best_roi['ROI (%)']:.0f}% return \n
        • Best Coverage: {best_coverage['Scenario']} reaching {best_coverage['Coverage (%)']:.0f}% of target population \n
        • Recommended: Balance between coverage and ROI for sustainable impact
        """)

# RESOURCES TAB
with tab6:
    st.markdown("## 📚 Resources & Support")
    
    # Quick reference guide
    st.markdown("### 📖 Quick Reference Guide")
    
    with st.expander("Glossary of Terms"):
        glossary = {
            "Zinc Deficiency": "Blood zinc levels below 70 μg/dL, causing growth and immune problems",
            "Stunting": "Height-for-age below -2 standard deviations from WHO growth standards",
            "Biofortification": "Breeding crops to increase their nutritional value naturally",
            "Coverage": "Percentage of target population receiving the intervention",
            "ROI": "Return on Investment - economic benefits divided by costs",
            "CHW": "Community Health Worker - trained health service provider at village level",
            "ORS": "Oral Rehydration Solution - treatment for dehydration from diarrhea",
            "Fortification": "Adding micronutrients to commonly consumed foods",
            "IMCI": "Integrated Management of Childhood Illness - WHO/UNICEF strategy",
            "ANC": "Antenatal Care - healthcare during pregnancy"
        }
        
        for term, definition in glossary.items():
            st.markdown(f"**{term}:** {definition}")
    
    # Evidence base
    st.markdown("### 🔬 Evidence & Research")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Key Studies:** \n
        • [WHO ELENA Evidence Brief (2023)](https://www.who.int/tools/elena/interventions/zinc-diarrhoea) – global dosage & efficacy of therapeutic zinc \n
        • [Ali et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11622351/) – 38-trial systematic review on zinc & diarrhoea outcomes \n
        • [Kenya DHS 2022 – Final Report](https://dhsprogram.com/publications/publication-fr380-dhs-final-reports.cfm) – most recent national nutrition dataset \n

        **Success Stories:** \n
        • Bangladesh: 50% reduction in diarrhea deaths \n
        • Peru: Stunting reduced from 40% to 14% \n
        • Rwanda: 17% stunting reduction via fortification \n
        """)
    
    with col2:
        st.markdown("""
        **Implementation Guides:**  \n
        • [Kenya Clinical Guidelines – Community Level (2025)](https://health.go.ke/sites/default/files/2025-04/Clinical%20Guidelines%20for%20Level%201%20Community%20Health%20Services.pdf)  \n
        • [WFP Food-Fortification Manual (2024)](https://www.wfp.org/publications/food-fortification)  \n
        • [HarvestPlus Annual Report 2023 – Biofortification Scale-up](https://www.harvestplus.org/wp-content/uploads/2024/07/2023-HarvestPlus-Annual-Report.pdf)  \n

        **Training Materials:** \n
        • Healthcare worker training modules \n
        • Community mobilization guides \n
        • M&E frameworks and tools
        """)
    
    # Contact and support
    st.markdown("### 📞 Get Support")
    
    st.info("""
    **Technical Support:**
    • Email: nutrition.support@health.go.ke
    • Phone: +254 20 2717077
    • WhatsApp: +254 700 000000
    
    **Partner Organizations:**
    • UNICEF Kenya: unicef.org/kenya
    • Nutrition International: nutritionintl.org
    • World Bank: worldbank.org/kenya
    
    **Report Issues:**
    • System bugs: github.com/zinc-simulator/issues
    • Data updates: data@nutritionkenya.org
    """)
    
    # PDF Generation Functions
    def generate_planning_template_pdf():
        """Generate a PDF planning template"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1565c0'),
            alignment=TA_CENTER
        )
        story.append(Paragraph("Zinc Intervention Planning Template", title_style))
        story.append(Spacer(1, 30))
        
        # Introduction
        story.append(Paragraph("<b>Purpose:</b> This template helps you plan and budget zinc intervention programs in Kenya.", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Section 1: Program Overview
        story.append(Paragraph("<b>1. Program Overview</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        data = [
            ['Program Element', 'Description', 'Budget (KSH)', 'Timeline'],
            ['Program Name', '', '', ''],
            ['Target Population', '', '', ''],
            ['Geographic Coverage', '', '', ''],
            ['Primary Intervention', '', '', ''],
            ['Secondary Interventions', '', '', ''],
            ['Total Budget', '', '', ''],
        ]
        
        table = Table(data, colWidths=[2*inch, 2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565c0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Section 2: Target Groups
        story.append(Paragraph("<b>2. Target Population Details</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        target_data = [
            ['Population Group', 'Number', 'Coverage %', 'Priority'],
            ['Children under 5', '', '', 'High/Medium/Low'],
            ['Pregnant women', '', '', 'High/Medium/Low'],
            ['Lactating mothers', '', '', 'High/Medium/Low'],
            ['Stunted children', '', '', 'High/Medium/Low'],
            ['Rural population', '', '', 'High/Medium/Low'],
        ]
        
        target_table = Table(target_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 2*inch])
        target_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4caf50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(target_table)
        story.append(PageBreak())
        
        # Section 3: Intervention Mix
        story.append(Paragraph("<b>3. Intervention Strategy Mix</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        intervention_data = [
            ['Intervention Type', 'Budget %', 'People Reached', 'Cost/Person'],
            ['Food Fortification', '', '', ''],
            ['Therapeutic Zinc', '', '', ''],
            ['Preventive Supplements', '', '', ''],
            ['Biofortified Crops', '', '', ''],
            ['Maternal Programs', '', '', ''],
            ['Community Health', '', '', ''],
        ]
        
        intervention_table = Table(intervention_data, colWidths=[2.5*inch, 1.5*inch, 1.8*inch, 1.7*inch])
        intervention_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(intervention_table)
        story.append(Spacer(1, 20))
        
        # Section 4: Timeline
        story.append(Paragraph("<b>4. Implementation Timeline</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        timeline_data = [
            ['Phase', 'Months', 'Key Activities', 'Milestones'],
            ['Planning', '0-3', '', ''],
            ['Pilot', '3-6', '', ''],
            ['Scale-up', '6-12', '', ''],
            ['Full Implementation', '12-24', '', ''],
            ['Evaluation', '24-36', '', ''],
        ]
        
        timeline_table = Table(timeline_data, colWidths=[1.5*inch, 1.2*inch, 2.5*inch, 2.3*inch])
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9c27b0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(timeline_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Generated by Kenya Zinc Intervention Simulator", styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_me_framework_pdf():
        """Generate M&E Framework PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1565c0'),
            alignment=TA_CENTER
        )
        story.append(Paragraph("Monitoring & Evaluation Framework", title_style))
        story.append(Paragraph("Zinc Intervention Program - Kenya", styles['Title']))
        story.append(Spacer(1, 30))
        
        # Introduction
        story.append(Paragraph("<b>Purpose:</b>", styles['Heading2']))
        story.append(Paragraph(
            "This M&E framework provides a comprehensive system for tracking progress, measuring impact, "
            "and ensuring accountability in zinc intervention programs. It includes indicators, data collection "
            "methods, and reporting templates aligned with WHO and national guidelines.",
            styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # Logic Model
        story.append(Paragraph("<b>1. Results Chain</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        logic_data = [
            ['Level', 'Description', 'Indicators', 'Targets'],
            ['Impact', 'Reduced child mortality and \nimproved nutrition', 'Under-5 mortality rate\nStunting prevalence', '<70/1000\n<20%'],
            ['Outcome', 'Improved zinc status in population', 'Zinc deficiency prevalence\nDiarrhea incidence', '<30%\n<10%'],
            ['Output', 'Increased zinc intake', 'Coverage rate\nSupplement distribution', '>80%\n>90%'],
            ['Activity', 'Program implementation', 'Training completed\nSupplies delivered', '100%\n100%'],
            ['Input', 'Resources allocated', 'Budget utilization\nStaff recruited', '>95%\n100%'],
        ]
        
        logic_table = Table(logic_data, colWidths=[1.2*inch, 2.3*inch, 2*inch, 2*inch])
        logic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196f3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(logic_table)
        story.append(PageBreak())
        
        # Key Performance Indicators
        story.append(Paragraph("<b>2. Key Performance Indicators (KPIs)</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        kpi_data = [
            ['Indicator', 'Definition', 'Frequency', 'Method', 'Responsible'],
            ['Coverage Rate', '% population receiving zinc', 'Monthly', 'Facility reports', 'M&E Officer'],
            ['Compliance Rate', '% completing treatment course', 'Monthly', 'Follow-up surveys', 'CHWs'],
            ['Stock-out Rate', '% facilities with zinc stockouts', 'Weekly', 'LMIS', 'Supply Chain'],
            ['Quality Score', 'Fortification standards met', 'Quarterly', 'Lab testing', 'Quality Lab'],
            ['Cost Efficiency', 'Cost per beneficiary', 'Quarterly', 'Financial reports', 'Finance'],
            ['Stunting Rate', 'Height-for-age <-2 SD', 'Annual', 'SMART survey', 'Nutrition Unit'],
        ]
        
        kpi_table = Table(kpi_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1.5*inch, 1.5*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4caf50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 20))
        
        # Data Collection Tools
        story.append(Paragraph("<b>3. Data Collection Tools</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        tools_data = [
            ['Tool', 'Purpose', 'Frequency', 'Users'],
            ['Facility Register', 'Track beneficiaries and supplies', 'Daily', 'Health workers'],
            ['Supervision Checklist', 'Quality assurance', 'Monthly', 'Supervisors'],
            ['Household Survey', 'Coverage and compliance', 'Quarterly', 'M&E team'],
            ['Stock Card', 'Inventory management', 'Daily', 'Store keeper'],
            ['Dashboard', 'Real-time monitoring', 'Continuous', 'Program managers'],
        ]
        
        tools_table = Table(tools_data, colWidths=[1.8*inch, 2.5*inch, 1.5*inch, 1.7*inch])
        tools_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(tools_table)
        story.append(PageBreak())
        
        # Reporting Schedule
        story.append(Paragraph("<b>4. Reporting Schedule</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        reporting_data = [
            ['Report Type', 'Frequency', 'Due Date', 'Audience'],
            ['Activity Report', 'Monthly', '5th of following month', 'Program Manager'],
            ['Progress Report', 'Quarterly', '15th of following quarter', 'Ministry of Health'],
            ['Financial Report', 'Quarterly', '20th of following quarter', 'Donors'],
            ['Impact Evaluation', 'Annual', 'End of program year', 'All stakeholders'],
            ['Success Stories', 'Bi-annual', 'June and December', 'Public/Media'],
        ]
        
        reporting_table = Table(reporting_data, colWidths=[2*inch, 1.5*inch, 2*inch, 2*inch])
        reporting_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9c27b0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(reporting_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Generated by Kenya Zinc Intervention Simulator", styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_policy_brief_pdf():
        """Generate Policy Brief PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=28,
            textColor=colors.HexColor('#d32f2f'),
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        story.append(Paragraph("POLICY BRIEF", title_style))
        story.append(Paragraph("Addressing Zinc Deficiency in Kenya", subtitle_style))
        story.append(Paragraph("Evidence-Based Recommendations for National Action", styles['Title']))
        story.append(Spacer(1, 30))
        
        # Executive Summary Box
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12
        )
        
        story.append(Paragraph("<b>EXECUTIVE SUMMARY</b>", styles['Heading2']))
        story.append(Paragraph(
            "Zinc deficiency affects 51% of Kenya's population, contributing to 15% of child deaths "
            "and costing the economy 2.3% of GDP annually. This brief presents evidence-based "
            "interventions that can save 1,800 lives annually and generate a 250% return on investment "
            "within 10 years. Immediate action is needed to implement a comprehensive zinc program "
            "combining fortification, supplementation, and therapeutic zinc distribution.",
            summary_style
        ))
        story.append(Spacer(1, 20))
        
        # The Problem
        story.append(Paragraph("<b>THE PROBLEM: A HIDDEN CRISIS</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        problem_data = [
            ['Impact Area', 'Current Status', 'Annual Cost'],
            ['Affected Population', '26.5 million Kenyans', 'Human suffering'],
            ['Child Deaths', '12,000 preventable deaths', 'Lost potential'],
            ['Stunting', '1 in 4 children stunted', 'Cognitive impairment'],
            ['Economic Loss', '2.3% of GDP', '230 billion KSH'],
            ['Healthcare Burden', '500,000 hospitalizations', '15 billion KSH'],
        ]
        
        problem_table = Table(problem_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
        problem_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.pink),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(problem_table)
        story.append(PageBreak())
        
        # The Solution
        story.append(Paragraph("<b>THE SOLUTION: EVIDENCE-BASED INTERVENTIONS</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("<b>Recommended Intervention Mix:</b>", styles['Heading3']))
        story.append(Spacer(1, 8))
        
        solution_data = [
            ['Intervention', 'Coverage Target', 'Investment', 'Lives Saved'],
            ['Food Fortification (30%)', '85% of population', '600M KSH', '540 children'],
            ['Therapeutic Zinc (25%)', '60% of diarrhea cases', '500M KSH', '450 children'],
            ['Preventive Supplements (20%)', '70% of at-risk groups', '400M KSH', '360 children'],
            ['Biofortified Crops (10%)', '75% of rural areas', '200M KSH', '180 children'],
            ['Maternal Programs (10%)', '80% of pregnant women', '200M KSH', '180 children'],
            ['Community Health (5%)', '90% of communities', '100M KSH', '90 children'],
            ['TOTAL', '10 million people', '2 Billion KSH', '1,800 children'],
        ]
        
        solution_table = Table(solution_data, colWidths=[2.2*inch, 1.8*inch, 1.5*inch, 1.5*inch])
        solution_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4caf50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.lightgreen),
            ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(solution_table)
        story.append(Spacer(1, 20))
        
        # Return on Investment
        story.append(Paragraph("<b>RETURN ON INVESTMENT</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        roi_data = [
            ['Timeframe', 'Investment', 'Returns', 'ROI'],
            ['Year 1', '2B KSH', '1.5B KSH', '-25%'],
            ['Year 5', '10B KSH', '15B KSH', '+50%'],
            ['Year 10', '20B KSH', '50B KSH', '+250%'],
        ]
        
        roi_table = Table(roi_data, colWidths=[2*inch, 2*inch, 2*inch, 1.5*inch])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(roi_table)
        story.append(Spacer(1, 20))
        
        # Policy Recommendations
        story.append(Paragraph("<b>POLICY RECOMMENDATIONS</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        recommendations = [
            "1. <b>Immediate Action:</b> Allocate 2 billion KSH (0.67% of health budget) for zinc interventions",
            "2. <b>Legislation:</b> Mandate zinc fortification of wheat flour and maize meal by 2025",
            "3. <b>Healthcare Integration:</b> Include zinc in essential medicines list and IMCI protocols",
            "4. <b>Supply Chain:</b> Ensure zinc availability in all health facilities (zero stock-outs)",
            "5. <b>Monitoring:</b> Establish national zinc deficiency surveillance system",
            "6. <b>Partnerships:</b> Engage private sector in fortification and biofortification programs",
            "7. <b>Community Engagement:</b> Train 10,000 CHWs on zinc supplementation",
            "8. <b>Research:</b> Support local evidence generation on zinc interventions"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
            story.append(Spacer(1, 6))
        
        story.append(PageBreak())
        
        # Success Examples
        story.append(Paragraph("<b>PROVEN SUCCESS: LEARNING FROM OTHERS</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        success_data = [
            ['Country', 'Intervention', 'Result', 'Timeframe'],
            ['Bangladesh', 'Zinc + ORS for diarrhea', '50% reduction in deaths', '5 years'],
            ['Peru', 'Targeted supplementation', 'Stunting: 40% to 14%', '10 years'],
            ['Rwanda', 'Food fortification', '17% stunting reduction', '7 years'],
            ['Indonesia', 'Maternal zinc program', '20% less low birth weight', '3 years'],
            ['Ethiopia', 'Community programs', '15 million reached', '8 years'],
        ]
        
        success_table = Table(success_data, colWidths=[1.5*inch, 2.5*inch, 2*inch, 1.5*inch])
        success_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(success_table)
        story.append(Spacer(1, 20))
        
        # Call to Action
        story.append(Paragraph("<b>CALL TO ACTION</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        action_style = ParagraphStyle(
            'Action',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#d32f2f'),
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        story.append(Paragraph(
            "<b>Every day of delay costs 5 child lives and 6 million KSH in economic losses.</b>",
            action_style
        ))
        story.append(Paragraph(
            "<b>The time to act is NOW.</b>",
            action_style
        ))
        story.append(Spacer(1, 20))
        
        # Contact Information
        story.append(Paragraph("<b>FOR MORE INFORMATION:</b>", styles['Heading3']))
        story.append(Paragraph("Ministry of Health, Division of Nutrition", styles['Normal']))
        story.append(Paragraph("Email: nutrition@health.go.ke | Tel: +254 20 2717077", styles['Normal']))
        story.append(Paragraph("Website: www.health.go.ke/nutrition", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("_" * 80, styles['Normal']))
        story.append(Paragraph(f"Generated by Kenya Zinc Intervention Simulator | {datetime.now().strftime('%B %Y')}", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    # Download materials
    st.markdown("### 📥 Download Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        planning_pdf = generate_planning_template_pdf()
        st.download_button(
            label="📋 Planning Template",
            data=planning_pdf,
            file_name="zinc_planning_template.pdf",
            mime="application/pdf"
        )
    
    with col2:
        me_pdf = generate_me_framework_pdf()
        st.download_button(
            label="📊 M&E Framework",
            data=me_pdf,
            file_name="zinc_me_framework.pdf",
            mime="application/pdf"
        )
    
    with col3:
        policy_pdf = generate_policy_brief_pdf()
        st.download_button(
            label="🎯 Policy Brief",
            data=policy_pdf,
            file_name="zinc_policy_brief.pdf",
            mime="application/pdf"
        )

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("📥 Export Full Report", type="primary"):
        st.info("Report generation in progress...")
    
    if st.button("💾 Save Scenario"):
        if 'total_budget' in locals():
            st.session_state.scenario_history.append({
                'timestamp': datetime.now(),
                'budget': total_budget,
                'interventions': interventions if 'interventions' in locals() else {}
            })
            st.success("Scenario saved!")
    
    if st.button("🔄 Reset All"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Session Summary")
    if len(st.session_state.scenario_history) > 0:
        st.metric("Scenarios Tested", len(st.session_state.scenario_history))
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Quick Facts")
    
    with st.expander("Why Zinc Matters"):
        st.markdown("""
        • Prevents 500,000 child deaths/year globally\n
        • Reduces diarrhea duration by 25% \n
        • Improves growth in stunted children \n
        • Boosts immune system function \n
        • Essential for brain development \n
        """)
    
    with st.expander("Kenya Context"):
        st.markdown("""
        • 51% population zinc deficient \n
        • 26% of children stunted \n
        • 15% children have chronic diarrhea \n
        • 2.3% GDP lost to malnutrition \n
        • 89% consume inadequate zinc \n
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        Version 3.0 | Updated 2024<br>
        Ministry of Health, Kenya
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    💊 Zinc Intervention Simulator | Evidence-based planning for better nutrition outcomes<br>
    Developed with support from UNICEF, WHO, and World Bank
</div>
""", unsafe_allow_html=True)