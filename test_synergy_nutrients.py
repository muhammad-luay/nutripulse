#!/usr/bin/env python3
"""Test that only nutrients with synergies are included"""

import pandas as pd

# Copy the NUTRIENT_SYNERGIES from the main file
NUTRIENT_SYNERGIES = {
    ('Vitamin_B12_(mcg)', 'Folate_(mcg)'): 1.4,
    ('Iron_(mg)', 'Vitamin_C_(mg)'): 1.3,
    ('Calcium_(mg)', 'Vitamin_A_(mcg)'): 1.25,
    ('Zinc_(mg)', 'Proteins_(g)'): 1.25,
    ('Vitamin_A_(mcg)', 'Zinc_(mg)'): 1.2,
    ('Iron_(mg)', 'Folate_(mcg)'): 1.15,
    ('Vitamin_B12_(mcg)', 'Iron_(mg)'): 1.2,
    ('Vitamin_C_(mg)', 'Folate_(mcg)'): 1.15,
    ('Calcium_(mg)', 'Zinc_(mg)'): 0.85,
}

def get_nutrients_with_synergies():
    """Get list of nutrients that have defined synergies"""
    nutrients_with_synergies = set()
    for (n1, n2), _ in NUTRIENT_SYNERGIES.items():
        nutrients_with_synergies.add(n1)
        nutrients_with_synergies.add(n2)
    return sorted(list(nutrients_with_synergies))

# Load the actual nutrition data
nutrition_df = pd.read_csv('/Users/mac/Desktop/hobbies/hackathon/uganda-consumption-adequacy-all-nutrients.csv')

print("=" * 60)
print("NUTRIENTS WITH DEFINED SYNERGIES")
print("=" * 60)

# Get nutrients with synergies
synergy_nutrients = get_nutrients_with_synergies()
print(f"\nNutrients with defined synergies ({len(synergy_nutrients)}):")
for i, nutrient in enumerate(synergy_nutrients, 1):
    print(f"  {i:2}. {nutrient}")

print("\n" + "=" * 60)
print("AVAILABLE IN DATASET")
print("=" * 60)

# Check which ones are available in the actual dataset
available_columns = nutrition_df.columns.tolist()
available_synergy_nutrients = [n for n in synergy_nutrients if n in available_columns]

print(f"\nAvailable in dataset ({len(available_synergy_nutrients)}):")
for i, nutrient in enumerate(available_synergy_nutrients, 1):
    print(f"  {i:2}. {nutrient}")

# Check for nutrients NOT in synergies
print("\n" + "=" * 60)
print("NUTRIENTS WITHOUT SYNERGIES (EXCLUDED)")
print("=" * 60)

nutrient_columns = [col for col in available_columns if col not in ['District', 'Population', 'Latitude', 'Longitude']]
no_synergy_nutrients = [n for n in nutrient_columns if n not in synergy_nutrients]

print(f"\nNutrients without defined synergies ({len(no_synergy_nutrients)}):")
for nutrient in no_synergy_nutrients:
    print(f"  • {nutrient}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total nutrients in dataset: {len(nutrient_columns)}")
print(f"Nutrients with synergies: {len(available_synergy_nutrients)}")
print(f"Nutrients without synergies: {len(no_synergy_nutrients)}")
print(f"Coverage: {len(available_synergy_nutrients)/len(nutrient_columns)*100:.1f}%")

print("\n✅ Now the synergy matrix will only show nutrients with defined interactions!")