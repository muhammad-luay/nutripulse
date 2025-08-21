#!/usr/bin/env python3
"""
Test the Risk Model Integration with sample district data
Including validation of problematic data values
"""

import pandas as pd
import numpy as np
from risk_model_integration import RiskModelIntegration, integrate_risk_model_with_dashboard

# Test with the problematic data provided by user
print("="*60)
print("TESTING RISK MODEL INTEGRATION")
print("="*60)

# Create test data with problematic values from user
test_data = pd.DataFrame({
    'District': ['RUBANDA', 'LAMWO', 'NAMTUMBA', 'NWOYA', 'MANAFWA'],
    'Value1': [50, 50, 50, 50, 50],
    'Vitamin_A_(mcg)': [13663.0, 9074.5, 2999.2, 17645.6, 11296.0],  # Problematic percentages
    'Iron_(mg)': [3, 6, 3, 5, 3],
    'Zinc_(mg)': [1, 2, 3, 4, 5],
    'Population': [100000, 150000, 80000, 120000, 110000],
    'Vitamin_B12_(mcg)': [45.3, 32.1, 67.8, 23.4, 51.2],  # Normal values
    'Folate_(mcg)': [78.9, 56.4, 89.2, 34.5, 67.3],  # Normal values
    'Calcium_(mg)': [234.5, 345.6, 456.7, 123.4, 234.5]  # Values that look like they need /100
})

print("\n1. ORIGINAL DATA (with problematic values):")
print("="*40)
print(test_data[['District', 'Vitamin_A_(mcg)', 'Iron_(mg)', 'Vitamin_B12_(mcg)']].to_string())

# Initialize risk model
risk_model = RiskModelIntegration()

print("\n2. DATA VALIDATION:")
print("="*40)

# Validate and clean data
cleaned_data, issues = risk_model.validate_adequacy_data(test_data)

print(f"Found {len(issues)} data issues:")
for issue in issues:
    print(f"  • {issue}")

print("\n3. CLEANED DATA:")
print("="*40)
print(cleaned_data[['District', 'Vitamin_A_(mcg)', 'Iron_(mg)', 'Vitamin_B12_(mcg)']].to_string())

print("\n4. RISK ASSESSMENT RESULTS:")
print("="*40)

# Calculate risks with validation
risk_results = risk_model.batch_calculate_risks(test_data, validate_data=True)

# Display results
print("\nRisk Scores by District:")
print("-"*40)
for _, row in risk_results.iterrows():
    print(f"{row['Emoji']} {row['District']:12} | Score: {row['Risk Score']:5.1f} | Level: {row['Category']:8} | "
          f"Avg Adequacy: {row['Avg Adequacy']:5.1f}% | Critical Nutrients: {row['Critical Nutrients']}")

# Get summary statistics
summary = risk_model.get_risk_summary_stats(risk_results)

print("\n5. RISK SUMMARY STATISTICS:")
print("="*40)
print(f"Total Districts Assessed: {summary['total_districts']}")
print(f"Average Risk Score: {summary['avg_risk_score']:.1f}/100")
print(f"Critical Risk: {summary['critical']} districts")
print(f"High Risk: {summary['high']} districts")
print(f"Medium Risk: {summary['medium']} districts")
print(f"Low Risk: {summary['low']} districts")

print("\n6. HIGHEST RISK DISTRICTS:")
print("="*40)
for dist in summary['highest_risk_districts']:
    print(f"• {dist['District']}: Score {dist['Risk Score']:.1f} ({dist['Category']})")

print("\n7. INTERVENTION RECOMMENDATIONS:")
print("="*40)

recommendations = risk_model.generate_risk_based_recommendations(risk_results, budget_limit=5000000)

for rec in recommendations:
    if rec['priority'] != 'BUDGET_WARNING':
        print(f"\n{rec['priority']} Priority:")
        print(f"  Districts: {', '.join(rec['districts'][:3])}{'...' if len(rec['districts']) > 3 else ''}")
        print(f"  Intervention: {rec['intervention']}")
        print(f"  Timeline: {rec['timeline']}")
        print(f"  Cost/District: ${rec['estimated_cost_per_district']:,}")
        print(f"  Expected Impact: {rec['expected_impact']}")
    else:
        print(f"\n⚠️ BUDGET WARNING:")
        print(f"  {rec['message']}")
        print(f"  {rec['suggestion']}")

print("\n8. TESTING INTEGRATION FUNCTION:")
print("="*40)

# Test the main integration function
integration_results = integrate_risk_model_with_dashboard(test_data, validate=True)

print(f"Risk scores calculated: {len(integration_results['risk_scores'])}")
print(f"Summary generated: {'avg_risk_score' in integration_results['summary']}")
print(f"Recommendations generated: {len(integration_results['recommendations'])}")
print(f"Model available: {integration_results['model'] is not None}")

print("\n" + "="*60)
print("✅ RISK MODEL INTEGRATION TEST COMPLETE")
print("="*60)

# Test with more realistic data
print("\n9. TESTING WITH REALISTIC DATA:")
print("="*40)

realistic_data = pd.DataFrame({
    'District': ['KAMPALA', 'GULU', 'MBARARA', 'ARUA', 'KASESE'],
    'Vitamin_A_(mcg)': [75.2, 45.3, 62.1, 38.7, 51.4],
    'Iron_(mg)': [68.9, 42.3, 55.6, 35.2, 48.7],
    'Zinc_(mg)': [71.3, 39.8, 58.2, 33.4, 46.9],
    'Vitamin_B12_(mcg)': [82.4, 28.9, 65.3, 25.6, 41.2],
    'Folate_(mcg)': [79.1, 51.2, 67.8, 41.3, 55.6],
    'Calcium_(mg)': [64.5, 38.7, 52.3, 31.2, 43.8],
    'Population': [1500000, 350000, 450000, 280000, 320000],
    'health_facilities': [120, 25, 35, 18, 22],
    'poverty_rate': [0.15, 0.42, 0.28, 0.48, 0.35],
    'rural_percentage': [0.1, 0.65, 0.45, 0.75, 0.55]
})

realistic_results = risk_model.batch_calculate_risks(realistic_data, validate_data=False)

print("\nRealistic Data Risk Assessment:")
print("-"*40)
for _, row in realistic_results.iterrows():
    print(f"{row['Emoji']} {row['District']:12} | Score: {row['Risk Score']:5.1f} | "
          f"Priority: {row['Priority']} | Top Intervention: {row['Top Intervention']}")

print("\n✅ All tests completed successfully!")