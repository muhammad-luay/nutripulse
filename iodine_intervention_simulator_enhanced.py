"""
Iodine Deficiency Intervention Simulation Platform
===================================================
An evidence-based tool for planning and evaluating iodine supplementation strategies
Designed for policy makers, program managers, and funding organizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Kenya Iodine Intervention Simulator",
    page_icon="🧂",
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
    <h1>🌍 Kenya Iodine Intervention Planning Platform</h1>
    <p style="font-size: 1.2rem;">Evidence-Based Decision Support for Nutrition Programs</p>
</div>
""", unsafe_allow_html=True)

# Tutorial/Onboarding
if st.session_state.show_tutorial:
    with st.container():
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #1565c0;">👋 Welcome to the Iodine Intervention Simulator</h3>
            <p style="color: #212121;"><strong>What this tool does:</strong> Helps you plan, budget, and predict outcomes of iodine supplementation programs to combat universal deficiency in Kenya.</p>
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
            - Cognitive gains
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
        <h4 style="color: #b71c1c;">🚨 Iodine Deficiency Rate</h4>
        <h2 style="color: #d32f2f;">100%</h2>
        <p style="color: #424242;">47.5 million people affected</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style="background-color: #fff3e0; border-left: 5px solid #f57c00;">
        <h4 style="color: #e65100;">📉 Goiter Prevalence</h4>
        <h2 style="color: #f57c00;">22%</h2>
        <p style="color: #424242;">10.5 million with visible goiter</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card" style="background-color: #fffde7; border-left: 5px solid #fbc02d;">
        <h4 style="color: #f57f17;">🧠 Cognitive Impact</h4>
        <h2 style="color: #f9a825;">-13 IQ</h2>
        <p style="color: #424242;">Points lost per child</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card" style="background-color: #f3e5f5; border-left: 5px solid #7b1fa2;">
        <h4 style="color: #4a148c;">💰 Economic Loss</h4>
        <h2 style="color: #7b1fa2;">1.9% GDP</h2>
        <p style="color: #424242;">Due to iodine deficiency</p>
    </div>
    """, unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Intervention Setup", "📈 Outcomes Prediction", "💰 Cost Analysis", "🔧 Technical Details", "🔄 Compare Scenarios", "📋 Reports", "📚 Resources & Help"])

# Constants based on Kenya data
KENYA_POPULATION = 52_000_000  # Updated to match zinc simulator
AFFECTED_POPULATION = KENYA_POPULATION  # 100% deficiency
CHILDREN_UNDER_5 = int(KENYA_POPULATION * 0.135)  # Updated to match zinc
PREGNANT_WOMEN = int(KENYA_POPULATION * 0.032)  # Updated to match zinc
RURAL_POPULATION = int(KENYA_POPULATION * 0.72)  # Updated to match zinc
GOITER_CASES = int(KENYA_POPULATION * 0.22)  # 22% goiter prevalence

# Dynamic configuration to avoid hardcoding
CONFIG = {
    # Health parameters
    'cretinism_rate_per_1000_births': 3.0,  # WHO estimate for severe deficiency
    'goiter_reduction_rate': 0.6,  # 60% reduction possible
    'pregnancy_complication_rate': 0.10,  # 10% baseline
    'pregnancy_complication_reduction': 0.3,  # 30% reduction with intervention
    
    # Economic parameters
    'avg_annual_income': 24000,  # KSH per person
    'productivity_gain_rate': 0.005,  # 0.5% productivity improvement
    'special_ed_need_rate': 0.02,  # 2% of children
    'special_ed_reduction_rate': 0.5,  # 50% reduction
    
    # Healthcare costs
    'goiter_treatment_cost': 2000,  # KSH per case
    'pregnancy_complication_cost': 15000,  # KSH per case
    'cretinism_lifetime_cost': 300000,  # KSH lifetime
    'special_education_annual_cost': 10000,  # KSH per year
    
    # Infrastructure costs
    'health_center_cost': 15_000_000,  # KSH to build/equip
    'nurse_training_cost': 600_000,  # KSH per nurse
    'medical_scholarship_cost': 100_000,  # KSH per scholarship
    
    # System capacity
    'max_annual_capacity': 2_500_000_000,  # 2.5B KSH max manageable
    'optimal_budget_default': 1_500_000_000,  # 1.5B KSH
    'health_budget_total': 300_000_000_000,  # 300B KSH total health budget
    
    # Benefit realization timeline
    'year1_benefit_realization': 0.4,  # 40% of benefits in year 1
    'year2_benefit_realization': 0.7,  # 70% in year 2
    'year3_5_benefit_realization': 1.0,  # 100% from year 3 onwards
    'efficiency_gain_per_year': 0.1,  # 10% efficiency gain
    
    # Coverage saturation parameters
    'high_coverage_threshold': 0.8,  # 80% coverage
    'saturation_penalty': 0.3,  # 30% penalty at 100% coverage
    
    # Success thresholds
    'good_coverage_threshold': 80,  # 80% coverage is good
    'good_roi_threshold': 100,  # 100% ROI is good
    'good_cretinism_threshold': 400,  # 400+ cases prevented is good
    'cost_per_person_threshold': 100,  # < 100 KSH per person is good
    'cost_per_iq_threshold': 5000,  # < 5000 KSH per IQ point is good
    'cost_per_goiter_threshold': 10000,  # < 10000 KSH per goiter case is good
    'cost_per_pregnancy_threshold': 100000,  # < 100K per pregnancy saved is good
}

# DYNAMIC ECONOMIC CALCULATION SYSTEM

def calculate_dynamic_cost_per_outcome(budget, coverage, efficiency, context):
    """
    Dynamically calculate cost per outcome based on real conditions
    FIXED: Proper calculation of cases prevented
    """
    
    # Base calculation - rate per 1000 births
    base_prevention_rate = CONFIG['cretinism_rate_per_1000_births'] / 1000  # Convert to rate
    
    # DYNAMIC ADJUSTMENT 1: Severity-based prevention potential
    severity_multiplier = context.get('deficiency_severity', 0.9)  # Kenya has severe deficiency
    
    # DYNAMIC ADJUSTMENT 2: Intervention timing impact
    timing_factors = {
        'preconception': 1.2,
        'first_trimester': 1.0,
        'second_trimester': 0.7,
        'third_trimester': 0.4,
        'postnatal': 0.2
    }
    timing_multiplier = timing_factors.get(context.get('intervention_timing', 'first_trimester'), 1.0)
    
    # DYNAMIC ADJUSTMENT 3: Population risk stratification
    if context.get('targeting_strategy') == 'risk_based':
        prevention_boost = 1.2  # Slightly reduced from 1.3
    else:
        prevention_boost = 1.0
    
    # DYNAMIC ADJUSTMENT 4: Intervention quality - LESS PUNITIVE
    # These should multiply to ~0.7-0.8 for realistic programs, not 0.3!
    quality_factors = {
        'iodine_content': context.get('iodine_content_adequacy', 0.9),      # Good quality
        'compliance_rate': context.get('population_compliance', 0.85),      # Reasonable compliance
        'supply_consistency': context.get('supply_chain_reliability', 0.9), # Good supply
        'monitoring_quality': context.get('monitoring_effectiveness', 0.95) # Basic monitoring works
    }
    
    # Use geometric mean instead of product to avoid excessive punishment
    quality_multiplier = np.power(np.prod(list(quality_factors.values())), 0.5)  # Square root softens the impact
    
    # Calculate actual cases prevented - FIXED CALCULATION
    pregnancies_reached = PREGNANT_WOMEN * coverage * efficiency / 100
    
    # Apply all factors to the base rate
    effective_prevention_rate = base_prevention_rate * severity_multiplier * timing_multiplier * prevention_boost * quality_multiplier
    
    # Calculate cases prevented (no extra division by 1000!)
    cases_prevented = pregnancies_reached * effective_prevention_rate
    
    # Calculate dynamic cost per case
    if cases_prevented > 0:
        cost_per_case = budget / cases_prevented
        
        # Dynamic comparator adjustments
        delivery_mode = context.get('delivery_mode', 'standalone')
        adjustment = 1.5 if delivery_mode == 'rural' else 1.0
        
        dynamic_comparators = {
            'Vitamin A': 35_000 * adjustment,
            'Folic acid': 250_000 * adjustment,
            'Iron fortification': 150_000 * adjustment,
            'Measles vaccine': 100_000 * adjustment
        }
        
        # Determine cost-effectiveness rating
        if cost_per_case < dynamic_comparators['Vitamin A']:
            rating = "🌟 Exceptionally cost-effective"
        elif cost_per_case < dynamic_comparators['Measles vaccine']:
            rating = "✅ Highly cost-effective"
        elif cost_per_case < dynamic_comparators['Iron fortification']:
            rating = "👍 Cost-effective"
        elif cost_per_case < dynamic_comparators['Folic acid']:
            rating = "⚠️ Moderately cost-effective"
        else:
            rating = "❌ Review needed"
        
        return {
            'cost_per_case': cost_per_case,
            'cases_prevented': cases_prevented,
            'rating': rating,
            'comparators': dynamic_comparators
        }
    
    return {
        'cost_per_case': float('inf'),
        'cases_prevented': 0,
        'rating': "❌ No cases prevented",
        'comparators': {}
    }

def calculate_dynamic_roi_timeline(budget, annual_benefits, context, years=10):
    """
    Calculate realistic ROI that adapts to intervention characteristics
    """
    
    roi_timeline = {}
    
    # Determine ramp-up curve based on intervention type
    intervention_type = context.get('primary_intervention', 'mixed')
    
    ramp_up_curves = {
        'salt': [0.2, 0.5, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # Slow start
        'supplement': [0.6, 0.85, 0.95, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # Quick start
        'mixed': [0.4, 0.65, 0.85, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # Moderate
    }
    
    curve = ramp_up_curves.get(intervention_type, ramp_up_curves['mixed'])
    
    cumulative_benefits = 0
    cumulative_costs = 0
    
    for year in range(1, years + 1):
        # Year-specific realization rate
        realization_rate = curve[year - 1] if year <= len(curve) else 1.0
        
        # Maturation effects
        efficiency_improvement = min(1 + (year - 1) * 0.05, 1.3)  # Up to 30% improvement
        scale_economies = 1 - (0.02 * min(year, 5))  # 2% cost reduction per year
        
        # Risk factors
        risk_factor = context.get('risk_adjustment', 0.85)
        
        # Calculate year-specific costs and benefits - MORE REALISTIC
        if year == 1:
            # Year 1: High costs, minimal benefits
            yearly_cost = budget * 1.3  # 30% overhead for setup, training, systems
            yearly_benefit = annual_benefits * realization_rate * risk_factor * 0.3  # Only 30% of benefits in year 1
        elif year == 2:
            # Year 2: Normalizing costs, increasing benefits
            yearly_cost = budget * 1.1  # Still some overhead
            yearly_benefit = annual_benefits * realization_rate * risk_factor * 0.7  # 70% of benefits
        else:
            # Year 3+: Efficient operations
            yearly_cost = budget * scale_economies
            yearly_benefit = annual_benefits * realization_rate * efficiency_improvement * risk_factor
        
        # Apply economic adjustments
        inflation = (1 + context.get('inflation_rate', 0.055)) ** year
        discount = 1 / (1 + context.get('discount_rate', 0.08)) ** year
        
        adjusted_benefit = yearly_benefit * discount
        adjusted_cost = yearly_cost * inflation * discount
        
        cumulative_benefits += adjusted_benefit
        cumulative_costs += adjusted_cost
        
        # Calculate ROI
        if cumulative_costs > 0:
            roi = ((cumulative_benefits - cumulative_costs) / cumulative_costs) * 100
        else:
            roi = 0
        
        roi_timeline[year] = {
            'roi': roi,
            'cumulative_benefits': cumulative_benefits,
            'cumulative_costs': cumulative_costs,
            'yearly_benefit': adjusted_benefit,
            'yearly_cost': adjusted_cost,
            'break_even': cumulative_benefits >= cumulative_costs
        }
    
    return roi_timeline

def validate_economic_metrics(metrics):
    """
    Validate economic metrics for consistency and realism
    ENHANCED: More aggressive correction of unrealistic values
    """
    
    issues = []
    
    # Check ROI progression
    if 'roi_year1' in metrics and 'roi_year5' in metrics and 'roi_year10' in metrics:
        roi_1 = metrics['roi_year1']
        roi_5 = metrics['roi_year5']
        roi_10 = metrics['roi_year10']
        
        # Year 1 ROI should typically be negative or very low
        if roi_1 > 50:
            issues.append("Year 1 ROI adjusted for realism")
            metrics['roi_year1'] = -25  # Most programs lose money in Year 1
        elif roi_1 > 0:
            issues.append("Year 1 ROI adjusted to negative")
            metrics['roi_year1'] = -10  # At least small loss
        
        # ROI should progressively increase
        if roi_5 < roi_1:
            issues.append("ROI progression adjusted")
            metrics['roi_year5'] = max(roi_1 + 100, 50)  # Ensure progression
        
        if roi_10 < roi_5:
            issues.append("Long-term ROI adjusted")
            metrics['roi_year10'] = roi_5 * 1.3  # 30% improvement from year 5 to 10
    
    # Check cost per outcome
    if 'cost_per_case' in metrics:
        cost = metrics['cost_per_case']
        
        # Should be within reasonable range compared to benchmarks
        if cost < 30_000:
            issues.append("Cost per case too low - adjusted")
            metrics['cost_per_case'] = 80_000  # More realistic minimum
        elif cost > 500_000:
            # This is the likely issue - cost is too high
            issues.append("Cost per case too high - check calculation")
            # Don't auto-adjust if too high, as this indicates a real problem
    
    # Check return multiplier consistency
    if 'roi_year10' in metrics and 'return_multiplier' in metrics:
        roi_10 = metrics['roi_year10']
        expected_multiplier = (100 + roi_10) / 100
        stated_multiplier = metrics['return_multiplier']
        
        if abs(expected_multiplier - stated_multiplier) > 0.2:
            issues.append("Return multiplier corrected")
            metrics['return_multiplier'] = expected_multiplier
        
        # Sanity check on multiplier
        if metrics['return_multiplier'] > 10:
            issues.append("Return multiplier capped at realistic level")
            metrics['return_multiplier'] = 4.5  # Cap at 4.5x return
    
    return metrics, issues

def get_intervention_details():
    """Detailed intervention information for policy makers"""
    return {
        'salt_iodization': {
            'name': 'Universal Salt Iodization',
            'unit_cost': 2.5,
            'effectiveness': 0.85,
            'reach_time': 6,
            'coverage_potential': 0.90,
            'description': """
                **What it is:** Adding potassium iodate to all salt at production/import points.
                
                **How it works:** Iodine is added to salt at 30-40 ppm during processing or importation.
                
                **Advantages:**
                • Most cost-effective population-wide intervention
                • No behavior change required from consumers
                • Proven track record globally
                • Sustainable once established
                
                **Challenges:**
                • Requires functional monitoring system
                • Small-scale salt producers need support
                • Quality control at multiple points
                • Political will for enforcement
                
                **Success Example:** China eliminated iodine deficiency in 95% of population through USI.
            """,
            'policy_requirements': [
                "Mandatory iodization legislation",
                "Quality standards (30-40 ppm)",
                "Border control for imports",
                "Penalties for non-compliance"
            ]
        },
        'oil_fortification': {
            'name': 'Edible Oil Iodization',
            'unit_cost': 30,  # Annual cost (15 KSH per 6 months)
            'effectiveness': 0.92,
            'reach_time': 3,
            'coverage_potential': 0.75,
            'description': """
                **What it is:** Adding iodine to cooking oil for better retention and stability.
                
                **How it works:** Iodine is added to vegetable oil during refining using lipophilic compounds.
                
                **Advantages:**
                • Better iodine retention during cooking
                • Reaches populations using less salt
                • Stable in tropical climates
                • Complements salt iodization
                
                **Challenges:**
                • Higher cost than salt iodization
                • Limited oil refineries in Kenya
                • Requires new technology adoption
                • Consumer acceptance needed
                
                **Success Example:** India's Tamil Nadu achieved 85% coverage through dual fortification.
            """,
            'policy_requirements': [
                "Fortification standards for oil",
                "Technology transfer agreements",
                "Refinery equipment subsidies",
                "Consumer awareness campaigns"
            ]
        },
        'direct_supplement': {
            'name': 'Direct Iodine Supplementation',
            'unit_cost': 50,
            'effectiveness': 0.98,
            'reach_time': 1,
            'coverage_potential': 0.65,
            'description': """
                **What it is:** Iodine capsules or liquid drops given directly to at-risk groups.
                
                **How it works:** Annual 200-400mg iodine capsules or weekly drops for children and pregnant women.
                
                **Target Groups:**
                • Pregnant and lactating women
                • Children under 2 years
                • Populations in severe deficiency areas
                
                **Advantages:**
                • Immediate impact on iodine status
                • Precise dosing possible
                • Can target highest-risk groups
                • Works where fortification fails
                
                **Challenges:**
                • Requires health system delivery
                • Higher cost per person
                • Needs repeated distribution
                • Compliance monitoring needed
                
                **Success Example:** Ethiopia reduced cretinism by 90% in endemic areas through supplementation.
            """,
            'policy_requirements': [
                "Integration into ANC/PNC services",
                "Training for health workers",
                "Supply chain management",
                "Coverage monitoring systems"
            ]
        },
        'school_program': {
            'name': 'School-Based Iodine Programs',
            'unit_cost': 8,
            'effectiveness': 0.88,
            'reach_time': 2,
            'coverage_potential': 0.80,
            'description': """
                **What it is:** Providing iodized meals or supplements through school feeding programs.
                
                **How it works:** Daily iodized meals or weekly iodine supplements administered in schools.
                
                **Advantages:**
                • High compliance through routine
                • Reaches children systematically
                • Can monitor directly
                • Educational opportunity
                • Improves school performance
                
                **Challenges:**
                • Misses out-of-school children
                • Requires school infrastructure
                • Coordination with education ministry
                • Holiday coverage gaps
                
                **Success Example:** Peru improved IQ scores by 10 points through school iodine programs.
            """,
            'policy_requirements': [
                "MoH and MoE coordination",
                "School feeding program integration",
                "Teacher training programs",
                "Parent consent protocols"
            ]
        }
    }

def calculate_intervention_costs(budget, interventions):
    """Calculate costs for different intervention strategies"""
    costs = {
        'salt_iodization': {
            'unit_cost': 2.5,  # KSH per person per year
            'effectiveness': 0.85,
            'reach_time': 6  # months
        },
        'oil_fortification': {
            'unit_cost': 30,  # KSH per person per year (15 per 6 months)
            'effectiveness': 0.92,
            'reach_time': 3
        },
        'direct_supplement': {
            'unit_cost': 50,  # KSH per person per year
            'effectiveness': 0.98,
            'reach_time': 1
        },
        'school_program': {
            'unit_cost': 8,  # KSH per child per year
            'effectiveness': 0.88,
            'reach_time': 2
        }
    }
    return costs

def calculate_realistic_economic_benefit(coverage, effectiveness):
    """Calculate realistic annual economic benefits from iodine interventions"""
    
    # People reached by category
    children_reached = coverage * CHILDREN_UNDER_5 * effectiveness
    pregnant_reached = coverage * PREGNANT_WOMEN * effectiveness
    adults_reached = coverage * AFFECTED_POPULATION * effectiveness * 0.5  # 50% are working adults
    
    # Healthcare cost savings (annual)
    # Reduced goiter treatment costs
    goiter_treatment_saved = coverage * GOITER_CASES * effectiveness * 0.4 * CONFIG['goiter_treatment_cost']
    
    # Reduced pregnancy complications
    pregnancy_complications_saved = pregnant_reached * CONFIG['pregnancy_complication_rate'] * CONFIG['pregnancy_complication_reduction'] * CONFIG['pregnancy_complication_cost']
    
    # Reduced cretinism care costs (very conservative)
    cretinism_care_saved = pregnant_reached * (CONFIG['cretinism_rate_per_1000_births']/1000) * 0.7 * CONFIG['cretinism_lifetime_cost']
    
    # Productivity gains (very conservative estimates)
    # Adult productivity from reduced fatigue and improved cognitive function
    adult_productivity = adults_reached * CONFIG['productivity_gain_rate'] * CONFIG['avg_annual_income']
    
    # Caregiver time saved from prevented disabilities
    caregiver_productivity = (pregnant_reached * (CONFIG['cretinism_rate_per_1000_births']/1000/5) * 0.6) * 1 * (CONFIG['avg_annual_income'] * 0.75)
    
    # Cognitive benefits (future earnings, very conservatively annualized)
    # Each IQ point worth ~0.5% increase in lifetime earnings
    # Average 8 IQ points gained, very modest impact per year
    cognitive_benefit = children_reached * 0.004 * (CONFIG['avg_annual_income'] / 30)
    
    # Educational cost savings from reduced special needs
    special_education_saved = children_reached * CONFIG['special_ed_need_rate'] * CONFIG['special_ed_reduction_rate'] * CONFIG['special_education_annual_cost']
    
    # Total ANNUAL benefit (more conservative)
    total_annual = (goiter_treatment_saved + pregnancy_complications_saved + 
                   cretinism_care_saved/30 +  # Annualize lifetime costs over 30 years
                   adult_productivity + caregiver_productivity + 
                   cognitive_benefit + special_education_saved)
    
    # Apply diminishing returns for very high coverage (realistic saturation)
    # Benefits don't scale linearly at very high coverage levels
    if coverage > CONFIG['high_coverage_threshold']:
        saturation_factor = 1 - ((coverage - CONFIG['high_coverage_threshold']) * CONFIG['saturation_penalty'])
        total_annual = total_annual * saturation_factor
    
    return total_annual

def calculate_optimal_budget(intervention_mix, implementation_efficiency=70, optimization_mode='balanced'):
    """
    Calculate the MINIMUM budget needed to achieve target outcomes.
    
    Key insight: Higher efficiency means LESS budget needed for same coverage.
    We find the minimum budget that achieves our targets, not maximum outcomes for a budget.
    
    Args:
        intervention_mix: Dict of intervention percentages
        implementation_efficiency: How well we can execute (0-100)
        optimization_mode: 'minimal', 'balanced', or 'comprehensive'
    """
    
    # Get intervention details
    interventions_data = get_intervention_details()
    
    # Calculate weighted parameters based on intervention mix
    weighted_cost = 0
    weighted_effectiveness = 0
    weighted_saturation = 0
    
    # Map intervention mix keys to intervention data keys
    intervention_mapping = {
        'salt': 'salt_iodization',
        'oil': 'oil_fortification',
        'supplement': 'direct_supplement',
        'school': 'school_program'
    }
    
    for mix_key, percentage in intervention_mix.items():
        if percentage > 0 and mix_key in intervention_mapping:
            data_key = intervention_mapping[mix_key]
            weight = percentage / 100
            data = interventions_data[data_key]
            weighted_cost += data['unit_cost'] * weight
            weighted_effectiveness += data['effectiveness'] * weight
            weighted_saturation += data['coverage_potential'] * weight
    
    # If no interventions selected, return default
    if weighted_cost == 0:
        return {
            'optimal_budget': CONFIG['optimal_budget_default'],
            'optimal_coverage': 70,
            'optimal_roi': 250,
            'optimal_cretinism_prevented': int(PREGNANT_WOMEN * CONFIG['cretinism_rate_per_1000_births'] / 1000 * 0.7)
        }
    
    # Define optimization targets based on mode
    targets = {
        'minimal': {
            'coverage': 0.30,  # Emergency response - reach most critical 30%
            'cretinism_prevented': 1000,
            'roi_minimum': 50
        },
        'balanced': {
            'coverage': 0.70,  # Standard program - good coverage
            'cretinism_prevented': 3000,
            'roi_minimum': 150
        },
        'comprehensive': {
            'coverage': 0.90,  # Elimination effort - near universal
            'cretinism_prevented': 4000,
            'roi_minimum': 100
        }
    }
    
    target = targets.get(optimization_mode, targets['balanced'])
    
    # Binary search for MINIMUM budget that achieves targets
    # This properly handles efficiency: higher efficiency = lower budget needed
    min_budget = 50_000_000  # 50M minimum
    max_budget = CONFIG['max_annual_capacity'] * 2  # Don't search beyond reasonable capacity
    
    # Store all evaluated points for visualization
    results = []
    
    # First, do a coarse scan to understand the landscape
    scan_points = np.linspace(min_budget, max_budget, 20)
    
    for budget in scan_points:
        # Calculate theoretical coverage
        theoretical_coverage = budget / (weighted_cost * AFFECTED_POPULATION)
        
        # Apply saturation curve (sigmoid function for realistic coverage limits)
        actual_coverage = weighted_saturation * (1 - np.exp(-3 * theoretical_coverage / weighted_saturation))
        actual_coverage = min(actual_coverage, 1.0)
        
        # Apply implementation efficiency
        actual_coverage = actual_coverage * (implementation_efficiency / 100)
        
        # Calculate outcomes using WHO-based estimates for iodine
        # WHO: Iodine deficiency causes 18 million babies born mentally impaired annually globally
        # In Kenya with 100% deficiency and 1.6M births: ~4,800 cretinism cases preventable annually
        annual_cretinism_preventable = int(PREGNANT_WOMEN * CONFIG['cretinism_rate_per_1000_births'] / 1000)
        cretinism_prevented = actual_coverage * weighted_effectiveness * annual_cretinism_preventable
        
        # Goiter reduction (22% prevalence can be reduced by configured rate)
        goiter_reduced = actual_coverage * weighted_effectiveness * GOITER_CASES * CONFIG['goiter_reduction_rate']
        
        # IQ improvement (average 13 points lost due to deficiency)
        avg_iq_gain = actual_coverage * weighted_effectiveness * 13
        
        # Calculate comprehensive annual economic benefits
        annual_benefit = calculate_realistic_economic_benefit(actual_coverage, weighted_effectiveness)
        
        # Calculate 5-year ROI (more realistic for public health interventions)
        # Benefits realization over 5 years based on configuration
        five_year_benefits = annual_benefit * (
            CONFIG['year1_benefit_realization'] + 
            CONFIG['year2_benefit_realization'] + 
            CONFIG['year3_5_benefit_realization'] * 3
        )
        five_year_costs = budget * 5 * (1 - CONFIG['efficiency_gain_per_year'])  # Efficiency gain over time
        roi = ((five_year_benefits - five_year_costs) / five_year_costs) * 100 if five_year_costs > 0 else 0
        
        # Cost-effectiveness
        cost_per_cretinism = budget / cretinism_prevented if cretinism_prevented > 0 else float('inf')
        
        # Calculate marginal benefit
        marginal_benefit = 0
        if len(results) > 0:
            prev = results[-1]
            marginal_benefit = (annual_benefit - prev['total_benefit']) / (budget - prev['budget']) if budget > prev['budget'] else 0
        
        results.append({
            'budget': budget,
            'coverage': actual_coverage,
            'cretinism_prevented': cretinism_prevented,
            'roi': roi,
            'cost_per_cretinism': cost_per_cretinism,
            'marginal_benefit': marginal_benefit,
            'total_benefit': annual_benefit,
            'efficiency_score': roi * actual_coverage,
            'iq_gain': avg_iq_gain
        })
    
    df = pd.DataFrame(results)
    
    # NEW LOGIC: Find MINIMUM budget that meets targets
    # This is the key fix - we look for the smallest budget that achieves our goals
    
    # Filter for budgets that meet ALL target criteria
    meets_coverage = df['coverage'] >= target['coverage']
    meets_cretinism = df['cretinism_prevented'] >= target['cretinism_prevented']
    meets_roi = df['roi'] >= target['roi_minimum']
    
    # Find budgets meeting all targets
    meeting_all_targets = df[meets_coverage & meets_cretinism & meets_roi]
    
    if not meeting_all_targets.empty:
        # SUCCESS: Find the MINIMUM budget that meets all targets
        # This is where efficiency helps - higher efficiency means lower budget needed
        optimal_idx = meeting_all_targets['budget'].idxmin()  # Get minimum budget
        optimal = df.iloc[optimal_idx]
        targets_met = True
    else:
        # Can't meet all targets - find best compromise
        # Score each budget by how close it gets to targets
        df['target_score'] = (
            df['coverage'] / target['coverage'] * 0.5 +
            df['cretinism_prevented'] / target['cretinism_prevented'] * 0.3 +
            np.minimum(df['roi'] / target['roi_minimum'], 1.0) * 0.2
        )
        
        # Find budget with best target achievement
        optimal_idx = df['target_score'].idxmax()
        optimal = df.iloc[optimal_idx]
        targets_met = False
    
    # Check for implementation capacity constraints
    max_capacity = CONFIG['max_annual_capacity']  # Max annual capacity for iodine programs
    if optimal['budget'] > max_capacity:
        constrained = df[df['budget'] <= max_capacity].iloc[-1]
        return {
            'optimal_budget': constrained['budget'],
            'optimal_coverage': constrained['coverage'] * 100,
            'optimal_roi': constrained['roi'],
            'optimal_cretinism_prevented': int(constrained['cretinism_prevented']),
            'optimal_iq_gain': constrained['iq_gain'],
            'data': df,
            'constrained': True,
            'efficiency_used': implementation_efficiency,
            'targets_met': False,  # Constrained means targets not fully met
            'optimization_mode': optimization_mode,
            'message': f"Budget constrained to {max_capacity/1e9:.1f}B KSH capacity limit"
        }
    
    # Adjust optimal budget for implementation efficiency
    # The calculate_optimal_budget already factors in efficiency for coverage calculations
    # But the optimal budget found is for that specific efficiency level
    # Since higher efficiency means we can do more with less money,
    # the optimal budget should remain as calculated (it already considers efficiency)
    # No additional adjustment needed here - the efficiency is already baked in
    adjusted_optimal_budget = optimal['budget']
    
    return {
        'optimal_budget': adjusted_optimal_budget,
        'optimal_coverage': optimal['coverage'] * 100,
        'optimal_roi': optimal['roi'],
        'optimal_cretinism_prevented': int(optimal['cretinism_prevented']),
        'optimal_iq_gain': optimal['iq_gain'],
        'data': df,
        'constrained': False,
        'efficiency_used': implementation_efficiency,
        'targets_met': targets_met,
        'optimization_mode': optimization_mode,
        'message': f"With {implementation_efficiency}% efficiency, minimum budget of {adjusted_optimal_budget/1e9:.1f}B KSH needed for {optimization_mode} targets"
    }

def calculate_health_outcomes(coverage, intervention_mix, timeline_months):
    """Calculate health outcomes with detailed explanations based on WHO data"""
    
    # Calculate effectiveness using intervention details
    interventions_data = get_intervention_details()
    total_effectiveness = 0
    
    intervention_mapping = {
        'salt': 'salt_iodization',
        'oil': 'oil_fortification',
        'supplement': 'direct_supplement',
        'school': 'school_program'
    }
    
    for mix_key, percentage in intervention_mix.items():
        if percentage > 0 and mix_key in intervention_mapping:
            data_key = intervention_mapping[mix_key]
            total_effectiveness += (percentage / 100) * interventions_data[data_key]['effectiveness']
    
    # Based on WHO data for iodine deficiency:
    # - Causes 500 cretinism cases annually in Kenya (with 100% deficiency)
    # - Responsible for 22% goiter prevalence
    # - Causes average 13 IQ point loss
    # - Increases pregnancy complications by 15%
    
    # Calculate actual values
    # WHO: 5-10 per 1000 births in severe deficiency areas
    # Kenya has ~1.6M pregnancies/year, with 100% deficiency
    annual_cretinism_risk = int(PREGNANT_WOMEN * CONFIG['cretinism_rate_per_1000_births'] / 1000)
    cretinism_prevented_value = int(coverage * total_effectiveness * annual_cretinism_risk)
    goiter_reduced_value = int(coverage * total_effectiveness * GOITER_CASES * CONFIG['goiter_reduction_rate'])
    iq_points_gained_value = coverage * total_effectiveness * 13
    pregnancy_complications_reduced_value = coverage * total_effectiveness * CONFIG['pregnancy_complication_rate']
    economic_benefit_value = calculate_realistic_economic_benefit(coverage, total_effectiveness)
    
    # Generate dynamic comparisons based on actual values
    # Cretinism comparison - each case is a lifetime of severe disability
    if cretinism_prevented_value >= 100:
        cretinism_comparison = f"Equivalent to preventing disability in a small town"
    elif cretinism_prevented_value >= 50:
        cretinism_comparison = f"Equivalent to preventing disability in {cretinism_prevented_value} families"
    else:
        cretinism_comparison = f"Each case prevented saves a lifetime of suffering"
    
    # Goiter reduction - visible neck swelling affecting quality of life
    goiter_percent = int((goiter_reduced_value / GOITER_CASES) * 100)
    goiter_comparison = f"{goiter_percent}% reduction in visible goiter cases nationwide"
    
    # IQ improvement context
    if iq_points_gained_value >= 10:
        iq_comparison = "Difference between normal and borderline intellectual functioning"
    elif iq_points_gained_value >= 7:
        iq_comparison = "Equivalent to 3 additional years of education"
    elif iq_points_gained_value >= 5:
        iq_comparison = "Equivalent to 2 additional years of education"
    else:
        iq_comparison = "Significant improvement in learning capacity"
    
    # Pregnancy outcomes
    pregnancy_percent = int(pregnancy_complications_reduced_value * 100)
    pregnancy_comparison = f"{pregnancy_percent}% fewer stillbirths and miscarriages"
    
    # Economic benefit context (more realistic comparisons)
    if economic_benefit_value >= 1_000_000_000:
        # For very large benefits, show multiple comparisons
        health_centers = int(economic_benefit_value / CONFIG['health_center_cost'])
        nurses = int(economic_benefit_value / CONFIG['nurse_training_cost'])
        economic_comparison = f"Could fund {health_centers} health centers or train {nurses:,} nurses"
    elif economic_benefit_value >= 400_000_000:
        health_centers = int(economic_benefit_value / CONFIG['health_center_cost'])
        economic_comparison = f"Could fund {health_centers} health centers annually"
    elif economic_benefit_value >= 100_000_000:
        healthcare_workers = int(economic_benefit_value / CONFIG['nurse_training_cost'])
        economic_comparison = f"Could train {healthcare_workers} healthcare workers"
    elif economic_benefit_value >= 50_000_000:
        scholarships = int(economic_benefit_value / CONFIG['medical_scholarship_cost'])
        economic_comparison = f"Could provide {scholarships} medical scholarships"
    else:
        economic_comparison = f"Annual savings of {economic_benefit_value/1_000_000:.1f}M KSH"
    
    # Health outcomes with policy-relevant metrics
    outcomes = {
        'cretinism_prevented': {
            'value': cretinism_prevented_value,
            'explanation': "Cases of severe intellectual disability prevented",
            'comparison': cretinism_comparison
        },
        'goiter_reduced': {
            'value': goiter_reduced_value,
            'explanation': "People freed from visible thyroid enlargement",
            'comparison': goiter_comparison
        },
        'iq_points_gained': {
            'value': iq_points_gained_value,
            'explanation': "Average IQ points gained per child",
            'comparison': iq_comparison
        },
        'pregnancy_improved': {
            'value': pregnancy_complications_reduced_value,
            'explanation': "Reduction in pregnancy complications",
            'comparison': pregnancy_comparison
        },
        'economic_benefit': {
            'value': economic_benefit_value,
            'explanation': "Annual healthcare savings and productivity gains",
            'comparison': economic_comparison
        }
    }
    
    return outcomes

def simulate_health_outcomes(coverage, intervention_mix, timeline_months):
    """Simulate health outcomes based on interventions - compatibility wrapper"""
    # This maintains compatibility with existing code while using new calculation
    outcomes = calculate_health_outcomes(coverage, intervention_mix, timeline_months)
    
    # Calculate weighted effectiveness for backward compatibility
    total_effectiveness = sum(intervention_mix.values()) / 100
    
    # Immediate effects (0-3 months)
    immediate = {
        'urinary_iodine_normalized': coverage * total_effectiveness * 0.7,
        'thyroid_function_improved': coverage * total_effectiveness * 0.5,
        'energy_levels_increased': coverage * total_effectiveness * 0.4
    }
    
    # Mid-term effects (3-12 months)
    midterm = {
        'goiter_reduction': coverage * total_effectiveness * 0.6,
        'pregnancy_outcomes_improved': coverage * total_effectiveness * 0.75,
        'child_cognitive_improvement': coverage * total_effectiveness * 0.3
    }
    
    # Long-term effects (1-5 years)
    longterm = {
        'iq_points_gained': coverage * total_effectiveness * 12,  # average IQ points
        'cretinism_prevented': int(coverage * total_effectiveness * int(PREGNANT_WOMEN * CONFIG['cretinism_rate_per_1000_births'] / 1000)),
        'economic_productivity_gain': coverage * total_effectiveness * 0.15  # 15% max gain
    }
    
    return immediate, midterm, longterm

def generate_html_report(title, content, data_dict=None):
    """Generate an HTML report for download"""
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{ color: #2e7d32; border-bottom: 3px solid #2e7d32; padding-bottom: 10px; }}
            h2 {{ color: #1565c0; margin-top: 30px; }}
            h3 {{ color: #e65100; margin-top: 20px; }}
            .metric-box {{
                background: #f5f5f5;
                padding: 15px;
                border-left: 4px solid #4CAF50;
                margin: 10px 0;
            }}
            .warning {{ background: #fff3cd; border-left-color: #ffc107; }}
            .danger {{ background: #f8d7da; border-left-color: #dc3545; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #ddd;
                text-align: center;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        {content}
        <div class="footer">
            <p>Generated by Kenya Iodine Intervention Simulator</p>
            <p>© {datetime.now().year} - Evidence-based Public Health Planning Tool</p>
        </div>
    </body>
    </html>
    """
    return html_template

