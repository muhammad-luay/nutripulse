#!/usr/bin/env python3
"""
Reality check on ROI calculations - identifying the issue
"""

import numpy as np

def analyze_roi_problem():
    """Identify why ROI calculations are unrealistic"""
    
    print("="*60)
    print("ROI CALCULATION REALITY CHECK")
    print("="*60)
    
    # Let's trace through a specific example: 500M UGX budget
    budget = 500_000_000  # 500 million UGX
    
    # Population parameters
    total_population = 47_840_590
    children_under_5 = int(total_population * 0.15)  # 7,176,088
    pregnant_women = int(total_population * 0.038)
    lactating_women = int(total_population * 0.045)
    target_population = children_under_5 + pregnant_women + lactating_women
    
    # Cost per person
    annual_cost_per_person = 40_000
    
    # Coverage calculation
    coverage = min(1.0, budget / (target_population * annual_cost_per_person))
    people_reached = int(coverage * target_population)
    
    print(f"\n1. BUDGET SCENARIO: {budget/1_000_000:.0f} Million UGX")
    print(f"   Coverage: {coverage*100:.2f}%")
    print(f"   People reached: {people_reached:,}")
    
    # Health impacts
    u5_mortality_rate = 46.4 / 1000
    mortality_reduction = 0.23
    lives_saved = int(coverage * children_under_5 * u5_mortality_rate * mortality_reduction)
    
    stunted_children = int(children_under_5 * 0.232)
    stunting_reduction_rate = 0.36
    stunting_prevented = int(coverage * stunted_children * stunting_reduction_rate)
    
    anemic_children = int(children_under_5 * 0.53)
    anemic_women = int((pregnant_women + lactating_women) * 0.28)
    anemia_reduction_rate = 0.42
    anemia_cases_prevented = int(coverage * (anemic_children + anemic_women) * anemia_reduction_rate)
    
    print(f"\n2. HEALTH IMPACTS:")
    print(f"   Lives saved: {lives_saved}")
    print(f"   Stunting prevented: {stunting_prevented}")
    print(f"   Anemia prevented: {anemia_cases_prevented}")
    
    # THE PROBLEM: Economic valuation
    value_per_life = 150_000_000  # 150 MILLION UGX per life!!!
    value_per_stunting = 25_000_000  # 25 MILLION UGX per stunting case
    value_per_anemia = 2_000_000  # 2 MILLION UGX per anemia case
    
    print(f"\n3. ECONOMIC VALUES (THE PROBLEM!):")
    print(f"   Value per life: {value_per_life:,} UGX")
    print(f"   Value per stunting: {value_per_stunting:,} UGX")
    print(f"   Value per anemia: {value_per_anemia:,} UGX")
    
    # Calculate benefits
    mortality_benefit = lives_saved * value_per_life
    stunting_benefit = stunting_prevented * value_per_stunting
    anemia_benefit = anemia_cases_prevented * value_per_anemia
    total_benefit = mortality_benefit + stunting_benefit + anemia_benefit
    
    print(f"\n4. BENEFIT CALCULATION:")
    print(f"   Mortality benefit: {mortality_benefit:,} UGX")
    print(f"   Stunting benefit: {stunting_benefit:,} UGX")
    print(f"   Anemia benefit: {anemia_benefit:,} UGX")
    print(f"   TOTAL BENEFIT: {total_benefit:,} UGX")
    
    # ROI calculation
    efficiency = 1.0 - (0.3 * coverage)
    adjusted_benefit = total_benefit * efficiency
    roi = ((adjusted_benefit - budget) / budget * 100)
    
    print(f"\n5. ROI CALCULATION:")
    print(f"   Total benefit: {total_benefit:,} UGX")
    print(f"   Efficiency factor: {efficiency:.4f}")
    print(f"   Adjusted benefit: {adjusted_benefit:,} UGX")
    print(f"   ROI: {roi:.2f}%")
    
    print("\n" + "="*60)
    print("ISSUE IDENTIFIED!")
    print("="*60)
    
    print("""
The problem is the ECONOMIC VALUATION:

1. Value per life saved: 150,000,000 UGX ($40,000 USD)
   - This might be a statistical value of life (VSL) for economic modeling
   - But it's being applied as IMMEDIATE RETURN, not lifetime value
   
2. Value per stunting prevented: 25,000,000 UGX ($6,700 USD)
   - This represents LIFETIME productivity loss
   - Should be discounted to present value
   
3. These are SOCIAL benefits over DECADES, not financial returns

REALISTIC ROI for nutrition interventions:
- Typical range: 10-30% annual return
- Best case: 50-100% over project lifetime
- The 6,700% is mixing up social value with financial ROI
""")
    
    print("\nREALISTIC CALCULATION:")
    # More realistic immediate economic benefit
    realistic_value_per_life = 5_000_000  # Immediate healthcare savings
    realistic_value_per_stunting = 500_000  # Annual productivity gain
    realistic_value_per_anemia = 100_000  # Immediate productivity improvement
    
    realistic_mortality = lives_saved * realistic_value_per_life
    realistic_stunting = stunting_prevented * realistic_value_per_stunting
    realistic_anemia = anemia_cases_prevented * realistic_value_per_anemia
    realistic_total = realistic_mortality + realistic_stunting + realistic_anemia
    
    realistic_roi = ((realistic_total - budget) / budget * 100)
    
    print(f"With realistic immediate values:")
    print(f"  Mortality savings: {realistic_mortality:,} UGX")
    print(f"  Stunting benefit: {realistic_stunting:,} UGX")
    print(f"  Anemia benefit: {realistic_anemia:,} UGX")
    print(f"  Total benefit: {realistic_total:,} UGX")
    print(f"  REALISTIC ROI: {realistic_roi:.2f}%")
    
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print("""
1. Separate SOCIAL VALUE from FINANCIAL ROI
   - Social value: Long-term societal benefits (current calculation)
   - Financial ROI: Direct economic returns (needs different calculation)

2. Apply proper discounting for future benefits
   - Use Net Present Value (NPV) for lifetime benefits
   - Typical discount rate: 3-5% annually

3. Realistic expectations:
   - Social Benefit-Cost Ratio: 10:1 to 20:1 (excellent)
   - Financial ROI: 15-30% annually (very good)
   - NOT 6,700% immediate return!

4. The algorithm is technically correct for SOCIAL VALUE
   But it's misleading to call this "ROI" without clarification
""")

if __name__ == "__main__":
    analyze_roi_problem()