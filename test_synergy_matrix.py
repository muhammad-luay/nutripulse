#!/usr/bin/env python3
"""Test script for nutrient synergy matrix functionality"""

import numpy as np
import pandas as pd

# Copy the NUTRIENT_SYNERGIES from the main file
NUTRIENT_SYNERGIES = {
    ('Vitamin_B12_(mcg)', 'Folate_(mcg)'): 1.4,  # B12 and Folate work together
    ('Iron_(mg)', 'Vitamin_C_(mg)'): 1.3,  # Vitamin C enhances iron absorption
    ('Calcium_(mg)', 'Vitamin_A_(mcg)'): 1.25,  # Vitamin A helps calcium utilization
    ('Zinc_(mg)', 'Proteins_(g)'): 1.25,  # Protein enhances zinc utilization
    ('Vitamin_A_(mcg)', 'Zinc_(mg)'): 1.2,  # Zinc helps vitamin A metabolism
    ('Iron_(mg)', 'Folate_(mcg)'): 1.15,  # Both needed for red blood cell formation
    ('Vitamin_B12_(mcg)', 'Iron_(mg)'): 1.2,  # B12 and iron work together for blood health
    ('Vitamin_C_(mg)', 'Folate_(mcg)'): 1.15,  # Vitamin C protects folate
    ('Calcium_(mg)', 'Zinc_(mg)'): 0.85,  # Calcium can inhibit zinc absorption (antagonistic)
}

def test_synergy_matrix():
    """Test the synergy matrix generation logic"""
    
    print("=" * 60)
    print("NUTRIENT SYNERGY MATRIX TEST")
    print("=" * 60)
    
    # Test case 1: Nutrients with known synergies
    print("\nTest 1: Nutrients with synergies")
    selected_nutrients = ['Iron_(mg)', 'Vitamin_C_(mg)', 'Folate_(mcg)', 'Vitamin_B12_(mcg)']
    print(f"Selected: {selected_nutrients}")
    
    # Create synergy matrix
    synergy_matrix = np.ones((len(selected_nutrients), len(selected_nutrients)))
    found_synergies = []
    
    for i, n1 in enumerate(selected_nutrients):
        for j, n2 in enumerate(selected_nutrients):
            if i != j:
                for (sn1, sn2), value in NUTRIENT_SYNERGIES.items():
                    if (n1 == sn1 and n2 == sn2) or (n1 == sn2 and n2 == sn1):
                        synergy_matrix[i, j] = value
                        found_synergies.append(f"{n1} × {n2} = {value}")
                        break
    
    print(f"\nFound {len(found_synergies)} synergies:")
    for synergy in found_synergies:
        print(f"  • {synergy}")
    
    print("\nSynergy Matrix:")
    df = pd.DataFrame(synergy_matrix, 
                      index=[n.split('_')[0] for n in selected_nutrients],
                      columns=[n.split('_')[0] for n in selected_nutrients])
    print(df.round(2))
    
    # Test case 2: Nutrients with antagonistic effects
    print("\n" + "=" * 60)
    print("Test 2: Nutrients with antagonistic effects")
    selected_nutrients = ['Calcium_(mg)', 'Zinc_(mg)', 'Vitamin_A_(mcg)']
    print(f"Selected: {selected_nutrients}")
    
    synergy_matrix = np.ones((len(selected_nutrients), len(selected_nutrients)))
    found_synergies = []
    
    for i, n1 in enumerate(selected_nutrients):
        for j, n2 in enumerate(selected_nutrients):
            if i != j:
                for (sn1, sn2), value in NUTRIENT_SYNERGIES.items():
                    if (n1 == sn1 and n2 == sn2) or (n1 == sn2 and n2 == sn1):
                        synergy_matrix[i, j] = value
                        effect_type = "synergistic" if value > 1.0 else "antagonistic"
                        found_synergies.append(f"{n1} × {n2} = {value} ({effect_type})")
                        break
    
    print(f"\nFound {len(found_synergies)} interactions:")
    for synergy in found_synergies:
        print(f"  • {synergy}")
    
    print("\nSynergy Matrix:")
    df = pd.DataFrame(synergy_matrix, 
                      index=[n.split('_')[0] for n in selected_nutrients],
                      columns=[n.split('_')[0] for n in selected_nutrients])
    print(df.round(2))
    
    # Test case 3: Mixed nutrients (some with synergies, some without)
    print("\n" + "=" * 60)
    print("Test 3: Mixed nutrients")
    selected_nutrients = ['Kilocalories_(kcal)', 'Iron_(mg)', 'Vitamin_C_(mg)', 'Niacin_(mg)', 'Riboflavin_(mg)']
    print(f"Selected: {selected_nutrients}")
    
    synergy_matrix = np.ones((len(selected_nutrients), len(selected_nutrients)))
    found_synergies = []
    
    for i, n1 in enumerate(selected_nutrients):
        for j, n2 in enumerate(selected_nutrients):
            if i != j:
                for (sn1, sn2), value in NUTRIENT_SYNERGIES.items():
                    if (n1 == sn1 and n2 == sn2) or (n1 == sn2 and n2 == sn1):
                        synergy_matrix[i, j] = value
                        found_synergies.append(f"{n1} × {n2} = {value}")
                        break
    
    if found_synergies:
        print(f"\nFound {len(found_synergies)} synergies:")
        for synergy in found_synergies:
            print(f"  • {synergy}")
    else:
        print("\n⚠️  No synergies found for this combination")
    
    print("\nSynergy Matrix:")
    df = pd.DataFrame(synergy_matrix, 
                      index=[n.split('_')[0] for n in selected_nutrients],
                      columns=[n.split('_')[0] for n in selected_nutrients])
    print(df.round(2))
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    synergistic_count = sum(1 for val in synergy_matrix.flatten() if val > 1.0)
    antagonistic_count = sum(1 for val in synergy_matrix.flatten() if val < 1.0)
    neutral_count = sum(1 for val in synergy_matrix.flatten() if val == 1.0)
    
    print(f"Synergistic pairs (>1.0): {synergistic_count}")
    print(f"Antagonistic pairs (<1.0): {antagonistic_count}")
    print(f"Neutral pairs (=1.0): {neutral_count}")
    
    if synergy_matrix[synergy_matrix != 1.0].size > 0:
        avg_synergy = np.mean(synergy_matrix[synergy_matrix != 1.0])
        print(f"Average synergy factor (excluding 1.0): {avg_synergy:.2f}x")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_synergy_matrix()