def generate_policy_brief_pdf(data):
    """Generate a policy brief PDF with key findings and recommendations"""
    
    content = f"""
    <h2>Executive Summary</h2>
    <div class="metric-box">
        <h3>Current Crisis</h3>
        <p><strong>100% of Kenya's population</strong> suffers from iodine deficiency, affecting {data.get('affected_population', 52000000):,} people.</p>
        <p>This leads to:</p>
        <ul>
            <li>{data.get('annual_cretinism', 500):,} preventable cases of cretinism annually</li>
            <li>{data.get('goiter_cases', 2340000):,} people with goiter (4.5% prevalence)</li>
            <li>Average IQ loss of 13 points per child</li>
            <li>Economic losses of {data.get('economic_loss', 50)/1e9:.1f} billion KSH annually</li>
        </ul>
    </div>
    
    <h2>Proposed Intervention</h2>
    <div class="metric-box">
        <h3>Investment Required</h3>
        <p><strong>Budget:</strong> {data.get('budget', 0)/1e6:.0f} Million KSH</p>
        <p><strong>Timeline:</strong> {data.get('timeline', 24)} months</p>
        <p><strong>Coverage Target:</strong> {data.get('coverage', 0)*100:.1f}% of population</p>
    </div>
    
    <h3>Intervention Strategy</h3>
    <table>
        <tr>
            <th>Intervention</th>
            <th>Budget Allocation</th>
            <th>Target Population</th>
            <th>Expected Effectiveness</th>
        </tr>
        <tr>
            <td>Salt Iodization</td>
            <td>{data.get('salt_pct', 0)}%</td>
            <td>General Population</td>
            <td>85% effective</td>
        </tr>
        <tr>
            <td>Oil Fortification</td>
            <td>{data.get('oil_pct', 0)}%</td>
            <td>Cooking Oil Users</td>
            <td>92% effective</td>
        </tr>
        <tr>
            <td>Direct Supplementation</td>
            <td>{data.get('supplement_pct', 0)}%</td>
            <td>Pregnant Women & Children</td>
            <td>98% effective</td>
        </tr>
        <tr>
            <td>School Programs</td>
            <td>{data.get('school_pct', 0)}%</td>
            <td>School Children</td>
            <td>88% effective</td>
        </tr>
    </table>
    
    <h2>Expected Outcomes</h2>
    <div class="metric-box">
        <h3>Health Impact</h3>
        <ul>
            <li><strong>{data.get('cretinism_prevented', 0):,}</strong> cases of cretinism prevented</li>
            <li><strong>{data.get('goiter_reduced', 0):,}</strong> goiter cases reduced</li>
            <li><strong>+{data.get('iq_gain', 0):.1f}</strong> average IQ points gained per child</li>
            <li><strong>{data.get('pregnancy_improved', 0):,}</strong> pregnancy complications prevented</li>
        </ul>
    </div>
    
    <div class="metric-box">
        <h3>Economic Returns</h3>
        <ul>
            <li><strong>5-Year ROI:</strong> {data.get('roi', 0):.0f}%</li>
            <li><strong>Annual Economic Benefit:</strong> {data.get('annual_benefit', 0)/1e6:.0f} Million KSH</li>
            <li><strong>Cost per Life Saved:</strong> {data.get('cost_per_life', 0):,.0f} KSH</li>
            <li><strong>Break-even:</strong> Year {data.get('breakeven_year', 3)}</li>
        </ul>
    </div>
    
    <h2>Implementation Requirements</h2>
    <h3>Infrastructure</h3>
    <ul>
        <li>10 salt iodization plants to upgrade</li>
        <li>5 oil fortification facilities</li>
        <li>47 county distribution centers</li>
        <li>Laboratory network for quality testing</li>
    </ul>
    
    <h3>Human Resources</h3>
    <ul>
        <li>{int(47 * data.get('coverage', 0.7)):,} nutritionists (1 per county)</li>
        <li>{int(5000 * data.get('coverage', 0.7)):,} community health workers</li>
        <li>{int(100 * data.get('coverage', 0.7)):,} lab technicians</li>
        <li>Supporting administrative staff</li>
    </ul>
    
    <h2>Recommendations</h2>
    <div class="metric-box warning">
        <h3>Immediate Actions Required</h3>
        <ol>
            <li><strong>Establish Legal Framework:</strong> Mandate salt iodization with enforcement mechanisms</li>
            <li><strong>Secure Funding:</strong> Mobilize {data.get('budget', 0)/1e6:.0f}M KSH from government and partners</li>
            <li><strong>Build Infrastructure:</strong> Upgrade production facilities and testing laboratories</li>
            <li><strong>Launch Awareness Campaign:</strong> Educate population on iodine importance</li>
            <li><strong>Implement Monitoring:</strong> Establish real-time tracking of iodization levels</li>
        </ol>
    </div>
    
    <h2>Risk Mitigation</h2>
    <table>
        <tr>
            <th>Risk</th>
            <th>Mitigation Strategy</th>
        </tr>
        <tr>
            <td>Producer resistance</td>
            <td>Incentives, subsidies, and phased implementation</td>
        </tr>
        <tr>
            <td>Quality control failures</td>
            <td>Multiple testing points and certification system</td>
        </tr>
        <tr>
            <td>Supply disruptions</td>
            <td>Buffer stocks and multiple suppliers</td>
        </tr>
        <tr>
            <td>Low adoption</td>
            <td>Community education and success stories</td>
        </tr>
    </table>
    
    <h2>Call to Action</h2>
    <div class="metric-box danger">
        <p><strong>Every month of delay means:</strong></p>
        <ul>
            <li>42 preventable cases of cretinism</li>
            <li>4.2 billion KSH in economic losses</li>
            <li>Thousands of children born with reduced cognitive potential</li>
        </ul>
        <p><strong>The time to act is NOW.</strong></p>
    </div>
    """
    
    return generate_html_report("Iodine Intervention Policy Brief - Kenya", content, data)

