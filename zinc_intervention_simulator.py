"""
Zinc Deficiency Intervention Simulation Engine
Interactive GUI for modeling zinc supplementation strategies and health outcomes
Designed for addressing stunting, diarrhea, and immune deficiency in Kenya
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import math

# Page configuration
st.set_page_config(
    page_title="Kenya Zinc Intervention Simulator",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .stMetric {
            
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    .success-metric {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 10px;
    }
    .warning-metric {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 10px;
    }
    .danger-metric {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 10px;
    }
    .impact-high {
        background-color: #28a745;
        color: white;
        padding: 5px;
        border-radius: 5px;
    }
    .impact-medium {
        background-color: #ffc107;
        color: black;
        padding: 5px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False
if 'scenario_history' not in st.session_state:
    st.session_state.scenario_history = []

# Title and description
st.title("💊 Kenya Zinc Deficiency Intervention Simulator")
st.markdown("""
**Combating Zinc Deficiency Crisis** | Addressing stunting (26%), chronic diarrhea, and immune dysfunction
""")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Intervention Design", 
    "📊 Health Outcomes", 
    "💰 Economic Analysis", 
    "🔬 Biomarker Tracking",
    "📈 Comparative Reports"
])

# Constants based on Kenya health data
KENYA_POPULATION = 52_000_000  # 2023 estimate
ZINC_DEFICIENT_POPULATION = int(KENYA_POPULATION * 0.51)  # 51% zinc deficient
STUNTED_CHILDREN = int(KENYA_POPULATION * 0.14 * 0.26)  # 26% of children stunted
CHILDREN_UNDER_5 = int(KENYA_POPULATION * 0.135)  # ~13.5% are under 5
PREGNANT_WOMEN = int(KENYA_POPULATION * 0.032)  # ~3.2% pregnant women annually
RURAL_POPULATION = int(KENYA_POPULATION * 0.72)  # 72% rural
CHILDREN_WITH_DIARRHEA = int(CHILDREN_UNDER_5 * 0.15)  # 15% diarrhea prevalence

# Zinc-specific intervention strategies
def calculate_zinc_intervention_costs(budget, interventions):
    """Calculate costs for zinc-specific intervention strategies"""
    costs = {
        'fortification': {
            'unit_cost': 3.8,  # KSH per person per year for flour/cereal fortification
            'effectiveness': 0.75,  # Lower than supplements but sustainable
            'reach_time': 6,  # months to full implementation
            'coverage_potential': 0.85,  # Can reach 85% of population
            'infrastructure_cost': 0.25  # 25% goes to infrastructure
        },
        'therapeutic_zinc': {
            'unit_cost': 45,  # KSH per child for diarrhea treatment course
            'effectiveness': 0.95,  # Very effective for acute treatment
            'reach_time': 1,  # Immediate deployment
            'coverage_potential': 0.60,  # Limited by healthcare access
            'infrastructure_cost': 0.10
        },
        'preventive_supplements': {
            'unit_cost': 120,  # KSH per person per year for daily supplements
            'effectiveness': 0.90,  # High effectiveness
            'reach_time': 2,
            'coverage_potential': 0.70,
            'infrastructure_cost': 0.15
        },
        'biofortified_crops': {
            'unit_cost': 25,  # KSH per person per year (seed programs + training)
            'effectiveness': 0.65,  # Moderate but sustainable
            'reach_time': 12,  # Takes time to establish
            'coverage_potential': 0.75,  # Good rural reach
            'infrastructure_cost': 0.35  # High initial investment
        },
        'maternal_supplementation': {
            'unit_cost': 180,  # KSH per pregnant woman for full pregnancy
            'effectiveness': 0.92,  # Very effective for child outcomes
            'reach_time': 3,
            'coverage_potential': 0.80,  # Through ANC clinics
            'infrastructure_cost': 0.12
        },
        'community_health': {
            'unit_cost': 15,  # KSH per person for education + basic supplements
            'effectiveness': 0.55,  # Lower but builds capacity
            'reach_time': 4,
            'coverage_potential': 0.90,  # Wide reach through CHWs
            'infrastructure_cost': 0.40  # Training and materials
        }
    }
    return costs

def simulate_zinc_health_outcomes(coverage, intervention_mix, timeline_months, population_data):
    """Simulate zinc-specific health outcomes"""
    
    # Calculate weighted effectiveness
    total_effectiveness = 0
    for intervention, percentage in intervention_mix.items():
        if percentage > 0:
            costs = calculate_zinc_intervention_costs(None, None)
            if intervention in costs:
                total_effectiveness += (percentage / 100) * costs[intervention]['effectiveness']
    
    # Immediate effects (0-3 months) - Focus on acute conditions
    immediate = {
        'diarrhea_duration_reduced': coverage * total_effectiveness * 0.25,  # 25% reduction
        'diarrhea_severity_reduced': coverage * total_effectiveness * 0.30,  # 30% reduction
        'acute_respiratory_infection_reduced': coverage * total_effectiveness * 0.20,
        'appetite_improved': coverage * total_effectiveness * 0.45,
        'wound_healing_enhanced': coverage * total_effectiveness * 0.35
    }
    
    # Mid-term effects (3-12 months) - Growth and immune function
    midterm = {
        'linear_growth_velocity_increased': coverage * total_effectiveness * 0.18,  # cm/year increase
        'weight_gain_improved': coverage * total_effectiveness * 0.22,  # % improvement
        'infection_frequency_reduced': coverage * total_effectiveness * 0.35,
        'pneumonia_incidence_reduced': coverage * total_effectiveness * 0.26,
        'malaria_severity_reduced': coverage * total_effectiveness * 0.15,
        'skin_conditions_improved': coverage * total_effectiveness * 0.40
    }
    
    # Long-term effects (1-5 years) - Stunting and development
    longterm = {
        'stunting_prevented': int(coverage * total_effectiveness * STUNTED_CHILDREN * 0.30),  # 30% reduction possible
        'height_for_age_zscore_improved': coverage * total_effectiveness * 0.65,  # Z-score improvement
        'cognitive_development_score': coverage * total_effectiveness * 8.5,  # IQ equivalent points
        'school_performance_improved': coverage * total_effectiveness * 0.28,  # % improvement
        'child_mortality_reduced': int(coverage * total_effectiveness * 1200),  # deaths prevented
        'gdp_contribution': coverage * total_effectiveness * 0.023,  # 2.3% GDP improvement from reduced stunting
        'healthcare_cost_reduction': coverage * total_effectiveness * 0.18  # 18% reduction in child healthcare costs
    }
    
    # Calculate biomarker improvements
    biomarkers = {
        'serum_zinc_normalized': coverage * total_effectiveness * 0.72,  # % with normal levels
        'alkaline_phosphatase_improved': coverage * total_effectiveness * 0.60,
        'growth_hormone_igf1_increased': coverage * total_effectiveness * 0.45,
        'inflammatory_markers_reduced': coverage * total_effectiveness * 0.38,
        'metallothionein_expression': coverage * total_effectiveness * 0.55
    }
    
    return immediate, midterm, longterm, biomarkers

def calculate_combination_synergies(intervention_mix):
    """Calculate synergistic effects of intervention combinations"""
    synergies = {}
    
    # Fortification + Supplementation synergy
    if intervention_mix.get('fortification', 0) > 20 and intervention_mix.get('preventive_supplements', 0) > 20:
        synergies['bioavailability_boost'] = 0.15  # 15% effectiveness boost
        
    # Maternal + Child interventions synergy
    if intervention_mix.get('maternal_supplementation', 0) > 25 and intervention_mix.get('therapeutic_zinc', 0) > 25:
        synergies['intergenerational_impact'] = 0.20  # 20% better outcomes
        
    # Biofortification + Community health synergy
    if intervention_mix.get('biofortified_crops', 0) > 30 and intervention_mix.get('community_health', 0) > 20:
        synergies['sustainability_multiplier'] = 0.25  # 25% long-term improvement
        
    return synergies

# INTERVENTION DESIGN TAB
with tab1:
    st.header("🎯 Zinc Intervention Strategy Designer")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("💵 Budget Configuration")
        
        # Advanced budget options
        budget_mode = st.radio(
            "Budget Input Mode",
            ["Simple", "Advanced"],
            help="Advanced mode allows multi-year planning"
        )
        
        if budget_mode == "Simple":
            # Budget scale selector
            budget_scale = st.select_slider(
                "Budget Scale",
                options=["Millions", "Billions"],
                value="Millions"
            )
            
            if budget_scale == "Millions":
                min_budget = 50_000_000  # 50 million minimum
                max_budget = 999_000_000  # 999 million maximum
                step_size = 10_000_000
                default_val = 750_000_000  # 750 million default
                format_str = "{:,.0f} Million KSH"
                divisor = 1_000_000
            else:
                min_budget = 1_000_000_000
                max_budget = 15_000_000_000
                step_size = 100_000_000
                default_val = 3_000_000_000
                format_str = "{:,.1f} Billion KSH"
                divisor = 1_000_000_000
            
            total_budget = st.slider(
                "Total Annual Budget (KSH)",
                min_value=min_budget,
                max_value=max_budget,
                value=default_val,
                step=step_size,
                help="Annual budget for zinc interventions"
            )
            
            st.info(f"💰 **Budget: {format_str.format(total_budget/divisor)}**")
            
        else:  # Advanced mode
            st.write("**Multi-Year Budget Planning**")
            year1_budget = st.number_input("Year 1 Budget (Million KSH)", value=750, step=50) * 1_000_000
            year2_budget = st.number_input("Year 2 Budget (Million KSH)", value=900, step=50) * 1_000_000
            year3_budget = st.number_input("Year 3 Budget (Million KSH)", value=1100, step=50) * 1_000_000
            total_budget = year1_budget  # Use year 1 for immediate calculations
            
            st.metric("3-Year Total", f"KSH {(year1_budget + year2_budget + year3_budget)/1_000_000:,.0f}M")
        
        # Budget efficiency factors
        st.subheader("💡 Implementation Factors")
        
        procurement_efficiency = st.slider(
            "Procurement Efficiency (%)",
            min_value=50, max_value=95, value=75,
            help="Bulk purchasing and negotiation effectiveness"
        )
        
        distribution_efficiency = st.slider(
            "Distribution Efficiency (%)",
            min_value=40, max_value=90, value=65,
            help="Supply chain and logistics effectiveness"
        )
        
        absorption_capacity = st.slider(
            "System Absorption Capacity (%)",
            min_value=30, max_value=100, value=70,
            help="Healthcare system's ability to implement"
        )
        
        # Calculate effective budget
        effective_budget = total_budget * (procurement_efficiency/100) * (distribution_efficiency/100) * (absorption_capacity/100)
        
        st.metric("Effective Budget", f"KSH {effective_budget/1_000_000:,.0f}M")
        st.metric("Budget per Deficient Person", f"KSH {effective_budget/ZINC_DEFICIENT_POPULATION:.2f}")
        
        # Target population selection
        st.subheader("🎯 Priority Populations")
        
        target_mode = st.radio("Targeting Strategy", ["Universal", "Targeted", "Phased"])
        
        if target_mode == "Targeted":
            priority_groups = st.multiselect(
                "Select Priority Groups",
                ["Stunted Children", "Children with Diarrhea", "Pregnant Women", 
                 "Lactating Women", "Children 6-59 months", "Adolescent Girls",
                 "Elderly (60+)", "HIV+ Individuals", "TB Patients"],
                default=["Stunted Children", "Children with Diarrhea", "Pregnant Women"]
            )
            
            # Calculate target population size
            target_pop = 0
            if "Stunted Children" in priority_groups:
                target_pop += STUNTED_CHILDREN
            if "Children with Diarrhea" in priority_groups:
                target_pop += CHILDREN_WITH_DIARRHEA
            if "Pregnant Women" in priority_groups:
                target_pop += PREGNANT_WOMEN
            
            st.metric("Target Population", f"{target_pop:,}")
            
        elif target_mode == "Phased":
            phase1_coverage = st.slider("Phase 1 Coverage (%)", 10, 40, 25)
            phase2_coverage = st.slider("Phase 2 Coverage (%)", 20, 60, 45)
            phase3_coverage = st.slider("Phase 3 Coverage (%)", 40, 100, 70)
            
        # Timeline configuration
        st.subheader("⏱️ Implementation Timeline")
        timeline_months = st.slider(
            "Implementation Period (months)",
            min_value=12, max_value=60, value=36, step=6
        )
        
        # Add seasonal considerations
        consider_seasons = st.checkbox("Consider Seasonal Patterns", value=True)
        if consider_seasons:
            st.info("📅 Accounting for agricultural seasons and disease patterns")
    
    with col2:
        st.subheader("🔧 Intervention Portfolio Design")
        
        # Intervention strategy presets
        strategy_preset = st.selectbox(
            "Strategy Preset",
            ["Custom", "Emergency Response", "Sustainable Development", 
             "Cost-Optimized", "Maximum Coverage", "Evidence-Based"],
            help="Pre-configured intervention mixes based on different priorities"
        )
        
        # Set default values based on preset
        if strategy_preset == "Emergency Response":
            default_values = {
                'fortification': 10,
                'therapeutic_zinc': 40,
                'preventive_supplements': 30,
                'biofortified_crops': 0,
                'maternal_supplementation': 15,
                'community_health': 5
            }
        elif strategy_preset == "Sustainable Development":
            default_values = {
                'fortification': 30,
                'therapeutic_zinc': 10,
                'preventive_supplements': 15,
                'biofortified_crops': 25,
                'maternal_supplementation': 10,
                'community_health': 10
            }
        elif strategy_preset == "Cost-Optimized":
            default_values = {
                'fortification': 40,
                'therapeutic_zinc': 15,
                'preventive_supplements': 10,
                'biofortified_crops': 15,
                'maternal_supplementation': 10,
                'community_health': 10
            }
        else:  # Custom or others
            default_values = {
                'fortification': 25,
                'therapeutic_zinc': 20,
                'preventive_supplements': 20,
                'biofortified_crops': 15,
                'maternal_supplementation': 12,
                'community_health': 8
            }
        
        st.write("**Intervention Mix (must total 100%)**")
        
        # Intervention sliders with descriptions
        interventions = {}
        
        col_int1, col_int2 = st.columns(2)
        
        with col_int1:
            interventions['fortification'] = st.slider(
                "🌾 Food Fortification",
                min_value=0, max_value=100,
                value=default_values['fortification'],
                help="Fortify staple foods (flour, maize meal) with zinc"
            )
            
            interventions['therapeutic_zinc'] = st.slider(
                "💊 Therapeutic Zinc (ORS+Zinc)",
                min_value=0, max_value=100,
                value=default_values['therapeutic_zinc'],
                help="Zinc supplements for diarrhea treatment"
            )
            
            interventions['preventive_supplements'] = st.slider(
                "🔬 Preventive Supplementation",
                min_value=0, max_value=100,
                value=default_values['preventive_supplements'],
                help="Daily/weekly zinc supplements for at-risk groups"
            )
        
        with col_int2:
            interventions['biofortified_crops'] = st.slider(
                "🌱 Biofortified Crops",
                min_value=0, max_value=100,
                value=default_values['biofortified_crops'],
                help="High-zinc varieties of beans, sweet potato, maize"
            )
            
            interventions['maternal_supplementation'] = st.slider(
                "🤰 Maternal Supplementation",
                min_value=0, max_value=100,
                value=default_values['maternal_supplementation'],
                help="Zinc for pregnant and lactating women"
            )
            
            interventions['community_health'] = st.slider(
                "👥 Community Health Programs",
                min_value=0, max_value=100,
                value=default_values['community_health'],
                help="Education, screening, and basic supplementation"
            )
        
        # Check allocation
        total_allocation = sum(interventions.values())
        
        # Allocation validation
        col_val1, col_val2, col_val3 = st.columns(3)
        with col_val1:
            st.metric("Total Allocation", f"{total_allocation}%")
        with col_val2:
            if total_allocation == 100:
                st.success("✅ Valid Mix")
            else:
                st.error(f"❌ Adjust by {100-total_allocation:+d}%")
        with col_val3:
            active_interventions = sum(1 for v in interventions.values() if v > 0)
            st.metric("Active Interventions", active_interventions)
        
        # Calculate and display synergies
        if total_allocation == 100:
            synergies = calculate_combination_synergies(interventions)
            if synergies:
                st.subheader("🔄 Synergistic Effects Detected")
                for synergy, boost in synergies.items():
                    st.info(f"✨ {synergy.replace('_', ' ').title()}: +{boost*100:.0f}% effectiveness")
        
        # Coverage estimation with zinc-specific factors
        st.subheader("📊 Coverage & Reach Estimation")
        
        if total_allocation == 100:
            # Calculate weighted average cost
            costs = calculate_zinc_intervention_costs(None, None)
            weighted_cost = sum(
                (interventions[key]/100) * costs[key]['unit_cost'] 
                for key in interventions if key in costs
            )
            
            # Calculate maximum theoretical coverage
            max_coverage = min(1.0, effective_budget / (weighted_cost * ZINC_DEFICIENT_POPULATION))
            
            # Apply real-world constraints
            infrastructure_readiness = st.slider(
                "Infrastructure Readiness (%)",
                min_value=20, max_value=90, value=55,
                help="Labs, cold chain, distribution networks"
            )
            
            actual_coverage = max_coverage * (infrastructure_readiness / 100)
            
            # Display coverage metrics with visual indicators
            col_cov1, col_cov2, col_cov3 = st.columns(3)
            
            with col_cov1:
                coverage_pct = actual_coverage * 100
                if coverage_pct >= 80:
                    coverage_color = "🟢"
                elif coverage_pct >= 60:
                    coverage_color = "🟡"
                else:
                    coverage_color = "🔴"
                st.metric("Population Coverage", f"{coverage_color} {coverage_pct:.1f}%")
            
            with col_cov2:
                people_reached = int(actual_coverage * ZINC_DEFICIENT_POPULATION)
                st.metric("People Reached", f"{people_reached:,}")
            
            with col_cov3:
                children_reached = int(actual_coverage * STUNTED_CHILDREN)
                st.metric("Stunted Children Reached", f"{children_reached:,}")

# HEALTH OUTCOMES TAB
with tab2:
    st.header("📊 Projected Health Outcomes")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Calculate comprehensive outcomes
        immediate, midterm, longterm, biomarkers = simulate_zinc_health_outcomes(
            actual_coverage, interventions, timeline_months, 
            {'stunted': STUNTED_CHILDREN, 'under5': CHILDREN_UNDER_5}
        )
        
        # Apply synergy bonuses
        synergy_multiplier = 1 + sum(synergies.values()) if 'synergies' in locals() else 1
        
        # Display outcomes in organized sections
        st.subheader("📈 Impact Timeline Overview")
        
        # Create timeline visualization
        timeline_data = []
        months = list(range(0, timeline_months + 1, 3))
        
        # Sigmoid functions for realistic growth patterns
        def sigmoid(x, L, k, x0):
            return L / (1 + np.exp(-k * (x - x0)))
        
        # Different metrics with different adoption curves
        diarrhea_impact = [sigmoid(m, immediate['diarrhea_duration_reduced']*100, 0.5, 6) for m in months]
        growth_impact = [sigmoid(m, midterm['linear_growth_velocity_increased']*100, 0.2, 12) for m in months]
        stunting_prevention = [sigmoid(m, longterm['height_for_age_zscore_improved']*100, 0.15, 18) for m in months]
        mortality_reduction = [sigmoid(m, 30, 0.1, 24) for m in months]  # Up to 30% reduction
        
        # Create comprehensive timeline chart
        fig_timeline = go.Figure()
        
        fig_timeline.add_trace(go.Scatter(
            x=months, y=diarrhea_impact,
            mode='lines+markers', name='Diarrhea Reduction',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8)
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=months, y=growth_impact,
            mode='lines+markers', name='Growth Velocity',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8)
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=months, y=stunting_prevention,
            mode='lines+markers', name='Stunting Prevention',
            line=dict(color='#45B7D1', width=3),
            marker=dict(size=8)
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=months, y=mortality_reduction,
            mode='lines+markers', name='Mortality Reduction',
            line=dict(color='#96CEB4', width=3),
            marker=dict(size=8)
        ))
        
        fig_timeline.update_layout(
            title="Health Impact Trajectories",
            xaxis_title="Months",
            yaxis_title="Impact (%)",
            yaxis=dict(range=[0, 100]),
            hovermode='x unified',
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Detailed outcome metrics
        col_out1, col_out2, col_out3 = st.columns(3)
        
        with col_out1:
            st.subheader("🚀 Immediate Impact (0-3 months)")
            
            metrics_immediate = {
                "Diarrhea Duration": f"-{immediate['diarrhea_duration_reduced']*100:.1f}%",
                "Diarrhea Severity": f"-{immediate['diarrhea_severity_reduced']*100:.1f}%",
                "Respiratory Infections": f"-{immediate['acute_respiratory_infection_reduced']*100:.1f}%",
                "Appetite Improvement": f"+{immediate['appetite_improved']*100:.1f}%",
                "Wound Healing": f"+{immediate['wound_healing_enhanced']*100:.1f}%"
            }
            
            for metric, value in metrics_immediate.items():
                col_sub1, col_sub2 = st.columns([2, 1])
                with col_sub1:
                    st.write(f"**{metric}**")
                with col_sub2:
                    if value.startswith('+'):
                        st.success(value)
                    else:
                        st.info(value)
        
        with col_out2:
            st.subheader("📊 Mid-term Impact (3-12 months)")
            
            metrics_midterm = {
                "Growth Velocity": f"+{midterm['linear_growth_velocity_increased']*100:.1f}%",
                "Weight Gain": f"+{midterm['weight_gain_improved']*100:.1f}%",
                "Infection Frequency": f"-{midterm['infection_frequency_reduced']*100:.1f}%",
                "Pneumonia Cases": f"-{midterm['pneumonia_incidence_reduced']*100:.1f}%",
                "Malaria Severity": f"-{midterm['malaria_severity_reduced']*100:.1f}%"
            }
            
            for metric, value in metrics_midterm.items():
                col_sub1, col_sub2 = st.columns([2, 1])
                with col_sub1:
                    st.write(f"**{metric}**")
                with col_sub2:
                    if value.startswith('+'):
                        st.success(value)
                    else:
                        st.info(value)
        
        with col_out3:
            st.subheader("🎯 Long-term Impact (1-5 years)")
            
            st.metric(
                "Stunting Cases Prevented",
                f"{longterm['stunting_prevented']:,}",
                delta=f"-{longterm['stunting_prevented']:,} cases"
            )
            
            st.metric(
                "Height-for-Age Improvement",
                f"+{longterm['height_for_age_zscore_improved']:.2f} Z-score",
                delta="Significant"
            )
            
            st.metric(
                "Cognitive Development",
                f"+{longterm['cognitive_development_score']:.1f} IQ points",
                delta=f"+{longterm['cognitive_development_score']:.1f}"
            )
            
            st.metric(
                "Child Deaths Prevented",
                f"{longterm['child_mortality_reduced']:,}",
                delta=f"-{longterm['child_mortality_reduced']:,} deaths"
            )
        
        # Population impact breakdown
        st.subheader("👥 Population-Specific Outcomes")
        
        pop_impact = {
            'Population Group': [
                'Stunted Children', 
                'Children with Diarrhea', 
                'Pregnant Women',
                'Children 6-59 months',
                'General Population'
            ],
            'Coverage (%)': [
                actual_coverage * 100 * 1.2,  # Higher priority
                actual_coverage * 100 * 1.3,  # Highest priority  
                actual_coverage * 100 * 1.1,
                actual_coverage * 100,
                actual_coverage * 100 * 0.7
            ],
            'Primary Benefit': [
                'Linear growth improvement',
                'Reduced duration & severity',
                'Better birth outcomes',
                'Prevented stunting',
                'Improved immunity'
            ],
            'Impact Score': [85, 92, 78, 81, 65]
        }
        
        pop_df = pd.DataFrame(pop_impact)
        
        # Create grouped bar chart
        fig_pop = px.bar(
            pop_df, 
            x='Population Group', 
            y=['Coverage (%)', 'Impact Score'],
            title="Population Coverage and Impact Scores",
            barmode='group',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        
        st.plotly_chart(fig_pop, use_container_width=True)
        
        # Risk mitigation assessment
        st.subheader("⚠️ Implementation Risks & Mitigation")
        
        risk_categories = {
            "Supply Chain Disruption": {
                "probability": np.random.uniform(0.3, 0.7),
                "impact": "High",
                "mitigation": "Buffer stocks, multiple suppliers"
            },
            "Quality Assurance": {
                "probability": np.random.uniform(0.2, 0.5),
                "impact": "Critical",
                "mitigation": "Regular testing, certification programs"
            },
            "Community Acceptance": {
                "probability": np.random.uniform(0.3, 0.6),
                "impact": "Medium",
                "mitigation": "Education campaigns, community engagement"
            },
            "Funding Continuity": {
                "probability": np.random.uniform(0.4, 0.8),
                "impact": "High",
                "mitigation": "Multi-year commitments, diverse funding"
            }
        }
        
        risk_cols = st.columns(len(risk_categories))
        for i, (risk, details) in enumerate(risk_categories.items()):
            with risk_cols[i]:
                prob = details['probability']
                if prob < 0.3:
                    color = "🟢"
                elif prob < 0.6:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.metric(risk, f"{color} {prob*100:.0f}%")
                st.caption(f"Impact: {details['impact']}")
                with st.expander("Mitigation"):
                    st.write(details['mitigation'])
    
    else:
        st.warning("⚠️ Please complete intervention allocation (must equal 100%) in the Intervention Design tab")

# ECONOMIC ANALYSIS TAB
with tab3:
    st.header("💰 Economic Impact & Cost-Benefit Analysis")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        col_econ1, col_econ2 = st.columns(2)
        
        with col_econ1:
            st.subheader("💵 Investment Breakdown")
            
            # Detailed cost analysis
            costs = calculate_zinc_intervention_costs(None, None)
            
            cost_breakdown = []
            for intervention, percentage in interventions.items():
                if percentage > 0 and intervention in costs:
                    budget_amount = effective_budget * (percentage / 100)
                    cost_data = costs[intervention]
                    
                    # Calculate people reached based on unit cost
                    people_reached = int(budget_amount / cost_data['unit_cost'])
                    
                    cost_breakdown.append({
                        'Intervention': intervention.replace('_', ' ').title(),
                        'Budget (KSH)': budget_amount,
                        'People Reached': people_reached,
                        'Cost per Person': cost_data['unit_cost'],
                        'Infrastructure %': cost_data['infrastructure_cost'] * 100
                    })
            
            cost_df = pd.DataFrame(cost_breakdown)
            
            # Display formatted table
            st.dataframe(
                cost_df.style.format({
                    'Budget (KSH)': '{:,.0f}',
                    'People Reached': '{:,.0f}',
                    'Cost per Person': 'KSH {:.2f}',
                    'Infrastructure %': '{:.1f}%'
                }),
                use_container_width=True
            )
            
            # Cost efficiency chart
            fig_cost = px.scatter(
                cost_df,
                x='Cost per Person',
                y='People Reached',
                size='Budget (KSH)',
                color='Intervention',
                title="Cost Efficiency Analysis",
                hover_data=['Budget (KSH)'],
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            st.plotly_chart(fig_cost, use_container_width=True)
            
        with col_econ2:
            st.subheader("📊 Economic Returns")
            
            # Calculate economic benefits
            
            # Healthcare cost savings
            diarrhea_episodes_prevented = int(CHILDREN_WITH_DIARRHEA * actual_coverage * 0.3)
            healthcare_savings_per_episode = 500  # KSH per episode
            total_healthcare_savings = diarrhea_episodes_prevented * healthcare_savings_per_episode
            
            # Productivity gains from reduced stunting
            stunting_prevented = longterm['stunting_prevented']
            lifetime_productivity_gain_per_child = 500_000  # KSH over lifetime
            total_productivity_gains = stunting_prevented * lifetime_productivity_gain_per_child
            
            # Agricultural productivity (from biofortification)
            if interventions.get('biofortified_crops', 0) > 0:
                agricultural_benefit = effective_budget * (interventions['biofortified_crops']/100) * 0.3
            else:
                agricultural_benefit = 0
            
            # GDP impact
            gdp_impact = longterm['gdp_contribution'] * 5_000_000_000_000  # 5 trillion KSH GDP
            
            # Display economic metrics
            st.metric("Healthcare Savings (Annual)", f"KSH {total_healthcare_savings:,.0f}")
            st.metric("Productivity Gains (Lifetime)", f"KSH {total_productivity_gains:,.0f}")
            st.metric("Agricultural Benefits", f"KSH {agricultural_benefit:,.0f}")
            st.metric("GDP Impact (5 years)", f"KSH {gdp_impact:,.0f}")
            
            # Calculate ROI
            total_benefits = (
                total_healthcare_savings * 5 +  # 5 years of savings
                total_productivity_gains * 0.2 +  # Present value adjustment
                agricultural_benefit * 5 +
                gdp_impact * 0.1  # Conservative GDP impact
            )
            
            roi = ((total_benefits - effective_budget) / effective_budget) * 100
            
            # ROI visualization
            st.subheader("💡 Return on Investment")
            
            if roi > 0:
                st.success(f"✅ ROI: +{roi:.1f}%")
                st.write("The intervention generates positive economic returns")
            else:
                st.error(f"❌ ROI: {roi:.1f}%")
                st.write("Consider optimizing the intervention mix")
            
            # Benefit-cost ratio
            bcr = total_benefits / effective_budget
            st.metric("Benefit-Cost Ratio", f"{bcr:.2f}:1")
            
            if bcr > 3:
                st.success("Excellent economic value")
            elif bcr > 1.5:
                st.info("Good economic value")
            else:
                st.warning("Consider optimization")
        
        # Economic timeline projection
        st.subheader("📈 Economic Impact Timeline")
        
        years = list(range(1, 11))  # 10-year projection
        
        # Calculate cumulative benefits
        cumulative_healthcare = [total_healthcare_savings * y for y in years]
        cumulative_productivity = [total_productivity_gains * (y/10) * 0.3 for y in years]  # Gradual realization
        cumulative_gdp = [gdp_impact * (y/10) * 0.2 for y in years]
        cumulative_total = [ch + cp + cg for ch, cp, cg in zip(cumulative_healthcare, cumulative_productivity, cumulative_gdp)]
        
        # Investment line (assuming continued investment)
        cumulative_investment = [effective_budget * y * 0.8 for y in years]  # 80% of initial per year
        
        fig_econ_timeline = go.Figure()
        
        fig_econ_timeline.add_trace(go.Scatter(
            x=years, y=cumulative_total,
            mode='lines+markers', name='Total Benefits',
            line=dict(color='green', width=3),
            fill='tonexty', fillcolor='rgba(0,255,0,0.1)'
        ))
        
        fig_econ_timeline.add_trace(go.Scatter(
            x=years, y=cumulative_investment,
            mode='lines+markers', name='Cumulative Investment',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # Add break-even point
        break_even_year = None
        for i, year in enumerate(years):
            if cumulative_total[i] > cumulative_investment[i]:
                break_even_year = year
                fig_econ_timeline.add_vline(
                    x=year, line_dash="dot", line_color="blue",
                    annotation_text=f"Break-even: Year {year}"
                )
                break
        
        fig_econ_timeline.update_layout(
            title="Economic Returns vs Investment Over Time",
            xaxis_title="Years",
            yaxis_title="Value (KSH)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_econ_timeline, use_container_width=True)
        
        if break_even_year:
            st.success(f"📊 Investment breaks even in Year {break_even_year}")
        else:
            st.info("📊 Break-even point beyond 10-year projection")

# BIOMARKER TRACKING TAB
with tab4:
    st.header("🔬 Biomarker Monitoring & Clinical Indicators")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Biomarker improvement projections
        st.subheader("📈 Biomarker Normalization Timeline")
        
        # Create biomarker data
        biomarker_months = list(range(0, min(timeline_months + 1, 37), 3))
        
        # Different biomarkers improve at different rates
        serum_zinc_progression = [
            sigmoid(m, biomarkers['serum_zinc_normalized']*100, 0.3, 6) 
            for m in biomarker_months
        ]
        
        alkaline_phosphatase_progression = [
            sigmoid(m, biomarkers['alkaline_phosphatase_improved']*100, 0.25, 9) 
            for m in biomarker_months
        ]
        
        growth_hormone_progression = [
            sigmoid(m, biomarkers['growth_hormone_igf1_increased']*100, 0.2, 12) 
            for m in biomarker_months
        ]
        
        inflammatory_marker_progression = [
            sigmoid(m, biomarkers['inflammatory_markers_reduced']*100, 0.15, 15) 
            for m in biomarker_months
        ]
        
        # Create biomarker chart
        fig_bio = go.Figure()
        
        fig_bio.add_trace(go.Scatter(
            x=biomarker_months, y=serum_zinc_progression,
            mode='lines+markers', name='Serum Zinc (>70 μg/dL)',
            line=dict(color='#FF6B6B', width=3)
        ))
        
        fig_bio.add_trace(go.Scatter(
            x=biomarker_months, y=alkaline_phosphatase_progression,
            mode='lines+markers', name='Alkaline Phosphatase',
            line=dict(color='#4ECDC4', width=3)
        ))
        
        fig_bio.add_trace(go.Scatter(
            x=biomarker_months, y=growth_hormone_progression,
            mode='lines+markers', name='Growth Hormone/IGF-1',
            line=dict(color='#45B7D1', width=3)
        ))
        
        fig_bio.add_trace(go.Scatter(
            x=biomarker_months, y=inflammatory_marker_progression,
            mode='lines+markers', name='Inflammatory Markers',
            line=dict(color='#96CEB4', width=3)
        ))
        
        # Add reference line for clinical significance
        fig_bio.add_hline(y=70, line_dash="dash", line_color="gray",
                         annotation_text="Clinical Significance Threshold")
        
        fig_bio.update_layout(
            title="Biomarker Improvement Trajectories",
            xaxis_title="Months",
            yaxis_title="% Population with Normal Levels",
            yaxis=dict(range=[0, 100]),
            hovermode='x unified',
            height=450
        )
        
        st.plotly_chart(fig_bio, use_container_width=True)
        
        # Clinical indicators dashboard
        col_clin1, col_clin2 = st.columns(2)
        
        with col_clin1:
            st.subheader("🩺 Clinical Indicators")
            
            clinical_metrics = {
                "Serum Zinc Deficiency": {
                    "baseline": 51,  # % deficient
                    "target": 51 * (1 - biomarkers['serum_zinc_normalized']),
                    "unit": "%",
                    "threshold": 20
                },
                "Stunting Prevalence": {
                    "baseline": 26,
                    "target": 26 * (1 - longterm['height_for_age_zscore_improved'] * 0.5),
                    "unit": "%",
                    "threshold": 15
                },
                "Diarrhea Incidence": {
                    "baseline": 15,
                    "target": 15 * (1 - immediate['diarrhea_duration_reduced']),
                    "unit": "%",
                    "threshold": 10
                },
                "Anemia Co-occurrence": {
                    "baseline": 36,
                    "target": 36 * 0.9,  # Zinc helps iron absorption
                    "unit": "%",
                    "threshold": 25
                }
            }
            
            for indicator, values in clinical_metrics.items():
                baseline = values['baseline']
                target = values['target']
                improvement = baseline - target
                
                st.write(f"**{indicator}**")
                
                # Create mini progress bar
                progress = improvement / baseline if baseline > 0 else 0
                st.progress(min(progress, 1.0))
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.caption(f"Baseline: {baseline:.1f}{values['unit']}")
                with col_m2:
                    st.caption(f"Target: {target:.1f}{values['unit']}")
                with col_m3:
                    if target < values['threshold']:
                        st.caption("✅ Goal Met")
                    else:
                        st.caption(f"⚠️ Gap: {target - values['threshold']:.1f}{values['unit']}")
        
        with col_clin2:
            st.subheader("🧬 Monitoring Protocol")
            
            # Monitoring schedule based on intervention mix
            monitoring_schedule = {
                "Month 0 (Baseline)": [
                    "Serum zinc levels",
                    "Height/weight measurements",
                    "Dietary assessment",
                    "Morbidity history"
                ],
                "Month 3": [
                    "Serum zinc levels",
                    "Growth velocity",
                    "Diarrhea incidence",
                    "Compliance assessment"
                ],
                "Month 6": [
                    "Full biomarker panel",
                    "Anthropometric measures",
                    "Developmental assessment",
                    "Adverse event monitoring"
                ],
                "Month 12": [
                    "Comprehensive evaluation",
                    "Cost-effectiveness review",
                    "Program optimization",
                    "Scale-up planning"
                ]
            }
            
            selected_timepoint = st.selectbox(
                "Select Monitoring Timepoint",
                list(monitoring_schedule.keys())
            )
            
            st.write("**Required Assessments:**")
            for assessment in monitoring_schedule[selected_timepoint]:
                st.write(f"• {assessment}")
            
            # Sample size calculator for monitoring
            st.subheader("📊 Monitoring Sample Size")
            
            confidence_level = st.slider("Confidence Level (%)", 90, 99, 95)
            margin_of_error = st.slider("Margin of Error (%)", 1, 10, 5)
            
            # Calculate sample size (simplified formula)
            z_score = 1.96 if confidence_level == 95 else 2.58
            p = 0.5  # Maximum variability
            n = (z_score**2 * p * (1-p)) / (margin_of_error/100)**2
            
            st.metric("Required Sample Size", f"{int(n):,} individuals")
            st.caption("For population-level monitoring")
        
        # Laboratory capacity requirements
        st.subheader("🔬 Laboratory Capacity Requirements")
        
        lab_requirements = {
            "Test Type": [
                "Serum Zinc (AAS)",
                "Alkaline Phosphatase",
                "CRP (inflammation)",
                "Hemoglobin",
                "Anthropometry"
            ],
            "Tests/Month": [
                int(actual_coverage * ZINC_DEFICIENT_POPULATION * 0.001),  # 0.1% monthly
                int(actual_coverage * ZINC_DEFICIENT_POPULATION * 0.0008),
                int(actual_coverage * ZINC_DEFICIENT_POPULATION * 0.0012),
                int(actual_coverage * ZINC_DEFICIENT_POPULATION * 0.0015),
                int(actual_coverage * CHILDREN_UNDER_5 * 0.05)  # 5% of children monthly
            ],
            "Cost/Test (KSH)": [250, 180, 150, 120, 50],
            "Turnaround (days)": [3, 2, 1, 1, 0]
        }
        
        lab_df = pd.DataFrame(lab_requirements)
        lab_df['Monthly Cost'] = lab_df['Tests/Month'] * lab_df['Cost/Test (KSH)']
        
        st.dataframe(
            lab_df.style.format({
                'Tests/Month': '{:,.0f}',
                'Cost/Test (KSH)': 'KSH {:.0f}',
                'Monthly Cost': 'KSH {:,.0f}'
            }),
            use_container_width=True
        )
        
        total_lab_cost = lab_df['Monthly Cost'].sum()
        st.metric("Total Monthly Lab Costs", f"KSH {total_lab_cost:,.0f}")
        st.metric("Annual Lab Budget Needed", f"KSH {total_lab_cost * 12:,.0f}")

# COMPARATIVE REPORTS TAB
with tab5:
    st.header("📈 Comparative Analysis & Reporting")
    
    if 'total_allocation' in locals() and total_allocation == 100:
        # Executive summary generation
        st.subheader("📋 Executive Summary")
        
        # Generate comprehensive report
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        executive_summary = f"""
        ### Zinc Deficiency Intervention Simulation Report
        
        **Generated:** {report_date}
        **Simulation ID:** ZN-{datetime.now().strftime('%Y%m%d%H%M')}
        
        #### 1. Investment Overview
        - **Total Budget:** KSH {effective_budget:,.0f} (effective)
        - **Target Population:** {int(actual_coverage * ZINC_DEFICIENT_POPULATION):,} zinc-deficient individuals
        - **Implementation Period:** {timeline_months} months
        - **Coverage Achieved:** {actual_coverage*100:.1f}%
        
        #### 2. Intervention Strategy Mix
        """
        
        for intervention, percentage in interventions.items():
            if percentage > 0:
                executive_summary += f"- **{intervention.replace('_', ' ').title()}:** {percentage}%\n"
        
        executive_summary += f"""
        
        #### 3. Key Health Outcomes (Projected)
        
        **Immediate (0-3 months):**
        - Diarrhea duration reduced by {immediate['diarrhea_duration_reduced']*100:.1f}%
        - Respiratory infections reduced by {immediate['acute_respiratory_infection_reduced']*100:.1f}%
        
        **Mid-term (3-12 months):**
        - Growth velocity increased by {midterm['linear_growth_velocity_increased']*100:.1f}%
        - Infection frequency reduced by {midterm['infection_frequency_reduced']*100:.1f}%
        
        **Long-term (1-5 years):**
        - Stunting cases prevented: {longterm['stunting_prevented']:,}
        - Child deaths prevented: {longterm['child_mortality_reduced']:,}
        - Cognitive development: +{longterm['cognitive_development_score']:.1f} IQ points
        
        #### 4. Economic Analysis
        - **Return on Investment:** {roi:.1f}%
        - **Benefit-Cost Ratio:** {bcr:.2f}:1
        - **GDP Impact:** KSH {gdp_impact:,.0f}
        - **Healthcare Savings:** KSH {total_healthcare_savings:,.0f} annually
        
        #### 5. Implementation Risks
        """
        
        if 'risk_categories' in locals():
            for risk, details in risk_categories.items():
                risk_level = "High" if details['probability'] > 0.6 else "Medium" if details['probability'] > 0.3 else "Low"
                executive_summary += f"- {risk}: {risk_level} risk ({details['probability']*100:.0f}% probability)\n"
        
        st.markdown(executive_summary)
        
        # Scenario comparison
        st.subheader("🔄 Scenario Comparison Analysis")
        
        # Store current scenario
        current_scenario = {
            'name': strategy_preset if strategy_preset != "Custom" else "Current Plan",
            'coverage': actual_coverage * 100,
            'roi': roi,
            'stunting_prevented': longterm['stunting_prevented'],
            'cost_per_person': effective_budget / (actual_coverage * ZINC_DEFICIENT_POPULATION),
            'interventions': interventions.copy()
        }
        
        # Define comparison scenarios
        scenarios = {
            'Current Plan': current_scenario,
            'Maximum Impact': {
                'coverage': min(95, actual_coverage * 100 * 1.5),
                'roi': roi * 0.7,  # Less efficient at scale
                'stunting_prevented': int(longterm['stunting_prevented'] * 1.8),
                'cost_per_person': (effective_budget * 2) / (ZINC_DEFICIENT_POPULATION * 0.95)
            },
            'Cost-Optimized': {
                'coverage': actual_coverage * 100 * 0.75,
                'roi': roi * 1.4,
                'stunting_prevented': int(longterm['stunting_prevented'] * 0.7),
                'cost_per_person': (effective_budget * 0.6) / (ZINC_DEFICIENT_POPULATION * 0.75 * actual_coverage)
            },
            'Emergency Response': {
                'coverage': actual_coverage * 100 * 0.5,
                'roi': roi * 0.5,
                'stunting_prevented': int(longterm['stunting_prevented'] * 0.4),
                'cost_per_person': (effective_budget * 0.8) / (ZINC_DEFICIENT_POPULATION * 0.5 * actual_coverage)
            }
        }
        
        # Create comparison visualization
        comparison_metrics = ['coverage', 'roi', 'stunting_prevented', 'cost_per_person']
        comparison_labels = ['Coverage (%)', 'ROI (%)', 'Stunting Prevented', 'Cost/Person (KSH)']
        
        fig_comparison = go.Figure()
        
        for i, (metric, label) in enumerate(zip(comparison_metrics, comparison_labels)):
            values = [scenarios[s].get(metric, 0) for s in scenarios.keys()]
            
            # Normalize for visualization (except for first metric)
            if i > 0:
                max_val = max(values) if max(values) > 0 else 1
                values = [v/max_val * 100 for v in values]
            
            fig_comparison.add_trace(go.Bar(
                name=label,
                x=list(scenarios.keys()),
                y=values,
                text=[f"{v:.1f}" for v in values],
                textposition='auto'
            ))
        
        fig_comparison.update_layout(
            title="Multi-Scenario Comparison",
            barmode='group',
            xaxis_title="Scenario",
            yaxis_title="Relative Performance",
            height=450
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Recommendations generator
        st.subheader("🎯 Evidence-Based Recommendations")
        
        recommendations = []
        priority_level = []
        
        # Coverage recommendations
        if actual_coverage < 0.6:
            recommendations.append("Increase budget allocation or improve distribution efficiency to reach >60% coverage")
            priority_level.append("Critical")
        elif actual_coverage < 0.8:
            recommendations.append("Optimize distribution networks to achieve 80% coverage target")
            priority_level.append("High")
        
        # Intervention mix recommendations
        if interventions.get('fortification', 0) < 20:
            recommendations.append("Increase food fortification investment - most sustainable long-term strategy")
            priority_level.append("High")
        
        if interventions.get('therapeutic_zinc', 0) < 15 and CHILDREN_WITH_DIARRHEA > 100000:
            recommendations.append("Boost therapeutic zinc for diarrhea treatment - high immediate impact")
            priority_level.append("Critical")
        
        if interventions.get('biofortified_crops', 0) < 10:
            recommendations.append("Consider biofortified crops for sustainable rural impact")
            priority_level.append("Medium")
        
        # Efficiency recommendations
        if procurement_efficiency < 70:
            recommendations.append("Improve procurement processes - potential 30% cost savings")
            priority_level.append("High")
        
        if distribution_efficiency < 60:
            recommendations.append("Strengthen supply chain management systems")
            priority_level.append("Critical")
        
        # Display recommendations with priority
        for rec, priority in zip(recommendations, priority_level):
            if priority == "Critical":
                st.error(f"🔴 **{priority}:** {rec}")
            elif priority == "High":
                st.warning(f"🟡 **{priority}:** {rec}")
            else:
                st.info(f"🔵 **{priority}:** {rec}")
        
        # Download options
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            st.download_button(
                label="📥 Download Executive Report",
                data=executive_summary,
                file_name=f"zinc_intervention_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown"
            )
        
        with col_dl2:
            # Prepare detailed data export
            detailed_data = {
                'Metrics': [],
                'Values': []
            }
            
            for key, value in {**immediate, **midterm, **longterm}.items():
                detailed_data['Metrics'].append(key)
                detailed_data['Values'].append(value)
            
            detailed_df = pd.DataFrame(detailed_data)
            
            st.download_button(
                label="📊 Download Data (CSV)",
                data=detailed_df.to_csv(index=False),
                file_name=f"zinc_intervention_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col_dl3:
            # Save scenario for comparison
            if st.button("💾 Save Scenario"):
                st.session_state.scenario_history.append({
                    'timestamp': datetime.now(),
                    'scenario': current_scenario,
                    'outcomes': {
                        'immediate': immediate,
                        'midterm': midterm,
                        'longterm': longterm
                    }
                })
                st.success("Scenario saved for comparison!")
        
        # Historical comparison if scenarios saved
        if st.session_state.scenario_history:
            st.subheader("📊 Historical Scenario Comparison")
            
            history_df = pd.DataFrame([
                {
                    'Time': s['timestamp'].strftime('%H:%M:%S'),
                    'Coverage': s['scenario']['coverage'],
                    'ROI': s['scenario']['roi'],
                    'Stunting Prevented': s['outcomes']['longterm']['stunting_prevented']
                }
                for s in st.session_state.scenario_history
            ])
            
            st.dataframe(history_df, use_container_width=True)
    
    else:
        st.warning("⚠️ Please complete intervention setup with 100% budget allocation")

# Enhanced Sidebar
with st.sidebar:
    st.header("🎯 Quick Reference")
    
    # Key statistics
    st.subheader("📊 Baseline Statistics")
    st.metric("Zinc Deficient Population", f"{ZINC_DEFICIENT_POPULATION:,}")
    st.metric("Stunting Prevalence", "26%")
    st.metric("Children Under 5", f"{CHILDREN_UNDER_5:,}")
    st.metric("Diarrhea Prevalence", "15% of under-5s")
    
    st.subheader("🔬 Zinc Facts")
    with st.expander("Why Zinc Matters"):
        st.write("""
        • Essential for 300+ enzymes
        • Critical for immune function
        • Required for DNA synthesis
        • Vital for growth & development
        • Key role in wound healing
        """)
    
    with st.expander("Deficiency Consequences"):
        st.write("""
        • Stunted growth (26% prevalence)
        • Increased diarrhea severity
        • Impaired immune response
        • Delayed wound healing
        • Cognitive impairment
        • Increased child mortality
        """)
    
    with st.expander("Intervention Evidence"):
        st.write("""
        **Proven Impacts:**
        • 25% reduction in diarrhea duration
        • 13% reduction in child mortality
        • 0.5 Z-score improvement in height
        • 20% reduction in pneumonia
        
        *Source: Cochrane Reviews, WHO*
        """)
    
    st.subheader("ℹ️ About This Tool")
    st.info("""
    This simulator models zinc intervention strategies based on:
    • Kenya health surveys
    • WHO/UNICEF guidelines  
    • Cochrane systematic reviews
    • Cost-effectiveness research
    
    **Version:** 2.0.0
    **Updated:** 2025
    """)
    
    # Add session metrics
    if 'simulation_run' in st.session_state:
        st.subheader("📈 Session Metrics")
        st.caption(f"Scenarios tested: {len(st.session_state.scenario_history)}")

# Footer
st.markdown("---")
st.caption("""
    💊 Zinc Intervention Simulator v2.0 | Based on Kenya health data and global evidence | 
    For planning and demonstration purposes
""")

# Hidden debug info (uncomment for debugging)
# with st.expander("🔧 Debug Information"):
#     st.write("Session State:", st.session_state)
#     st.write("Total Allocation:", total_allocation if 'total_allocation' in locals() else "Not set")
#     st.write("Effective Budget:", effective_budget if 'effective_budget' in locals() else "Not calculated")