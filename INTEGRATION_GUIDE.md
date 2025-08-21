# Dynamic Data Integration Guide

## How to Replace Hardcoded Values with Dynamic Data

### 1. Import the Dynamic Data Provider

```python
from dynamic_data_integration import get_data_provider

# Initialize at the start of your app
data_provider = get_data_provider()
```

### 2. Replace Population Constants

**OLD CODE:**
```python
UGANDA_POPULATION = 47_000_000
STUNTED_CHILDREN = int(UGANDA_POPULATION * 0.14 * 0.29)
CHILDREN_UNDER_5 = int(UGANDA_POPULATION * 0.15)
```

**NEW CODE:**
```python
# Get dynamic population data
pop_constants = data_provider.get_population_constants()
UGANDA_POPULATION = pop_constants['UGANDA_POPULATION']
STUNTED_CHILDREN = pop_constants['STUNTED_CHILDREN']
CHILDREN_UNDER_5 = pop_constants['CHILDREN_UNDER_5']
```

### 3. Replace Intervention Details

**OLD CODE:**
```python
def get_intervention_details():
    return {
        'fortification': {
            'unit_cost': 15,
            'effectiveness': 0.75,
            # ... hardcoded values
        }
    }
```

**NEW CODE:**
```python
def get_intervention_details():
    return data_provider.get_intervention_details()
```

### 4. Replace Health Outcome Calculations

**OLD CODE:**
```python
def calculate_health_outcomes(budget, population, intervention_mix, selected_nutrients):
    # Hardcoded calculations
    mortality_reduction_rate = 0.15
    lives_saved = int(coverage * total_effectiveness * baseline_u5_deaths * mortality_reduction_rate)
```

**NEW CODE:**
```python
def calculate_health_outcomes(budget, population, intervention_mix, selected_nutrients):
    return data_provider.calculate_health_outcomes(
        budget, population, intervention_mix, selected_nutrients
    )
```

### 5. Replace Monitoring Metrics

**OLD CODE:**
```python
def generate_monitoring_metrics(intervention_data, time_period):
    metrics = {
        'coverage_rate': np.random.uniform(45, 75),
        'compliance_rate': np.random.uniform(65, 85),
        # ... random values
    }
```

**NEW CODE:**
```python
def generate_monitoring_metrics(intervention_data, time_period):
    return data_provider.get_monitoring_metrics(intervention_data, time_period)
```

### 6. Replace Staffing Requirements

**OLD CODE:**
```python
staffing_requirements = {
    'Nutritionists': int(coverage_population / 50000),
    'Community Health Workers': int(coverage_population / 500),
    'Lab Technicians': 50,  # Fixed number
}
```

**NEW CODE:**
```python
staffing_requirements = data_provider.get_staffing_requirements(coverage_population)
```

### 7. Replace KPI Targets

**OLD CODE:**
```python
kpi_data = {
    'Target': ['80%', '70%', '95%', '<5%', '<$20', '20%', '15%', '25%'],
}
```

**NEW CODE:**
```python
kpi_targets = data_provider.get_kpi_targets()
kpi_data = {
    'Target': list(kpi_targets.values()),
}
```

### 8. Replace Financial Projections

**OLD CODE:**
```python
costs = [total_budget * 0.8 if i == 0 else total_budget * 0.2 for i in years]
benefits = [total_budget * 0.3 * (1 + i * 0.2) for i in years]
irr = 0.15 if npv > 0 else 0.05
```

**NEW CODE:**
```python
financial_projections = data_provider.get_financial_projections(total_budget, len(years))
costs = financial_projections['costs']
benefits = financial_projections['benefits']
npv = financial_projections['npv']
irr = financial_projections['irr']
```

### 9. Replace Scenario Analysis

**OLD CODE:**
```python
scenarios = {
    'Best Case': {'probability': 0.25, 'impact': 1.3, 'color': 'green'},
    'Expected': {'probability': 0.50, 'impact': 1.0, 'color': 'blue'},
    'Worst Case': {'probability': 0.25, 'impact': 0.6, 'color': 'red'}
}
```

**NEW CODE:**
```python
scenarios = data_provider.get_scenario_analysis()
```

### 10. Replace Gauge Values

**OLD CODE:**
```python
value = 65,  # Hardcoded coverage rate
value = 72,  # Hardcoded compliance
```

**NEW CODE:**
```python
gauge_values = data_provider.get_gauge_values()
value = gauge_values['coverage_rate'],
value = gauge_values['compliance'],
```