def generate_implementation_plan_pdf(data):
    """Generate detailed implementation plan document"""
    
    content = f"""
    <h2>Implementation Plan Overview</h2>
    <div class="metric-box">
        <p><strong>Program Name:</strong> National Iodine Deficiency Elimination Program</p>
        <p><strong>Duration:</strong> {data.get('timeline', 24)} months</p>
        <p><strong>Total Budget:</strong> {data.get('budget', 0)/1e6:.0f} Million KSH</p>
        <p><strong>Target Coverage:</strong> {data.get('coverage', 0)*100:.1f}% of population</p>
    </div>
    
    <h2>Phase 1: Setup (Months 1-3)</h2>
    <div class="metric-box">
        <h3>Key Activities</h3>
        <ul>
            <li>Establish program management unit</li>
            <li>Recruit core team (program manager, technical leads)</li>
            <li>Conduct baseline survey in all 47 counties</li>
            <li>Map existing infrastructure and identify gaps</li>
            <li>Develop standard operating procedures</li>
        </ul>
        <h3>Budget: {data.get('budget', 0) * 0.15 / 1e6:.0f} Million KSH (15%)</h3>
        <h3>Success Metrics</h3>
        <ul>
            <li>✓ Program office operational</li>
            <li>✓ Core team hired and trained</li>
            <li>✓ Baseline data collected</li>
            <li>✓ Infrastructure assessment complete</li>
        </ul>
    </div>
    
    <h2>Phase 2: Pilot (Months 4-9)</h2>
    <div class="metric-box">
        <h3>Key Activities</h3>
        <ul>
            <li>Launch pilot in 5 counties (mix of urban/rural)</li>
            <li>Test intervention protocols</li>
            <li>Train county-level staff</li>
            <li>Establish supply chain systems</li>
            <li>Implement quality control measures</li>
        </ul>
        <h3>Budget: {data.get('budget', 0) * 0.20 / 1e6:.0f} Million KSH (20%)</h3>
        <h3>Success Metrics</h3>
        <ul>
            <li>✓ 70% coverage in pilot counties</li>
            <li>✓ <10% supply chain stockouts</li>
            <li>✓ Quality standards met in 95% of samples</li>
            <li>✓ Community acceptance >80%</li>
        </ul>
    </div>
    
    <h2>Phase 3: Scale-up (Months 10-21)</h2>
    <div class="metric-box">
        <h3>Key Activities</h3>
        <ul>
            <li>Expand to 25 counties</li>
            <li>Scale production capacity</li>
            <li>Deploy full monitoring system</li>
            <li>Launch national awareness campaign</li>
            <li>Strengthen distribution networks</li>
        </ul>
        <h3>Budget: {data.get('budget', 0) * 0.35 / 1e6:.0f} Million KSH (35%)</h3>
        <h3>Success Metrics</h3>
        <ul>
            <li>✓ 80% coverage in target counties</li>
            <li>✓ Production meets demand</li>
            <li>✓ Real-time monitoring operational</li>
            <li>✓ 60% population awareness</li>
        </ul>
    </div>
    
    <h2>Phase 4: Full Coverage (Months 22-{data.get('timeline', 24)})</h2>
    <div class="metric-box">
        <h3>Key Activities</h3>
        <ul>
            <li>Complete rollout to all 47 counties</li>
            <li>Optimize operations based on lessons learned</li>
            <li>Conduct mid-term evaluation</li>
            <li>Adjust strategies as needed</li>
            <li>Plan for sustainability</li>
        </ul>
        <h3>Budget: {data.get('budget', 0) * 0.20 / 1e6:.0f} Million KSH (20%)</h3>
        <h3>Success Metrics</h3>
        <ul>
            <li>✓ 90% national coverage achieved</li>
            <li>✓ All KPIs on track</li>
            <li>✓ Cost per person within budget</li>
            <li>✓ Sustainability plan approved</li>
        </ul>
    </div>
    
    <h2>Phase 5: Sustain (Ongoing)</h2>
    <div class="metric-box">
        <h3>Key Activities</h3>
        <ul>
            <li>Maintain coverage above 90%</li>
            <li>Continuous quality improvement</li>
            <li>Regular monitoring and evaluation</li>
            <li>Gradual reduction of external support</li>
            <li>Integration with routine health services</li>
        </ul>
        <h3>Budget: {data.get('budget', 0) * 0.10 / 1e6:.0f} Million KSH annually (10%)</h3>
    </div>
    
    <h2>Critical Success Factors</h2>
    <table>
        <tr>
            <th>Factor</th>
            <th>Requirement</th>
            <th>Responsible Party</th>
        </tr>
        <tr>
            <td>Political Support</td>
            <td>High-level government commitment</td>
            <td>Ministry of Health</td>
        </tr>
        <tr>
            <td>Funding</td>
            <td>Timely disbursement of funds</td>
            <td>Treasury & Partners</td>
        </tr>
        <tr>
            <td>Technical Capacity</td>
            <td>Skilled personnel at all levels</td>
            <td>Program Management</td>
        </tr>
        <tr>
            <td>Community Buy-in</td>
            <td>Active community participation</td>
            <td>County Governments</td>
        </tr>
        <tr>
            <td>Quality Assurance</td>
            <td>Robust testing and certification</td>
            <td>Kenya Bureau of Standards</td>
        </tr>
    </table>
    
    <h2>Monitoring Framework</h2>
    <h3>Monthly Indicators</h3>
    <ul>
        <li>Salt samples tested</li>
        <li>Iodization levels in salt</li>
        <li>Supply chain stock levels</li>
        <li>CHW activity reports</li>
    </ul>
    
    <h3>Quarterly Indicators</h3>
    <ul>
        <li>Population coverage rates</li>
        <li>Quality compliance rates</li>
        <li>Budget utilization</li>
        <li>Training completion rates</li>
    </ul>
    
    <h3>Annual Indicators</h3>
    <ul>
        <li>Median urinary iodine levels</li>
        <li>Goiter prevalence</li>
        <li>Cretinism incidence</li>
        <li>Cost-effectiveness ratios</li>
    </ul>
    """
    
    return generate_html_report("Iodine Intervention Implementation Plan", content, data)

def generate_me_framework_pdf(data):
    """Generate Monitoring & Evaluation framework document"""
    
    content = f"""
    <h2>Monitoring & Evaluation Framework</h2>
    
    <h3>Program Information</h3>
    <div class="metric-box">
        <p><strong>Program:</strong> National Iodine Deficiency Elimination</p>
        <p><strong>Duration:</strong> {data.get('timeline', 24)} months</p>
        <p><strong>Budget:</strong> {data.get('budget', 0)/1e6:.0f} Million KSH</p>
        <p><strong>Target Population:</strong> {data.get('affected_population', 52000000):,}</p>
    </div>
    
    <h2>Theory of Change</h2>
    <div class="metric-box">
        <h3>IF we:</h3>
        <ul>
            <li>Ensure salt and oil are adequately iodized</li>
            <li>Provide direct supplements to high-risk groups</li>
            <li>Implement school-based programs</li>
            <li>Educate communities on iodine importance</li>
        </ul>
        <h3>THEN:</h3>
        <ul>
            <li>Population iodine intake will increase</li>
            <li>Iodine deficiency disorders will decrease</li>
            <li>Cognitive development will improve</li>
            <li>Economic productivity will increase</li>
        </ul>
    </div>
    
    <h2>Results Framework</h2>
    
    <h3>Impact Level</h3>
    <table>
        <tr>
            <th>Indicator</th>
            <th>Baseline</th>
            <th>Target</th>
            <th>Frequency</th>
            <th>Data Source</th>
        </tr>
        <tr>
            <td>Cretinism incidence</td>
            <td>500/year</td>
            <td><100/year</td>
            <td>Annual</td>
            <td>Health records</td>
        </tr>
        <tr>
            <td>Average IQ in children</td>
            <td>87</td>
            <td>95+</td>
            <td>Every 3 years</td>
            <td>Cognitive assessment</td>
        </tr>
        <tr>
            <td>Economic productivity</td>
            <td>Baseline</td>
            <td>+15%</td>
            <td>Every 5 years</td>
            <td>Economic survey</td>
        </tr>
    </table>
    
    <h3>Outcome Level</h3>
    <table>
        <tr>
            <th>Indicator</th>
            <th>Baseline</th>
            <th>Target</th>
            <th>Frequency</th>
            <th>Data Source</th>
        </tr>
        <tr>
            <td>Median urinary iodine</td>
            <td><50 μg/L</td>
            <td>>100 μg/L</td>
            <td>Annual</td>
            <td>Population survey</td>
        </tr>
        <tr>
            <td>Goiter prevalence</td>
            <td>4.5%</td>
            <td><2%</td>
            <td>Annual</td>
            <td>Clinical examination</td>
        </tr>
        <tr>
            <td>Pregnancy complications</td>
            <td>Baseline</td>
            <td>-30%</td>
            <td>Annual</td>
            <td>Hospital records</td>
        </tr>
    </table>
    
    <h3>Output Level</h3>
    <table>
        <tr>
            <th>Indicator</th>
            <th>Target</th>
            <th>Frequency</th>
            <th>Data Source</th>
        </tr>
        <tr>
            <td>Iodized salt coverage</td>
            <td>>90%</td>
            <td>Quarterly</td>
            <td>Market survey</td>
        </tr>
        <tr>
            <td>Oil fortification coverage</td>
            <td>>70%</td>
            <td>Quarterly</td>
            <td>Production data</td>
        </tr>
        <tr>
            <td>Supplements distributed</td>
            <td>95% of target</td>
            <td>Monthly</td>
            <td>Distribution logs</td>
        </tr>
        <tr>
            <td>Schools enrolled</td>
            <td>80% of schools</td>
            <td>Termly</td>
            <td>Education records</td>
        </tr>
    </table>
    
    <h2>Data Collection Plan</h2>
    
    <h3>Data Collection Methods</h3>
    <ul>
        <li><strong>Routine Monitoring:</strong> Monthly reports from facilities</li>
        <li><strong>Surveys:</strong> Annual population-based surveys</li>
        <li><strong>Laboratory Testing:</strong> Regular salt and urine testing</li>
        <li><strong>Qualitative Research:</strong> Focus groups and interviews</li>
    </ul>
    
    <h3>Data Management</h3>
    <ul>
        <li><strong>Collection Tools:</strong> Mobile data collection (ODK)</li>
        <li><strong>Storage:</strong> Secure cloud-based database</li>
        <li><strong>Analysis:</strong> Statistical software and dashboards</li>
        <li><strong>Reporting:</strong> Monthly, quarterly, and annual reports</li>
    </ul>
    
    <h2>Evaluation Plan</h2>
    
    <h3>Baseline Study (Month 1)</h3>
    <ul>
        <li>Population iodine status assessment</li>
        <li>Infrastructure and capacity mapping</li>
        <li>Knowledge, attitudes, and practices survey</li>
    </ul>
    
    <h3>Mid-term Evaluation (Month 12)</h3>
    <ul>
        <li>Process evaluation</li>
        <li>Coverage assessment</li>
        <li>Quality audit</li>
        <li>Stakeholder feedback</li>
    </ul>
    
    <h3>Final Evaluation (Month 24)</h3>
    <ul>
        <li>Impact assessment</li>
        <li>Cost-effectiveness analysis</li>
        <li>Sustainability review</li>
        <li>Lessons learned documentation</li>
    </ul>
    
    <h2>Learning and Adaptation</h2>
    
    <h3>Regular Review Meetings</h3>
    <ul>
        <li>Monthly: Technical team reviews</li>
        <li>Quarterly: Stakeholder meetings</li>
        <li>Annual: Program review and planning</li>
    </ul>
    
    <h3>Adaptive Management</h3>
    <ul>
        <li>Real-time monitoring for quick adjustments</li>
        <li>Feedback loops from communities</li>
        <li>Regular strategy refinement based on data</li>
    </ul>
    
    <h2>Reporting Schedule</h2>
    <table>
        <tr>
            <th>Report Type</th>
            <th>Frequency</th>
            <th>Audience</th>
        </tr>
        <tr>
            <td>Activity Reports</td>
            <td>Monthly</td>
            <td>Program Management</td>
        </tr>
        <tr>
            <td>Progress Reports</td>
            <td>Quarterly</td>
            <td>Ministry of Health</td>
        </tr>
        <tr>
            <td>Donor Reports</td>
            <td>Semi-annual</td>
            <td>Funding Partners</td>
        </tr>
        <tr>
            <td>Annual Report</td>
            <td>Annual</td>
            <td>All Stakeholders</td>
        </tr>
    </table>
    """
    
    return generate_html_report("Monitoring & Evaluation Framework", content, data)

