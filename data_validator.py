"""
Data Validation Module for Uganda Nutrition Intervention System
Ensures data consistency across different data sources
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import difflib

class DataValidator:
    """Validates and reconciles data across different sources"""
    
    def __init__(self):
        self.validation_results = {
            'errors': [],
            'warnings': [],
            'info': [],
            'fixes_applied': []
        }
        
    def validate_district_names(self, 
                               nutrition_df: pd.DataFrame,
                               population_df: pd.DataFrame,
                               facilities_df: pd.DataFrame) -> Dict:
        """
        Validate and reconcile district names across datasets
        
        Returns:
            Dictionary with validation results and mapping table
        """
        
        # Extract district names from each dataset
        nutrition_districts = set(nutrition_df['District'].str.upper().unique()) if 'District' in nutrition_df.columns else set()
        population_districts = set(population_df['ADM2_EN'].str.upper().unique()) if 'ADM2_EN' in population_df.columns else set()
        facilities_districts = set(facilities_df['District'].str.upper().unique()) if 'District' in facilities_df.columns else set()
        
        # Find mismatches
        all_districts = nutrition_districts | population_districts | facilities_districts
        
        results = {
            'total_unique_districts': len(all_districts),
            'nutrition_only': nutrition_districts - (population_districts | facilities_districts),
            'population_only': population_districts - (nutrition_districts | facilities_districts),
            'facilities_only': facilities_districts - (nutrition_districts | population_districts),
            'common_to_all': nutrition_districts & population_districts & facilities_districts,
            'mapping': {}
        }
        
        # Create fuzzy matching for mismatched districts
        unmatched_nutrition = results['nutrition_only']
        potential_matches = population_districts | facilities_districts
        
        for district in unmatched_nutrition:
            # Find closest match using fuzzy matching
            matches = difflib.get_close_matches(district, potential_matches, n=1, cutoff=0.8)
            if matches:
                results['mapping'][district] = matches[0]
                self.validation_results['fixes_applied'].append(
                    f"Mapped '{district}' to '{matches[0]}'"
                )
            else:
                self.validation_results['warnings'].append(
                    f"No match found for district '{district}'"
                )
        
        # Log validation results
        self.validation_results['info'].append(
            f"Found {len(results['common_to_all'])} districts common to all datasets"
        )
        
        if results['nutrition_only']:
            self.validation_results['warnings'].append(
                f"{len(results['nutrition_only'])} districts only in nutrition data"
            )
        
        if results['population_only']:
            self.validation_results['warnings'].append(
                f"{len(results['population_only'])} districts only in population data"
            )
            
        return results
    
    def validate_nutrient_data(self, nutrition_df: pd.DataFrame) -> Dict:
        """
        Validate nutrient adequacy data for consistency
        
        Returns:
            Validation results with data quality metrics
        """
        
        nutrient_columns = [col for col in nutrition_df.columns if '(' in col]
        
        results = {
            'nutrients_tracked': len(nutrient_columns),
            'missing_values': {},
            'outliers': {},
            'invalid_ranges': {}
        }
        
        for nutrient in nutrient_columns:
            # Check for missing values
            missing_count = nutrition_df[nutrient].isna().sum()
            if missing_count > 0:
                results['missing_values'][nutrient] = missing_count
                self.validation_results['warnings'].append(
                    f"Missing {missing_count} values for {nutrient}"
                )
            
            # Check for outliers (values > 200% or < 0%)
            outliers = nutrition_df[
                (nutrition_df[nutrient] > 200) | (nutrition_df[nutrient] < 0)
            ]
            if not outliers.empty:
                results['outliers'][nutrient] = len(outliers)
                self.validation_results['errors'].append(
                    f"Found {len(outliers)} outlier values for {nutrient}"
                )
            
            # Check for invalid ranges
            if nutrition_df[nutrient].min() < 0:
                results['invalid_ranges'][nutrient] = 'negative_values'
                self.validation_results['errors'].append(
                    f"Negative values found for {nutrient}"
                )
        
        return results
    
    def validate_population_data(self, population_df: pd.DataFrame) -> Dict:
        """
        Validate population data for consistency
        
        Returns:
            Validation results
        """
        
        results = {
            'total_population': 0,
            'districts_with_zero_pop': [],
            'population_anomalies': []
        }
        
        if 'T_TL' in population_df.columns:
            # Check total population
            results['total_population'] = population_df['T_TL'].sum()
            
            # Check for zero or negative population
            zero_pop = population_df[population_df['T_TL'] <= 0]
            if not zero_pop.empty:
                results['districts_with_zero_pop'] = zero_pop['ADM2_EN'].tolist()
                self.validation_results['errors'].append(
                    f"Found {len(zero_pop)} districts with zero/negative population"
                )
            
            # Check for population anomalies (too high or too low)
            mean_pop = population_df['T_TL'].mean()
            std_pop = population_df['T_TL'].std()
            
            anomalies = population_df[
                (population_df['T_TL'] > mean_pop + 3 * std_pop) |
                (population_df['T_TL'] < mean_pop - 3 * std_pop)
            ]
            
            if not anomalies.empty:
                results['population_anomalies'] = anomalies[['ADM2_EN', 'T_TL']].to_dict('records')
                self.validation_results['info'].append(
                    f"Found {len(anomalies)} districts with unusual population values"
                )
        
        return results
    
    def reconcile_data(self, 
                       nutrition_df: pd.DataFrame,
                       population_df: pd.DataFrame,
                       facilities_df: pd.DataFrame,
                       mapping: Dict[str, str]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Apply mapping to reconcile district names across datasets
        
        Returns:
            Tuple of reconciled dataframes
        """
        
        # Apply mapping to nutrition data
        nutrition_df_fixed = nutrition_df.copy()
        if mapping:
            nutrition_df_fixed['District'] = nutrition_df_fixed['District'].str.upper().replace(mapping)
            self.validation_results['fixes_applied'].append(
                f"Applied {len(mapping)} district name mappings"
            )
        
        # Ensure all district names are uppercase for consistency
        nutrition_df_fixed['District'] = nutrition_df_fixed['District'].str.upper()
        population_df['ADM2_EN'] = population_df['ADM2_EN'].str.upper()
        if 'District' in facilities_df.columns:
            facilities_df['District'] = facilities_df['District'].str.upper()
        
        return nutrition_df_fixed, population_df, facilities_df
    
    def validate_intervention_parameters(self, 
                                        budget: float,
                                        coverage_target: float,
                                        population: int) -> Dict:
        """
        Validate intervention parameters for feasibility
        
        Returns:
            Validation results with recommendations
        """
        
        results = {
            'feasible': True,
            'warnings': [],
            'recommendations': []
        }
        
        # Check budget adequacy
        min_cost_per_person = 0.50  # Minimum for basic supplementation
        max_reachable = budget / min_cost_per_person
        
        if coverage_target > max_reachable / population:
            results['feasible'] = False
            results['warnings'].append(
                f"Budget insufficient for {coverage_target*100:.0f}% coverage"
            )
            results['recommendations'].append(
                f"Maximum achievable coverage with current budget: {max_reachable/population*100:.1f}%"
            )
        
        # Check coverage target realism
        if coverage_target > 0.95:
            results['warnings'].append(
                "Coverage target >95% may be unrealistic"
            )
            results['recommendations'].append(
                "Consider 80-90% coverage as more achievable target"
            )
        
        # Check budget reasonableness
        if budget / population < 0.10:
            results['warnings'].append(
                "Budget may be too low for meaningful impact"
            )
            results['recommendations'].append(
                f"Minimum recommended budget: ${population * 0.50:,.0f}"
            )
        
        return results
    
    def get_validation_summary(self) -> Dict:
        """Get summary of all validation results"""
        
        return {
            'errors': len(self.validation_results['errors']),
            'warnings': len(self.validation_results['warnings']),
            'fixes_applied': len(self.validation_results['fixes_applied']),
            'details': self.validation_results
        }

