#!/usr/bin/env python3
"""
Test script to verify economic metrics calculations
"""

import numpy as np

# Configuration
CONFIG = {
    'kenya_population': 52_000_000,
    'children_under_5': 7_280_000,
    'pregnant_women': 1_768_000,
    'women_reproductive_age': 13_520_000,
    'rural_population': 37_960_000,
    'iodine_deficiency_rate': 1.0,
    'cretinism_rate_per_1000_births': 13.1,
    'annual_births': 1_300_000,
    'gdp_per_capita': 1_879,
    'total_gdp': 97_708_000_000,
    'health_budget': 4_885_400_000,
    'disability_weight_cretinism': 0.8,
    'daly_per_case': 35.2,
    'productivity_loss_per_iq': 0.02,
    'avg_iq_gain_potential': 12.0,
    'cost_per_daly_threshold': 100,
    'willingness_to_pay': 100_000,
    'discount_rate': 0.03
}

def calculate_dynamic_cost_per_outcome(budget, coverage, efficiency, context):
    """Calculate dynamic cost per outcome with realistic formulas"""
    
    # Get population targets
    population = context.get('population', CONFIG['kenya_population'])
    
    # Calculate pregnancies reached (primary prevention target)
    annual_pregnancies = CONFIG['annual_births'] * 1.1  # Account for pregnancy loss
    pregnancies_reached = annual_pregnancies * coverage * (efficiency / 100)
    
    # Base prevention rate from WHO data (iodine prevents ~70% of cretinism when properly implemented)
    base_prevention_rate = CONFIG['cretinism_rate_per_1000_births'] / 1000  # Convert to rate
    
    # Quality factors affecting prevention effectiveness
    quality_factors = {
        'coverage_quality': min(1.0, coverage * 1.2),  # Better coverage improves quality
        'implementation_quality': efficiency / 100,
        'intervention_effectiveness': 0.7,  # WHO estimate for iodine intervention
        'compliance_rate': 0.85,  # Real-world compliance
        'supply_chain_reliability': 0.9  # Account for supply issues
    }
    
    # Use geometric mean instead of product to avoid excessive punishment
    # This gives a more balanced quality score
    quality_multiplier = np.power(np.prod(list(quality_factors.values())), 1/len(quality_factors))
    
    # Effective prevention rate
    effective_prevention_rate = base_prevention_rate * quality_multiplier
    
    # Calculate cases prevented (no extra division by 1000!)
    cases_prevented = pregnancies_reached * effective_prevention_rate
    
    # Ensure minimum cases for very small programs
    cases_prevented = max(cases_prevented, pregnancies_reached * 0.001)  # At least 0.1% prevention
    
    # Cost per case prevented
    cost_per_case = budget / max(cases_prevented, 1)
    
    print(f"\nDetailed Calculation:")
    print(f"Budget: {budget:,.0f} KSH")
    print(f"Annual pregnancies: {annual_pregnancies:,.0f}")
    print(f"Pregnancies reached: {pregnancies_reached:,.0f}")
    print(f"Base prevention rate: {base_prevention_rate:.4f} ({CONFIG['cretinism_rate_per_1000_births']:.1f} per 1000)")
    print(f"Quality factors: {quality_factors}")
    print(f"Quality multiplier (geometric mean): {quality_multiplier:.4f}")
    print(f"Effective prevention rate: {effective_prevention_rate:.4f}")
    print(f"Cases prevented: {cases_prevented:.1f}")
    print(f"Cost per case: {cost_per_case:,.0f} KSH")
    
    return {
        'cost_per_case': cost_per_case,
        'cases_prevented': cases_prevented,
        'pregnancies_reached': pregnancies_reached,
        'quality_score': quality_multiplier
    }