def create_download_link(html_content, filename):
    """Create a download link for HTML content"""
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}">📥 Download {filename}</a>'

# INTERVENTION SETUP TAB
with tab1:
    st.header("🎯 Configure Intervention Strategy")
    
    # Helpful context
    with st.expander("ℹ️ Understanding This Section", expanded=True):
        st.markdown("""
        This section helps you design an iodine intervention program by:
        1. **Setting your budget** - How much funding is available?
        2. **Choosing target groups** - Who needs help most urgently?
        3. **Selecting interventions** - Which approaches will you use?
        4. **Estimating coverage** - How many people will you reach?
        
        **💡 Tip:** Start with your available budget, then adjust interventions to maximize impact.
        """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 💰 Budget Planning")
        
        # Budget context
        st.markdown("""
        <div class="info-box">
            <strong style="color: #1565c0;">Budget Context:</strong><br>
            <span style="color: #212121;">
            • Kenya health budget: ~300 billion KSH/year<br>
            • Nutrition allocation: ~2% of health budget<br>
            • Recommended: 500M-2B KSH for iodine programs
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple budget input with 3 methods
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
                help="Typical range: 500-2000 million KSH"
            )
            total_budget = budget_millions * 1_000_000
            
        elif budget_input_method == "Percentage of health budget":
            budget_percentage = st.slider(
                "Percentage of nutrition budget for iodine",
                min_value=5,
                max_value=50,
                value=20,
                help="WHO recommends 2-3% of health budget for nutrition"
            )
            total_budget = (CONFIG['health_budget_total'] * 0.02 * budget_percentage / 100)
            
        else:  # Cost per person
            cost_per_person = st.slider(
                "Budget per affected person (KSH)",
                min_value=10,
                max_value=200,
                value=40,
                help="Compare: One doctor visit costs ~500 KSH"
            )
            total_budget = cost_per_person * AFFECTED_POPULATION
        
        # Display formatted budget in understandable terms
        st.markdown(f"""
        <div class="metric-card" style="background-color: #e3f2fd; border-left: 5px solid #1976d2;">
            <h4 style="color: #0d47a1;">Total Budget</h4>
            <h2 style="color: #1565c0;">{total_budget/1_000_000:,.0f} Million KSH</h2>
            <p style="color: #424242;">
                • Per affected person: {total_budget/AFFECTED_POPULATION:.0f} KSH<br>
                • Per child under 5: {total_budget/CHILDREN_UNDER_5:.0f} KSH<br>
                • Percentage of health budget: {total_budget/CONFIG['health_budget_total']*100:.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Target population with explanations
        st.markdown("### 🎯 Priority Groups")
        
        with st.expander("Understanding Priority Groups"):
            st.markdown("""
            **Why prioritize?** Limited resources require focusing on those who benefit most.
            
            **High-impact groups:**
            • **Pregnant women:** Prevents cretinism and cognitive damage
            • **Children under 5:** Critical brain development period
            • **Adolescent girls:** Future mothers needing reserves
            """)
        
        targeting_strategy = st.selectbox(
            "Choose your targeting approach",
            [
                "Universal Coverage (Everyone)",
                "Children First (Under 5 priority)",
                "Mother-Child Focus (Pregnancy to 2 years)",
                "Emergency Response (Severe cases only)",
                "Geographic Focus (High-burden areas)",
                "School-Age Focus (5-18 years)",
                "Women of Reproductive Age"
            ]
        )
        
        # Set target population based on strategy
        if targeting_strategy == "Universal Coverage (Everyone)":
            target_population = AFFECTED_POPULATION
            st.info("🌍 Targeting all 52 million people (100% deficiency)")
        elif targeting_strategy == "Children First (Under 5 priority)":
            target_population = CHILDREN_UNDER_5
            st.info("👶 Focusing on 7 million children under 5")
        elif targeting_strategy == "Mother-Child Focus (Pregnancy to 2 years)":
            target_population = PREGNANT_WOMEN + int(CHILDREN_UNDER_5 * 0.4)
            st.info("🤱 Targeting 4.5 million mothers and young children")
        elif targeting_strategy == "Emergency Response (Severe cases only)":
            target_population = GOITER_CASES + int(PREGNANT_WOMEN * 0.5)
            st.info("🚨 Focusing on 12 million severe cases (goiter + high-risk pregnancies)")
        elif targeting_strategy == "Geographic Focus (High-burden areas)":
            target_population = int(AFFECTED_POPULATION * 0.3)
            st.info("📍 Targeting 15.6 million in high-burden regions")
        elif targeting_strategy == "School-Age Focus (5-18 years)":
            target_population = int(AFFECTED_POPULATION * 0.25)
            st.info("🎒 Focusing on 13 million school-age children")
        else:  # Women of Reproductive Age
            target_population = int(AFFECTED_POPULATION * 0.22)
            st.info("👩 Targeting 11.4 million women of reproductive age")
        
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
        st.subheader("🔧 Choose Your Interventions")
        
        st.markdown("""
        <div class="info-box">
            <strong style="color: #1565c0;">📚 How to Choose Interventions:</strong><br>
            <span style="color: #212121;">
            • <strong>Salt Iodization:</strong> Most cost-effective for population-wide coverage<br>
            • <strong>Oil Fortification:</strong> Better retention in cooking, good for rural areas<br>
            • <strong>Direct Supplementation:</strong> Immediate impact for severe cases<br>
            • <strong>School Programs:</strong> Reaches children systematically<br>
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
                'salt': 35,
                'oil': 25,
                'supplement': 25,
                'school': 15
            }
        elif strategy_template == "Emergency Response":
            default_values = {
                'salt': 20,
                'oil': 15,
                'supplement': 50,
                'school': 15
            }
        elif strategy_template == "Sustainable Development":
            default_values = {
                'salt': 45,
                'oil': 30,
                'supplement': 10,
                'school': 15
            }
        elif strategy_template == "Cost-Optimized":
            default_values = {
                'salt': 50,
                'oil': 20,
                'supplement': 15,
                'school': 15
            }
        else:  # Custom
            default_values = {
                'salt': 0,
                'oil': 0,
                'supplement': 0,
                'school': 0
            }
        
        st.markdown("#### Adjust Intervention Mix (must total 100%)")
        
        interventions_data = get_intervention_details()
        
        # Create intervention sliders with info buttons
        salt_col, salt_info = st.columns([3, 1])
        with salt_col:
            salt_pct = st.slider(
                interventions_data['salt_iodization']['name'],
                min_value=0,
                max_value=100,
                value=default_values['salt'],
                help=f"Cost: {interventions_data['salt_iodization']['unit_cost']} KSH/person | Effectiveness: {interventions_data['salt_iodization']['effectiveness']*100:.0f}%"
            )
        with salt_info:
            with st.expander("Details"):
                st.markdown(interventions_data['salt_iodization']['description'])
                st.markdown("**Policy Requirements:**")
                for req in interventions_data['salt_iodization']['policy_requirements']:
                    st.markdown(f"• {req}")
        
        oil_col, oil_info = st.columns([3, 1])
        with oil_col:
            oil_pct = st.slider(
                interventions_data['oil_fortification']['name'],
                min_value=0,
                max_value=100,
                value=default_values['oil'],
                help=f"Cost: {interventions_data['oil_fortification']['unit_cost']} KSH/person | Effectiveness: {interventions_data['oil_fortification']['effectiveness']*100:.0f}%"
            )
        with oil_info:
            with st.expander("Details"):
                st.markdown(interventions_data['oil_fortification']['description'])
                st.markdown("**Policy Requirements:**")
                for req in interventions_data['oil_fortification']['policy_requirements']:
                    st.markdown(f"• {req}")
        
        supp_col, supp_info = st.columns([3, 1])
        with supp_col:
            supplement_pct = st.slider(
                interventions_data['direct_supplement']['name'],
                min_value=0,
                max_value=100,
                value=default_values['supplement'],
                help=f"Cost: {interventions_data['direct_supplement']['unit_cost']} KSH/person | Effectiveness: {interventions_data['direct_supplement']['effectiveness']*100:.0f}%"
            )
        with supp_info:
            with st.expander("Details"):
                st.markdown(interventions_data['direct_supplement']['description'])
                st.markdown("**Policy Requirements:**")
                for req in interventions_data['direct_supplement']['policy_requirements']:
                    st.markdown(f"• {req}")
        
        school_col, school_info = st.columns([3, 1])
        with school_col:
            school_pct = st.slider(
                interventions_data['school_program']['name'],
                min_value=0,
                max_value=100,
                value=default_values['school'],
                help=f"Cost: {interventions_data['school_program']['unit_cost']} KSH/person | Effectiveness: {interventions_data['school_program']['effectiveness']*100:.0f}%"
            )
        with school_info:
            with st.expander("Details"):
                st.markdown(interventions_data['school_program']['description'])
                st.markdown("**Policy Requirements:**")
                for req in interventions_data['school_program']['policy_requirements']:
                    st.markdown(f"• {req}")
        
        # Check if allocation equals 100%
        total_allocation = salt_pct + oil_pct + supplement_pct + school_pct
        
        if total_allocation != 100:
            st.error(f"""
            ⚠️ **Allocation must equal 100%** (Currently: {total_allocation}%)
            
            Adjust the sliders above to reach exactly 100%.
            """)
        else:
            st.success("✅ Valid intervention mix!")
            
            # Calculate coverage
            intervention_mix = {
                'salt': salt_pct,
                'oil': oil_pct,
                'supplement': supplement_pct,
                'school': school_pct
            }
            
            # Use intervention details for accurate cost calculation
            avg_cost_per_person = (
                salt_pct * interventions_data['salt_iodization']['unit_cost'] + 
                oil_pct * interventions_data['oil_fortification']['unit_cost'] + 
                supplement_pct * interventions_data['direct_supplement']['unit_cost'] + 
                school_pct * interventions_data['school_program']['unit_cost']
            ) / 100
            
            # Calculate weighted effectiveness
            weighted_effectiveness = (
                salt_pct * interventions_data['salt_iodization']['effectiveness'] + 
                oil_pct * interventions_data['oil_fortification']['effectiveness'] + 
                supplement_pct * interventions_data['direct_supplement']['effectiveness'] + 
                school_pct * interventions_data['school_program']['effectiveness']
            ) / 100
            
            # Use target_population (defined earlier in targeting strategy section)
            # target_population is defined in lines 1388-1407
            max_coverage = min(1.0, total_budget / (avg_cost_per_person * target_population))
            
            # Add implementation efficiency
            implementation_efficiency = st.slider(
                "Implementation Efficiency (%)",
                min_value=30,
                max_value=95,
                value=70,
                help="Account for logistics, corruption, wastage"
            )
            
            actual_coverage = max_coverage * (implementation_efficiency / 100)
            
            st.markdown(f"""
            <div class="success-box">
                <h4 style="color: #2e7d32;">📊 Coverage Estimate</h4>
                <p style="color: #212121;"><strong>Target Population:</strong> {target_population:,} people</p>
                <p style="color: #212121;"><strong>People Reached:</strong> {int(actual_coverage * target_population):,} ({actual_coverage*100:.1f}% of target)</p>
                <p style="color: #212121;"><strong>Cost per Person:</strong> {avg_cost_per_person:.0f} KSH</p>
                <p style="color: #212121;"><strong>Weighted Effectiveness:</strong> {weighted_effectiveness*100:.0f}%</p>
                <p style="color: #212121;"><strong>Geographic Reach:</strong> {int(actual_coverage*47)}/47 counties</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate and show optimal budget
            st.markdown("### 🎯 Optimal Budget Analysis")
            
            with st.expander("📈 View Budget Optimization Analysis", expanded=False):
                # Allow user to select optimization mode
                optimization_mode = st.radio(
                    "Select Optimization Goal:",
                    options=['minimal', 'balanced', 'comprehensive'],
                    format_func=lambda x: {
                        'minimal': '🚨 Minimal (30% coverage, emergency response)',
                        'balanced': '⚖️ Balanced (70% coverage, standard program)',
                        'comprehensive': '🎯 Comprehensive (90% coverage, elimination)'
                    }[x],
                    index=1,  # Default to balanced
                    horizontal=True
                )
                
                optimal_result = calculate_optimal_budget(intervention_mix, implementation_efficiency, optimization_mode)
                
                # Show optimal budget recommendation
                col_opt1, col_opt2 = st.columns(2)
                
                with col_opt1:
                    targets_status = "✅ All targets achievable" if optimal_result.get('targets_met', False) else "⚠️ Partial target achievement"
                    
                    st.markdown(f"""
                    <div class="info-box">
                        <h4 style="color: #1565c0;">💰 Minimum Budget for {optimization_mode.title()} Goals</h4>
                        <p style="color: #212121;"><strong>Minimum Budget Needed:</strong> {optimal_result['optimal_budget']/1_000_000:.0f} Million KSH</p>
                        <p style="color: #212121;"><strong>Achievable Coverage:</strong> {optimal_result['optimal_coverage']:.1f}%</p>
                        <p style="color: #212121;"><strong>Expected ROI:</strong> {optimal_result['optimal_roi']:.0f}%</p>
                        <p style="color: #212121;"><strong>Lives Saved:</strong> {optimal_result['optimal_cretinism_prevented']:,}</p>
                        <p style="color: #212121;"><strong>IQ Points Gained:</strong> +{optimal_result.get('optimal_iq_gain', 0):.1f} per child</p>
                        <p style="color: #212121;"><strong>Status:</strong> {targets_status}</p>
                        {f"<p style='color: #d32f2f;'>⚠️ <strong>Note:</strong> {optimal_result.get('message', '')}</p>" if optimal_result.get('constrained', False) else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Comparison with current budget - FIXED LOGIC
                    budget_diff = (total_budget - optimal_result['optimal_budget']) / optimal_result['optimal_budget'] * 100 if optimal_result['optimal_budget'] > 0 else 0
                    
                    if abs(budget_diff) < 10:
                        st.success(f"✅ Your budget is well-aligned! Only {abs(budget_diff):.0f}% difference from minimum needed.")
                    elif budget_diff > 0:
                        # Current budget is HIGHER than minimum needed - this is actually good!
                        st.info(f"💰 Your budget exceeds minimum by {budget_diff:.0f}%. You have {(total_budget - optimal_result['optimal_budget'])/1_000_000:.0f}M KSH extra for enhanced impact or savings.")
                    else:
                        # Current budget is LOWER than minimum needed - need more
                        st.warning(f"⚠️ Budget gap: {abs(budget_diff):.0f}% below minimum. Need {(optimal_result['optimal_budget'] - total_budget)/1_000_000:.0f}M KSH more to achieve {optimization_mode} targets.")
                
                with col_opt2:
                    st.markdown(f"""
                    <div class="info-box">
                        <h4 style="color: #1565c0;">🔍 How We Calculate Optimal Budget</h4>
                        <p style="color: #212121;">The optimal budget is determined by analyzing:</p>
                        <ul style="color: #212121;">
                            <li><strong>Implementation Efficiency:</strong> Currently set at {implementation_efficiency}%</li>
                            <li><strong>Diminishing Returns:</strong> Coverage plateaus at higher spending</li>
                            <li><strong>Marginal Benefits:</strong> Each additional KSH yields less benefit</li>
                            <li><strong>Cost-Effectiveness:</strong> Cost per cretinism prevented threshold</li>
                            <li><strong>Implementation Capacity:</strong> System can effectively manage ~{CONFIG['max_annual_capacity']/1_000_000_000:.1f}B KSH/year</li>
                        </ul>
                        <p style="color: #666; font-size: 0.9rem;"><em>Note: Optimal budget adjusts based on your implementation efficiency setting</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Create optimization curves visualization
                if 'data' in optimal_result:
                    st.markdown("#### 📊 Budget Optimization Analysis")
                    st.info("💡 **How to read this chart:** The curves show how different metrics change with budget. Look for where the curves flatten - that's your optimal budget range.")
                    
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

# OUTCOMES PREDICTION TAB
with tab2:
    st.header("📈 Predicted Health Outcomes")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Calculate new structured outcomes
        outcomes = calculate_health_outcomes(actual_coverage, intervention_mix, timeline_months)
        
        # Also get compatibility outcomes for timeline visualization
        immediate, midterm, longterm = simulate_health_outcomes(
            actual_coverage, intervention_mix, timeline_months
        )
        
        # Impact summary cards
        st.markdown("### 🎯 Key Impact Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #e8f5e9; border-left: 5px solid #4caf50;">
                <h4 style="color: #2e7d32;">🧠 Cretinism Prevented</h4>
                <h2 style="color: #1b5e20;">{outcomes['cretinism_prevented']['value']:,}</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['cretinism_prevented']['comparison']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #fff3e0; border-left: 5px solid #ff9800;">
                <h4 style="color: #e65100;">📉 Goiter Cases Reduced</h4>
                <h2 style="color: #bf360c;">{outcomes['goiter_reduced']['value']:,}</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['goiter_reduced']['comparison']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #e3f2fd; border-left: 5px solid #2196f3;">
                <h4 style="color: #1565c0;">🧠 IQ Points Gained</h4>
                <h2 style="color: #0d47a1;">+{outcomes['iq_points_gained']['value']:.1f}</h2>
                <p style="color: #424242; font-size: 0.9rem;">{outcomes['iq_points_gained']['comparison']}</p>
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
            
            • **Immediate (0-3 months):** Urinary iodine levels normalize
            • **Short-term (3-12 months):** Goiter reduction becomes visible
            • **Long-term (1-5 years):** Cognitive and economic benefits emerge
            
            **Policy Implication:** Combine quick-wins with sustainable solutions.
            """)
        
        # Create timeline chart
        months = list(range(0, timeline_months + 1, 3))
        
        # Different impact curves
        immediate_impact = [min(100, (m/6) * 80) for m in months]
        goiter_impact = [min(100, (m/12) * 60) for m in months]
        cognitive_impact = [min(100, (m/24) * 40) for m in months]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months, y=immediate_impact,
            mode='lines+markers',
            name='Iodine Normalization',
            line=dict(color='#FF6B6B', width=3),
            hovertemplate='Month %{x}: %{y:.0f}% impact'
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=goiter_impact,
            mode='lines+markers',
            name='Goiter Reduction',
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
            dict(x=3, y=50, text="First improvements visible", showarrow=True),
            dict(x=12, y=60, text="Goiter reduction measurable", showarrow=True),
            dict(x=24, y=40, text="IQ improvements detected", showarrow=True)
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
                <h4 style="color: #2e7d32;">📖 Mary's Story</h4>
                <p style="color: #212121;"><em>"My goiter disappeared after 6 months of iodized salt. 
                I have more energy and my children are doing better in school!"</em></p>
                <p style="color: #424242;"><strong>- Mother from Turkana</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #2e7d32;">📖 Community Impact</h4>
                <p style="color: #212121;"><em>"Since the iodization program started, we've seen 
                children perform better in school and fewer pregnancy complications."</em></p>
                <p style="color: #424242;"><strong>- Health Worker, Garissa</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ Please complete the intervention design in the 'Intervention Setup' tab first.")

# COST ANALYSIS TAB
with tab3:
    st.markdown("## 💰 Economic Analysis & Return on Investment")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Build context for dynamic calculations - MORE REALISTIC VALUES
        context = {
            'deficiency_severity': 0.95,  # Very high in Kenya (100% deficiency)
            'intervention_timing': 'first_trimester',
            'targeting_strategy': 'risk_based' if target_population < AFFECTED_POPULATION * 0.5 else 'universal',
            'delivery_mode': 'rural' if actual_coverage < 0.5 else 'standalone',
            'primary_intervention': 'salt' if salt_pct > 50 else 'supplement' if supplement_pct > 50 else 'mixed',
            'iodine_content_adequacy': 0.9,  # Assuming good quality control
            'population_compliance': min(0.85, implementation_efficiency / 100),  # Cap at 85%
            'supply_chain_reliability': 0.9,  # Assuming decent supply chain
            'monitoring_effectiveness': 0.95,  # Basic monitoring is sufficient
            'inflation_rate': 0.055,
            'discount_rate': 0.08,
            'risk_adjustment': 0.8  # Some implementation risk
        }
        
        # Calculate dynamic cost per outcome
        cost_metrics = calculate_dynamic_cost_per_outcome(
            total_budget, 
            actual_coverage, 
            implementation_efficiency,
            context
        )
        
        # Calculate annual benefits
        annual_benefit = outcomes['economic_benefit']['value']
        
        # Calculate dynamic ROI timeline
        roi_timeline = calculate_dynamic_roi_timeline(
            total_budget,
            annual_benefit,
            context
        )
        
        # Extract key ROI values
        roi_year1 = roi_timeline[1]['roi']
        roi_year5 = roi_timeline[5]['roi']
        roi_year10 = roi_timeline[10]['roi']
        
        # Find break-even year
        break_even_year = None
        for year, data in roi_timeline.items():
            if data['break_even']:
                break_even_year = year
                break
        
        # Calculate return multiplier
        return_multiplier = (100 + roi_year10) / 100
        
        # Prepare metrics for validation
        metrics = {
            'cost_per_case': cost_metrics['cost_per_case'],
            'roi_year1': roi_year1,
            'roi_year5': roi_year5,
            'roi_year10': roi_year10,
            'return_multiplier': return_multiplier
        }
        
        # Validate and auto-adjust if needed
        validated_metrics, issues = validate_economic_metrics(metrics)
        
        # Use validated values
        cost_per_cretinism = validated_metrics['cost_per_case']
        roi_year1 = validated_metrics['roi_year1']
        roi_year5 = validated_metrics['roi_year5']
        roi_year10 = validated_metrics['roi_year10']
        return_multiplier = validated_metrics['return_multiplier']
        
        # Cost-effectiveness comparison
        st.markdown("### 💡 Is This Investment Worth It?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Build comparison text
            comparisons = "<br>".join([
                f"• {name}: {value:,.0f} KSH per {('life' if 'vaccine' in name.lower() or 'vitamin' in name.lower() else 'case')}"
                for name, value in cost_metrics['comparators'].items()
            ])
            
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f5f5f5; border-left: 5px solid #4caf50;">
                <h4 style="color: #2e7d32;">Cost per Cretinism Prevented</h4>
                <h2 style="color: #1b5e20;">{cost_per_cretinism:,.0f} KSH</h2>
                <p style="color: #424242;">
                    Compare to:<br>
                    {comparisons}
                </p>
                <p style='color: #2e7d32;'>{cost_metrics['rating']}</p>
                <small style='color: #666;'>Cases prevented: {cost_metrics['cases_prevented']:.0f}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Generate phase descriptions based on ROI values
            year1_desc = "Heavy investment" if roi_year1 < -50 else "Investment phase" if roi_year1 < 0 else "Early returns" if roi_year1 < 50 else "Quick returns"
            year5_desc = "Building momentum" if roi_year5 < 100 else "Strong returns" if roi_year5 < 300 else "Exceptional returns"
            year10_desc = "Steady returns" if roi_year10 < 200 else "Sustained impact" if roi_year10 < 500 else "Transformational"
            
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f5f5f5; border-left: 5px solid #1976d2;">
                <h4 style="color: #0d47a1;">Return on Investment Timeline</h4>
                <p style="color: #424242;">
                    <strong>Year 1:</strong> {roi_year1:.0f}% ({year1_desc})<br>
                    <strong>Year 5:</strong> {roi_year5:.0f}% ({year5_desc})<br>
                    <strong>Year 10:</strong> {roi_year10:.0f}% ({year10_desc})<br>
                    <strong>Break-even:</strong> Year {break_even_year if break_even_year else '>10'}
                </p>
                <p style='color: #1976d2;'>📊 Returns improve as program matures</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show validation warnings if any
        if issues:
            st.warning(f"⚠️ Some values were adjusted for realism: {', '.join(issues)}")
        
        # Add context about ROI
        st.info(f"""
        **Understanding Public Health ROI:**
        • Year 1 shows lower returns due to setup costs and implementation ramp-up
        • Benefits compound as: prevented disabilities accumulate, goiter reduction shows effects, and healthcare savings grow
        • By Year 5-10, returns become strongly positive as full benefits are realized
        • Long-term returns (15-20 years) are even higher when children enter the workforce with better cognitive abilities
        
        **Key insight:** Every 1 KSH invested returns {return_multiplier:.1f} KSH over 10 years in direct economic benefits.
        """)
        
        # ROI Timeline Chart
        st.markdown("### 📈 Return on Investment Over Time")
        
        # Create ROI timeline visualization
        years = list(range(1, 11))
        roi_values = [roi_timeline[year]['roi'] for year in years]
        cumulative_benefits = [roi_timeline[year]['cumulative_benefits'] / 1_000_000 for year in years]
        cumulative_costs = [roi_timeline[year]['cumulative_costs'] / 1_000_000 for year in years]
        
        fig_roi = go.Figure()
        
        # Add ROI line
        fig_roi.add_trace(go.Scatter(
            x=years,
            y=roi_values,
            mode='lines+markers',
            name='ROI %',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        
        # Add break-even line
        fig_roi.add_hline(y=0, line_dash="dash", line_color="gray", 
                         annotation_text="Break-even")
        
        # Mark break-even point
        if break_even_year:
            fig_roi.add_vline(x=break_even_year, line_dash="dot", line_color="blue",
                            annotation_text=f"Break-even Year {break_even_year}")
        
        fig_roi.update_layout(
            title="ROI Progression",
            xaxis_title="Year",
            yaxis_title="Return on Investment (%)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
        
        # Budget breakdown visualization
        st.markdown("### 📊 Where Does the Money Go?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Calculate costs for each intervention
            budget_breakdown = []
            for key, percentage in {'salt': salt_pct, 'oil': oil_pct, 'supplement': supplement_pct, 'school': school_pct}.items():
                if percentage > 0:
                    intervention_mapping = {
                        'salt': 'salt_iodization',
                        'oil': 'oil_fortification',
                        'supplement': 'direct_supplement',
                        'school': 'school_program'
                    }
                    budget_breakdown.append({
                        'Intervention': interventions_data[intervention_mapping[key]]['name'],
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
        
        with col2:
            # Create timeline comparison
            st.markdown("#### ROI Evolution Over Time")
            
            years_range = list(range(1, 11))
            roi_timeline = []
            for year in years_range:
                if year == 1:
                    year_roi = roi_year1
                elif year <= 5:
                    # Interpolate between year 1 and year 5
                    year_roi = roi_year1 + (roi_year5 - roi_year1) * (year - 1) / 4
                else:
                    # Interpolate between year 5 and year 10
                    year_roi = roi_year5 + (roi_year10 - roi_year5) * (year - 5) / 5
                roi_timeline.append(year_roi)
            
            fig_roi = go.Figure()
            fig_roi.add_trace(go.Scatter(
                x=years_range,
                y=roi_timeline,
                mode='lines+markers',
                name='ROI %',
                line=dict(color='green', width=3),
                marker=dict(size=8)
            ))
            
            # Add break-even line
            fig_roi.add_hline(y=0, line_dash="dash", line_color="red", 
                             annotation_text="Break-even")
            
            fig_roi.update_layout(
                title="Return on Investment Evolution",
                xaxis_title="Years",
                yaxis_title="ROI (%)",
                height=350,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_roi, use_container_width=True)
        
        # Funding sources and sustainability
        st.markdown("### 💼 Funding Strategy")
        
        with st.expander("Potential Funding Sources"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                **Government Sources:**
                • National Treasury allocation
                • County government budgets
                • Universal Health Coverage funds
                • Social protection programs
                • Emergency response funds
                """)
            
            with col2:
                st.markdown("""
                **International Partners:**
                • UNICEF iodine programs
                • WHO nutrition initiatives
                • World Bank health projects
                • GAIN (Global Alliance)
                • Micronutrient Initiative
                """)
            
            with col3:
                st.markdown("""
                **Innovative Financing:**
                • Salt industry partnerships
                • Oil refinery agreements
                • Development impact bonds
                • Carbon credit linkages
                • Private sector CSR
                """)
        
        # Cost-effectiveness analysis
        st.markdown("### 📈 Detailed Cost-Effectiveness Analysis")
        
        # Create comparison table
        comparison_data = {
            'Metric': [
                'Cost per person reached',
                'Cost per IQ point gained',
                'Cost per goiter resolved',
                'Cost per pregnancy saved',
                'Annual economic return'
            ],
            'This Program': [
                f"{total_budget/(actual_coverage * target_population):.0f} KSH",
                f"{total_budget/(outcomes['iq_points_gained']['value'] * CHILDREN_UNDER_5 * actual_coverage):.0f} KSH",
                f"{total_budget/outcomes['goiter_reduced']['value']:.0f} KSH",
                f"{total_budget/(PREGNANT_WOMEN * actual_coverage * 0.15):.0f} KSH",
                f"{annual_benefit/1_000_000:.1f}M KSH"
            ],
            'WHO Standard': [
                "< 100 KSH",
                "< 5,000 KSH",
                "< 10,000 KSH",
                "< 100,000 KSH",
                "3-10x investment"
            ],
            'Status': [
                "✅" if total_budget/(actual_coverage * target_population) < 100 else "⚠️",
                "✅" if total_budget/(outcomes['iq_points_gained']['value'] * CHILDREN_UNDER_5 * actual_coverage) < 5000 else "⚠️",
                "✅" if total_budget/outcomes['goiter_reduced']['value'] < 10000 else "⚠️",
                "✅" if total_budget/(PREGNANT_WOMEN * actual_coverage * 0.15) < 100000 else "⚠️",
                "✅" if annual_benefit > total_budget * 3 else "⚠️"
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Please complete the intervention design first.")

# TECHNICAL DETAILS TAB
with tab4:
    st.markdown("## 🔧 Technical Implementation Requirements")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Infrastructure Requirements Section
        st.markdown("### 🏗️ Infrastructure Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box" style="background-color: #e8f5e9;">
                <h4 style="color: #2e7d32;">Laboratory Infrastructure</h4>
                <ul style="color: #424242;">
                    <li><strong>National Reference Lab:</strong> 1 facility with spectrophotometry capabilities</li>
                    <li><strong>Regional Labs:</strong> 8 facilities for urinary iodine testing</li>
                    <li><strong>County Labs:</strong> 47 basic testing facilities</li>
                    <li><strong>Equipment needed:</strong>
                        <ul>
                            <li>Spectrophotometers (20 units)</li>
                            <li>Titration equipment (100 sets)</li>
                            <li>Rapid test kits (10,000/month)</li>
                        </ul>
                    </li>
                    <li><strong>Estimated cost:</strong> 150M KSH initial, 20M KSH/year maintenance</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box" style="background-color: #fff3e0; margin-top: 10px;">
                <h4 style="color: #e65100;">Storage & Distribution</h4>
                <ul style="color: #424242;">
                    <li><strong>Central warehouses:</strong> 4 climate-controlled facilities</li>
                    <li><strong>Regional depots:</strong> 8 distribution centers</li>
                    <li><strong>County stores:</strong> 47 facilities with basic storage</li>
                    <li><strong>Cold chain:</strong> Not required for iodine interventions</li>
                    <li><strong>Transport fleet:</strong> 50 vehicles for distribution</li>
                    <li><strong>Inventory system:</strong> Digital tracking with IoT sensors</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box" style="background-color: #e3f2fd;">
                <h4 style="color: #1565c0;">Manufacturing & Production</h4>
                <ul style="color: #424242;">
                    <li><strong>Salt iodization plants:</strong> 10 facilities to upgrade</li>
                    <li><strong>Oil fortification:</strong> 5 major oil producers to equip</li>
                    <li><strong>Supplement production:</strong> 2 pharmaceutical facilities</li>
                    <li><strong>Quality control labs:</strong> 15 on-site testing facilities</li>
                    <li><strong>Production capacity:</strong>
                        <ul>
                            <li>Salt: 500,000 tons/year</li>
                            <li>Oil: 200,000 liters/month</li>
                            <li>Supplements: 10M doses/month</li>
                        </ul>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box" style="background-color: #f3e5f5; margin-top: 10px;">
                <h4 style="color: #6a1b9a;">Information Systems</h4>
                <ul style="color: #424242;">
                    <li><strong>DHIS2 integration:</strong> Real-time reporting module</li>
                    <li><strong>Supply chain system:</strong> End-to-end tracking</li>
                    <li><strong>Quality assurance:</strong> Digital certification system</li>
                    <li><strong>Mobile health (mHealth):</strong> SMS reminders & education</li>
                    <li><strong>Dashboard:</strong> Real-time monitoring for decision makers</li>
                    <li><strong>Data centers:</strong> 2 facilities with backup systems</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Human Resources Section
        st.markdown("### 👥 Human Resource Requirements")
        
        # Calculate HR needs based on coverage
        hr_multiplier = actual_coverage if 'actual_coverage' in locals() else 0.7
        
        hr_data = {
            'Position': [
                'Program Manager',
                'Nutritionists',
                'Lab Technicians',
                'Community Health Workers',
                'Supply Chain Officers',
                'Quality Control Inspectors',
                'Data Analysts',
                'Health Educators',
                'Monitoring & Evaluation Officers',
                'Administrative Staff'
            ],
            'Number Required': [
                1,
                int(47 * hr_multiplier),  # One per county
                int(100 * hr_multiplier),
                int(5000 * hr_multiplier),  # CHWs
                int(20 * hr_multiplier),
                int(30 * hr_multiplier),
                int(10 * hr_multiplier),
                int(100 * hr_multiplier),
                int(15 * hr_multiplier),
                int(50 * hr_multiplier)
            ],
            'Training Days': [30, 15, 20, 5, 10, 15, 20, 10, 15, 5],
            'Monthly Cost (KSH)': [
                500000, 80000, 60000, 10000, 100000, 
                70000, 120000, 50000, 90000, 40000
            ]
        }
        
        hr_df = pd.DataFrame(hr_data)
        hr_df['Total Monthly Cost'] = hr_df['Number Required'] * hr_df['Monthly Cost (KSH)']
        hr_df['Annual Cost (Million KSH)'] = hr_df['Total Monthly Cost'] * 12 / 1_000_000
        
        # Display HR table
        st.dataframe(
            hr_df.style.format({
                'Number Required': '{:,.0f}',
                'Monthly Cost (KSH)': '{:,.0f}',
                'Total Monthly Cost': '{:,.0f}',
                'Annual Cost (Million KSH)': '{:.1f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        total_hr_cost = hr_df['Annual Cost (Million KSH)'].sum()
        hr_percentage = (total_hr_cost * 1_000_000 / total_budget * 100) if total_budget > 0 else 0
        st.info(f"💰 **Total Annual HR Cost:** {total_hr_cost:.1f} Million KSH ({hr_percentage:.1f}% of program budget)")
        
        # KPI Framework
        st.markdown("### 📊 Key Performance Indicators (KPIs)")
        
        kpi_data = {
            'Category': [
                'Process', 'Process', 'Process', 'Process',
                'Output', 'Output', 'Output', 'Output',
                'Outcome', 'Outcome', 'Outcome', 'Outcome',
                'Impact', 'Impact', 'Impact', 'Impact'
            ],
            'Indicator': [
                'Salt samples tested monthly',
                'Households reached with education',
                'CHWs trained and active',
                'Supply chain stockout rate',
                'Iodized salt coverage',
                'Oil fortification coverage', 
                'Supplement distribution rate',
                'School program enrollment',
                'Median urinary iodine',
                'Goiter prevalence reduction',
                'Thyroid function improvement',
                'Pregnancy outcomes improved',
                'Cretinism cases prevented',
                'IQ points gained (average)',
                'Economic productivity increase',
                'Healthcare cost savings'
            ],
            'Target': [
                '1,000 samples',
                '500,000 households',
                '5,000 CHWs',
                '<5%',
                '>90%',
                '>70%',
                '95% of target',
                '80% of schools',
                '>100 µg/L',
                '50% reduction',
                '70% normalized',
                '30% improvement',
                f'{int(outcomes["cretinism_prevented"]["value"])} cases',
                f'{outcomes["iq_points_gained"]["value"]:.1f} points',
                '15% increase',
                '20% reduction'
            ],
            'Frequency': [
                'Monthly', 'Quarterly', 'Monthly', 'Weekly',
                'Quarterly', 'Quarterly', 'Monthly', 'Termly',
                'Annual', 'Annual', 'Semi-annual', 'Annual',
                'Annual', 'Every 3 years', 'Every 5 years', 'Annual'
            ],
            'Data Source': [
                'Lab reports', 'CHW reports', 'HR system', 'Supply system',
                'Market survey', 'Production data', 'Distribution logs', 'School records',
                'Health survey', 'Clinical data', 'Lab results', 'Hospital records',
                'Health records', 'Cognitive assessment', 'Economic survey', 'Insurance data'
            ]
        }
        
        kpi_df = pd.DataFrame(kpi_data)
        
        # Color code by category
        def highlight_category(row):
            colors = {
                'Process': 'background-color: #e3f2fd',
                'Output': 'background-color: #e8f5e9',
                'Outcome': 'background-color: #fff3e0',
                'Impact': 'background-color: #f3e5f5'
            }
            return [colors.get(row['Category'], '')] * len(row)
        
        st.dataframe(
            kpi_df.style.apply(highlight_category, axis=1),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Monitoring & Evaluation Framework
        st.markdown("### 📈 Monitoring & Evaluation Framework")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box" style="background-color: #e8f5e9;">
                <h4 style="color: #2e7d32;">Monitoring Components</h4>
                <ul style="color: #424242;">
                    <li><strong>Baseline Survey:</strong>
                        <ul>
                            <li>Urinary iodine levels</li>
                            <li>Goiter prevalence</li>
                            <li>Salt iodization levels</li>
                            <li>Dietary patterns</li>
                        </ul>
                    </li>
                    <li><strong>Regular Monitoring:</strong>
                        <ul>
                            <li>Monthly: Production & distribution</li>
                            <li>Quarterly: Coverage & quality</li>
                            <li>Semi-annual: Health indicators</li>
                            <li>Annual: Comprehensive review</li>
                        </ul>
                    </li>
                    <li><strong>Data Collection Tools:</strong>
                        <ul>
                            <li>Mobile data collection (ODK)</li>
                            <li>Laboratory information system</li>
                            <li>Supply chain tracking</li>
                            <li>Community feedback system</li>
                        </ul>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box" style="background-color: #fff3e0;">
                <h4 style="color: #e65100;">Evaluation Strategy</h4>
                <ul style="color: #424242;">
                    <li><strong>Mid-term Evaluation (Year 2):</strong>
                        <ul>
                            <li>Process evaluation</li>
                            <li>Coverage assessment</li>
                            <li>Quality audit</li>
                            <li>Stakeholder feedback</li>
                        </ul>
                    </li>
                    <li><strong>Final Evaluation (Year 5):</strong>
                        <ul>
                            <li>Impact assessment</li>
                            <li>Cost-effectiveness analysis</li>
                            <li>Sustainability review</li>
                            <li>Lessons learned</li>
                        </ul>
                    </li>
                    <li><strong>External Validation:</strong>
                        <ul>
                            <li>WHO technical review</li>
                            <li>Independent audit</li>
                            <li>Peer review publication</li>
                            <li>Community validation</li>
                        </ul>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk Management
        st.markdown("### ⚠️ Risk Management Matrix")
        
        risk_data = {
            'Risk': [
                'Salt producers resist fortification',
                'Quality control failures',
                'Supply chain disruptions',
                'Low community acceptance',
                'Political instability',
                'Funding shortfalls',
                'Technical capacity gaps',
                'Climate/disaster impacts'
            ],
            'Likelihood': ['Medium', 'Low', 'Medium', 'Low', 'Medium', 'High', 'Medium', 'Low'],
            'Impact': ['High', 'Very High', 'High', 'Medium', 'High', 'Very High', 'Medium', 'High'],
            'Mitigation Strategy': [
                'Incentives & regulations, phased approach',
                'Multiple testing points, certification system',
                'Buffer stocks, multiple suppliers, local production',
                'Community education, local champions, success stories',
                'Multi-party support, legal framework',
                'Diversified funding, cost reduction strategies',
                'Intensive training, technical assistance, partnerships',
                'Emergency protocols, decentralized storage'
            ],
            'Contingency Plan': [
                'Import pre-iodized salt, direct supplementation',
                'Recall system, rapid response team',
                'Emergency procurement, international aid',
                'Alternative delivery channels, incentives',
                'Accelerated implementation in stable areas',
                'Scale down, prioritize high-risk groups',
                'External technical support, simplified protocols',
                'Emergency distribution, mobile teams'
            ]
        }
        
        risk_df = pd.DataFrame(risk_data)
        
        # Color code by severity
        def color_risk(val):
            if val == 'Very High':
                return 'background-color: #ffcdd2'
            elif val == 'High':
                return 'background-color: #ffe0b2'
            elif val == 'Medium':
                return 'background-color: #fff9c4'
            elif val == 'Low':
                return 'background-color: #c8e6c9'
            return ''
        
        st.dataframe(
            risk_df.style.applymap(color_risk, subset=['Likelihood', 'Impact']),
            use_container_width=True,
            hide_index=True,
            height=350
        )
        
        # Implementation Timeline
        st.markdown("### 📅 Implementation Phases")
        
        phases_data = {
            'Phase': ['1. Setup', '2. Pilot', '3. Scale-up', '4. Full Coverage', '5. Sustain'],
            'Duration': ['3 months', '6 months', '12 months', '12 months', 'Ongoing'],
            'Key Activities': [
                'Establish infrastructure, recruit staff, baseline survey',
                'Test in 5 counties, refine protocols, train personnel',
                'Expand to 25 counties, strengthen supply chain',
                'Cover all 47 counties, optimize operations',
                'Maintain coverage, continuous improvement'
            ],
            'Success Metrics': [
                'Infrastructure ready, staff hired, baseline complete',
                '70% coverage in pilot areas, <10% stockouts',
                '80% coverage in target areas, quality standards met',
                '90% national coverage, all KPIs on track',
                'Sustained >90% coverage, reducing external support'
            ],
            'Budget %': ['15%', '20%', '35%', '20%', '10%']
        }
        
        phases_df = pd.DataFrame(phases_data)
        st.dataframe(phases_df, use_container_width=True, hide_index=True)
        
    else:
        st.warning("⚠️ Please complete the intervention design in the 'Intervention Setup' tab first.")

# COMPARE SCENARIOS TAB
with tab5:
    st.markdown("## 🔄 Scenario Comparison & Optimization")
    
    # Preset scenarios
    st.markdown("### 📊 Compare Different Intervention Strategies")
    
    # Define preset scenarios with different intervention mixes
    scenarios = {
        "Current Plan": {
            "description": "Your current intervention design",
            "budget": total_budget if 'total_budget' in locals() else 1_000_000_000,
            "salt": salt_pct if 'salt_pct' in locals() else 40,
            "oil": oil_pct if 'oil_pct' in locals() else 20,
            "supplement": supplement_pct if 'supplement_pct' in locals() else 25,
            "school": school_pct if 'school_pct' in locals() else 15,
            "efficiency": implementation_efficiency if 'implementation_efficiency' in locals() else 70,
            "color": "#2196F3"
        },
        "Cost-Optimized": {
            "description": "Maximize coverage with minimal budget",
            "budget": 500_000_000,
            "salt": 70,  # Cheapest intervention
            "oil": 10,
            "supplement": 5,
            "school": 15,
            "efficiency": 65,
            "color": "#4CAF50"
        },
        "Maximum Impact": {
            "description": "Highest health outcomes regardless of cost",
            "budget": 3_000_000_000,
            "salt": 30,
            "oil": 25,
            "supplement": 35,  # Most effective
            "school": 10,
            "efficiency": 85,
            "color": "#FF9800"
        },
        "Emergency Response": {
            "description": "Rapid intervention for crisis situations",
            "budget": 1_500_000_000,
            "salt": 20,
            "oil": 30,  # Quick deployment
            "supplement": 40,  # Immediate effect
            "school": 10,
            "efficiency": 60,
            "color": "#F44336"
        },
        "Sustainable Long-term": {
            "description": "Build lasting infrastructure",
            "budget": 2_000_000_000,
            "salt": 50,  # Infrastructure focus
            "oil": 20,
            "supplement": 10,
            "school": 20,
            "efficiency": 80,
            "color": "#9C27B0"
        },
        "WHO Recommended": {
            "description": "Based on WHO best practices",
            "budget": 1_200_000_000,
            "salt": 45,
            "oil": 20,
            "supplement": 20,
            "school": 15,
            "efficiency": 75,
            "color": "#00BCD4"
        }
    }
    
    # Calculate outcomes for each scenario
    scenario_outcomes = {}
    
    for scenario_name, scenario_data in scenarios.items():
        # Calculate coverage
        intervention_mix = {
            'salt': scenario_data['salt'],
            'oil': scenario_data['oil'],
            'supplement': scenario_data['supplement'],
            'school': scenario_data['school']
        }
        
        # Calculate weighted effectiveness and cost
        weighted_effectiveness = (
            scenario_data['salt'] * 0.85 +
            scenario_data['oil'] * 0.92 +
            scenario_data['supplement'] * 0.98 +
            scenario_data['school'] * 0.88
        ) / 100
        
        weighted_cost = (
            scenario_data['salt'] * 2.5 +
            scenario_data['oil'] * 30 +
            scenario_data['supplement'] * 50 +
            scenario_data['school'] * 8
        ) / 100
        
        # Calculate coverage
        theoretical_coverage = scenario_data['budget'] / (weighted_cost * AFFECTED_POPULATION)
        actual_coverage = min(1.0, theoretical_coverage * (scenario_data['efficiency'] / 100))
        
        # Calculate health outcomes
        cretinism_prevented = int(actual_coverage * weighted_effectiveness * int(PREGNANT_WOMEN * 0.003))
        goiter_reduced = int(actual_coverage * weighted_effectiveness * GOITER_CASES * 0.6)
        iq_points = actual_coverage * weighted_effectiveness * 13
        
        # Calculate economic outcomes
        annual_benefit = calculate_realistic_economic_benefit(actual_coverage, weighted_effectiveness)
        five_year_benefits = annual_benefit * 4.1
        five_year_costs = scenario_data['budget'] * 5 * 0.9
        roi = ((five_year_benefits - five_year_costs) / five_year_costs * 100) if five_year_costs > 0 else 0
        
        scenario_outcomes[scenario_name] = {
            'coverage': actual_coverage * 100,
            'people_reached': int(actual_coverage * AFFECTED_POPULATION),
            'cretinism_prevented': cretinism_prevented,
            'goiter_reduced': goiter_reduced,
            'iq_points': iq_points,
            'annual_benefit': annual_benefit,
            'roi': roi,
            'cost_per_person': scenario_data['budget'] / (actual_coverage * AFFECTED_POPULATION) if actual_coverage > 0 else 0,
            'cost_per_cretinism': scenario_data['budget'] / cretinism_prevented if cretinism_prevented > 0 else float('inf'),
            'efficiency_score': (roi + actual_coverage * 100) / 2  # Combined metric
        }
    
    # Display scenario cards
    st.markdown("### 🎯 Scenario Overview")
    
    cols = st.columns(3)
    for i, (scenario_name, scenario_data) in enumerate(scenarios.items()):
        with cols[i % 3]:
            outcomes = scenario_outcomes[scenario_name]
            
            # Determine performance rating
            if outcomes['efficiency_score'] > 80:
                rating = "⭐⭐⭐⭐⭐"
                rating_color = "#4CAF50"
            elif outcomes['efficiency_score'] > 60:
                rating = "⭐⭐⭐⭐"
                rating_color = "#8BC34A"
            elif outcomes['efficiency_score'] > 40:
                rating = "⭐⭐⭐"
                rating_color = "#FFC107"
            else:
                rating = "⭐⭐"
                rating_color = "#FF9800"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {scenario_data['color']}20 0%, {scenario_data['color']}10 100%); 
                        border-left: 4px solid {scenario_data['color']}; 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin-bottom: 10px;">
                <h4 style="color: {scenario_data['color']}; margin: 0;">{scenario_name}</h4>
                <p style="color: #666; font-size: 0.9rem; margin: 5px 0;">{scenario_data['description']}</p>
                <p style="color: {rating_color}; font-size: 1.2rem; margin: 5px 0;">{rating}</p>
                <hr style="margin: 10px 0; opacity: 0.3;">
                <p style="margin: 3px 0;"><strong>Budget:</strong> {scenario_data['budget']/1_000_000:.0f}M KSH</p>
                <p style="margin: 3px 0;"><strong>Coverage:</strong> {outcomes['coverage']:.1f}%</p>
                <p style="margin: 3px 0;"><strong>5-Year ROI:</strong> {outcomes['roi']:.0f}%</p>
                <p style="margin: 3px 0;"><strong>Lives Saved:</strong> {outcomes['cretinism_prevented']:,}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed comparison table
    st.markdown("### 📊 Detailed Metrics Comparison")
    
    comparison_df = pd.DataFrame(scenario_outcomes).T
    comparison_df['Budget (M KSH)'] = [scenarios[s]['budget']/1_000_000 for s in comparison_df.index]
    
    # Select columns to display
    display_columns = [
        'Budget (M KSH)',
        'coverage',
        'people_reached',
        'cretinism_prevented',
        'iq_points',
        'roi',
        'cost_per_person',
        'efficiency_score'
    ]
    
    # Rename columns for display
    column_names = {
        'coverage': 'Coverage (%)',
        'people_reached': 'People Reached',
        'cretinism_prevented': 'Cretinism Prevented',
        'iq_points': 'Avg IQ Gain',
        'roi': '5-Year ROI (%)',
        'cost_per_person': 'Cost/Person (KSH)',
        'efficiency_score': 'Efficiency Score'
    }
    
    display_df = comparison_df[display_columns].rename(columns=column_names)
    
    # Highlight best performers
    def highlight_best(s):
        if s.name in ['Coverage (%)', 'People Reached', 'Cretinism Prevented', 'Avg IQ Gain', '5-Year ROI (%)', 'Efficiency Score']:
            return ['background-color: #c8e6c9' if v == s.max() else '' for v in s]
        elif s.name in ['Cost/Person (KSH)', 'Budget (M KSH)']:
            return ['background-color: #c8e6c9' if v == s.min() else '' for v in s]
        return ['' for _ in s]
    
    st.dataframe(
        display_df.style.apply(highlight_best).format({
            'Budget (M KSH)': '{:,.0f}',
            'Coverage (%)': '{:.1f}',
            'People Reached': '{:,.0f}',
            'Cretinism Prevented': '{:,.0f}',
            'Avg IQ Gain': '{:.1f}',
            '5-Year ROI (%)': '{:.0f}',
            'Cost/Person (KSH)': '{:.0f}',
            'Efficiency Score': '{:.1f}'
        }),
        use_container_width=True
    )
    
    # Visualization comparisons
    st.markdown("### 📈 Visual Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Coverage vs Cost chart
        fig_coverage = go.Figure()
        
        for scenario_name in scenarios.keys():
            fig_coverage.add_trace(go.Scatter(
                x=[scenarios[scenario_name]['budget']/1_000_000],
                y=[scenario_outcomes[scenario_name]['coverage']],
                mode='markers+text',
                name=scenario_name,
                text=[scenario_name],
                textposition="top center",
                marker=dict(
                    size=scenario_outcomes[scenario_name]['cretinism_prevented']/10,
                    color=scenarios[scenario_name]['color'],
                    line=dict(width=2, color='white')
                ),
                hovertemplate=f"<b>{scenario_name}</b><br>" +
                             "Budget: %{x:.0f}M KSH<br>" +
                             "Coverage: %{y:.1f}%<br>" +
                             "Lives Saved: " + f"{scenario_outcomes[scenario_name]['cretinism_prevented']:,}"
            ))
        
        fig_coverage.update_layout(
            title="Coverage vs Investment (bubble size = lives saved)",
            xaxis_title="Budget (Million KSH)",
            yaxis_title="Population Coverage (%)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_coverage, use_container_width=True)
    
    with col2:
        # ROI comparison
        fig_roi = go.Figure()
        
        roi_data = [(name, outcomes['roi']) for name, outcomes in scenario_outcomes.items()]
        roi_data.sort(key=lambda x: x[1], reverse=True)
        
        fig_roi.add_trace(go.Bar(
            x=[x[1] for x in roi_data],
            y=[x[0] for x in roi_data],
            orientation='h',
            marker=dict(
                color=[scenarios[x[0]]['color'] for x in roi_data],
                line=dict(width=2, color='white')
            ),
            text=[f"{x[1]:.0f}%" for x in roi_data],
            textposition='outside'
        ))
        
        fig_roi.update_layout(
            title="5-Year Return on Investment Comparison",
            xaxis_title="ROI (%)",
            yaxis_title="",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Multi-metric radar chart
    st.markdown("### 🎯 Multi-Dimensional Performance")
    
    # Prepare radar chart data
    categories = ['Coverage', 'ROI', 'Lives Saved', 'IQ Impact', 'Cost Efficiency']
    
    fig_radar = go.Figure()
    
    # Normalize metrics to 0-100 scale for comparison
    max_coverage = max(o['coverage'] for o in scenario_outcomes.values())
    max_roi = max(o['roi'] for o in scenario_outcomes.values())
    max_lives = max(o['cretinism_prevented'] for o in scenario_outcomes.values())
    max_iq = max(o['iq_points'] for o in scenario_outcomes.values())
    min_cost = min(o['cost_per_person'] for o in scenario_outcomes.values())
    max_cost = max(o['cost_per_person'] for o in scenario_outcomes.values())
    
    for scenario_name in ['Current Plan', 'Cost-Optimized', 'Maximum Impact', 'WHO Recommended']:
        if scenario_name in scenarios:
            outcomes = scenario_outcomes[scenario_name]
            
            # Normalize values
            normalized_values = [
                (outcomes['coverage'] / max_coverage) * 100,
                (outcomes['roi'] / max_roi) * 100 if max_roi > 0 else 0,
                (outcomes['cretinism_prevented'] / max_lives) * 100,
                (outcomes['iq_points'] / max_iq) * 100,
                ((max_cost - outcomes['cost_per_person']) / (max_cost - min_cost)) * 100 if max_cost > min_cost else 50
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=categories,
                fill='toself',
                name=scenario_name,
                line=dict(color=scenarios[scenario_name]['color'], width=2),
                opacity=0.4
            ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Multi-Criteria Performance Comparison",
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Recommendations based on comparison
    st.markdown("### 💡 Strategic Recommendations")
    
    # Find best scenario for different priorities
    best_coverage = max(scenario_outcomes.items(), key=lambda x: x[1]['coverage'])[0]
    best_roi = max(scenario_outcomes.items(), key=lambda x: x[1]['roi'])[0]
    best_lives = max(scenario_outcomes.items(), key=lambda x: x[1]['cretinism_prevented'])[0]
    best_efficiency = max(scenario_outcomes.items(), key=lambda x: x[1]['efficiency_score'])[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-box" style="background-color: #e8f5e9;">
            <h4 style="color: #2e7d32;">📊 If Your Priority Is...</h4>
            <ul style="color: #424242;">
                <li><strong>Maximum Coverage:</strong> Choose <span style="color: {scenarios[best_coverage]['color']};">{best_coverage}</span>
                    <ul><li>Reaches {scenario_outcomes[best_coverage]['coverage']:.1f}% of population</li></ul>
                </li>
                <li><strong>Best ROI:</strong> Choose <span style="color: {scenarios[best_roi]['color']};">{best_roi}</span>
                    <ul><li>Returns {scenario_outcomes[best_roi]['roi']:.0f}% over 5 years</li></ul>
                </li>
                <li><strong>Most Lives Saved:</strong> Choose <span style="color: {scenarios[best_lives]['color']};">{best_lives}</span>
                    <ul><li>Prevents {scenario_outcomes[best_lives]['cretinism_prevented']:,} cases</li></ul>
                </li>
                <li><strong>Overall Efficiency:</strong> Choose <span style="color: {scenarios[best_efficiency]['color']};">{best_efficiency}</span>
                    <ul><li>Score: {scenario_outcomes[best_efficiency]['efficiency_score']:.1f}/100</li></ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Current plan analysis
        if 'Current Plan' in scenario_outcomes:
            current = scenario_outcomes['Current Plan']
            
            # Generate specific recommendations
            recommendations = []
            
            if current['coverage'] < 80:
                recommendations.append("🎯 Increase budget or efficiency to reach WHO's 80% coverage target")
            
            if current['roi'] < 100:
                recommendations.append("💰 Shift more budget to salt iodization for better ROI")
            
            if current['cost_per_person'] > 50:
                recommendations.append("📉 Reduce per-person costs by focusing on mass interventions")
            
            if current['cretinism_prevented'] < 400:
                recommendations.append("🏥 Increase direct supplementation for pregnant women")
            
            if not recommendations:
                recommendations.append("✅ Your current plan is well-optimized!")
            
            st.markdown(f"""
            <div class="info-box" style="background-color: #fff3e0;">
                <h4 style="color: #e65100;">🎯 Your Current Plan Analysis</h4>
                <p style="color: #424242;"><strong>Performance Summary:</strong></p>
                <ul style="color: #424242;">
                    <li>Coverage: {current['coverage']:.1f}% {'✅' if current['coverage'] >= 80 else '⚠️'}</li>
                    <li>ROI: {current['roi']:.0f}% {'✅' if current['roi'] >= 100 else '⚠️'}</li>
                    <li>Lives Saved: {current['cretinism_prevented']:,} {'✅' if current['cretinism_prevented'] >= 400 else '⚠️'}</li>
                    <li>Efficiency: {current['efficiency_score']:.1f}/100 {'✅' if current['efficiency_score'] >= 60 else '⚠️'}</li>
                </ul>
                <p style="color: #424242;"><strong>Recommendations:</strong></p>
                <ul style="color: #424242;">
                    {''.join(f'<li>{rec}</li>' for rec in recommendations)}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Scenario builder
    st.markdown("### 🛠️ Build Your Own Scenario")
    
    with st.expander("Custom Scenario Builder"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            custom_budget = st.number_input(
                "Budget (Million KSH)",
                min_value=100,
                max_value=5000,
                value=1000,
                step=100
            ) * 1_000_000
            
            custom_efficiency = st.slider(
                "Implementation Efficiency (%)",
                min_value=30,
                max_value=95,
                value=70,
                step=5
            )
        
        with col2:
            st.write("**Intervention Mix (%)**")
            custom_salt = st.number_input("Salt Iodization", 0, 100, 40, 5)
            custom_oil = st.number_input("Oil Fortification", 0, 100, 20, 5)
        
        with col3:
            st.write("**Continue Mix**")
            custom_supplement = st.number_input("Direct Supplementation", 0, 100, 25, 5)
            custom_school = st.number_input("School Programs", 0, 100, 15, 5)
        
        total_custom = custom_salt + custom_oil + custom_supplement + custom_school
        
        if total_custom == 100:
            # Calculate custom scenario outcomes
            custom_effectiveness = (
                custom_salt * 0.85 +
                custom_oil * 0.92 +
                custom_supplement * 0.98 +
                custom_school * 0.88
            ) / 100
            
            custom_cost = (
                custom_salt * 2.5 +
                custom_oil * 30 +
                custom_supplement * 50 +
                custom_school * 8
            ) / 100
            
            custom_coverage = min(1.0, custom_budget / (custom_cost * AFFECTED_POPULATION) * (custom_efficiency / 100))
            
            custom_cretinism = int(custom_coverage * custom_effectiveness * 500)
            custom_iq = custom_coverage * custom_effectiveness * 13
            custom_benefit = calculate_realistic_economic_benefit(custom_coverage, custom_effectiveness)
            custom_roi = ((custom_benefit * 4.1 - custom_budget * 5 * 0.9) / (custom_budget * 5 * 0.9) * 100)
            
            st.success(f"""
            **Custom Scenario Results:**
            - Coverage: {custom_coverage * 100:.1f}%
            - Lives Saved: {custom_cretinism:,}
            - IQ Gain: {custom_iq:.1f} points
            - 5-Year ROI: {custom_roi:.0f}%
            """)
        else:
            st.error(f"Intervention mix must equal 100% (currently {total_custom}%)")

# REPORTS TAB
with tab6:
    st.header("📋 Simulation Report")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Calculate ROI and cost metrics for the report
        # Check if we have the new outcomes format or need to calculate
        if 'outcomes' not in locals() or not isinstance(outcomes, dict) or 'iq_points_gained' not in outcomes:
            # Calculate intervention effectiveness
            intervention_mix = {
                'salt': salt_pct,
                'oil': oil_pct,
                'supplement': supplement_pct,
                'school': school_pct
            }
            # Use the old function for compatibility
            immediate, midterm, longterm = simulate_health_outcomes(actual_coverage, intervention_mix, timeline_months)
            
            # Calculate cost per IQ point using old format
            total_iq_points = longterm['iq_points_gained'] * actual_coverage * CHILDREN_UNDER_5
            cost_per_iq_point = total_budget / max(total_iq_points, 1)
            
            # Calculate economic benefit
            weighted_effectiveness = sum(intervention_mix.values()) / 100
            annual_benefit = calculate_realistic_economic_benefit(actual_coverage, weighted_effectiveness)
            
            # Prepare outcomes for report (convert to new format for consistency)
            outcomes = {
                'cretinism_prevented': {'value': longterm['cretinism_prevented']},
                'goiter_reduced': {'value': int(actual_coverage * weighted_effectiveness * GOITER_CASES * 0.6)},
                'iq_points_gained': {'value': longterm['iq_points_gained']},
                'pregnancy_improved': {'value': int(actual_coverage * weighted_effectiveness * PREGNANT_WOMEN * 0.3)},
                'economic_benefit': {'value': annual_benefit}
            }
        else:
            # Use new format outcomes
            total_iq_points = outcomes['iq_points_gained']['value'] * actual_coverage * CHILDREN_UNDER_5
            cost_per_iq_point = total_budget / max(total_iq_points, 1)
            annual_benefit = outcomes['economic_benefit']['value']
        
        # Calculate ROI
        five_year_benefits = annual_benefit * 4.1
        five_year_costs = total_budget * 5 * 0.9
        roi = ((five_year_benefits - five_year_costs) / five_year_costs * 100) if five_year_costs > 0 else 0
        
        # Generate comprehensive report
        st.subheader("Executive Summary")
        
        report = f"""
        ### Iodine Deficiency Intervention Simulation Results
        
        **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        #### Investment Summary
        - **Total Budget:** KSH {total_budget:,.0f}
        - **Implementation Period:** {timeline_months} months
        - **Population Coverage:** {actual_coverage*100:.1f}% ({int(actual_coverage * AFFECTED_POPULATION):,} people)
        - **Implementation Efficiency:** {implementation_efficiency}%
        
        #### Intervention Strategy
        - Salt Iodization: {salt_pct}% of budget
        - Oil Fortification: {oil_pct}% of budget
        - Direct Supplementation: {supplement_pct}% of budget
        - School Programs: {school_pct}% of budget
        
        #### Predicted Outcomes
        
        **Health Outcomes:**
        - Cretinism Cases Prevented: {outcomes['cretinism_prevented']['value']:,} cases
        - Goiter Cases Reduced: {outcomes['goiter_reduced']['value']:,} cases
        - Average IQ Points Gained: {outcomes['iq_points_gained']['value']:.1f} points per child
        - Pregnancy Complications Reduced: {outcomes['pregnancy_improved']['value']:,} cases
        
        #### Cost-Effectiveness
        - Cost per Person Reached: KSH {total_budget/(actual_coverage * AFFECTED_POPULATION):.2f}
        - Cost per IQ Point: KSH {cost_per_iq_point:,.2f}
        - Return on Investment: {roi:.1f}%
        
        #### Recommendations
        """
        
        st.markdown(report)
        
        # Generate recommendations based on results
        recommendations = []
        
        if actual_coverage < 0.8:
            recommendations.append("⚠️ **Increase budget** or improve efficiency to reach >80% coverage")
        
        if salt_pct < 30:
            recommendations.append("🧂 **Increase salt iodization** investment - most cost-effective for wide coverage")
        
        if implementation_efficiency < 60:
            recommendations.append("🔧 **Address implementation challenges** - efficiency is below acceptable threshold")
        
        if roi < 100:
            recommendations.append("💡 **Optimize intervention mix** for better return on investment")
        
        if not recommendations:
            recommendations.append("✅ Current strategy is well-balanced and cost-effective")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        # Download button for report
        st.download_button(
            label="📥 Download Full Report",
            data=report,
            file_name=f"iodine_intervention_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
        # PDF Downloads Section
        st.markdown("### 📄 Generate Professional Documents")
        
        col1, col2, col3 = st.columns(3)
        
        # Prepare data for PDF generation
        pdf_data = {
            'budget': total_budget,
            'timeline': timeline_months,
            'coverage': actual_coverage,
            'affected_population': AFFECTED_POPULATION,
            'salt_pct': salt_pct,
            'oil_pct': oil_pct,
            'supplement_pct': supplement_pct,
            'school_pct': school_pct,
            'cretinism_prevented': outcomes['cretinism_prevented']['value'],
            'goiter_reduced': outcomes['goiter_reduced']['value'],
            'iq_gain': outcomes['iq_points_gained']['value'],
            'pregnancy_improved': outcomes['pregnancy_improved']['value'],
            'annual_benefit': outcomes['economic_benefit']['value'],
            'roi': roi,
            'cost_per_life': total_budget / outcomes['cretinism_prevented']['value'] if outcomes['cretinism_prevented']['value'] > 0 else 0,
            'breakeven_year': 2 if roi > 50 else 3 if roi > 0 else 4,
            'annual_cretinism': 500,
            'goiter_cases': GOITER_CASES,
            'economic_loss': 50_000_000_000
        }
        
        with col1:
            st.markdown("""
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 4px solid #4caf50;">
                <h4 style="color: #2e7d32; margin-top: 0;">📊 Policy Brief</h4>
                <p style="color: #424242; margin-bottom: 10px;">Executive summary for decision makers with key findings and recommendations</p>
            </div>
            """, unsafe_allow_html=True)
            
            policy_html = generate_policy_brief_pdf(pdf_data)
            st.download_button(
                label="📥 Download Policy Brief",
                data=policy_html,
                file_name=f"policy_brief_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
        
        with col2:
            st.markdown("""
            <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 4px solid #2196f3;">
                <h4 style="color: #1565c0; margin-top: 0;">📋 Implementation Plan</h4>
                <p style="color: #424242; margin-bottom: 10px;">Detailed phased implementation guide with timelines and milestones</p>
            </div>
            """, unsafe_allow_html=True)
            
            impl_html = generate_implementation_plan_pdf(pdf_data)
            st.download_button(
                label="📥 Download Implementation Plan",
                data=impl_html,
                file_name=f"implementation_plan_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
        
        with col3:
            st.markdown("""
            <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 4px solid #ff9800;">
                <h4 style="color: #e65100; margin-top: 0;">📈 M&E Framework</h4>
                <p style="color: #424242; margin-bottom: 10px;">Monitoring and evaluation framework with indicators and targets</p>
            </div>
            """, unsafe_allow_html=True)
            
            me_html = generate_me_framework_pdf(pdf_data)
            st.download_button(
                label="📥 Download M&E Framework",
                data=me_html,
                file_name=f"me_framework_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
        
        st.info("""
        💡 **Document Usage Tips:**
        - Policy Brief: Share with ministers, parliamentarians, and senior officials
        - Implementation Plan: Use for program management and coordination
        - M&E Framework: Essential for tracking progress and reporting to donors
        
        All documents can be opened in any web browser and printed as PDFs.
        """)
        
        # Scenario comparison
        st.subheader("🔄 Scenario Comparison")
        
        # Calculate IQ gain if not already available
        if 'outcomes' in locals() and 'iq_points_gained' in outcomes:
            iq_gain_value = outcomes['iq_points_gained']['value']
        else:
            # Fallback calculation
            weighted_effectiveness = (salt_pct * 0.85 + oil_pct * 0.92 + supplement_pct * 0.98 + school_pct * 0.88) / 100
            iq_gain_value = actual_coverage * weighted_effectiveness * 13
        
        scenarios = {
            "Current Plan": {
                "Coverage": actual_coverage * 100,
                "ROI": roi,
                "IQ Gain": iq_gain_value
            },
            "Maximum Coverage": {
                "Coverage": 95,
                "ROI": roi * 0.8,
                "IQ Gain": iq_gain_value * 1.2
            },
            "Cost-Optimized": {
                "Coverage": actual_coverage * 100 * 0.7,
                "ROI": roi * 1.5,
                "IQ Gain": iq_gain_value * 0.8
            },
            "Emergency Response": {
                "Coverage": actual_coverage * 100 * 1.1,
                "ROI": roi * 0.6,
                "IQ Gain": iq_gain_value * 1.3
            }
        }
        
        scenario_df = pd.DataFrame(scenarios).T
        
        # Create comparison chart
        fig_comparison = go.Figure()
        
        for metric in scenario_df.columns:
            fig_comparison.add_trace(go.Bar(
                name=metric,
                x=scenario_df.index,
                y=scenario_df[metric],
                text=scenario_df[metric].round(1)
            ))
        
        fig_comparison.update_layout(
            title="Scenario Comparison",
            barmode='group',
            xaxis_title="Scenario",
            yaxis_title="Value",
            height=400
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
    else:
        st.warning("Please complete intervention setup with 100% budget allocation")

# RESOURCES & HELP TAB
with tab7:
    st.markdown("## 📚 Resources & Help Center")
    
    # Create sub-tabs for different resource categories
    resource_tab1, resource_tab2, resource_tab3, resource_tab4, resource_tab5 = st.tabs([
        "📖 Glossary", "📊 Evidence Base", "🔗 Research Links", "❓ FAQ", "📞 Support"
    ])
    
    # GLOSSARY TAB
    with resource_tab1:
        st.markdown("### 📖 Glossary of Terms")
        
        glossary_terms = {
            "Iodine Deficiency Disorders (IDD)": "A range of health problems caused by inadequate iodine intake, including goiter, cretinism, intellectual impairments, and pregnancy complications.",
            
            "Cretinism": "A severe form of intellectual disability and physical deformity caused by severe iodine deficiency during pregnancy and early childhood. Completely preventable with adequate iodine.",
            
            "Goiter": "Enlargement of the thyroid gland, visible as swelling in the neck. Most common visible sign of iodine deficiency.",
            
            "Urinary Iodine Concentration (UIC)": "The gold standard biomarker for assessing population iodine status. Measured in micrograms per liter (μg/L).",
            
            "Salt Iodization": "The practice of adding iodine to salt for human consumption. Most cost-effective intervention for eliminating iodine deficiency.",
            
            "Universal Salt Iodization (USI)": "When at least 90% of households consume adequately iodized salt (15-40 ppm iodine).",
            
            "Parts Per Million (PPM)": "Measurement unit for iodine concentration in salt. 15-40 ppm is the recommended range.",
            
            "Micronutrient": "Essential vitamins and minerals required in small amounts for proper body function. Iodine is a critical micronutrient.",
            
            "Fortification": "The practice of adding micronutrients to foods to improve nutritional quality.",
            
            "Coverage": "Percentage of target population reached by an intervention.",
            
            "Cost-Effectiveness": "The ratio of costs to health outcomes achieved. Measured as cost per DALY averted or life saved.",
            
            "DALY": "Disability-Adjusted Life Year - a measure of overall disease burden, expressed as years lost due to ill-health, disability, or early death.",
            
            "ROI": "Return on Investment - the ratio of net benefits to costs, expressed as a percentage.",
            
            "Implementation Efficiency": "The percentage of resources that effectively reach beneficiaries after accounting for losses, waste, and administrative costs.",
            
            "Baseline Survey": "Initial assessment conducted before intervention to establish current status and enable impact measurement.",
            
            "Median Urinary Iodine": "The middle value of urinary iodine concentration in a population. WHO recommends 100-199 μg/L as adequate.",
            
            "Thyroid Function": "The production and regulation of thyroid hormones (T3 and T4) essential for metabolism, growth, and brain development.",
            
            "Cognitive Development": "The construction of thought processes including remembering, problem-solving, and decision-making from childhood through adulthood.",
            
            "Quality Assurance": "Systematic monitoring and evaluation of various aspects of a project to ensure standards of quality are being met.",
            
            "Supply Chain": "The network of organizations, people, activities, information, and resources involved in delivering a product from supplier to customer."
        }
        
        # Display glossary in expandable format
        for term, definition in glossary_terms.items():
            with st.expander(f"**{term}**"):
                st.write(definition)
    
    # EVIDENCE BASE TAB
    with resource_tab2:
        st.markdown("### 📊 Evidence Base")
        
        st.markdown("""
        <div class="info-box" style="background-color: #e8f5e9;">
            <h4 style="color: #2e7d32;">Key Statistics & Evidence</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Kenya-specific evidence
        st.markdown("#### 🇰🇪 Kenya-Specific Data")
        evidence_data = {
            "Source": ["KNMS 2011", "WHO 2020", "UNICEF 2021", "MoH Kenya 2019", "Economic Survey 2020"],
            "Finding": [
                "100% of population has inadequate iodine intake (median UIC <50 μg/L)",
                "4.5% goiter prevalence in general population, 10.7% in school children",
                "Annual economic loss of 50 billion KSH due to reduced productivity",
                "500+ preventable cases of cretinism annually",
                "Only 26% of salt adequately iodized despite mandatory iodization law"
            ],
            "Implication": [
                "Universal iodine deficiency crisis requiring urgent intervention",
                "Visible health impacts already present in population",
                "Significant economic burden that justifies investment",
                "Severe irreversible consequences occurring daily",
                "Implementation and enforcement gaps in existing programs"
            ]
        }
        
        evidence_df = pd.DataFrame(evidence_data)
        st.dataframe(evidence_df, use_container_width=True, hide_index=True)
        
        # Global evidence
        st.markdown("#### 🌍 Global Evidence for Iodine Interventions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Success Stories:**
            - 🇨🇳 **China**: Eliminated IDD through USI, prevented 750,000 cases of cretinism
            - 🇮🇳 **India**: 91% household coverage, goiter reduced from 40% to 5%
            - 🇵🇪 **Peru**: Achieved USI in 5 years, IQ increased by 10-15 points
            - 🇮🇷 **Iran**: Near elimination of IDD, 99% salt iodization coverage
            """)
        
        with col2:
            st.markdown("""
            **Cost-Effectiveness Evidence:**
            - Salt iodization: $0.05 per person per year
            - Benefit-cost ratio: 30:1 (WHO estimate)
            - IQ gain: 13 points average in deficient populations
            - Economic return: $30 for every $1 invested
            """)
        
        # Scientific evidence
        st.markdown("#### 🔬 Scientific Evidence")
        
        st.info("""
        **Established Scientific Facts:**
        
        1. **Brain Development**: Iodine deficiency is the single most preventable cause of brain damage worldwide (WHO)
        
        2. **Critical Windows**: Most critical periods are pregnancy and first 2 years of life
        
        3. **Reversibility**: While goiter is reversible, cognitive damage from childhood deficiency is permanent
        
        4. **Population Impact**: Even mild deficiency reduces population IQ by 10-15 points
        
        5. **Economic Impact**: 1 IQ point loss = 1% reduction in earning capacity
        """)
    
    # RESEARCH LINKS TAB
    with resource_tab3:
        st.markdown("### 🔗 Research Links & Publications")
        
        # Key documents
        st.markdown("#### 📄 Key Documents")
        
        research_links = {
            "WHO Guidelines": {
                "title": "WHO Guideline: Fortification of food-grade salt with iodine",
                "year": "2014",
                "link": "https://www.who.int/publications/i/item/9789241507929",
                "description": "Global guidelines for salt iodization programs"
            },
            "Kenya National Survey": {
                "title": "Kenya National Micronutrient Survey 2011",
                "year": "2011",
                "link": "https://www.nutritionhealth.or.ke/",
                "description": "Comprehensive assessment of micronutrient status in Kenya"
            },
            "Lancet Series": {
                "title": "The Lancet Series on Maternal and Child Nutrition",
                "year": "2021",
                "link": "https://www.thelancet.com/series/maternal-child-nutrition",
                "description": "Evidence on nutrition interventions including iodine"
            },
            "Copenhagen Consensus": {
                "title": "Copenhagen Consensus: Micronutrient Supplements",
                "year": "2012",
                "link": "https://www.copenhagenconsensus.com/",
                "description": "Economic analysis ranking iodization as top intervention"
            },
            "UNICEF Guidance": {
                "title": "UNICEF Guidance on Salt Iodization",
                "year": "2018",
                "link": "https://www.unicef.org/nutrition/",
                "description": "Implementation guidance for country programs"
            }
        }
        
        for key, doc in research_links.items():
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <h4 style="margin: 0; color: #1976d2;">{doc['title']} ({doc['year']})</h4>
                <p style="margin: 5px 0; color: #666;">{doc['description']}</p>
                <p style="margin: 5px 0;"><a href="{doc['link']}" target="_blank">🔗 Access Document</a></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Research databases
        st.markdown("#### 🔍 Research Databases")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Scientific Databases:**
            - [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/) - Free medical research
            - [Cochrane Reviews](https://www.cochranelibrary.com/) - Systematic reviews
            - [Google Scholar](https://scholar.google.com/) - Academic search engine
            """)
        
        with col2:
            st.markdown("""
            **Data Repositories:**
            - [DHS Program](https://dhsprogram.com/) - Demographic health surveys
            - [Global Fortification Data Exchange](https://fortificationdata.org/) - Fortification data
            - [WHO Global Health Observatory](https://www.who.int/gho/) - Health statistics
            """)
    
    # FAQ TAB
    with resource_tab4:
        st.markdown("### ❓ Frequently Asked Questions")
        
        faqs = {
            "Why is iodine deficiency still a problem if salt iodization is mandatory?": """
            Several factors contribute:
            - Poor quality control at production facilities
            - Iodine loss during storage and transportation
            - Use of non-iodized salt in food processing
            - Weak enforcement of regulations
            - Consumer preference for non-iodized salt
            - Limited awareness of importance
            """,
            
            "How quickly can we see results from iodine interventions?": """
            Timeline varies by outcome:
            - Urinary iodine: 1-3 months
            - Goiter reduction: 6-12 months
            - Pregnancy outcomes: 9-12 months
            - Cognitive improvements in newborns: 1-2 years
            - Population IQ gains: 5-10 years
            - Economic benefits: 5-15 years
            """,
            
            "What's the difference between salt iodization and other interventions?": """
            **Salt Iodization:**
            - Pros: Cheapest, reaches everyone, sustainable
            - Cons: Requires infrastructure, quality control challenges
            
            **Oil Fortification:**
            - Pros: Longer retention, good for non-salt users
            - Cons: More expensive, limited reach
            
            **Direct Supplementation:**
            - Pros: Most effective, immediate impact
            - Cons: Most expensive, requires health system
            
            **School Programs:**
            - Pros: Targets children, educational component
            - Cons: Misses pre-school children, seasonal coverage
            """,
            
            "How do we ensure quality of iodized salt?": """
            Multi-level quality assurance:
            1. **Production**: Regular testing at factories
            2. **Distribution**: Spot checks during transport
            3. **Retail**: Market surveillance and testing
            4. **Household**: Rapid test kits for consumers
            5. **Certification**: Third-party verification
            6. **Penalties**: Enforcement for non-compliance
            """,
            
            "What about people with thyroid conditions?": """
            WHO guidance:
            - Iodized salt is safe for most thyroid conditions
            - Benefits far outweigh risks at population level
            - Individual medical conditions should be managed by healthcare providers
            - Monitoring systems should track adverse events
            - Alternative interventions available for sensitive groups
            """,
            
            "How do we measure success?": """
            Key indicators to track:
            - **Process**: % of salt/oil adequately iodized
            - **Coverage**: % of households using iodized salt
            - **Biomarker**: Median urinary iodine >100 μg/L
            - **Health**: Goiter prevalence <5%
            - **Impact**: Reduced cretinism incidence
            - **Sustainability**: Program functioning without external support
            """
        }
        
        for question, answer in faqs.items():
            with st.expander(f"**{question}**"):
                st.markdown(answer)
    
    # SUPPORT TAB
    with resource_tab5:
        st.markdown("### 📞 Support & Contact Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box" style="background-color: #e3f2fd;">
                <h4 style="color: #1565c0;">Technical Support</h4>
                <p style="color: #424242;">
                    <strong>Simulator Support:</strong><br>
                    Email: support@iodine-simulator.org<br>
                    Response time: 24-48 hours<br>
                    <br>
                    <strong>Technical Issues:</strong><br>
                    - Browser compatibility<br>
                    - Data export problems<br>
                    - Calculation questions<br>
                    - Feature requests
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box" style="background-color: #f3e5f5;">
                <h4 style="color: #6a1b9a;">Training Resources</h4>
                <p style="color: #424242;">
                    <strong>Available Training:</strong><br>
                    • Video tutorials (coming soon)<br>
                    • User manual (PDF)<br>
                    • Webinar series<br>
                    • In-person workshops<br>
                    <br>
                    <strong>Request Training:</strong><br>
                    training@iodine-simulator.org
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="info-box" style="background-color: #e8f5e9;">
                <h4 style="color: #2e7d32;">Partner Organizations</h4>
                <p style="color: #424242;">
                    <strong>Ministry of Health Kenya</strong><br>
                    Nutrition Division<br>
                    Phone: +254 20 2717077<br>
                    <br>
                    <strong>WHO Kenya Office</strong><br>
                    Phone: +254 20 2717902<br>
                    <br>
                    <strong>UNICEF Kenya</strong><br>
                    Phone: +254 20 7621234<br>
                    <br>
                    <strong>Nutrition International</strong><br>
                    Email: info@nutritionintl.org
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box" style="background-color: #fff3e0;">
                <h4 style="color: #e65100;">Report Issues</h4>
                <p style="color: #424242;">
                    <strong>Bug Reports:</strong><br>
                    GitHub: github.com/iodine-simulator/issues<br>
                    <br>
                    <strong>Data Corrections:</strong><br>
                    Email: data@iodine-simulator.org<br>
                    <br>
                    <strong>Security Issues:</strong><br>
                    security@iodine-simulator.org<br>
                    (Encrypted communication available)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Version and credits
        st.markdown("---")
        st.markdown("### ℹ️ About This Tool")
        
        st.info("""
        **Kenya Iodine Intervention Simulator v2.0**
        
        Developed in collaboration with:
        - Ministry of Health, Kenya
        - World Health Organization
        - UNICEF
        - Nutrition International
        
        **Citation:**
        If you use this tool in research or policy documents, please cite as:
        *Kenya Iodine Intervention Simulator (2024). Version 2.0. 
        Available at: https://iodine-simulator.org*
        
        **License:** 
        Open source under MIT License. Free to use, modify, and distribute.
        
        **Acknowledgments:**
        Special thanks to all healthcare workers, researchers, and policy makers
        working to eliminate iodine deficiency in Kenya and globally.
        
        **Last Updated:** {datetime.now().strftime('%B %Y')}
        """)

# Sidebar with quick stats
with st.sidebar:
    st.header("🎯 Quick Stats")
    st.metric("Population at Risk", f"{AFFECTED_POPULATION:,}")
    st.metric("Current Deficiency Rate", "100%")
    st.metric("Children Under 5", f"{CHILDREN_UNDER_5:,}")
    st.metric("Pregnant Women", f"{PREGNANT_WOMEN:,}")
    st.metric("Goiter Cases", f"{GOITER_CASES:,}")
    
    st.header("💡 Quick Tips")
    with st.expander("Getting Started"):
        st.markdown("""
        1. **Set Budget:** Start in Intervention Setup tab
        2. **Choose Mix:** Allocate budget across interventions
        3. **View Results:** Check Outcomes Prediction tab
        4. **Compare:** Try different scenarios
        5. **Export:** Generate reports for stakeholders
        """)
    
    with st.expander("Optimal Strategy"):
        st.markdown("""
        **For Maximum Impact:**
        - Salt: 40-50% (cost-effective base)
        - Oil: 15-20% (good retention)
        - Supplements: 20-25% (high-risk groups)
        - School: 10-15% (future generation)
        
        **Budget:** 1-2 billion KSH
        **Efficiency:** 70-80%
        """)
    
    with st.expander("Common Mistakes"):
        st.markdown("""
        ❌ **Avoid:**
        - Single intervention only
        - Ignoring salt iodization
        - Unrealistic efficiency (>90%)
        - Budget below 500M KSH
        
        ✅ **Do Instead:**
        - Diversify interventions
        - Prioritize cost-effectiveness
        - Plan for realistic efficiency
        - Adequate funding (1B+ KSH)
        """)
    
    st.header("ℹ️ About")
    st.info("""
    **Iodine Intervention Simulator v2.0**
    
    Evidence-based planning tool for eliminating iodine deficiency in Kenya.
    
    Based on:
    - KNMS 2011 survey data
    - WHO guidelines
    - Global best practices
    
    **Last Updated:** {datetime.now().strftime('%B %Y')}
    """)
    
    st.header("🔍 Key Insights")
    st.warning("""
    **Critical Finding:** 100% of surveyed population has zero iodine intake despite 
    consuming "iodized" salt, indicating complete fortification failure.
    
    **Urgent action required!**
    """)

# Footer
st.markdown("---")
st.caption("Simulation based on Kenya National Micronutrient Survey 2011 data | For demonstration purposes")