"""
Test and demonstrate the dynamic data system
Run this to see how values change realistically
"""

import pandas as pd
import numpy as np
from dynamic_data_integration import get_data_provider
from uganda_nutrition_config import get_config
from datetime import datetime

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def main():
    # Initialize providers
    data_provider = get_data_provider()
    config = get_config()
    
    print_section("DYNAMIC POPULATION DATA (Updates with Current Year)")
    pop_data = data_provider.get_population_constants()
    for key, value in pop_data.items():
        print(f"{key:20} : {value:,}")
    
    print_section("INTERVENTION COSTS (With Inflation & Context)")
    for intervention in ['fortification', 'supplementation', 'education', 'biofortification']:
        costs = config.get_intervention_costs(intervention)
        rural_costs = config.get_intervention_costs(intervention, 'KOTIDO')  # Rural district
        urban_costs = config.get_intervention_costs(intervention, 'KAMPALA')  # Urban district
        print(f"\n{intervention.upper()}:")
        print(f"  Base Cost: ${costs['unit_cost']:.2f}")
        print(f"  Rural Cost (Kotido): ${rural_costs['unit_cost']:.2f}")
        print(f"  Urban Cost (Kampala): ${urban_costs['unit_cost']:.2f}")
        print(f"  Effectiveness: {costs['effectiveness']:.1%}")
    
    print_section("HEALTH OUTCOMES (Evidence-Based Calculations)")
    outcomes = data_provider.calculate_health_outcomes(
        budget=5_000_000,
        population=1_000_000,
        intervention_mix={'fortification': 50, 'supplementation': 30, 'education': 20},
        selected_nutrients=['Iron_(mg)', 'Vitamin_A_(mcg)', 'Zinc_(mg)']
    )
    for key, value in outcomes.items():
        if isinstance(value, float):
            if 'cost' in key:
                print(f"{key:25} : ${value:,.2f}")
            else:
                print(f"{key:25} : {value:.2f}")
        else:
            print(f"{key:25} : {value:,}")
    
    print_section("MONITORING METRICS BY PROGRAM PHASE")
    for phase in ['pilot', 'implementation', 'scale_up', 'mature']:
        metrics = config.get_monitoring_metrics(phase)
        print(f"\n{phase.upper()} PHASE:")
        print(f"  Coverage: {metrics['coverage_rate']:.1f}%")
        print(f"  Compliance: {metrics['compliance_rate']:.1f}%")
        print(f"  Quality Score: {metrics['quality_scores']:.1f}")
        print(f"  Stunting Reduction: {metrics['impact_indicators']['stunting_reduction']:.1f}%")
    
    print_section("STAFFING REQUIREMENTS (WHO Standards Adapted)")
    staff = data_provider.get_staffing_requirements(500_000)
    for role, count in staff.items():
        ratio = 500_000 / count if count > 0 else 0
        print(f"{role:30} : {count:,} staff (1 per {ratio:,.0f} people)")
    
    print_section("KPI TARGETS (Progressive by Year)")
    for year in [1, 2, 3, 5]:
        targets = config.get_kpi_targets(year)
        print(f"\nYEAR {year} TARGETS:")
        print(f"  Coverage: {targets['coverage_rate']*100:.0f}%")
        print(f"  Compliance: {targets['compliance_rate']*100:.0f}%")
        print(f"  Cost/Beneficiary: ${targets['cost_per_beneficiary']:.0f}")
        print(f"  Stunting Reduction: {targets['stunting_reduction']*100:.1f}%")
    
    print_section("FINANCIAL PROJECTIONS (Realistic NPV/IRR)")
    financial = data_provider.get_financial_projections(10_000_000, 5)
    print(f"Base Budget: $10,000,000")
    print(f"NPV: ${financial['npv']:,.0f}")
    print(f"IRR: {financial['irr']*100:.1f}%")
    print(f"Payback Period: {financial['payback_period']} years")
    print(f"Benefit-Cost Ratio: {financial['benefit_cost_ratio']:.2f}x")
    print("\nYear-by-Year Cash Flow:")
    for i, (cost, benefit) in enumerate(zip(financial['costs'], financial['benefits'])):
        net = benefit - cost
        print(f"  Year {i}: Cost=${cost:,.0f}, Benefit=${benefit:,.0f}, Net=${net:,.0f}")
    
    print_section("SCENARIO ANALYSIS (Risk-Adjusted)")
    scenarios = data_provider.get_scenario_analysis()
    for name, params in scenarios.items():
        print(f"\n{name}:")
        print(f"  Probability: {params['probability']*100:.0f}%")
        print(f"  Impact Multiplier: {params['impact']:.2f}x")
        print(f"  Cost Multiplier: {params['cost']:.2f}x")
        print(f"  Timeline Multiplier: {params['timeline']:.2f}x")
    
    print_section("DISTRICT-SPECIFIC DATA")
    districts = ['KAMPALA', 'KOTIDO', 'MBARARA', 'GULU']
    for district in districts:
        data = config.get_district_specific_data(district)
        is_rural = config.is_rural_district(district)
        print(f"\n{district} ({'Rural' if is_rural else 'Urban'}):")
        print(f"  Stunting Rate: {data['stunting_rate']*100:.1f}%")
        print(f"  Poverty Rate: {data['poverty_rate']*100:.1f}%")
        print(f"  Health Facility Access: {data['health_facility_access']*100:.0f}%")
        print(f"  Food Security Index: {data['food_security_index']:.2f}")
    
    print_section("LIVE DATA FEED (Realistic Daily Metrics)")
    live_data = data_provider.get_live_data_feed()
    print("\nCurrent Activity:")
    for _, row in live_data.iterrows():
        print(f"  {row['Metric']:25} : {row['Value']:,} ({row['Status']})")
    
    print_section("SUCCESS METRICS TABLE (Trend-Based)")
    success_table = data_provider.get_success_metrics_table()
    print("\n" + success_table.to_string(index=False))
    
    print_section("COMPARISON: OLD vs NEW VALUES")
    print("\nPopulation Constants:")
    print(f"  OLD: Fixed 47,000,000")
    print(f"  NEW: {pop_data['UGANDA_POPULATION']:,} (grows annually)")
    
    print("\nIntervention Costs:")
    print(f"  OLD: Fortification = $15 (fixed)")
    print(f"  NEW: Fortification = ${config.get_intervention_costs('fortification')['unit_cost']:.2f} (inflation-adjusted)")
    
    print("\nHealth Impact:")
    print(f"  OLD: Mortality reduction = 15% (fixed)")
    print(f"  NEW: Mortality reduction = {outcomes['lives_saved']/1000:.1f} per 1000 (evidence-based)")
    
    print("\nMonitoring Metrics:")
    print(f"  OLD: Coverage = random(45, 75)")
    metrics = config.get_monitoring_metrics('implementation')
    print(f"  NEW: Coverage = {metrics['coverage_rate']:.1f}% (phase-based)")
    
    print("\nFinancial Analysis:")
    print(f"  OLD: IRR = 15% if positive, else 5%")
    print(f"  NEW: IRR = {financial['irr']*100:.1f}% (calculated from cash flows)")
    
    print("\n" + "="*60)
    print("  All values now update dynamically based on:")
    print("  - Current year and trends")
    print("  - Program phase and maturity")
    print("  - District characteristics")
    print("  - Evidence-based research")
    print("  - Economic indicators")
    print("="*60)

if __name__ == "__main__":
    main()