# Utility function for data cleaning
def clean_and_standardize_districts(df: pd.DataFrame, district_column: str) -> pd.DataFrame:
    """
    Clean and standardize district names in a dataframe
    
    Args:
        df: DataFrame to clean
        district_column: Name of the column containing district names
        
    Returns:
        Cleaned DataFrame
    """
    
    df = df.copy()
    
    # Remove leading/trailing whitespace
    df[district_column] = df[district_column].str.strip()
    
    # Convert to uppercase for consistency
    df[district_column] = df[district_column].str.upper()
    
    # Remove common suffixes/prefixes
    df[district_column] = df[district_column].str.replace(' DISTRICT', '')
    df[district_column] = df[district_column].str.replace('DISTRICT ', '')
    
    # Fix common misspellings
    common_fixes = {
        'KALANGALA': 'KALANGALA',
        'KALANGLA': 'KALANGALA',
        'SEMBABULE': 'SSEMBABULE',
        'LUWERO': 'LUWEERO',
        'BUNDIBUGYO': 'BUNDIBUGYO',
        'BUNDIBUJO': 'BUNDIBUGYO'
    }
    
    df[district_column] = df[district_column].replace(common_fixes)
    
    return df

# Example usage
if __name__ == "__main__":
    print("Data Validator Module")
    print("="*60)
    
    # Create sample data for testing
    nutrition_df = pd.DataFrame({
        'District': ['KAMPALA', 'WAKISO', 'MUKONO', 'UNKNOWN_DISTRICT'],
        'Iron_(mg)': [45, 50, 48, -10],  # Note the invalid -10
        'Zinc_(mg)': [60, 65, 58, 250]  # Note the outlier 250
    })
    
    population_df = pd.DataFrame({
        'ADM2_EN': ['KAMPALA', 'WAKISO', 'MUKONO', 'JINJA'],
        'T_TL': [1650000, 2000000, 600000, 500000]
    })
    
    facilities_df = pd.DataFrame({
        'District': ['Kampala', 'Wakiso', 'Mukono', 'Gulu'],
        'Hospitals': [5, 3, 2, 1]
    })
    
    # Initialize validator
    validator = DataValidator()
    
    # Validate district names
    print("\n1. Validating District Names:")
    district_results = validator.validate_district_names(
        nutrition_df, population_df, facilities_df
    )
    print(f"   Common to all: {len(district_results['common_to_all'])} districts")
    print(f"   Mapping created: {len(district_results['mapping'])} districts")
    
    # Validate nutrient data
    print("\n2. Validating Nutrient Data:")
    nutrient_results = validator.validate_nutrient_data(nutrition_df)
    print(f"   Nutrients tracked: {nutrient_results['nutrients_tracked']}")
    print(f"   Outliers found: {sum(nutrient_results['outliers'].values())}")
    
    # Get validation summary
    print("\n3. Validation Summary:")
    summary = validator.get_validation_summary()
    print(f"   Errors: {summary['errors']}")
    print(f"   Warnings: {summary['warnings']}")
    print(f"   Fixes applied: {summary['fixes_applied']}")
    
    print("\n" + "="*60)
    print("Validation Complete!")