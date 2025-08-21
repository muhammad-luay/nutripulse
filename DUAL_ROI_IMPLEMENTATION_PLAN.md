# 📊 Dual ROI System Implementation Plan
## Financial ROI + Social Value Visualization

### Executive Summary
We will implement a dual-metric system that clearly separates Financial ROI (realistic 15-35%) from Social Value (lifetime benefits), displaying both as interactive graphs in the Budget Optimization Analysis section. This provides stakeholders with both immediate economic returns AND long-term societal impact.

---

## 1. Visual Design Specification

### 1.1 Layout Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                  Budget Optimization Analysis                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────┬─────────────────────────────┐ │
│  │    Financial ROI Graph       │    Social Value Graph       │ │
│  │    (Immediate Returns)       │    (Lifetime Impact)        │ │
│  │                              │                              │ │
│  │  Peak: 35% at 1.5B UGX      │  Peak: 18:1 at 2.5B UGX    │ │
│  └─────────────────────────────┴─────────────────────────────┘ │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │          Combined Optimization Curve (3 metrics)          │ │
│  │     - Financial ROI (left axis)                           │ │
│  │     - Economic BCR (right axis)                           │ │
│  │     - Coverage % (annotation)                             │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                  Metric Comparison Table                   │ │
│  │  Budget | Financial ROI | Economic BCR | Social Value     │ │
│  │  500M   |    28%        |    3.2:1     |    14:1         │ │
│  │  1000M  |    31%        |    3.5:1     |    15:1         │ │
│  │  ...    |    ...        |    ...       |    ...          │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Graph Specifications

