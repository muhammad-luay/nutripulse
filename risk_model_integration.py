"""
Risk Model Integration Module
Properly integrates ML-based risk scoring into the Uganda Nutrition Dashboard
"""

import pandas as pd
import numpy as np
from ml_prediction_models import RiskScoringModel
import warnings
warnings.filterwarnings('ignore')

class RiskModelIntegration:
    """Handles risk scoring with data validation and ML model integration"""
    
    def __init__(self):
        """Initialize the risk model"""
        self.risk_model = RiskScoringModel()
        self.is_trained = False
        self.validation_errors = []
        
    def validate_adequacy_data(self, data):
        """
        Validate and fix adequacy data
        Returns cleaned data and list of issues found
        """
        issues = []
        cleaned_data = data.copy()
        
        # Find nutrient columns (containing mg, mcg, g)
        nutrient_cols = [col for col in data.columns 
                        if any(unit in str(col) for unit in ['(mg)', '(mcg)', '(g)', '(IU)', '(kcal)'])]
        
        for col in nutrient_cols:
            # Check for values > 100
            if col in cleaned_data.columns:
                invalid_mask = cleaned_data[col] > 100
                if invalid_mask.any():
                    # Check if values look like they were multiplied by 100
                    sample_values = cleaned_data.loc[invalid_mask, col].head()
                    
                    # If values are in thousands (e.g., 13663), divide by 100
                    if (cleaned_data[col] > 1000).any():
                        issues.append(f"Found values >1000% in {col}, dividing by 100")
                        cleaned_data.loc[cleaned_data[col] > 1000, col] = cleaned_data.loc[cleaned_data[col] > 1000, col] / 100
                    
                    # If values are in hundreds (e.g., 356), cap at 100
                    elif (cleaned_data[col] > 100).any():
                        issues.append(f"Found values >100% in {col}, capping at 100")
                        cleaned_data.loc[cleaned_data[col] > 100, col] = 100
                
                # Check for negative values
                if (cleaned_data[col] < 0).any():
                    issues.append(f"Found negative values in {col}, setting to 0")
                    cleaned_data.loc[cleaned_data[col] < 0, col] = 0
                    
                # Check for NaN values
                if cleaned_data[col].isna().any():
                    median_val = cleaned_data[col].median()
                    if pd.isna(median_val):
                        median_val = 50  # Default if all values are NaN
                    issues.append(f"Found NaN values in {col}, filling with median ({median_val:.1f})")
                    cleaned_data[col].fillna(median_val, inplace=True)
        
        return cleaned_data, issues
    
    def prepare_risk_features(self, district_data):
        """
        Prepare features for risk scoring from district data
        """
        features = {}
        
        # Handle both Series and DataFrame input
        if hasattr(district_data, 'to_dict'):
            # Convert Series to dict for easier processing
            if hasattr(district_data, 'index'):
                data_dict = district_data.to_dict()
                columns = list(data_dict.keys())
            else:
                data_dict = district_data
                columns = list(data_dict.keys())
        else:
            data_dict = district_data
            columns = list(data_dict.keys()) if isinstance(data_dict, dict) else []
        
        # Get nutrient columns
        nutrient_cols = [col for col in columns 
                        if any(unit in str(col) for unit in ['(mg)', '(mcg)', '(g)', '(IU)', '(kcal)'])]
        
        if nutrient_cols:
            # Extract nutrient values
            if isinstance(data_dict, dict):
                nutrient_values = [data_dict[col] for col in nutrient_cols]
            else:
                nutrient_values = [district_data[col] for col in nutrient_cols]
            
            # Convert to numpy array for calculations
            nutrient_array = np.array(nutrient_values)
            features['avg_adequacy'] = float(np.mean(nutrient_array))
            features['min_adequacy'] = float(np.min(nutrient_array))
            features['nutrients_below_50'] = int(np.sum(nutrient_array < 50))
            features['nutrients_below_30'] = int(np.sum(nutrient_array < 30))
        else:
            # Default values if no nutrient data
            features['avg_adequacy'] = 50.0
            features['min_adequacy'] = 30.0
            features['nutrients_below_50'] = 2
            features['nutrients_below_30'] = 1
        
        # Population features (with defaults)
        # Use data_dict for access
        features['under5_proportion'] = float(data_dict.get('under5_proportion', 0.15) if isinstance(data_dict, dict) else 0.15)
        features['pregnant_women_proportion'] = float(data_dict.get('pregnant_women_proportion', 0.032) if isinstance(data_dict, dict) else 0.032)
        features['poverty_rate'] = float(data_dict.get('poverty_rate', 0.3) if isinstance(data_dict, dict) else 0.3)
        
        # Health system features
        if isinstance(data_dict, dict):
            population = float(data_dict.get('Population', data_dict.get('population', 100000)))
            health_facilities = float(data_dict.get('health_facilities', 5))
        else:
            population = 100000
            health_facilities = 5
        features['health_facility_ratio'] = health_facilities / (population / 10000)
        
        # Geographic features
        features['rural_percentage'] = float(data_dict.get('rural_percentage', 0.7) if isinstance(data_dict, dict) else 0.7)
        features['distance_to_capital'] = float(data_dict.get('distance_to_capital', 100) if isinstance(data_dict, dict) else 100)
        
        return features
    
    def calculate_district_risk(self, district_data, district_name=None):
        """
        Calculate risk score for a single district
        Returns comprehensive risk assessment
        """
        # Prepare features
        features = self.prepare_risk_features(district_data)
        
        # Calculate risk using the model
        risk_result = self.risk_model.calculate_risk_score(features)
        
        # Add district name if provided
        if district_name:
            risk_result['district'] = district_name
        
        # Add feature details for transparency
        risk_result['features'] = features
        
        # Enhanced risk categorization
        score = risk_result['risk_score']
        if score >= 70:
            risk_result['category'] = 'Critical'
            risk_result['color'] = '#FF0000'
            risk_result['emoji'] = '🔴'
            risk_result['priority'] = 1
        elif score >= 50:
            risk_result['category'] = 'High'
            risk_result['color'] = '#FFA500'
            risk_result['emoji'] = '🟠'
            risk_result['priority'] = 2
        elif score >= 30:
            risk_result['category'] = 'Medium'
            risk_result['color'] = '#FFFF00'
            risk_result['emoji'] = '🟡'
            risk_result['priority'] = 3
        else:
            risk_result['category'] = 'Low'
            risk_result['color'] = '#00FF00'
            risk_result['emoji'] = '🟢'
            risk_result['priority'] = 4
        
        return risk_result
    
    def batch_calculate_risks(self, districts_df, validate_data=True):
        """
        Calculate risk scores for multiple districts
        Returns DataFrame with risk assessments
        """
        if validate_data:
            # Validate and clean data first
            districts_df, issues = self.validate_adequacy_data(districts_df)
            if issues:
                print(f"Data validation found {len(issues)} issues:")
                for issue in issues[:5]:  # Show first 5 issues
                    print(f"  - {issue}")
        
        results = []
        
        for idx, row in districts_df.iterrows():
            district_name = row.get('District', f'District_{idx}')
            
            try:
                risk_result = self.calculate_district_risk(row, district_name)
                
                results.append({
                    'District': district_name,
                    'Risk Score': risk_result['risk_score'],
                    'Risk Level': risk_result['risk_level'],
                    'Category': risk_result['category'],
                    'Emoji': risk_result['emoji'],
                    'Priority': risk_result['priority'],
                    'Avg Adequacy': risk_result['features']['avg_adequacy'],
                    'Critical Nutrients': risk_result['features']['nutrients_below_30'],
                    'Min Adequacy': risk_result['features']['min_adequacy'],
                    'Health Facility Ratio': risk_result['features']['health_facility_ratio'],
                    'Key Risk Factors': ', '.join(risk_result.get('key_risk_factors', [])[:3]),
                    'Top Intervention': risk_result.get('recommended_interventions', ['Supplementation'])[0] if risk_result.get('recommended_interventions') else 'Supplementation'
                })
                
            except Exception as e:
                print(f"Error processing {district_name}: {str(e)}")
                results.append({
                    'District': district_name,
                    'Risk Score': 50,
                    'Risk Level': 'medium',
                    'Category': 'Medium',
                    'Emoji': '🟡',
                    'Priority': 3,
                    'Avg Adequacy': 50,
                    'Critical Nutrients': 2,
                    'Min Adequacy': 30,
                    'Health Facility Ratio': 1.0,
                    'Key Risk Factors': 'Data error',
                    'Top Intervention': 'Data validation needed'
                })
        
        return pd.DataFrame(results)
    
    def get_risk_summary_stats(self, risk_df):
        """
        Generate summary statistics from risk assessment results
        """
        if risk_df.empty:
            return {
                'total_districts': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'avg_risk_score': 0,
                'highest_risk_districts': [],
                'intervention_priorities': {}
            }
        
        summary = {
            'total_districts': len(risk_df),
            'critical': len(risk_df[risk_df['Category'] == 'Critical']),
            'high': len(risk_df[risk_df['Category'] == 'High']),
            'medium': len(risk_df[risk_df['Category'] == 'Medium']),
            'low': len(risk_df[risk_df['Category'] == 'Low']),
            'avg_risk_score': risk_df['Risk Score'].mean(),
            'highest_risk_districts': risk_df.nlargest(5, 'Risk Score')[['District', 'Risk Score', 'Category']].to_dict('records'),
            'intervention_priorities': risk_df.groupby('Top Intervention').size().to_dict()
        }
        
        return summary
    
    def generate_risk_based_recommendations(self, risk_df, budget_limit=None):
        """
        Generate intervention recommendations based on risk assessment
        """
        recommendations = []
        
        # Sort by priority (highest risk first)
        priority_df = risk_df.sort_values('Priority')
        
        # Critical districts - immediate action
        critical_districts = priority_df[priority_df['Category'] == 'Critical']
        if not critical_districts.empty:
            recommendations.append({
                'priority': 'IMMEDIATE',
                'districts': critical_districts['District'].tolist(),
                'intervention': 'Emergency supplementation + Fortification',
                'timeline': '0-3 months',
                'estimated_cost_per_district': 500000,
                'expected_impact': 'Prevent acute malnutrition crisis'
            })
        
        # High risk districts - urgent action
        high_risk_districts = priority_df[priority_df['Category'] == 'High']
        if not high_risk_districts.empty:
            recommendations.append({
                'priority': 'URGENT',
                'districts': high_risk_districts['District'].tolist(),
                'intervention': 'Targeted supplementation + Education',
                'timeline': '1-6 months',
                'estimated_cost_per_district': 300000,
                'expected_impact': 'Reduce severe deficiencies by 40%'
            })
        
        # Medium risk districts - planned intervention
        medium_risk_districts = priority_df[priority_df['Category'] == 'Medium']
        if not medium_risk_districts.empty:
            recommendations.append({
                'priority': 'PLANNED',
                'districts': medium_risk_districts['District'].tolist()[:10],  # Top 10
                'intervention': 'Fortification + Biofortification',
                'timeline': '3-12 months',
                'estimated_cost_per_district': 200000,
                'expected_impact': 'Improve nutrition sustainably'
            })
        
        # Calculate total budget needed
        total_budget_needed = 0
        for rec in recommendations:
            total_budget_needed += rec['estimated_cost_per_district'] * len(rec['districts'])
        
        # Add budget analysis
        if budget_limit:
            if total_budget_needed > budget_limit:
                recommendations.append({
                    'priority': 'BUDGET_WARNING',
                    'message': f'Total budget needed ({total_budget_needed:,.0f}) exceeds limit ({budget_limit:,.0f})',
                    'suggestion': 'Focus on critical districts first or seek additional funding'
                })
        
        return recommendations

# Utility function for easy integration
def integrate_risk_model_with_dashboard(nutrition_df, validate=True):
    """
    Main integration function to be called from the dashboard
    """
    # Initialize the risk model integration
    risk_integration = RiskModelIntegration()
    
    # Calculate risks for all districts
    risk_results = risk_integration.batch_calculate_risks(nutrition_df, validate_data=validate)
    
    # Get summary statistics
    summary_stats = risk_integration.get_risk_summary_stats(risk_results)
    
    # Generate recommendations
    recommendations = risk_integration.generate_risk_based_recommendations(risk_results)
    
    return {
        'risk_scores': risk_results,
        'summary': summary_stats,
        'recommendations': recommendations,
        'model': risk_integration
    }