### 11. Replace Success Metrics

**OLD CODE:**
```python
success_metrics = pd.DataFrame({
    'Baseline (2020)': ['29%', '28%', '37% deficient', '0%', 'N/A'],
    'Current (2024)': ['26%', '24%', '31% deficient', '45%', '$18/person'],
    # ... hardcoded values
})
```

**NEW CODE:**
```python
success_metrics = data_provider.get_success_metrics_table()
```

### 12. Replace Live Data Feed

**OLD CODE:**
```python
live_data = pd.DataFrame({
    'Value': [
        np.random.randint(100, 500),  # Random beneficiaries
        np.random.randint(1000, 5000),  # Random supplies
    ]
})
```

**NEW CODE:**
```python
live_data = data_provider.get_live_data_feed()
```

## Complete Integration Example

Here's how to integrate everything in your main app:

```python
import streamlit as st
from dynamic_data_integration import get_data_provider

# Initialize once at app start
@st.cache_resource
def init_data_provider():
    return get_data_provider()

data_provider = init_data_provider()

# Use throughout your app
def main():
    # Get all dynamic constants
    pop_constants = data_provider.get_population_constants()
    
    # Use in calculations
    health_outcomes = data_provider.calculate_health_outcomes(
        budget=st.session_state.budget,
        population=pop_constants['UGANDA_POPULATION'],
        intervention_mix=st.session_state.intervention_mix,
        selected_nutrients=st.session_state.selected_nutrients
    )
    
    # Display dynamic metrics
    st.metric("Lives Saved", health_outcomes['lives_saved'])
    st.metric("Coverage", f"{health_outcomes['coverage']:.1f}%")
    
    # Get real-time monitoring data
    monitoring = data_provider.get_monitoring_metrics({}, 'current')
    st.metric("Compliance Rate", f"{monitoring['compliance_rate']:.1f}%")
```

## Benefits of This Approach

1. **Real-time Updates**: Data automatically adjusts based on current year and trends
2. **Evidence-based**: Values derived from WHO standards and research
3. **Context-aware**: Adjusts for rural/urban, program phase, and district specifics
4. **Scalable**: Easy to add new data sources and parameters
5. **Maintainable**: All data logic centralized in configuration modules
6. **Testable**: Can mock data provider for testing
7. **Realistic**: No more arbitrary random ranges - all based on actual distributions

## Advanced Features

### District-Specific Data
```python
district_data = data_provider.get_district_data('KAMPALA')
# Returns stunting rate, poverty rate, health access specific to Kampala
```

### Program Phase Awareness
```python
# Automatically adjusts metrics based on program maturity
st.session_state.program_phase = 'scale_up'
metrics = data_provider.get_monitoring_metrics({}, 'current')
# Returns more optimistic but realistic metrics for scale-up phase
```

### Supply Chain Parameters
```python
supply_params = data_provider.config.get_supply_chain_parameters()
# Returns warehouse capacities, distribution frequencies, transport costs
```

## Testing the Integration

```python
# Test with different scenarios
def test_dynamic_values():
    provider = get_data_provider()
    
    # Test population grows over time
    pop_2024 = provider.get_population_constants()['UGANDA_POPULATION']
    assert pop_2024 > 47_000_000  # Should be higher than 2020 census
    
    # Test intervention costs include inflation
    costs = provider.get_intervention_costs('fortification')
    assert costs['unit_cost'] > 12  # Base cost with inflation
    
    # Test health outcomes are realistic
    outcomes = provider.calculate_health_outcomes(
        budget=1_000_000,
        population=1_000_000,
        intervention_mix={'fortification': 100},
        selected_nutrients=['Iron', 'Vitamin_A']
    )
    assert 0 <= outcomes['coverage'] <= 100
    assert outcomes['lives_saved'] > 0
```

## Migration Checklist

- [ ] Import dynamic_data_integration module
- [ ] Initialize data_provider at app start
- [ ] Replace population constants
- [ ] Replace intervention details function
- [ ] Replace health outcome calculations
- [ ] Replace monitoring metrics generation
- [ ] Replace staffing requirements
- [ ] Replace KPI targets
- [ ] Replace financial projections
- [ ] Replace scenario analysis
- [ ] Replace gauge values
- [ ] Replace success metrics table
- [ ] Replace live data feed
- [ ] Test all replaced values
- [ ] Verify realistic ranges
- [ ] Check district-specific features