def calculate_roi_timeline(budget, efficiency, coverage, timeline_months):
    """Calculate ROI over time with realistic assumptions"""
    
    years = min(10, max(1, timeline_months // 12))
    annual_budget = budget / max(years, 1)
    
    # Calculate health outcomes
    result = calculate_dynamic_cost_per_outcome(annual_budget, coverage, efficiency, {'population': CONFIG['kenya_population']})
    annual_cases_prevented = result['cases_prevented']
    
    # Economic benefits per case prevented
    productivity_gain_per_case = CONFIG['gdp_per_capita'] * CONFIG['productivity_loss_per_iq'] * CONFIG['avg_iq_gain_potential']
    healthcare_savings_per_case = CONFIG['daly_per_case'] * CONFIG['cost_per_daly_threshold']
    social_value_per_case = CONFIG['willingness_to_pay'] * 0.1  # Conservative social value
    
    total_value_per_case = productivity_gain_per_case + healthcare_savings_per_case + social_value_per_case
    
    print(f"\nEconomic Benefits per Case:")
    print(f"Productivity gain: {productivity_gain_per_case:,.0f} KSH")
    print(f"Healthcare savings: {healthcare_savings_per_case:,.0f} KSH")
    print(f"Social value: {social_value_per_case:,.0f} KSH")
    print(f"Total value per case: {total_value_per_case:,.0f} KSH")
    
    roi_timeline = []
    cumulative_cost = 0
    cumulative_benefit = 0
    
    for year in range(1, years + 1):
        # Year-specific adjustments
        if year == 1:
            # First year: high setup costs, low benefits
            yearly_cost = annual_budget * 1.3  # 30% overhead for setup
            yearly_benefit = annual_cases_prevented * total_value_per_case * 0.3  # Only 30% of benefits realized
            realization_rate = 0.3
        elif year == 2:
            # Second year: normalizing
            yearly_cost = annual_budget * 1.1
            yearly_benefit = annual_cases_prevented * total_value_per_case * 0.6
            realization_rate = 0.6
        else:
            # Subsequent years: full operation
            yearly_cost = annual_budget
            yearly_benefit = annual_cases_prevented * total_value_per_case * min(1.0, 0.8 + year * 0.05)
            realization_rate = min(1.0, 0.8 + year * 0.05)
        
        # Apply discount rate
        discount_factor = 1 / ((1 + CONFIG['discount_rate']) ** year)
        yearly_cost *= discount_factor
        yearly_benefit *= discount_factor
        
        cumulative_cost += yearly_cost
        cumulative_benefit += yearly_benefit
        
        roi = ((cumulative_benefit - cumulative_cost) / cumulative_cost) * 100
        
        roi_timeline.append({
            'year': year,
            'cost': yearly_cost,
            'benefit': yearly_benefit,
            'cumulative_cost': cumulative_cost,
            'cumulative_benefit': cumulative_benefit,
            'roi': roi,
            'realization_rate': realization_rate
        })
        
        print(f"\nYear {year}:")
        print(f"  Cost: {yearly_cost:,.0f} KSH")
        print(f"  Benefit: {yearly_benefit:,.0f} KSH")
        print(f"  Cumulative ROI: {roi:.1f}%")
    
    return roi_timeline

# Test with typical values
print("=" * 80)
print("TESTING ECONOMIC METRICS WITH TYPICAL VALUES")
print("=" * 80)

# Typical scenario
budget = 500_000_000  # 500M KSH
coverage = 0.7  # 70% coverage
efficiency = 70  # 70% efficiency
timeline_months = 60  # 5 years

print(f"\nTest Parameters:")
print(f"Budget: {budget:,.0f} KSH")
print(f"Coverage: {coverage*100:.0f}%")
print(f"Efficiency: {efficiency:.0f}%")
print(f"Timeline: {timeline_months} months")

# Calculate cost per outcome
metrics = calculate_dynamic_cost_per_outcome(budget, coverage, efficiency, {'population': CONFIG['kenya_population']})

print(f"\n" + "=" * 40)
print(f"COST PER CRETINISM PREVENTED: {metrics['cost_per_case']:,.0f} KSH")
print(f"CASES PREVENTED: {metrics['cases_prevented']:.0f}")
print(f"=" * 40)

# Calculate ROI timeline
print(f"\n" + "=" * 80)
print("ROI TIMELINE ANALYSIS")
print("=" * 80)

roi_data = calculate_roi_timeline(budget, efficiency, coverage, timeline_months)

print(f"\n" + "=" * 40)
print(f"YEAR 1 ROI: {roi_data[0]['roi']:.1f}%")
print(f"YEAR 5 ROI: {roi_data[-1]['roi']:.1f}%" if len(roi_data) >= 5 else "N/A")
print(f"=" * 40)

# Validate metrics
print(f"\n" + "=" * 80)
print("VALIDATION RESULTS")
print("=" * 80)

issues = []

if metrics['cost_per_case'] > 500_000:
    issues.append(f"❌ Cost per case too high: {metrics['cost_per_case']:,.0f} KSH (should be < 500,000)")
else:
    print(f"✅ Cost per case reasonable: {metrics['cost_per_case']:,.0f} KSH")

if metrics['cases_prevented'] < 1000:
    issues.append(f"❌ Cases prevented too low: {metrics['cases_prevented']:.0f} (should be > 1,000)")
else:
    print(f"✅ Cases prevented reasonable: {metrics['cases_prevented']:.0f}")

if roi_data[0]['roi'] > 0:
    issues.append(f"❌ Year 1 ROI should be negative: {roi_data[0]['roi']:.1f}%")
else:
    print(f"✅ Year 1 ROI correctly negative: {roi_data[0]['roi']:.1f}%")

if issues:
    print(f"\n⚠️ ISSUES FOUND:")
    for issue in issues:
        print(f"  {issue}")
else:
    print(f"\n✅ ALL METRICS VALIDATED SUCCESSFULLY!")