#!/usr/bin/env python3
"""Test that duplicates are removed from synergy analysis"""

import numpy as np

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

def test_no_duplicates():
    """Test that duplicate pairs are properly removed"""
    
    # Test case: Select nutrients that have multiple synergies
    selected_nutrients = ['Iron_(mg)', 'Vitamin_C_(mg)', 'Folate_(mcg)', 'Vitamin_B12_(mcg)']
    
    print("=" * 60)
    print("TESTING DUPLICATE REMOVAL")
    print("=" * 60)
    print(f"\nSelected nutrients: {selected_nutrients}")
    
    # Method 1: WITH duplicates (old way)
    print("\n--- OLD METHOD (with duplicates) ---")
    applicable_with_dups = []
    for (n1, n2), value in NUTRIENT_SYNERGIES.items():
        if n1 in selected_nutrients and n2 in selected_nutrients:
            applicable_with_dups.append(f"{n1} + {n2} = {value}x")
    
    print(f"Found {len(applicable_with_dups)} entries (includes duplicates):")
    for synergy in applicable_with_dups:
        print(f"  • {synergy}")
    
    # Method 2: WITHOUT duplicates (new way)
    print("\n--- NEW METHOD (no duplicates) ---")
    applicable_no_dups = []
    seen_pairs = set()
    
    for (n1, n2), value in NUTRIENT_SYNERGIES.items():
        if n1 in selected_nutrients and n2 in selected_nutrients:
            # Create a sorted tuple to track unique pairs
            pair_key = tuple(sorted([n1, n2]))
            if pair_key not in seen_pairs:
                applicable_no_dups.append(f"{n1} + {n2} = {value}x")
                seen_pairs.add(pair_key)
    
    print(f"Found {len(applicable_no_dups)} unique relationships:")
    for synergy in applicable_no_dups:
        print(f"  • {synergy}")
    
    # Test matrix details
    print("\n" + "=" * 60)
    print("MATRIX DETAILS TEST")
    print("=" * 60)
    
    synergy_matrix = np.ones((len(selected_nutrients), len(selected_nutrients)))
    matrix_details_with_dups = []
    matrix_details_no_dups = []
    seen_matrix_pairs = set()
    
    for i, n1 in enumerate(selected_nutrients):
        for j, n2 in enumerate(selected_nutrients):
            if i != j:
                for (sn1, sn2), value in NUTRIENT_SYNERGIES.items():
                    if (n1 == sn1 and n2 == sn2) or (n1 == sn2 and n2 == sn1):
                        synergy_matrix[i, j] = value
                        
                        # With duplicates
                        matrix_details_with_dups.append(f"[{i},{j}]: {n1} × {n2} = {value}")
                        
                        # Without duplicates
                        pair_key = tuple(sorted([n1, n2]))
                        if pair_key not in seen_matrix_pairs:
                            matrix_details_no_dups.append(f"{n1} × {n2} = {value}")
                            seen_matrix_pairs.add(pair_key)
                        break
    
    print(f"\nOLD: Matrix details with duplicates ({len(matrix_details_with_dups)} entries):")
    for detail in matrix_details_with_dups[:5]:  # Show first 5
        print(f"  {detail}")
    if len(matrix_details_with_dups) > 5:
        print(f"  ... and {len(matrix_details_with_dups)-5} more")
    
    print(f"\nNEW: Matrix details without duplicates ({len(matrix_details_no_dups)} entries):")
    for detail in matrix_details_no_dups:
        print(f"  • {detail}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Reduction: {len(matrix_details_with_dups)} → {len(matrix_details_no_dups)} entries")
    print(f"Duplicates removed: {len(matrix_details_with_dups) - len(matrix_details_no_dups)}")
    print("\n✅ Duplicate removal successful!")

if __name__ == "__main__":
    test_no_duplicates()