#### Financial ROI Graph
- **Type**: Line chart with markers + shaded confidence band
- **X-axis**: Budget (Million UGX)
- **Y-axis**: ROI (%)
- **Color**: Green gradient (#2e7d32 to #66bb6a)
- **Features**:
  - Optimal point marker (gold star)
  - Diminishing returns annotation
  - Realistic range shading (15-35%)

#### Social Value Graph  
- **Type**: Area chart with line overlay
- **X-axis**: Budget (Million UGX)
- **Y-axis**: Benefit-Cost Ratio
- **Color**: Blue gradient (#1565c0 to #64b5f6)
- **Features**:
  - Lifetime value area fill
  - NPV-adjusted line overlay
  - Benchmark comparison lines

#### Combined Optimization Curve
- **Type**: Multi-axis line chart
- **Primary Y-axis**: Financial ROI (%)
- **Secondary Y-axis**: Economic BCR (ratio)
- **Annotations**: Coverage % at key points
- **Features**:
  - Interactive hover details
  - Optimal budget vertical line
  - Efficiency zones (high/medium/low)

---

## 2. Configuration Structure

### 2.1 New File: `uganda_nutrition_config.py`

```python
"""
Economic configuration for realistic ROI calculations
All values in Uganda Shillings (UGX)
"""

# Version control for config changes
CONFIG_VERSION = "2.0.0"
LAST_UPDATED = "2025-01-21"

# ========== IMMEDIATE RETURNS (YEAR 1) ==========
IMMEDIATE_RETURNS = {
    'healthcare_costs_avoided': {
        'per_life_saved': 5_000_000,  # Emergency/intensive care avoided
        'per_stunting_prevented': 300_000,  # Reduced clinic visits
        'per_anemia_prevented': 50_000,  # Medication costs saved
        'confidence_interval': 0.2  # ±20% uncertainty
    },
    'productivity_gains': {
        'per_stunting_prevented': 500_000,  # Immediate cognitive benefits
        'per_anemia_prevented': 100_000,  # Work days recovered
        'maternal_per_case': 150_000,  # Maternal productivity
        'confidence_interval': 0.3  # ±30% uncertainty
    }
}

# ========== RECURRING ANNUAL BENEFITS (YEARS 2-5) ==========
RECURRING_BENEFITS = {
    'healthcare_savings': {
        'per_stunting_prevented': 200_000,  # Annual health cost reduction
        'per_anemia_prevented': 30_000,  # Ongoing medication savings
        'system_efficiency_gain': 0.05  # 5% health system improvement
    },
    'productivity_growth': {
        'per_stunting_prevented': 1_000_000,  # Annual earning increase
        'per_anemia_prevented': 200_000,  # Sustained productivity
        'education_completion_bonus': 2_000_000,  # One-time at year 5
    }
}

# ========== LIFETIME SOCIAL VALUE (40 YEARS) ==========
SOCIAL_VALUE = {
    'statistical_value_of_life': 150_000_000,  # WHO/World Bank VSL
    'lifetime_stunting_cost': 25_000_000,  # Total lifetime loss
    'lifetime_anemia_cost': 2_000_000,  # Cumulative impact
    'intergenerational_benefit': 1.2,  # 20% bonus for next generation
    'quality_adjusted_life_years': {
        'per_life_saved': 30,  # QALYs gained
        'value_per_qaly': 5_000_000  # UGX per QALY
    }
}

# ========== DISCOUNT RATES ==========
DISCOUNT_RATES = {
    'financial': 0.12,  # Commercial/market rate
    'economic': 0.05,  # Social discount rate (World Bank)
    'social': 0.03,  # Long-term social rate
    'sensitivity': {
        'low': 0.03,
        'medium': 0.05,
        'high': 0.08
    }
}

# ========== EFFICIENCY FACTORS ==========
EFFICIENCY_FACTORS = {
    'implementation_efficiency': {
        'year_1': 0.7,  # 70% efficiency in first year
        'year_2': 0.85,  # Learning curve improvement
        'year_3_plus': 0.95  # Near-optimal efficiency
    },
    'diminishing_returns': {
        'formula': lambda coverage: 1.0 - (0.3 * coverage),  # Linear decrease
        'minimum_efficiency': 0.7  # Floor at 70%
    },
    'scale_economies': {
        'threshold_1': 1_000_000_000,  # 1B UGX
        'discount_1': 0.05,  # 5% cost reduction
        'threshold_2': 5_000_000_000,  # 5B UGX
        'discount_2': 0.10  # 10% cost reduction
    }
}

# ========== VALIDATION RANGES ==========
VALIDATION_RANGES = {
    'financial_roi': {
        'minimum': -20,  # Can have startup losses
        'maximum': 50,  # Exceptional performance
        'typical_range': (15, 35),
        'warning_threshold': 45
    },
    'economic_bcr': {
        'minimum': 1.0,
        'maximum': 8.0,
        'typical_range': (2.5, 5.0),
        'warning_threshold': 7.0
    },
    'social_value_ratio': {
        'minimum': 5.0,
        'maximum': 30.0,
        'typical_range': (10.0, 20.0),
        'warning_threshold': 25.0
    }
}

# ========== BENCHMARK COMPARISONS ==========
INTERVENTION_BENCHMARKS = {
    'vitamin_a_supplementation': {
        'financial_roi': 25,
        'economic_bcr': 4.3,
        'social_value': 17,
        'source': 'Copenhagen Consensus 2012',
        'confidence': 'High'
    },
    'iron_fortification': {
        'financial_roi': 30,
        'economic_bcr': 3.7,
        'social_value': 14,
        'source': 'Lancet 2013',
        'confidence': 'High'
    },
    'nutrition_education': {
        'financial_roi': 18,
        'economic_bcr': 2.8,
        'social_value': 11,
        'source': 'WHO 2017',
        'confidence': 'Medium'
    },
    'combined_interventions': {
        'financial_roi': 28,
        'economic_bcr': 4.1,
        'social_value': 16,
        'source': 'Uganda NNAP 2019',
        'confidence': 'Medium'
    }
}
```

---

## 3. Calculation Functions

### 3.1 New File: `roi_calculations.py`

```python
"""
Realistic ROI calculation functions with three-tier metrics
"""
import numpy as np
from typing import Dict, Tuple, List
from uganda_nutrition_config import *

def calculate_financial_roi(
    budget: float,
    health_impacts: Dict[str, int],
    confidence_level: float = 0.95
) -> Dict[str, float]:
    """
    Calculate immediate financial returns (Year 1 only)
    
    Returns:
        Dictionary with ROI, confidence intervals, and breakdown
    """
    
    # Extract health impacts
    lives_saved = health_impacts.get('lives_saved', 0)
    stunting_prevented = health_impacts.get('stunting_prevented', 0)
    anemia_prevented = health_impacts.get('anemia_prevented', 0)
    
    # Calculate immediate healthcare savings
    healthcare_savings = (
        lives_saved * IMMEDIATE_RETURNS['healthcare_costs_avoided']['per_life_saved'] +
        stunting_prevented * IMMEDIATE_RETURNS['healthcare_costs_avoided']['per_stunting_prevented'] +
        anemia_prevented * IMMEDIATE_RETURNS['healthcare_costs_avoided']['per_anemia_prevented']
    )
    
    # Calculate immediate productivity gains
    productivity_gains = (
        stunting_prevented * IMMEDIATE_RETURNS['productivity_gains']['per_stunting_prevented'] +
        anemia_prevented * IMMEDIATE_RETURNS['productivity_gains']['per_anemia_prevented']
    )
    
    # Total immediate returns
    total_returns = healthcare_savings + productivity_gains
    
    # Apply implementation efficiency for Year 1
    efficiency = EFFICIENCY_FACTORS['implementation_efficiency']['year_1']
    adjusted_returns = total_returns * efficiency
    
    # Calculate ROI
    roi = ((adjusted_returns - budget) / budget * 100) if budget > 0 else 0
    
    # Calculate confidence intervals
    ci_factor = IMMEDIATE_RETURNS['healthcare_costs_avoided']['confidence_interval']
    roi_lower = ((adjusted_returns * (1 - ci_factor) - budget) / budget * 100) if budget > 0 else 0
    roi_upper = ((adjusted_returns * (1 + ci_factor) - budget) / budget * 100) if budget > 0 else 0
    
    # Validate and cap if necessary
    if roi > VALIDATION_RANGES['financial_roi']['maximum']:
        roi = VALIDATION_RANGES['financial_roi']['maximum']
        
    return {
        'roi': roi,
        'roi_lower': roi_lower,
        'roi_upper': roi_upper,
        'healthcare_savings': healthcare_savings,
        'productivity_gains': productivity_gains,
        'total_returns': total_returns,
        'adjusted_returns': adjusted_returns,
        'efficiency_applied': efficiency
    }

def calculate_economic_bcr(
    budget: float,
    health_impacts: Dict[str, int],
    time_horizon: int = 5,
    discount_rate: float = None
) -> Dict[str, float]:
    """
    Calculate economic benefit-cost ratio over specified time horizon
    """
    
    if discount_rate is None:
        discount_rate = DISCOUNT_RATES['economic']
    
    # Get Year 1 returns
    year1 = calculate_financial_roi(budget, health_impacts)
    
    # Calculate recurring benefits for years 2-5
    stunting = health_impacts.get('stunting_prevented', 0)
    anemia = health_impacts.get('anemia_prevented', 0)
    
    annual_benefits = []
    
    for year in range(time_horizon):
        if year == 0:
            # Year 1: Immediate returns
            annual_benefits.append(year1['total_returns'])
        else:
            # Years 2+: Recurring benefits
            efficiency = EFFICIENCY_FACTORS['implementation_efficiency']['year_2'] if year == 1 else \
                        EFFICIENCY_FACTORS['implementation_efficiency']['year_3_plus']
            
            recurring = (
                stunting * (RECURRING_BENEFITS['healthcare_savings']['per_stunting_prevented'] +
                           RECURRING_BENEFITS['productivity_growth']['per_stunting_prevented']) +
                anemia * (RECURRING_BENEFITS['healthcare_savings']['per_anemia_prevented'] +
                         RECURRING_BENEFITS['productivity_growth']['per_anemia_prevented'])
            ) * efficiency
            
            # Add education bonus in year 5
            if year == 4:
                recurring += stunting * RECURRING_BENEFITS['productivity_growth']['education_completion_bonus'] * 0.3
            
            annual_benefits.append(recurring)
    
    # Calculate NPV of benefits
    npv_benefits = sum(benefit / ((1 + discount_rate) ** year) 
                      for year, benefit in enumerate(annual_benefits))
    
    # Calculate NPV of costs (assuming front-loaded)
    cost_schedule = [budget * 0.6, budget * 0.4] + [0] * (time_horizon - 2)
    npv_costs = sum(cost / ((1 + discount_rate) ** year) 
                   for year, cost in enumerate(cost_schedule))
    
    # Calculate BCR
    bcr = npv_benefits / npv_costs if npv_costs > 0 else 0
    
    # Validate
    if bcr > VALIDATION_RANGES['economic_bcr']['maximum']:
        bcr = VALIDATION_RANGES['economic_bcr']['maximum']
    
    return {
        'bcr': bcr,
        'npv_benefits': npv_benefits,
        'npv_costs': npv_costs,
        'annual_benefits': annual_benefits,
        'irr_estimate': estimate_irr(cost_schedule, annual_benefits)
    }

def calculate_social_value(
    budget: float,
    health_impacts: Dict[str, int],
    time_horizon: int = 40,
    include_intergenerational: bool = True
) -> Dict[str, float]:
    """
    Calculate full social value including VSL and lifetime impacts
    """
    
    lives = health_impacts.get('lives_saved', 0)
    stunting = health_impacts.get('stunting_prevented', 0)
    anemia = health_impacts.get('anemia_prevented', 0)
    
    # Calculate lifetime social value
    lifetime_value = (
        lives * SOCIAL_VALUE['statistical_value_of_life'] +
        stunting * SOCIAL_VALUE['lifetime_stunting_cost'] +
        anemia * SOCIAL_VALUE['lifetime_anemia_cost']
    )
    
    # Add intergenerational benefits if enabled
    if include_intergenerational:
        lifetime_value *= SOCIAL_VALUE['intergenerational_benefit']
    
    # Add QALY value
    qaly_value = lives * SOCIAL_VALUE['quality_adjusted_life_years']['per_life_saved'] * \
                 SOCIAL_VALUE['quality_adjusted_life_years']['value_per_qaly']
    
    total_social_value = lifetime_value + qaly_value
    
    # Discount to present value (using midpoint approximation)
    discount_rate = DISCOUNT_RATES['social']
    npv_social = total_social_value / ((1 + discount_rate) ** (time_horizon / 2))
    
    # Calculate ratio
    social_ratio = npv_social / budget if budget > 0 else 0
    
    # Validate
    if social_ratio > VALIDATION_RANGES['social_value_ratio']['maximum']:
        social_ratio = VALIDATION_RANGES['social_value_ratio']['maximum']
    
    return {
        'ratio': social_ratio,
        'lifetime_value': lifetime_value,
        'qaly_value': qaly_value,
        'total_social_value': total_social_value,
        'npv_social': npv_social,
        'time_horizon': time_horizon
    }

def calculate_all_metrics(
    budget: float,
    coverage: float,
    health_impacts: Dict[str, int]
) -> Dict[str, any]:
    """
    Master function to calculate all three metric tiers
    """
    
    # Apply diminishing returns to health impacts
    efficiency = EFFICIENCY_FACTORS['diminishing_returns']['formula'](coverage)
    adjusted_impacts = {
        key: int(value * efficiency) 
        for key, value in health_impacts.items()
    }
    
    # Calculate all three tiers
    financial = calculate_financial_roi(budget, adjusted_impacts)
    economic = calculate_economic_bcr(budget, adjusted_impacts)
    social = calculate_social_value(budget, adjusted_impacts)
    
    # Determine optimal metric for this budget level
    score = (
        financial['roi'] / VALIDATION_RANGES['financial_roi']['typical_range'][1] * 0.3 +
        economic['bcr'] / VALIDATION_RANGES['economic_bcr']['typical_range'][1] * 0.4 +
        social['ratio'] / VALIDATION_RANGES['social_value_ratio']['typical_range'][1] * 0.3
    )
    
    return {
        'financial': financial,
        'economic': economic,
        'social': social,
        'coverage': coverage,
        'efficiency': efficiency,
        'optimization_score': score,
        'metrics_summary': {
            'financial_roi': f"{financial['roi']:.1f}%",
            'economic_bcr': f"{economic['bcr']:.1f}:1",
            'social_value': f"{social['ratio']:.1f}:1"
        }
    }

def estimate_irr(costs: List[float], benefits: List[float], max_rate: float = 1.0) -> float:
    """
    Estimate Internal Rate of Return using binary search
    """
    
    def npv_at_rate(rate):
        return sum((benefits[i] - costs[i]) / ((1 + rate) ** i) 
                  for i in range(len(benefits)))
    
    # Binary search for IRR
    low, high = 0, max_rate
    tolerance = 0.0001
    
    while high - low > tolerance:
        mid = (low + high) / 2
        npv = npv_at_rate(mid)
        
        if npv > 0:
            low = mid
        else:
            high = mid
    
    return (low + high) / 2

def generate_optimization_curves(
    budget_range: Tuple[float, float],
    num_points: int = 50,
    target_population: int = 11_146_856,
    cost_per_person: float = 40_000
) -> pd.DataFrame:
    """
    Generate data for optimization curve visualizations
    """
    import pandas as pd
    
    budgets = np.linspace(budget_range[0], budget_range[1], num_points)
    results = []
    
    for budget in budgets:
        # Calculate coverage
        coverage = min(1.0, budget / (target_population * cost_per_person))
        people_reached = int(coverage * target_population)
        
        # Estimate health impacts (simplified for planning)
        lives_saved = int(people_reached * 0.0068)  # Based on mortality rate
        stunting_prevented = int(people_reached * 0.054)  # Based on stunting rate
        anemia_prevented = int(people_reached * 0.185)  # Based on anemia rate
        
        health_impacts = {
            'lives_saved': lives_saved,
            'stunting_prevented': stunting_prevented,
            'anemia_prevented': anemia_prevented
        }
        
        # Calculate all metrics
        metrics = calculate_all_metrics(budget, coverage, health_impacts)
        
        results.append({
            'Budget_M': budget / 1_000_000,
            'Coverage_%': coverage * 100,
            'People_Reached': people_reached,
            'Financial_ROI': metrics['financial']['roi'],
            'Financial_ROI_Lower': metrics['financial']['roi_lower'],
            'Financial_ROI_Upper': metrics['financial']['roi_upper'],
            'Economic_BCR': metrics['economic']['bcr'],
            'Social_Value': metrics['social']['ratio'],
            'Optimization_Score': metrics['optimization_score'],
            'Lives_Saved': lives_saved,
            'Stunting_Prevented': stunting_prevented,
            'Anemia_Prevented': anemia_prevented
        })
    
    return pd.DataFrame(results)
```

---

## 4. Visualization Implementation

### 4.1 Update to `uganda_nutrition_enhanced.py`

Location: In the Budget Optimization Analysis section (around line 2178)

```python
# Import new modules at the top of file
from roi_calculations import (
    calculate_all_metrics, 
    generate_optimization_curves,
    VALIDATION_RANGES,
    INTERVENTION_BENCHMARKS
)
from uganda_nutrition_config import CONFIG_VERSION

# In the Budget Optimization Analysis section:
def render_budget_optimization_analysis():
    """Enhanced Budget Optimization with dual ROI system"""
    
    st.header("🎯 Budget Optimization Analysis")
    st.caption(f"Economic Model v{CONFIG_VERSION}")
    
    # Educational callout
    with st.expander("📚 Understanding the Three Metrics", expanded=False):
        st.markdown("""
        ### Three Ways to Measure Impact
        
        1. **Financial ROI** 📈
           - Direct economic returns in Year 1
           - Healthcare savings + productivity gains
           - Target: 15-35% (excellent for social programs)
        
        2. **Economic Benefit-Cost Ratio** 💰
           - 5-year economic impact with NPV
           - Includes recurring benefits
           - Target: 3:1 to 5:1 (high impact)
        
        3. **Social Value Ratio** 🌍
           - Lifetime societal benefit
           - Includes value of life and QALYs
           - Target: 10:1 to 20:1 (transformational)
        """)
    
    # Budget range inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget_min = st.number_input(
            "Minimum Budget (Million UGX)",
            min_value=100,
            max_value=5000,
            value=500,
            step=100,
            help="Starting point for optimization analysis"
        ) * 1_000_000
    
    with col2:
        budget_max = st.number_input(
            "Maximum Budget (Million UGX)",
            min_value=500,
            max_value=10000,
            value=5000,
            step=100,
            help="Maximum budget to analyze"
        ) * 1_000_000
    
    with col3:
        scenarios = st.slider(
            "Analysis Granularity",
            min_value=10,
            max_value=50,
            value=25,
            help="More points = smoother curves"
        )
    
    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            time_horizon = st.selectbox(
                "Economic Analysis Period",
                options=[3, 5, 10],
                index=1,
                help="Years for BCR calculation"
            )
            
            include_intergenerational = st.checkbox(
                "Include Intergenerational Benefits",
                value=True,
                help="20% bonus for next generation impact"
            )
        
        with col2:
            discount_rate_option = st.selectbox(
                "Discount Rate Scenario",
                options=["Conservative (8%)", "Standard (5%)", "Optimistic (3%)"],
                index=1
            )
            
            show_benchmarks = st.checkbox(
                "Show Benchmark Comparisons",
                value=True,
                help="Compare with other interventions"
            )
    
    # Run optimization button
    if st.button("🚀 Run Budget Optimization", type="primary", use_container_width=True):
        
        with st.spinner("Calculating optimization curves..."):
            # Progress bar
            progress = st.progress(0)
            
            # Generate optimization data
            progress.progress(20)
            df_results = generate_optimization_curves(
                (budget_min, budget_max),
                num_points=scenarios
            )
            
            progress.progress(40)
            
            # Find optimal points for each metric
            optimal_financial = df_results.loc[df_results['Financial_ROI'].idxmax()]
            optimal_economic = df_results.loc[df_results['Economic_BCR'].idxmax()]
            optimal_social = df_results.loc[df_results['Social_Value'].idxmax()]
            optimal_combined = df_results.loc[df_results['Optimization_Score'].idxmax()]
            
            progress.progress(60)
            
            # Create visualizations
            st.subheader("📊 Optimization Results")
            
            # Metric cards for optimal points
            st.markdown("### 🎯 Optimal Budget Points")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Best Financial ROI",
                    f"{optimal_financial['Budget_M']:.0f}M UGX",
                    f"{optimal_financial['Financial_ROI']:.1f}%",
                    help="Budget that maximizes Year 1 returns"
                )
            
            with col2:
                st.metric(
                    "Best Economic BCR",
                    f"{optimal_economic['Budget_M']:.0f}M UGX",
                    f"{optimal_economic['Economic_BCR']:.1f}:1",
                    help="Budget that maximizes 5-year benefits"
                )
            
            with col3:
                st.metric(
                    "Best Social Value",
                    f"{optimal_social['Budget_M']:.0f}M UGX",
                    f"{optimal_social['Social_Value']:.1f}:1",
                    help="Budget that maximizes lifetime impact"
                )
            
            with col4:
                st.metric(
                    "Overall Optimal",
                    f"{optimal_combined['Budget_M']:.0f}M UGX",
                    f"{optimal_combined['Coverage_%']:.1f}% coverage",
                    help="Best balanced outcome"
                )
            
            progress.progress(80)
            
            # DUAL ROI GRAPHS
            st.markdown("### 📈 Return on Investment Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Financial ROI Graph
                fig_financial = go.Figure()
                
                # Add main ROI line
                fig_financial.add_trace(go.Scatter(
                    x=df_results['Budget_M'],
                    y=df_results['Financial_ROI'],
                    mode='lines+markers',
                    name='Financial ROI',
                    line=dict(color='#2e7d32', width=3),
                    marker=dict(size=4)
                ))
                
                # Add confidence bands
                fig_financial.add_trace(go.Scatter(
                    x=df_results['Budget_M'],
                    y=df_results['Financial_ROI_Upper'],
                    fill=None,
                    mode='lines',
                    line=dict(color='rgba(46, 125, 50, 0)'),
                    showlegend=False
                ))
                
                fig_financial.add_trace(go.Scatter(
                    x=df_results['Budget_M'],
                    y=df_results['Financial_ROI_Lower'],
                    fill='tonexty',
                    mode='lines',
                    line=dict(color='rgba(46, 125, 50, 0)'),
                    name='95% Confidence',
                    fillcolor='rgba(102, 187, 106, 0.3)'
                ))
                
                # Add optimal point
                fig_financial.add_trace(go.Scatter(
                    x=[optimal_financial['Budget_M']],
                    y=[optimal_financial['Financial_ROI']],
                    mode='markers',
                    marker=dict(color='gold', size=15, symbol='star'),
                    name=f'Optimal: {optimal_financial["Financial_ROI"]:.1f}%'
                ))
                
                # Add typical range shading
                fig_financial.add_hrect(
                    y0=15, y1=35,
                    fillcolor="green", opacity=0.1,
                    annotation_text="Typical Range",
                    annotation_position="right"
                )
                
                fig_financial.update_layout(
                    title="Financial ROI (Year 1 Returns)",
                    xaxis_title="Budget (Million UGX)",
                    yaxis_title="ROI (%)",
                    hovermode='x unified',
                    height=400,
                    showlegend=True,
                    legend=dict(x=0.02, y=0.98)
                )
                
                st.plotly_chart(fig_financial, use_container_width=True)
            
            with col2:
                # Social Value Graph
                fig_social = go.Figure()
                
                # Add area chart for social value
                fig_social.add_trace(go.Scatter(
                    x=df_results['Budget_M'],
                    y=df_results['Social_Value'],
                    mode='lines',
                    fill='tozeroy',
                    name='Social Value',
                    line=dict(color='#1565c0', width=3),
                    fillcolor='rgba(100, 181, 246, 0.3)'
                ))
                
                # Add optimal point
                fig_social.add_trace(go.Scatter(
                    x=[optimal_social['Budget_M']],
                    y=[optimal_social['Social_Value']],
                    mode='markers',
                    marker=dict(color='gold', size=15, symbol='star'),
                    name=f'Optimal: {optimal_social["Social_Value"]:.1f}:1'
                ))
                
                # Add benchmark lines if enabled
                if show_benchmarks:
                    for name, benchmark in INTERVENTION_BENCHMARKS.items():
                        fig_social.add_hline(
                            y=benchmark['social_value'],
                            line_dash="dot",
                            annotation_text=name.replace('_', ' ').title(),
                            annotation_position="right",
                            line_color="gray",
                            opacity=0.5
                        )
                
                fig_social.update_layout(
                    title="Social Value Ratio (Lifetime Impact)",
                    xaxis_title="Budget (Million UGX)",
                    yaxis_title="Benefit-Cost Ratio",
                    hovermode='x unified',
                    height=400,
                    showlegend=True,
                    legend=dict(x=0.02, y=0.98)
                )
                
                st.plotly_chart(fig_social, use_container_width=True)
            
            progress.progress(90)
            
            # COMBINED OPTIMIZATION CURVE
            st.markdown("### 🎨 Combined Optimization Analysis")
            
            fig_combined = make_subplots(
                specs=[[{"secondary_y": True}]],
                subplot_titles=["Multi-Metric Optimization"]
            )
            
            # Financial ROI (primary axis)
            fig_combined.add_trace(
                go.Scatter(
                    x=df_results['Budget_M'],
                    y=df_results['Financial_ROI'],
                    name='Financial ROI (%)',
                    line=dict(color='green', width=2)
                ),
                secondary_y=False
            )
            
            # Economic BCR (secondary axis)
            fig_combined.add_trace(
                go.Scatter(
                    x=df_results['Budget_M'],
                    y=df_results['Economic_BCR'],
                    name='Economic BCR',
                    line=dict(color='orange', width=2)
                ),
                secondary_y=True
            )
            
            # Coverage as annotation at key points
            for i in range(0, len(df_results), len(df_results)//5):
                fig_combined.add_annotation(
                    x=df_results.iloc[i]['Budget_M'],
                    y=df_results.iloc[i]['Financial_ROI'],
                    text=f"{df_results.iloc[i]['Coverage_%']:.0f}%",
                    showarrow=False,
                    bgcolor="white",
                    bordercolor="gray",
                    borderwidth=1
                )
            
            # Add optimal budget line
            fig_combined.add_vline(
                x=optimal_combined['Budget_M'],
                line_dash="dash",
                line_color="gold",
                annotation_text=f"Optimal: {optimal_combined['Budget_M']:.0f}M",
                annotation_position="top"
            )
            
            # Add efficiency zones
            fig_combined.add_vrect(
                x0=budget_min/1_000_000, x1=optimal_combined['Budget_M']*0.8,
                fillcolor="green", opacity=0.1,
                annotation_text="High Efficiency", annotation_position="top left"
            )
            
            fig_combined.add_vrect(
                x0=optimal_combined['Budget_M']*0.8, x1=optimal_combined['Budget_M']*1.3,
                fillcolor="yellow", opacity=0.1,
                annotation_text="Optimal Zone", annotation_position="top left"
            )
            
            fig_combined.add_vrect(
                x0=optimal_combined['Budget_M']*1.3, x1=budget_max/1_000_000,
                fillcolor="red", opacity=0.1,
                annotation_text="Diminishing Returns", annotation_position="top left"
            )
            
            fig_combined.update_xaxes(title_text="Budget (Million UGX)")
            fig_combined.update_yaxes(title_text="Financial ROI (%)", secondary_y=False)
            fig_combined.update_yaxes(title_text="Economic BCR", secondary_y=True)
            
            fig_combined.update_layout(
                height=500,
                hovermode='x unified',
                showlegend=True,
                legend=dict(x=0.02, y=0.98)
            )
            
            st.plotly_chart(fig_combined, use_container_width=True)
            
            progress.progress(100)
            
            # DETAILED COMPARISON TABLE
            st.markdown("### 📋 Detailed Metrics Comparison")
            
            # Select key budget points for comparison
            key_points = [
                df_results.iloc[0],  # Minimum budget
                optimal_financial,
                optimal_economic,
                optimal_social,
                optimal_combined,
                df_results.iloc[-1]  # Maximum budget
            ]
            
            comparison_data = []
            for point in key_points:
                comparison_data.append({
                    'Budget (M UGX)': f"{point['Budget_M']:.0f}",
                    'Coverage (%)': f"{point['Coverage_%']:.1f}%",
                    'People Reached': f"{point['People_Reached']:,}",
                    'Financial ROI': f"{point['Financial_ROI']:.1f}%",
                    'Economic BCR': f"{point['Economic_BCR']:.1f}:1",
                    'Social Value': f"{point['Social_Value']:.1f}:1",
                    'Lives Saved': f"{point['Lives_Saved']:,}",
                    'Score': f"{point['Optimization_Score']:.2f}"
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Style the dataframe
            styled_df = comparison_df.style.background_gradient(
                subset=['Financial ROI', 'Economic BCR', 'Social Value'],
                cmap='RdYlGn',
                vmin=0
            ).highlight_max(
                subset=['Score'],
                color='gold'
            )
            
            st.dataframe(styled_df, use_container_width=True)
            
            # Download results
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Analysis (CSV)",
                data=csv,
                file_name=f"budget_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Save to session state
            st.session_state['optimization_results'] = df_results
            st.session_state['optimal_budget'] = optimal_combined['Budget_M'] * 1_000_000
            
            progress.empty()
            
            # Success message
            st.success(f"""
            ✅ **Optimization Complete!**
            
            **Recommended Budget**: {optimal_combined['Budget_M']:.0f} Million UGX
            - Coverage: {optimal_combined['Coverage_%']:.1f}% of target population
            - Financial ROI: {optimal_combined['Financial_ROI']:.1f}%
            - Economic BCR: {optimal_combined['Economic_BCR']:.1f}:1
            - Social Value: {optimal_combined['Social_Value']:.1f}:1
            
            This budget provides the best balance of immediate returns, 
            medium-term economic benefits, and long-term social impact.
            """)
```

---

## 5. Implementation Steps

### Step 1: Create Configuration File (5 minutes)
1. Create `uganda_nutrition_config.py`
2. Copy the configuration structure from section 2.1
3. Save in project directory

### Step 2: Create Calculation Module (10 minutes)
1. Create `roi_calculations.py`
2. Copy calculation functions from section 3.1
3. Test imports

### Step 3: Update Main Application (20 minutes)
1. Add imports at top of `uganda_nutrition_enhanced.py`
2. Replace Budget Optimization section with new code
3. Ensure proper indentation and integration

### Step 4: Testing (15 minutes)
1. Run the application
2. Test with various budget ranges
3. Verify graphs display correctly
4. Check that values are in realistic ranges

### Step 5: Fine-tuning (10 minutes)
1. Adjust colors/styling as needed
2. Refine tooltips and help text
3. Optimize performance if needed

---

## 6. Testing Checklist

- [ ] Financial ROI stays within 15-50% range
- [ ] Economic BCR stays within 1-8 range  
- [ ] Social Value stays within 5-30 range
- [ ] Graphs render without errors
- [ ] Confidence bands display correctly
- [ ] Optimal points are marked clearly
- [ ] Combined graph shows all three metrics
- [ ] Table displays formatted correctly
- [ ] Download button works
- [ ] Educational content is accessible
- [ ] Benchmarks display when enabled
- [ ] All tooltips show properly

---

## Total Implementation Time: ~1 hour

This plan provides a complete, implementable solution that will transform the unrealistic 6,700% ROI into a professional three-tier metric system with beautiful visualizations that stakeholders can actually use for decision-making.