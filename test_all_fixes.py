"""
Comprehensive Test Suite for Uganda Intervention Engine Fixes
Tests all critical fixes and improvements made to the system
"""

import sys
import pandas as pd
import numpy as np
from typing import Dict, List
import json

print("="*80)
print("COMPREHENSIVE TEST SUITE - INTERVENTION ENGINE FIXES")
print("="*80)

# Track test results
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test_passed(test_name: str, details: str = ""):
    """Record a passed test"""
    test_results['passed'].append(test_name)
    print(f"✅ PASS: {test_name}")
    if details:
        print(f"         {details}")

def test_failed(test_name: str, error: str):
    """Record a failed test"""
    test_results['failed'].append(test_name)
    print(f"❌ FAIL: {test_name}")
    print(f"         Error: {error}")

def test_warning(test_name: str, warning: str):
    """Record a test warning"""
    test_results['warnings'].append(test_name)
    print(f"⚠️  WARN: {test_name}")
    print(f"         {warning}")

# ==============================================================================
# TEST 1: Staffing Calculation Fix
# ==============================================================================
print("\n" + "="*60)
print("TEST 1: STAFFING CALCULATION FIX")
print("-"*60)

try:
    from uganda_nutrition_config import get_config
    config = get_config()
    
    # Test with realistic population
    test_population = 500000
    staffing = config.get_staffing_requirements(test_population)
    
    # Check that all staffing numbers are reasonable
    all_reasonable = True
    for role, count in staffing.items():
        if count > test_population:  # No role should need more staff than population
            test_failed(
                "Staffing Calculation",
                f"{role} requires {count} staff for {test_population} people (impossible!)"
            )
            all_reasonable = False
            break
        
        # Check specific ratios
        if role == 'Nutritionists' and count != max(1, test_population // 40000):
            test_warning(
                "Nutritionist Ratio",
                f"Expected {test_population//40000}, got {count}"
            )
    
    if all_reasonable:
        test_passed(
            "Staffing Calculation",
            f"All staffing numbers reasonable (e.g., Nutritionists: {staffing.get('Nutritionists', 0)})"
        )
        
except Exception as e:
    test_failed("Staffing Calculation", str(e))

# ==============================================================================
# TEST 2: Session State and Outcomes Variable Fix
# ==============================================================================
print("\n" + "="*60)
print("TEST 2: SESSION STATE AND OUTCOMES VARIABLE")
print("-"*60)

try:
    # Check if session state initialization is in place
    with open('uganda_intervention_engine.py', 'r') as f:
        content = f.read()
        
    if "'simulation_outcomes' not in st.session_state" in content:
        test_passed("Session State Initialization", "simulation_outcomes properly initialized")
    else:
        test_failed("Session State Initialization", "simulation_outcomes not found in session state init")
    
    # Check if outcomes are saved to session state
    if "st.session_state.simulation_outcomes = outcomes" in content:
        test_passed("Outcomes Saved to Session", "Outcomes properly saved after simulation")
    else:
        test_failed("Outcomes Saved to Session", "Outcomes not saved to session state")
        
    # Check if report generation checks for outcomes
    if "'simulation_outcomes' not in st.session_state or st.session_state.simulation_outcomes is None" in content:
        test_passed("Report Generation Check", "Properly checks for outcomes before generating report")
    else:
        test_failed("Report Generation Check", "Missing outcomes validation in report generation")
        
except Exception as e:
    test_failed("Session State Tests", str(e))

# ==============================================================================
# TEST 3: Real Data Provider Percentage Fix
# ==============================================================================
print("\n" + "="*60)
print("TEST 3: REAL DATA PROVIDER PERCENTAGE CALCULATIONS")
print("-"*60)

try:
    from real_data_provider import UgandaRealDataProvider
    provider = UgandaRealDataProvider()
    
    # Test intervention effectiveness
    effectiveness = provider.get_intervention_effectiveness()
    
    # Check fortification population reached
    if 'fortification' in effectiveness:
        fort_data = effectiveness['fortification']
        if 'population_reached_percent' in fort_data:
            percent = fort_data['population_reached_percent']
            if 0 <= percent <= 100:
                test_passed(
                    "Fortification Percentage",
                    f"Population reached: {percent:.1f}% (valid range)"
                )
            else:
                test_failed(
                    "Fortification Percentage",
                    f"Invalid percentage: {percent}%"
                )
        else:
            test_warning(
                "Fortification Percentage",
                "Using old 'population_reached' key instead of 'population_reached_percent'"
            )
    
    # Test pregnancy rate
    pop_constants = provider.get_population_constants()
    pregnancy_rate = pop_constants['PREGNANT_WOMEN'] / pop_constants['UGANDA_POPULATION']
    
    if 0.02 <= pregnancy_rate <= 0.06:  # 2-6% is reasonable range
        test_passed(
            "Pregnancy Rate Fix",
            f"Pregnancy rate: {pregnancy_rate*100:.1f}% (realistic)"
        )
    else:
        test_failed(
            "Pregnancy Rate Fix",
            f"Pregnancy rate {pregnancy_rate*100:.1f}% is unrealistic"
        )
        
except Exception as e:
    test_failed("Real Data Provider Tests", str(e))

# ==============================================================================
# TEST 4: Supply Chain Optimization Module
# ==============================================================================
print("\n" + "="*60)
print("TEST 4: SUPPLY CHAIN OPTIMIZATION MODULE")
print("-"*60)

try:
    from supply_chain_optimizer import SupplyChainOptimizer, DistributionHub
    
    # Create test data
    test_facilities = pd.DataFrame({
        'District': ['KAMPALA', 'WAKISO', 'MUKONO'],
        'HOSPITAL': [5, 3, 2],
        'HC_IV': [10, 8, 5],
        'HC_III': [20, 15, 12]
    })
    
    test_population = pd.DataFrame({
        'ADM2_EN': ['KAMPALA', 'WAKISO', 'MUKONO'],
        'T_TL': [1650000, 2000000, 600000]
    })
    
    # Initialize optimizer
    optimizer = SupplyChainOptimizer(test_facilities, test_population)
    
    # Test network creation
    if optimizer.network.number_of_nodes() > 0:
        test_passed(
            "Supply Chain Network Creation",
            f"Network created with {optimizer.network.number_of_nodes()} nodes"
        )
    else:
        test_failed("Supply Chain Network Creation", "No nodes in network")
    
    # Test distribution optimization
    test_demand = {'KAMPALA': 1000, 'WAKISO': 1500, 'MUKONO': 500}
    plan = optimizer.optimize_distribution(
        demand=test_demand,
        budget=10000,
        priority_districts=['KAMPALA']
    )
    
    if 'coverage' in plan and plan['coverage'] > 0:
        test_passed(
            "Distribution Optimization",
            f"Achieved {plan['coverage']:.1f}% coverage"
        )
    else:
        test_failed("Distribution Optimization", "No coverage achieved")
    
    # Test bottleneck analysis
    bottlenecks = optimizer.analyze_bottlenecks()
    if isinstance(bottlenecks, dict):
        test_passed(
            "Bottleneck Analysis",
            f"Found {sum(len(v) for v in bottlenecks.values())} bottlenecks"
        )
    else:
        test_failed("Bottleneck Analysis", "Invalid bottleneck analysis output")
        
except Exception as e:
    test_failed("Supply Chain Module Tests", str(e))

# ==============================================================================
# TEST 5: Economic ROI Calculations
# ==============================================================================
print("\n" + "="*60)
print("TEST 5: ECONOMIC ROI CALCULATIONS")
print("-"*60)

try:
    # Load and test the intervention engine's economic calculations
    import uganda_intervention_engine as engine
    
    # Create a simulator instance
    nutrition_df = pd.read_csv('uganda-consumption-adequacy-all-nutrients.csv')
    population_df = pd.read_csv('ug2/uga_admpop_adm2_2023.csv')
    facilities_df = pd.read_csv('ug2/national-health-facility-master-list-2018-health-facility-level-by-district.csv')
    
    optimizer = engine.MultiNutrientOptimizer(nutrition_df, population_df, facilities_df)
    simulator = engine.InterventionSimulator(optimizer)
    
    # Test economic benefit calculation with realistic values
    test_lives = 100
    test_stunting = 1000
    test_iq = 2.0
    test_pop = 100000
    
    economic_benefit = simulator.calculate_economic_benefit(
        test_lives, test_stunting, test_iq, test_pop
    )
    
    # Check if economic benefit is positive and reasonable
    min_expected = test_lives * 1_000_000  # At minimum, value of lives saved
    max_expected = test_lives * 5_000_000 + test_stunting * 200_000  # Reasonable upper bound
    
    if min_expected <= economic_benefit <= max_expected:
        test_passed(
            "Economic Benefit Calculation",
            f"Benefit: ${economic_benefit:,.0f} (reasonable range)"
        )
    else:
        test_failed(
            "Economic Benefit Calculation",
            f"Benefit ${economic_benefit:,.0f} outside expected range"
        )
    
    # Test that ROI can be positive
    budget = 1_000_000
    if economic_benefit > budget:
        roi = (economic_benefit - budget) / budget * 100
        test_passed(
            "Positive ROI Achievable",
            f"ROI: {roi:.1f}% with test parameters"
        )
    else:
        test_warning(
            "Positive ROI",
            "Need to adjust parameters for positive ROI"
        )
        
except Exception as e:
    test_failed("Economic Calculation Tests", str(e))

# ==============================================================================
# TEST 6: Data Validation Module
# ==============================================================================
print("\n" + "="*60)
print("TEST 6: DATA VALIDATION MODULE")
print("-"*60)

try:
    from data_validator import DataValidator, clean_and_standardize_districts
    
    # Create test data with known issues
    test_nutrition = pd.DataFrame({
        'District': ['KAMPALA', 'WAKISO ', ' MUKONO', 'UNKNOWN'],
        'Iron_(mg)': [45, 50, 48, -10],  # Invalid negative value
        'Zinc_(mg)': [60, 65, 58, 250]   # Outlier value
    })
    
    test_population = pd.DataFrame({
        'ADM2_EN': ['KAMPALA', 'WAKISO', 'MUKONO', 'JINJA'],
        'T_TL': [1650000, 2000000, 600000, 500000]
    })
    
    # Initialize validator
    validator = DataValidator()
    
    # Test district validation
    district_results = validator.validate_district_names(
        test_nutrition, test_population, pd.DataFrame()
    )
    
    if 'mapping' in district_results:
        test_passed(
            "District Name Validation",
            f"Created mapping for {len(district_results['mapping'])} districts"
        )
    else:
        test_failed("District Name Validation", "No mapping created")
    
    # Test nutrient validation
    nutrient_results = validator.validate_nutrient_data(test_nutrition)
    
    if nutrient_results['outliers'] or nutrient_results['invalid_ranges']:
        test_passed(
            "Nutrient Data Validation",
            f"Detected {sum(nutrient_results['outliers'].values())} outliers and invalid ranges"
        )
    else:
        test_failed("Nutrient Data Validation", "Failed to detect known data issues")
    
    # Test district cleaning
    cleaned_df = clean_and_standardize_districts(test_nutrition, 'District')
    
    if all(cleaned_df['District'].str.isupper()):
        test_passed(
            "District Standardization",
            "All districts converted to uppercase"
        )
    else:
        test_failed("District Standardization", "Districts not properly standardized")
        
except Exception as e:
    test_failed("Data Validation Tests", str(e))

# ==============================================================================
# TEST 7: Integration Test - Full Workflow
# ==============================================================================
print("\n" + "="*60)
print("TEST 7: INTEGRATION TEST - FULL WORKFLOW")
print("-"*60)

try:
    # Test that all components work together
    from uganda_nutrition_config import get_config
    from real_data_provider import UgandaRealDataProvider
    from data_validator import DataValidator
    from supply_chain_optimizer import SupplyChainOptimizer
    
    # 1. Load configuration
    config = get_config()
    
    # 2. Get real data
    provider = UgandaRealDataProvider()
    pop_data = provider.get_population_constants()
    
    # 3. Validate staffing requirements
    staffing = config.get_staffing_requirements(pop_data['CHILDREN_UNDER_5'])
    
    # 4. Calculate intervention effectiveness
    effectiveness = provider.get_intervention_effectiveness()
    
    # 5. Validate all components integrate
    if (staffing and 
        'supplementation' in effectiveness and 
        pop_data['UGANDA_POPULATION'] > 0):
        
        test_passed(
            "Full Integration Test",
            "All components work together successfully"
        )
    else:
        test_failed(
            "Full Integration Test",
            "Components not properly integrated"
        )
        
except Exception as e:
    test_failed("Integration Test", str(e))

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================
print("\n" + "="*80)
print("TEST SUITE SUMMARY")
print("="*80)

total_tests = len(test_results['passed']) + len(test_results['failed'])
pass_rate = (len(test_results['passed']) / total_tests * 100) if total_tests > 0 else 0

print(f"""
Tests Run: {total_tests}
Passed: {len(test_results['passed'])} ✅
Failed: {len(test_results['failed'])} ❌
Warnings: {len(test_results['warnings'])} ⚠️
Pass Rate: {pass_rate:.1f}%

STATUS: {'ALL TESTS PASSED! 🎉' if len(test_results['failed']) == 0 else 'SOME TESTS FAILED ⚠️'}
""")

if test_results['failed']:
    print("Failed Tests:")
    for test in test_results['failed']:
        print(f"  - {test}")

if test_results['warnings']:
    print("\nTests with Warnings:")
    for test in test_results['warnings']:
        print(f"  - {test}")

print("="*80)

# Save test results to file
with open('test_results.json', 'w') as f:
    json.dump({
        'timestamp': pd.Timestamp.now().isoformat(),
        'summary': {
            'total': total_tests,
            'passed': len(test_results['passed']),
            'failed': len(test_results['failed']),
            'warnings': len(test_results['warnings']),
            'pass_rate': pass_rate
        },
        'details': test_results
    }, f, indent=2)
    
print("Test results saved to test_results.json")