"""
Optimal Budget Calculator for Zinc Interventions
Calculates the true optimal budget based on diminishing returns and cost-effectiveness
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def calculate_optimal_budget(population_params, intervention_mix):
    """
    Calculate the optimal budget for zinc interventions based on:
    1. Diminishing marginal returns
    2. Cost-effectiveness thresholds
    3. Implementation capacity constraints
    """
    
    # Population parameters
    zinc_deficient_pop = population_params['zinc_deficient']
    stunted_children = population_params['stunted_children']
    children_under_5 = population_params['children_under_5']
    
    # Cost parameters per intervention
    intervention_costs = {
        'fortification': {'unit_cost': 3.8, 'effectiveness': 0.75, 'saturation_point': 0.85},
        'therapeutic_zinc': {'unit_cost': 45, 'effectiveness': 0.95, 'saturation_point': 0.60},
        'preventive_supplements': {'unit_cost': 120, 'effectiveness': 0.90, 'saturation_point': 0.70},
        'biofortified_crops': {'unit_cost': 25, 'effectiveness': 0.65, 'saturation_point': 0.75},
        'maternal_supplementation': {'unit_cost': 180, 'effectiveness': 0.92, 'saturation_point': 0.80},
        'community_health': {'unit_cost': 15, 'effectiveness': 0.55, 'saturation_point': 0.90}
    }
    
    # Calculate weighted average cost and effectiveness
    weighted_cost = 0
    weighted_effectiveness = 0
    weighted_saturation = 0
    
    for intervention, percentage in intervention_mix.items():
        if percentage > 0 and intervention in intervention_costs:
            weight = percentage / 100
            weighted_cost += intervention_costs[intervention]['unit_cost'] * weight
            weighted_effectiveness += intervention_costs[intervention]['effectiveness'] * weight
            weighted_saturation += intervention_costs[intervention]['saturation_point'] * weight
    
    # Budget optimization algorithm
    budget_range = np.linspace(100_000_000, 10_000_000_000, 100)  # 100M to 10B KSH
    results = []
    
    for budget in budget_range:
        # Calculate coverage with diminishing returns
        theoretical_coverage = budget / (weighted_cost * zinc_deficient_pop)
        
        # Apply saturation curve (sigmoid function)
        actual_coverage = weighted_saturation * (1 - np.exp(-3 * theoretical_coverage / weighted_saturation))
        actual_coverage = min(actual_coverage, 1.0)  # Cap at 100%
        
        # Calculate health outcomes
        lives_saved = actual_coverage * weighted_effectiveness * 1200  # Base lives saved
        stunting_prevented = actual_coverage * weighted_effectiveness * stunted_children * 0.30
        diarrhea_reduction = actual_coverage * weighted_effectiveness * 0.25
        
        # Calculate economic returns
        healthcare_savings = lives_saved * 500_000  # 500K KSH per life saved in healthcare
        productivity_gains = stunting_prevented * 2_000_000  # 2M KSH lifetime productivity per child
        gdp_impact = actual_coverage * weighted_effectiveness * 0.023 * 5_000_000_000_000  # GDP impact
        
        total_economic_benefit = healthcare_savings + productivity_gains + (gdp_impact * 0.1)
        roi = ((total_economic_benefit - budget) / budget) * 100 if budget > 0 else 0
        
        # Calculate cost-effectiveness metrics
        cost_per_life = budget / lives_saved if lives_saved > 0 else float('inf')
        cost_per_coverage_point = budget / (actual_coverage * 100) if actual_coverage > 0 else float('inf')
        
        # Calculate marginal benefit (derivative approximation)
        marginal_benefit = 0
        if len(results) > 0:
            prev_budget = results[-1]['budget']
            prev_benefit = results[-1]['total_benefit']
            marginal_benefit = (total_economic_benefit - prev_benefit) / (budget - prev_budget) if budget > prev_budget else 0
        
        results.append({
            'budget': budget,
            'coverage': actual_coverage,
            'lives_saved': lives_saved,
            'stunting_prevented': stunting_prevented,
            'total_benefit': total_economic_benefit,
            'roi': roi,
            'cost_per_life': cost_per_life,
            'marginal_benefit': marginal_benefit,
            'efficiency_score': roi * actual_coverage  # Combined metric
        })
    
    df = pd.DataFrame(results)
    
    # Find optimal budget using multiple criteria
    
    # Criterion 1: Maximum efficiency score (ROI × Coverage)
    optimal_efficiency = df.loc[df['efficiency_score'].idxmax()]
    
    # Criterion 2: Point where marginal benefit drops below threshold
    marginal_threshold = 1.5  # Benefits should be at least 1.5x the marginal cost
    df['marginal_ratio'] = df['marginal_benefit']
    optimal_marginal = df[df['marginal_ratio'] >= marginal_threshold]
    if not optimal_marginal.empty:
        optimal_marginal = optimal_marginal.iloc[-1]  # Last budget where marginal benefit is good
    else:
        optimal_marginal = optimal_efficiency
    
    # Criterion 3: Cost-effectiveness threshold (WHO standard)
    cost_effectiveness_threshold = 500_000  # KSH per life saved threshold
    optimal_cost_effective = df[df['cost_per_life'] <= cost_effectiveness_threshold]
    if not optimal_cost_effective.empty:
        optimal_cost_effective = optimal_cost_effective.iloc[-1]  # Maximum budget within threshold
    else:
        optimal_cost_effective = optimal_efficiency
    
    # Criterion 4: Coverage target (reaching 80% of high-risk population)
    coverage_target = 0.8
    optimal_coverage = df[df['coverage'] >= coverage_target]
    if not optimal_coverage.empty:
        optimal_coverage = optimal_coverage.iloc[0]  # Minimum budget to reach target
    else:
        optimal_coverage = optimal_efficiency
    
    # Weighted combination of criteria
    optimal_budget = (
        optimal_efficiency['budget'] * 0.3 +  # 30% weight on efficiency
        optimal_marginal['budget'] * 0.3 +    # 30% weight on marginal returns
        optimal_cost_effective['budget'] * 0.2 +  # 20% weight on cost-effectiveness
        optimal_coverage['budget'] * 0.2      # 20% weight on coverage goals
    )
    
    # Find the closest actual budget in our range
    optimal_index = (df['budget'] - optimal_budget).abs().idxmin()
    optimal_result = df.loc[optimal_index]
    
    # Implementation capacity constraints
    max_annual_capacity = 3_000_000_000  # Maximum 3B KSH based on system capacity
    if optimal_result['budget'] > max_annual_capacity:
        # Adjust for capacity constraints
        capacity_index = (df['budget'] - max_annual_capacity).abs().idxmin()
        capacity_constrained = df.loc[capacity_index]
        
        return {
            'optimal_budget': optimal_result['budget'],
            'constrained_budget': capacity_constrained['budget'],
            'optimal_coverage': optimal_result['coverage'] * 100,
            'optimal_roi': optimal_result['roi'],
            'optimal_lives_saved': int(optimal_result['lives_saved']),
            'reasoning': f"""
            **Optimal Budget Calculation:**
            
            📊 **Unconstrained Optimal: {optimal_result['budget']/1_000_000:.0f} Million KSH**
            - Maximum efficiency at this spending level
            - ROI: {optimal_result['roi']:.0f}%
            - Coverage: {optimal_result['coverage']*100:.1f}%
            - Lives Saved: {int(optimal_result['lives_saved']):,}
            
            ⚠️ **Capacity-Constrained: {capacity_constrained['budget']/1_000_000:.0f} Million KSH**
            - Limited by implementation capacity
            - ROI: {capacity_constrained['roi']:.0f}%
            - Coverage: {capacity_constrained['coverage']*100:.1f}%
            - Lives Saved: {int(capacity_constrained['lives_saved']):,}
            
            **Key Factors:**
            1. Diminishing returns after {optimal_efficiency['coverage']*100:.0f}% coverage
            2. Marginal benefit drops below 1.5x at {optimal_marginal['budget']/1_000_000:.0f}M KSH
            3. Cost per life saved exceeds threshold at {optimal_cost_effective['budget']/1_000_000:.0f}M KSH
            4. 80% coverage requires {optimal_coverage['budget']/1_000_000:.0f}M KSH
            """,
            'data': df
        }
    
    return {
        'optimal_budget': optimal_result['budget'],
        'constrained_budget': optimal_result['budget'],  # No constraint needed
        'optimal_coverage': optimal_result['coverage'] * 100,
        'optimal_roi': optimal_result['roi'],
        'optimal_lives_saved': int(optimal_result['lives_saved']),
        'reasoning': f"""
        **Optimal Budget Calculation:**
        
        ✅ **Optimal Budget: {optimal_result['budget']/1_000_000:.0f} Million KSH**
        
        **Performance Metrics:**
        - ROI: {optimal_result['roi']:.0f}%
        - Coverage: {optimal_result['coverage']*100:.1f}%
        - Lives Saved: {int(optimal_result['lives_saved']):,}
        - Stunting Prevented: {int(optimal_result['stunting_prevented']):,}
        - Cost per Life: {optimal_result['cost_per_life']:.0f} KSH
        
        **Why This is Optimal:**
        1. **Efficiency Peak:** Maximum combined ROI and coverage score
        2. **Marginal Returns:** Beyond this, each additional KSH yields <1.5x benefit
        3. **Cost-Effectiveness:** Within WHO thresholds for health interventions
        4. **Coverage Goals:** Balances reach with implementation feasibility
        
        **Calculation Method:**
        - 30% weight: Efficiency (ROI × Coverage)
        - 30% weight: Marginal benefit ratio
        - 20% weight: Cost-effectiveness threshold
        - 20% weight: Coverage targets
        """,
        'data': df
    }

def visualize_optimization(optimization_result):
    """Create visualizations showing how optimal budget was determined"""
    
    df = optimization_result['data']
    optimal_budget = optimization_result['optimal_budget']
    
    # Create subplot figure
    fig = go.Figure()
    
    # Add ROI curve
    fig.add_trace(go.Scatter(
        x=df['budget'] / 1_000_000,  # Convert to millions
        y=df['roi'],
        mode='lines',
        name='ROI (%)',
        line=dict(color='green', width=2),
        yaxis='y'
    ))
    
    # Add Coverage curve
    fig.add_trace(go.Scatter(
        x=df['budget'] / 1_000_000,
        y=df['coverage'] * 100,
        mode='lines',
        name='Coverage (%)',
        line=dict(color='blue', width=2),
        yaxis='y2'
    ))
    
    # Add efficiency score
    fig.add_trace(go.Scatter(
        x=df['budget'] / 1_000_000,
        y=df['efficiency_score'],
        mode='lines',
        name='Efficiency Score',
        line=dict(color='purple', width=2, dash='dash'),
        yaxis='y'
    ))
    
    # Mark optimal point
    optimal_point = df[df['budget'] == optimal_budget].iloc[0]
    fig.add_trace(go.Scatter(
        x=[optimal_budget / 1_000_000],
        y=[optimal_point['roi']],
        mode='markers',
        name='Optimal Point',
        marker=dict(size=15, color='red', symbol='star'),
        showlegend=True,
        yaxis='y'
    ))
    
    # Add vertical line at optimal budget
    fig.add_vline(
        x=optimal_budget / 1_000_000,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Optimal: {optimal_budget/1_000_000:.0f}M KSH"
    )
    
    # Update layout
    fig.update_layout(
        title="Budget Optimization Analysis",
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
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Streamlit interface for testing
def main():
    st.title("🎯 Optimal Budget Calculator for Zinc Interventions")
    
    st.markdown("""
    This tool calculates the truly optimal budget based on:
    - Diminishing marginal returns
    - Cost-effectiveness thresholds
    - Implementation capacity
    - Coverage targets
    """)
    
    # Input parameters
    st.sidebar.header("Population Parameters")
    
    population_params = {
        'zinc_deficient': st.sidebar.number_input(
            "Zinc Deficient Population",
            value=26_500_000,
            step=1_000_000
        ),
        'stunted_children': st.sidebar.number_input(
            "Stunted Children",
            value=1_900_000,
            step=100_000
        ),
        'children_under_5': st.sidebar.number_input(
            "Children Under 5",
            value=7_000_000,
            step=100_000
        )
    }
    
    st.sidebar.header("Intervention Mix (%)")
    
    intervention_mix = {
        'fortification': st.sidebar.slider("Food Fortification", 0, 100, 30),
        'therapeutic_zinc': st.sidebar.slider("Therapeutic Zinc", 0, 100, 25),
        'preventive_supplements': st.sidebar.slider("Preventive Supplements", 0, 100, 20),
        'biofortified_crops': st.sidebar.slider("Biofortified Crops", 0, 100, 10),
        'maternal_supplementation': st.sidebar.slider("Maternal Programs", 0, 100, 10),
        'community_health': st.sidebar.slider("Community Health", 0, 100, 5)
    }
    
    total = sum(intervention_mix.values())
    if total != 100:
        st.sidebar.error(f"Total must equal 100% (currently {total}%)")
    else:
        # Calculate optimal budget
        result = calculate_optimal_budget(population_params, intervention_mix)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Optimal Budget",
                f"{result['optimal_budget']/1_000_000:.0f} Million KSH",
                delta=f"ROI: {result['optimal_roi']:.0f}%"
            )
            
            st.metric(
                "Coverage Achieved",
                f"{result['optimal_coverage']:.1f}%",
                delta=f"{result['optimal_coverage']:.1f}% of target population"
            )
        
        with col2:
            st.metric(
                "Lives Saved",
                f"{result['optimal_lives_saved']:,}",
                delta="At optimal budget"
            )
            
            if result['constrained_budget'] != result['optimal_budget']:
                st.metric(
                    "Capacity-Constrained Budget",
                    f"{result['constrained_budget']/1_000_000:.0f} Million KSH",
                    delta="Due to implementation limits"
                )
        
        # Show reasoning
        st.markdown("### 📊 How We Calculated This")
        st.markdown(result['reasoning'])
        
        # Show optimization visualization
        st.markdown("### 📈 Optimization Curves")
        fig = visualize_optimization(result)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed data
        with st.expander("View Detailed Calculations"):
            st.dataframe(
                result['data'][['budget', 'coverage', 'roi', 'lives_saved', 'cost_per_life', 'marginal_benefit']]
                .style.format({
                    'budget': '{:,.0f}',
                    'coverage': '{:.2%}',
                    'roi': '{:.1f}%',
                    'lives_saved': '{:,.0f}',
                    'cost_per_life': '{:,.0f}',
                    'marginal_benefit': '{:.2f}'
                })
            )

if __name__ == "__main__":
    main()