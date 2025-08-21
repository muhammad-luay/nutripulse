"""
Iodine Deficiency Intervention Simulation Engine
Interactive GUI for modeling intervention strategies and outcomes
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Kenya Iodine Intervention Simulator",
    page_icon="🧂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_run' not in st.session_state:
    st.session_state.simulation_run = False

# Title and description
st.title("🧂 Kenya Iodine Intervention Simulator")
st.markdown("""
**Addressing 100% Iodine Deficiency Crisis** | Based on KNMS 2011 Data showing universal iodine deficiency
""")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Intervention Setup", "📈 Outcomes Prediction", "💰 Cost Analysis", "📋 Reports"])

# Constants based on Kenya data
KENYA_POPULATION = 47_500_000  # 2019 estimate
AFFECTED_POPULATION = KENYA_POPULATION  # 100% deficiency
CHILDREN_UNDER_5 = int(KENYA_POPULATION * 0.14)  # ~14% are under 5
PREGNANT_WOMEN = int(KENYA_POPULATION * 0.034)  # ~3.4% pregnant women annually
RURAL_POPULATION = int(KENYA_POPULATION * 0.73)  # 73% rural

def calculate_intervention_costs(budget, interventions):
    """Calculate costs for different intervention strategies"""
    costs = {
        'salt_iodization': {
            'unit_cost': 2.5,  # KSH per person per year
            'effectiveness': 0.85,
            'reach_time': 6  # months
        },
        'oil_fortification': {
            'unit_cost': 15,  # KSH per person per 6 months
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

def simulate_health_outcomes(coverage, intervention_mix, timeline_months):
    """Simulate health outcomes based on interventions"""
    # Calculate weighted effectiveness
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
        'cretinism_prevented': int(coverage * total_effectiveness * 500),  # cases
        'economic_productivity_gain': coverage * total_effectiveness * 0.15  # 15% max gain
    }
    
    return immediate, midterm, longterm

# INTERVENTION SETUP TAB
with tab1:
    st.header("🎯 Configure Intervention Strategy")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("💵 Budget Allocation")
        
        # Budget range selector
        st.write("**Select Budget Range:**")
        budget_scale = st.select_slider(
            "Budget Scale",
            options=["Millions", "Billions"],
            value="Millions",
            help="Choose between millions or billions for easier adjustment"
        )
        
        # Set min/max based on scale
        if budget_scale == "Millions":
            min_budget = 10_000_000  # 10 million minimum
            max_budget = 999_000_000  # 999 million maximum
            step_size = 10_000_000  # 10 million steps
            default_val = 500_000_000  # 500 million default
            format_str = "{:,.0f} Million KSH"
            divisor = 1_000_000
        else:  # Billions
            min_budget = 1_000_000_000  # 1 billion minimum
            max_budget = 10_000_000_000  # 10 billion maximum
            step_size = 100_000_000  # 100 million steps
            default_val = 2_000_000_000  # 2 billion default
            format_str = "{:,.1f} Billion KSH"
            divisor = 1_000_000_000
        
        # Main budget slider
        total_budget = st.slider(
            "Total Budget (KSH)",
            min_value=min_budget,
            max_value=max_budget,
            value=default_val,
            step=step_size,
            format=f"%d",
            help="Slide to adjust total budget allocation"
        )
        
        # Display formatted budget
        st.info(f"💰 **Budget: {format_str.format(total_budget/divisor)}**")
        
        # Minimum budget allocation per intervention
        st.write("**Minimum Allocation Requirements:**")
        min_allocation = st.slider(
            "Minimum % per active intervention",
            min_value=0,
            max_value=25,
            value=5,
            step=5,
            help="Ensure each intervention gets minimum funding if selected"
        )
        
        # Budget per person
        budget_per_person = total_budget / AFFECTED_POPULATION
        st.metric("Budget per person", f"KSH {budget_per_person:.2f}")
        
        st.subheader("🎯 Target Population")
        
        # Population targeting
        target_all = st.checkbox("Target Entire Population", value=True)
        
        if not target_all:
            target_groups = st.multiselect(
                "Select Priority Groups",
                ["Children Under 5", "Pregnant Women", "Lactating Women", 
                 "School Children", "Rural Population", "Urban Population"],
                default=["Children Under 5", "Pregnant Women"]
            )
        
        # Timeline
        st.subheader("⏱️ Implementation Timeline")
        timeline_months = st.slider(
            "Implementation Period (months)",
            min_value=6,
            max_value=60,
            value=24,
            step=6
        )
    
    with col2:
        st.subheader("🔧 Intervention Mix")
        st.info(f"Allocate percentage of budget to each intervention. Minimum {min_allocation}% per active intervention.")
        
        # Track which interventions are active
        st.write("**Enable/Disable Interventions:**")
        col_a, col_b = st.columns(2)
        with col_a:
            use_salt = st.checkbox("Use Salt Iodization", value=True)
            use_oil = st.checkbox("Use Oil Fortification", value=True)
        with col_b:
            use_supplement = st.checkbox("Use Direct Supplementation", value=True)
            use_school = st.checkbox("Use School Programs", value=True)
        
        st.write("**Budget Allocation (%):**")
        
        # Count active interventions
        active_count = sum([use_salt, use_oil, use_supplement, use_school])
        
        if active_count == 0:
            st.error("⚠️ Please select at least one intervention strategy!")
            salt_pct = oil_pct = supplement_pct = school_pct = 0
        else:
            # Calculate max value for each slider
            max_per_intervention = 100 - (min_allocation * (active_count - 1))
            
            # Intervention sliders with dynamic min/max
            if use_salt:
                salt_pct = st.slider(
                    "🧂 Salt Iodization Program",
                    min_value=min_allocation,
                    max_value=max_per_intervention,
                    value=min(40, max_per_intervention),
                    help="Fix and maintain salt iodization infrastructure"
                )
            else:
                salt_pct = 0
            
            if use_oil:
                remaining = 100 - salt_pct
                oil_max = min(max_per_intervention, remaining - min_allocation * (sum([use_supplement, use_school])))
                oil_pct = st.slider(
                    "🛢️ Oil Fortification",
                    min_value=min_allocation,
                    max_value=max(min_allocation, oil_max),
                    value=min(20, max(min_allocation, oil_max)),
                    help="Fortify cooking oil with iodine (longer retention)"
                )
            else:
                oil_pct = 0
            
            if use_supplement:
                remaining = 100 - salt_pct - oil_pct
                supp_max = min(max_per_intervention, remaining - min_allocation * sum([use_school]))
                supplement_pct = st.slider(
                    "💊 Direct Supplementation",
                    min_value=min_allocation,
                    max_value=max(min_allocation, supp_max),
                    value=min(25, max(min_allocation, supp_max)),
                    help="Pills/drops for high-risk groups"
                )
            else:
                supplement_pct = 0
            
            if use_school:
                # School gets the remainder to ensure 100% total
                school_pct = 100 - salt_pct - oil_pct - supplement_pct
                st.info(f"🏫 School Feeding Programs: **{school_pct}%** (auto-calculated remainder)")
            else:
                school_pct = 0
        
        # Check if allocation equals 100%
        total_allocation = salt_pct + oil_pct + supplement_pct + school_pct
        
        # Display allocation summary
        st.write("**Allocation Summary:**")
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.metric("Total", f"{total_allocation}%")
        with col_2:
            if total_allocation == 100:
                st.success("✅ Valid")
            else:
                st.error("❌ Must = 100%")
        with col_3:
            st.metric("Active", f"{active_count} strategies")
        
        # Coverage estimation
        st.subheader("📊 Coverage Estimation")
        
        # Calculate coverage based on budget and intervention mix
        intervention_mix = {
            'salt': salt_pct,
            'oil': oil_pct,
            'supplement': supplement_pct,
            'school': school_pct
        }
        
        # Simplified coverage calculation
        avg_cost_per_person = (
            salt_pct * 2.5 + 
            oil_pct * 30 + 
            supplement_pct * 50 + 
            school_pct * 8
        ) / 100
        
        max_coverage = min(1.0, total_budget / (avg_cost_per_person * AFFECTED_POPULATION))
        
        # Add implementation efficiency
        implementation_efficiency = st.slider(
            "Implementation Efficiency (%)",
            min_value=30,
            max_value=95,
            value=70,
            help="Account for logistics, corruption, wastage"
        )
        
        actual_coverage = max_coverage * (implementation_efficiency / 100)
        
        # Display coverage metrics
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Population Reached", f"{actual_coverage*100:.1f}%")
        with col_b:
            st.metric("People Covered", f"{int(actual_coverage * AFFECTED_POPULATION):,}")
        with col_c:
            if actual_coverage < 0.8:
                color = "🔴"
            elif actual_coverage < 0.9:
                color = "🟡"
            else:
                color = "🟢"
            st.metric("Coverage Status", f"{color} {'Low' if actual_coverage < 0.8 else 'Good'}")

# OUTCOMES PREDICTION TAB
with tab2:
    st.header("📈 Predicted Health Outcomes")
    
    if total_allocation == 100:
        # Calculate outcomes
        immediate, midterm, longterm = simulate_health_outcomes(
            actual_coverage, intervention_mix, timeline_months
        )
        
        # Create three columns for different time periods
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🚀 Immediate (0-3 months)")
            st.metric(
                "Urinary Iodine Normalized",
                f"{immediate['urinary_iodine_normalized']*100:.1f}%",
                delta=f"+{immediate['urinary_iodine_normalized']*100:.1f}%"
            )
            st.metric(
                "Thyroid Function Improved",
                f"{immediate['thyroid_function_improved']*100:.1f}%",
                delta=f"+{immediate['thyroid_function_improved']*100:.1f}%"
            )
            st.metric(
                "Energy Levels Increased",
                f"{immediate['energy_levels_increased']*100:.1f}%",
                delta=f"+{immediate['energy_levels_increased']*100:.1f}%"
            )
        
        with col2:
            st.subheader("📊 Mid-term (3-12 months)")
            st.metric(
                "Goiter Reduction",
                f"{midterm['goiter_reduction']*100:.1f}%",
                delta=f"+{midterm['goiter_reduction']*100:.1f}%"
            )
            st.metric(
                "Pregnancy Outcomes",
                f"{midterm['pregnancy_outcomes_improved']*100:.1f}%",
                delta=f"+{midterm['pregnancy_outcomes_improved']*100:.1f}%"
            )
            st.metric(
                "Child Cognitive Gains",
                f"{midterm['child_cognitive_improvement']*100:.1f}%",
                delta=f"+{midterm['child_cognitive_improvement']*100:.1f}%"
            )
        
        with col3:
            st.subheader("🎯 Long-term (1-5 years)")
            st.metric(
                "Avg IQ Points Gained",
                f"{longterm['iq_points_gained']:.1f}",
                delta=f"+{longterm['iq_points_gained']:.1f}"
            )
            st.metric(
                "Cretinism Cases Prevented",
                f"{longterm['cretinism_prevented']:,}",
                delta=f"-{longterm['cretinism_prevented']:,}"
            )
            st.metric(
                "Economic Productivity",
                f"+{longterm['economic_productivity_gain']*100:.1f}%",
                delta=f"+{longterm['economic_productivity_gain']*100:.1f}%"
            )
        
        # Timeline visualization
        st.subheader("📅 Impact Timeline")
        
        # Create timeline data
        months = list(range(0, timeline_months + 1))
        
        # Sigmoid growth function for realistic adoption
        def sigmoid(x, L, k, x0):
            return L / (1 + np.exp(-k*(x-x0)))
        
        coverage_timeline = [sigmoid(m, actual_coverage*100, 0.3, timeline_months/3) for m in months]
        iodine_sufficiency = [sigmoid(m, actual_coverage*100*0.9, 0.25, timeline_months/2.5) for m in months]
        health_improvement = [sigmoid(m, actual_coverage*100*0.7, 0.2, timeline_months/2) for m in months]
        
        # Create plotly figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months, y=coverage_timeline,
            mode='lines', name='Population Coverage',
            line=dict(color='blue', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=iodine_sufficiency,
            mode='lines', name='Iodine Sufficiency',
            line=dict(color='green', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=months, y=health_improvement,
            mode='lines', name='Health Outcomes',
            line=dict(color='purple', width=3)
        ))
        
        fig.update_layout(
            title="Intervention Impact Over Time",
            xaxis_title="Months",
            yaxis_title="Percentage (%)",
            yaxis=dict(range=[0, 100]),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk factors
        st.subheader("⚠️ Risk Factors")
        
        risk_cols = st.columns(4)
        risks = {
            "Supply Chain": np.random.uniform(0.2, 0.8),
            "Quality Control": np.random.uniform(0.3, 0.9),
            "Community Adoption": np.random.uniform(0.4, 0.95),
            "Political Stability": np.random.uniform(0.5, 0.9)
        }
        
        for i, (risk, value) in enumerate(risks.items()):
            with risk_cols[i]:
                color = "🟢" if value > 0.7 else "🟡" if value > 0.4 else "🔴"
                st.metric(risk, f"{color} {value*100:.0f}%")
    else:
        st.warning("Please adjust intervention allocation to equal 100% in the Intervention Setup tab")

# COST ANALYSIS TAB
with tab3:
    st.header("💰 Cost-Benefit Analysis")
    
    if total_allocation == 100:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💵 Cost Breakdown")
            
            # Calculate costs for each intervention
            costs_data = {
                'Intervention': ['Salt Iodization', 'Oil Fortification', 'Direct Supplements', 'School Programs'],
                'Budget (KSH)': [
                    total_budget * salt_pct / 100,
                    total_budget * oil_pct / 100,
                    total_budget * supplement_pct / 100,
                    total_budget * school_pct / 100
                ],
                'People Reached': [
                    int(actual_coverage * AFFECTED_POPULATION * salt_pct / 100),
                    int(actual_coverage * AFFECTED_POPULATION * oil_pct / 100),
                    int(actual_coverage * AFFECTED_POPULATION * supplement_pct / 100),
                    int(actual_coverage * CHILDREN_UNDER_5 * school_pct / 100)
                ]
            }
            
            costs_df = pd.DataFrame(costs_data)
            costs_df['Cost per Person'] = costs_df['Budget (KSH)'] / costs_df['People Reached'].replace(0, 1)
            
            # Display cost table
            st.dataframe(
                costs_df.style.format({
                    'Budget (KSH)': '{:,.0f}',
                    'People Reached': '{:,.0f}',
                    'Cost per Person': 'KSH {:.2f}'
                }),
                use_container_width=True
            )
            
            # Pie chart of budget allocation
            fig_pie = px.pie(
                costs_df, 
                values='Budget (KSH)', 
                names='Intervention',
                title="Budget Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("📊 Return on Investment")
            
            # Calculate ROI metrics
            total_iq_points = longterm['iq_points_gained'] * actual_coverage * CHILDREN_UNDER_5
            economic_value = longterm['economic_productivity_gain'] * 50_000_000_000  # Rough GDP impact
            health_cost_savings = actual_coverage * AFFECTED_POPULATION * 100  # KSH saved per person
            
            # Cost per outcome metrics
            cost_per_iq_point = total_budget / max(total_iq_points, 1)
            cost_per_life_saved = total_budget / max(longterm['cretinism_prevented'], 1)
            
            st.metric("Cost per IQ Point Gained", f"KSH {cost_per_iq_point:,.2f}")
            st.metric("Cost per Cretinism Prevented", f"KSH {cost_per_life_saved:,.2f}")
            st.metric("Economic Return (5 years)", f"KSH {economic_value:,.0f}")
            st.metric("Health Cost Savings", f"KSH {health_cost_savings:,.0f}")
            
            # ROI calculation
            total_benefits = economic_value + health_cost_savings
            roi = ((total_benefits - total_budget) / total_budget) * 100
            
            st.subheader("💡 Overall ROI")
            if roi > 0:
                st.success(f"🟢 ROI: +{roi:.1f}% - Intervention is cost-effective")
            else:
                st.error(f"🔴 ROI: {roi:.1f}% - Intervention needs optimization")
            
            # Benefit timeline
            years = list(range(1, 6))
            cumulative_benefits = [total_benefits * (y/5) * 0.8 for y in years]
            
            fig_benefits = go.Figure()
            fig_benefits.add_trace(go.Bar(
                x=years,
                y=cumulative_benefits,
                name='Cumulative Benefits',
                marker_color='green'
            ))
            fig_benefits.add_trace(go.Scatter(
                x=years,
                y=[total_budget] * 5,
                mode='lines',
                name='Investment',
                line=dict(color='red', dash='dash')
            ))
            
            fig_benefits.update_layout(
                title="Cost vs Benefits Over Time",
                xaxis_title="Years",
                yaxis_title="Value (KSH)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_benefits, use_container_width=True)

# REPORTS TAB
with tab4:
    st.header("📋 Simulation Report")
    
    if total_allocation == 100:
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
        
        **Immediate (0-3 months):**
        - Urinary Iodine Normalized: {immediate['urinary_iodine_normalized']*100:.1f}% of covered population
        - Thyroid Function Improved: {immediate['thyroid_function_improved']*100:.1f}%
        - Energy Levels Increased: {immediate['energy_levels_increased']*100:.1f}%
        
        **Mid-term (3-12 months):**
        - Goiter Reduction: {midterm['goiter_reduction']*100:.1f}%
        - Pregnancy Outcomes Improved: {midterm['pregnancy_outcomes_improved']*100:.1f}%
        - Child Cognitive Improvement: {midterm['child_cognitive_improvement']*100:.1f}%
        
        **Long-term (1-5 years):**
        - Average IQ Points Gained: {longterm['iq_points_gained']:.1f} points per child
        - Cretinism Cases Prevented: {longterm['cretinism_prevented']:,} cases
        - Economic Productivity Gain: {longterm['economic_productivity_gain']*100:.1f}%
        
        #### Cost-Effectiveness
        - Cost per Person Reached: KSH {budget_per_person:.2f}
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
        
        # Scenario comparison
        st.subheader("🔄 Scenario Comparison")
        
        scenarios = {
            "Current Plan": {
                "Coverage": actual_coverage * 100,
                "ROI": roi,
                "IQ Gain": longterm['iq_points_gained']
            },
            "Maximum Coverage": {
                "Coverage": 95,
                "ROI": roi * 0.8,
                "IQ Gain": longterm['iq_points_gained'] * 1.2
            },
            "Cost-Optimized": {
                "Coverage": actual_coverage * 100 * 0.7,
                "ROI": roi * 1.5,
                "IQ Gain": longterm['iq_points_gained'] * 0.8
            },
            "Emergency Response": {
                "Coverage": actual_coverage * 100 * 1.1,
                "ROI": roi * 0.6,
                "IQ Gain": longterm['iq_points_gained'] * 1.3
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

# Sidebar with quick stats
with st.sidebar:
    st.header("🎯 Quick Stats")
    st.metric("Population at Risk", f"{AFFECTED_POPULATION:,}")
    st.metric("Current Deficiency Rate", "100%")
    st.metric("Children Under 5", f"{CHILDREN_UNDER_5:,}")
    st.metric("Pregnant Women", f"{PREGNANT_WOMEN:,}")
    
    st.header("ℹ️ About")
    st.info("""
    This simulator models iodine deficiency interventions based on:
    - Kenya National Micronutrient Survey 2011
    - WHO intervention guidelines
    - Cost-effectiveness research
    
    **Note:** Results are estimates based on available data and assumptions.
    """)
    
    st.header("🔍 Key Insights")
    st.warning("""
    **Critical Finding:** 100% of surveyed population has zero iodine intake despite 
    consuming "iodized" salt, indicating complete fortification failure.
    """)

# Footer
st.markdown("---")
st.caption("Simulation based on Kenya National Micronutrient Survey 2011 data | For demonstration purposes")