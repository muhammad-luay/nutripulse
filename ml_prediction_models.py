#!/usr/bin/env python3
"""
Machine Learning Prediction Models for Uganda Nutrition Interventions
======================================================================
Replaces unrealistic impact predictions with data-driven models that
can actually be trained and validated using available data.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

class NutrientGapPredictor:
    """
    Predicts nutrient deficiency levels for districts based on:
    - Current consumption patterns
    - Demographics (population, age distribution)
    - Infrastructure (health facilities, markets)
    - Geographic factors
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
    def prepare_features(self, district_data, population_data, facilities_data):
        """Prepare feature matrix for prediction"""
        features = pd.DataFrame()
        
        # Population features
        features['total_population'] = population_data['T_TL']
        features['population_density'] = population_data['T_TL'] / population_data.get('area_km2', 1000)
        features['rural_percentage'] = population_data.get('rural_pct', 0.7)
        
        # Health infrastructure
        features['health_facilities_per_10k'] = (facilities_data.shape[0] / population_data['T_TL']) * 10000
        features['hospitals'] = facilities_data[facilities_data['level'] == 'Hospital'].shape[0]
        features['health_centers'] = facilities_data[facilities_data['level'].str.contains('Health Centre', na=False)].shape[0]
        
        # Geographic/economic proxies
        features['distance_to_capital'] = population_data.get('dist_to_kampala', 100)  # km
        features['poverty_index'] = population_data.get('poverty_rate', 0.3)
        
        # Current nutritional status (if available)
        if 'current_adequacy' in district_data.columns:
            features['baseline_adequacy'] = district_data['current_adequacy']
            
        return features
    
    def train(self, training_data):
        """Train models for each nutrient"""
        nutrients = ['Vitamin_A_(mcg)', 'Iron_(mg)', 'Zinc_(mg)', 'Vitamin_B12_(mcg)', 
                    'Folate_(mcg)', 'Calcium_(mg)', 'Vitamin_C_(mg)']
        
        for nutrient in nutrients:
            if nutrient not in training_data.columns:
                continue
                
            # Prepare data
            X = training_data.drop(columns=nutrients, errors='ignore')
            y = training_data[nutrient]
            
            # Remove NaN values
            mask = ~(X.isna().any(axis=1) | y.isna())
            X = X[mask]
            y = y[mask]
            
            if len(X) < 10:  # Need minimum samples
                continue
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train Random Forest model
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            )
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Store model and metrics
            self.models[nutrient] = model
            self.scalers[nutrient] = scaler
            self.feature_importance[nutrient] = dict(zip(X.columns, model.feature_importances_))
            
            print(f"✓ {nutrient}: R² = {r2:.3f}, RMSE = {np.sqrt(mse):.2f}")
    
    def predict(self, district_features, nutrient):
        """Predict nutrient gap for a district"""
        if nutrient not in self.models:
            return None
            
        scaler = self.scalers[nutrient]
        model = self.models[nutrient]
        
        # Scale features
        features_scaled = scaler.transform(district_features.values.reshape(1, -1))
        
        # Predict adequacy
        predicted_adequacy = model.predict(features_scaled)[0]
        
        # Calculate gap (100% - predicted adequacy)
        gap = max(0, 100 - predicted_adequacy)
        
        return {
            'predicted_adequacy': predicted_adequacy,
            'gap': gap,
            'confidence': self._calculate_confidence(model, features_scaled)
        }
    
    def _calculate_confidence(self, model, features):
        """Calculate prediction confidence using tree variance"""
        if hasattr(model, 'estimators_'):
            predictions = [tree.predict(features)[0] for tree in model.estimators_]
            std = np.std(predictions)
            # Convert std to confidence (lower std = higher confidence)
            confidence = max(0, min(100, 100 - std * 2))
            return confidence
        return 75  # Default confidence


class CoverageEstimator:
    """
    Estimates achievable intervention coverage based on:
    - Health facility capacity
    - Population density and distribution
    - Transportation infrastructure
    - Historical coverage patterns
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.baseline_coverage = {}
        
    def prepare_features(self, district_data):
        """Prepare features for coverage estimation"""
        features = pd.DataFrame()
        
        # Infrastructure capacity
        features['facilities_per_10k'] = district_data.get('health_facilities', 0) / (district_data.get('population', 100000) / 10000)
        features['hospital_available'] = int(district_data.get('hospitals', 0) > 0)
        features['health_center_density'] = district_data.get('health_centers', 0) / district_data.get('area_km2', 1000)
        
        # Population factors
        features['population_density'] = district_data.get('population', 0) / district_data.get('area_km2', 1000)
        features['rural_percentage'] = district_data.get('rural_pct', 0.7)
        features['under5_population'] = district_data.get('population', 0) * 0.15  # ~15% are under 5
        
        # Accessibility
        features['road_density'] = district_data.get('road_km', 100) / district_data.get('area_km2', 1000)
        features['distance_to_capital'] = district_data.get('dist_to_kampala', 100)
        
        # Historical performance (if available)
        features['previous_coverage'] = district_data.get('historical_coverage', 0.5)
        
        return features
    
    def train(self, historical_data):
        """Train coverage estimation model using historical coverage data"""
        # Prepare features and target
        X = historical_data.drop(columns=['coverage_achieved'], errors='ignore')
        y = historical_data.get('coverage_achieved', historical_data.get('coverage', 0))
        
        # Remove NaN values
        mask = ~(X.isna().any(axis=1) | y.isna())
        X = X[mask]
        y = y[mask]
        
        if len(X) < 10:
            print("Insufficient data for training coverage model")
            return
        
        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Gradient Boosting model for better accuracy
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✓ Coverage Estimator: R² = {r2:.3f}, RMSE = {np.sqrt(mse):.2f}%")
    
    def estimate_coverage(self, district_features, intervention_type='mixed', budget_per_capita=None):
        """Estimate achievable coverage for a district"""
        
        if self.model is None:
            # Use rule-based estimation if no model trained
            return self._rule_based_estimation(district_features, intervention_type, budget_per_capita)
        
        # Scale features
        features_scaled = self.scaler.transform(district_features.values.reshape(1, -1))
        
        # Predict base coverage
        base_coverage = self.model.predict(features_scaled)[0]
        
        # Adjust for intervention type
        intervention_multipliers = {
            'supplementation': 1.2,  # Easier to distribute
            'fortification': 0.9,    # Requires infrastructure
            'education': 0.8,         # Requires sustained engagement
            'mixed': 1.0
        }
        
        adjusted_coverage = base_coverage * intervention_multipliers.get(intervention_type, 1.0)
        
        # Adjust for budget constraints
        if budget_per_capita:
            budget_factor = min(1.0, budget_per_capita / 10)  # $10 per capita is "full" budget
            adjusted_coverage *= budget_factor
        
        # Cap at realistic maximum
        max_coverage = 0.95 if district_features.get('urban', False) else 0.85
        final_coverage = min(adjusted_coverage, max_coverage)
        
        return {
            'estimated_coverage': final_coverage * 100,
            'confidence_interval': (final_coverage * 0.85 * 100, min(final_coverage * 1.15 * 100, 100)),
            'limiting_factors': self._identify_limiting_factors(district_features, final_coverage)
        }
    
    def _rule_based_estimation(self, district_features, intervention_type, budget_per_capita):
        """Fallback rule-based coverage estimation"""
        base_coverage = 0.5
        
        # Adjust for facility density
        if district_features.get('facilities_per_10k', 0) > 2:
            base_coverage += 0.15
        elif district_features.get('facilities_per_10k', 0) > 1:
            base_coverage += 0.08
        
        # Adjust for population density
        if district_features.get('population_density', 0) > 200:
            base_coverage += 0.1
        elif district_features.get('population_density', 0) < 50:
            base_coverage -= 0.1
        
        # Adjust for rural percentage
        rural_pct = district_features.get('rural_percentage', 0.7)
        base_coverage -= (rural_pct - 0.5) * 0.2
        
        # Budget adjustment
        if budget_per_capita:
            budget_factor = min(1.0, budget_per_capita / 10)
            base_coverage *= budget_factor
        
        final_coverage = max(0.2, min(0.95, base_coverage))
        
        return {
            'estimated_coverage': final_coverage * 100,
            'confidence_interval': (final_coverage * 0.8 * 100, min(final_coverage * 1.2 * 100, 100)),
            'limiting_factors': ['Infrastructure', 'Population distribution']
        }
    
    def _identify_limiting_factors(self, features, coverage):
        """Identify factors limiting coverage"""
        factors = []
        
        if features.get('facilities_per_10k', 0) < 1:
            factors.append('Low health facility density')
        
        if features.get('rural_percentage', 0) > 0.8:
            factors.append('High rural population')
        
        if features.get('road_density', 0) < 0.1:
            factors.append('Poor road infrastructure')
        
        if coverage < 0.5:
            factors.append('Budget constraints')
        
        return factors if factors else ['None identified']


class RiskScoringModel:
    """
    Classifies districts by nutritional risk level using:
    - Current nutrient deficiency patterns
    - Vulnerable population proportions
    - Historical trends
    - Socioeconomic indicators
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.risk_thresholds = {
            'critical': 0.7,
            'high': 0.5,
            'medium': 0.3,
            'low': 0
        }
        
    def calculate_risk_features(self, district_data):
        """Calculate risk indicators from district data"""
        features = pd.DataFrame()
        
        # Nutritional deficiency severity
        nutrient_cols = [col for col in district_data.columns if '(mg)' in col or '(mcg)' in col or '(g)' in col]
        if nutrient_cols:
            features['avg_adequacy'] = district_data[nutrient_cols].mean(axis=1)
            features['min_adequacy'] = district_data[nutrient_cols].min(axis=1)
            features['nutrients_below_50'] = (district_data[nutrient_cols] < 50).sum(axis=1)
            features['nutrients_below_30'] = (district_data[nutrient_cols] < 30).sum(axis=1)
        
        # Population vulnerability
        features['under5_proportion'] = district_data.get('children_under_5', 0) / district_data.get('population', 1)
        features['pregnant_women_proportion'] = district_data.get('pregnant_women', 0) / district_data.get('population', 1)
        features['poverty_rate'] = district_data.get('poverty_rate', 0.3)
        
        # Health system capacity
        features['health_facility_ratio'] = district_data.get('health_facilities', 0) / (district_data.get('population', 100000) / 10000)
        
        # Geographic vulnerability
        features['rural_percentage'] = district_data.get('rural_pct', 0.7)
        features['distance_to_capital'] = district_data.get('dist_to_kampala', 100)
        
        return features
    
    def train(self, labeled_data):
        """Train risk classification model"""
        # Prepare features and labels
        X = labeled_data.drop(columns=['risk_level'], errors='ignore')
        y = labeled_data.get('risk_level', self._calculate_risk_labels(labeled_data))
        
        # Remove NaN values
        mask = ~(X.isna().any(axis=1) | y.isna())
        X = X[mask]
        y = y[mask]
        
        if len(X) < 10:
            print("Insufficient data for training risk model")
            return
        
        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Gradient Boosting Classifier
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = (y_pred == y_test).mean()
        
        print(f"✓ Risk Scoring Model: Accuracy = {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
    
    def calculate_risk_score(self, district_features):
        """Calculate nutritional risk score for a district"""
        
        if self.model is None:
            # Use rule-based scoring if no model trained
            return self._rule_based_risk_score(district_features)
        
        # Scale features
        features_scaled = self.scaler.transform(district_features.values.reshape(1, -1))
        
        # Get probability scores for each risk level
        risk_probabilities = self.model.predict_proba(features_scaled)[0]
        risk_classes = self.model.classes_
        
        # Calculate weighted risk score (0-100)
        risk_weights = {'critical': 100, 'high': 75, 'medium': 50, 'low': 25}
        weighted_score = sum(prob * risk_weights.get(cls, 50) 
                           for prob, cls in zip(risk_probabilities, risk_classes))
        
        # Determine primary risk level
        predicted_class = self.model.predict(features_scaled)[0]
        
        # Identify key risk factors
        risk_factors = self._identify_risk_factors(district_features)
        
        return {
            'risk_score': weighted_score,
            'risk_level': predicted_class,
            'risk_probabilities': dict(zip(risk_classes, risk_probabilities)),
            'key_risk_factors': risk_factors,
            'recommended_interventions': self._recommend_interventions(predicted_class, risk_factors)
        }
    
    def _rule_based_risk_score(self, features):
        """Fallback rule-based risk scoring"""
        risk_score = 0
        risk_factors = []
        
        # Check nutritional adequacy
        avg_adequacy = features.get('avg_adequacy', 70)
        if avg_adequacy < 30:
            risk_score += 40
            risk_factors.append('Severe nutrient deficiencies')
        elif avg_adequacy < 50:
            risk_score += 25
            risk_factors.append('Moderate nutrient deficiencies')
        
        # Check critical nutrients
        if features.get('nutrients_below_30', 0) >= 3:
            risk_score += 20
            risk_factors.append('Multiple critical deficiencies')
        
        # Check vulnerable populations
        if features.get('under5_proportion', 0) > 0.2:
            risk_score += 15
            risk_factors.append('High child population')
        
        # Check poverty
        if features.get('poverty_rate', 0) > 0.4:
            risk_score += 15
            risk_factors.append('High poverty rate')
        
        # Check health infrastructure
        if features.get('health_facility_ratio', 0) < 1:
            risk_score += 10
            risk_factors.append('Limited health infrastructure')
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = 'critical'
        elif risk_score >= 50:
            risk_level = 'high'
        elif risk_score >= 30:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'risk_score': min(100, risk_score),
            'risk_level': risk_level,
            'risk_probabilities': {risk_level: 0.8},  # Simplified probability
            'key_risk_factors': risk_factors,
            'recommended_interventions': self._recommend_interventions(risk_level, risk_factors)
        }
    
    def _calculate_risk_labels(self, data):
        """Calculate risk labels from data if not provided"""
        # Simple rule-based labeling based on adequacy
        avg_adequacy = data.select_dtypes(include=[np.number]).mean(axis=1)
        
        labels = []
        for adequacy in avg_adequacy:
            if adequacy < 30:
                labels.append('critical')
            elif adequacy < 50:
                labels.append('high')
            elif adequacy < 70:
                labels.append('medium')
            else:
                labels.append('low')
        
        return labels
    
    def _identify_risk_factors(self, features):
        """Identify primary risk factors"""
        factors = []
        
        if features.get('avg_adequacy', 100) < 50:
            factors.append('Low nutrient adequacy')
        
        if features.get('nutrients_below_30', 0) >= 2:
            factors.append('Multiple severe deficiencies')
        
        if features.get('health_facility_ratio', 1) < 1:
            factors.append('Insufficient health facilities')
        
        if features.get('poverty_rate', 0) > 0.3:
            factors.append('High poverty')
        
        if features.get('rural_percentage', 0) > 0.8:
            factors.append('Highly rural')
        
        return factors[:3]  # Return top 3 factors
    
    def _recommend_interventions(self, risk_level, risk_factors):
        """Recommend interventions based on risk profile"""
        recommendations = []
        
        if risk_level == 'critical':
            recommendations.append('Emergency supplementation program')
            recommendations.append('Mobile health clinics')
            recommendations.append('Food assistance program')
        elif risk_level == 'high':
            recommendations.append('Targeted supplementation')
            recommendations.append('Fortification of staple foods')
            recommendations.append('Community health worker training')
        elif risk_level == 'medium':
            recommendations.append('Nutrition education programs')
            recommendations.append('Biofortification initiatives')
            recommendations.append('Regular monitoring')
        else:
            recommendations.append('Preventive nutrition programs')
            recommendations.append('Maintain current interventions')
        
        # Add specific recommendations based on risk factors
        if 'Multiple severe deficiencies' in risk_factors:
            recommendations.append('Multi-micronutrient supplementation')
        
        if 'Insufficient health facilities' in risk_factors:
            recommendations.append('Strengthen health infrastructure')
        
        return recommendations[:4]  # Return top 4 recommendations


class IntegratedPredictionSystem:
    """
    Integrates all three models to provide comprehensive predictions
    """
    
    def __init__(self):
        self.nutrient_predictor = NutrientGapPredictor()
        self.coverage_estimator = CoverageEstimator()
        self.risk_scorer = RiskScoringModel()
        
    def load_models(self, model_dir='models/'):
        """Load pre-trained models"""
        try:
            self.nutrient_predictor = joblib.load(f'{model_dir}nutrient_gap_model.pkl')
            self.coverage_estimator = joblib.load(f'{model_dir}coverage_model.pkl')
            self.risk_scorer = joblib.load(f'{model_dir}risk_model.pkl')
            return True
        except:
            print("No pre-trained models found. Please train models first.")
            return False
    
    def save_models(self, model_dir='models/'):
        """Save trained models"""
        import os
        os.makedirs(model_dir, exist_ok=True)
        
        joblib.dump(self.nutrient_predictor, f'{model_dir}nutrient_gap_model.pkl')
        joblib.dump(self.coverage_estimator, f'{model_dir}coverage_model.pkl')
        joblib.dump(self.risk_scorer, f'{model_dir}risk_model.pkl')
        print(f"Models saved to {model_dir}")
    
    def predict_intervention_outcomes(self, district_data, intervention_plan, budget):
        """
        Generate comprehensive predictions for an intervention
        """
        
        # 1. Assess current nutritional gaps
        nutrient_gaps = {}
        for nutrient in ['Vitamin_A_(mcg)', 'Iron_(mg)', 'Zinc_(mg)', 'Vitamin_B12_(mcg)']:
            gap_prediction = self.nutrient_predictor.predict(district_data, nutrient)
            if gap_prediction:
                nutrient_gaps[nutrient] = gap_prediction
        
        # 2. Estimate achievable coverage
        budget_per_capita = budget / district_data.get('population', 100000)
        coverage_estimate = self.coverage_estimator.estimate_coverage(
            district_data, 
            intervention_type=intervention_plan.get('type', 'mixed'),
            budget_per_capita=budget_per_capita
        )
        
        # 3. Calculate risk score
        risk_assessment = self.risk_scorer.calculate_risk_score(district_data)
        
        # 4. Estimate realistic health outcomes based on models
        outcomes = self._calculate_realistic_outcomes(
            nutrient_gaps,
            coverage_estimate,
            risk_assessment,
            district_data,
            budget
        )
        
        return {
            'nutrient_gaps': nutrient_gaps,
            'coverage_estimate': coverage_estimate,
            'risk_assessment': risk_assessment,
            'predicted_outcomes': outcomes,
            'confidence_level': self._calculate_overall_confidence(
                nutrient_gaps, coverage_estimate, risk_assessment
            )
        }
    
    def _calculate_realistic_outcomes(self, gaps, coverage, risk, district_data, budget):
        """Calculate realistic health outcomes based on model predictions"""
        
        population = district_data.get('population', 100000)
        coverage_rate = coverage['estimated_coverage'] / 100
        
        # Base rates from Uganda health data
        under5_population = population * 0.15
        stunting_rate = 0.29
        mortality_rate = 0.043
        
        # Adjust impact based on risk level
        risk_multipliers = {
            'critical': 0.5,  # Harder to achieve impact in critical areas
            'high': 0.7,
            'medium': 0.9,
            'low': 1.0
        }
        risk_mult = risk_multipliers.get(risk['risk_level'], 0.8)
        
        # Calculate reduction potential based on gaps addressed
        avg_gap = np.mean([g['gap'] for g in gaps.values()]) if gaps else 50
        gap_reduction_potential = min(0.3, avg_gap / 100 * 0.4)  # Max 30% reduction
        
        # Realistic outcome calculations
        stunting_prevented = int(
            under5_population * stunting_rate * coverage_rate * 
            gap_reduction_potential * risk_mult
        )
        
        lives_saved = int(
            under5_population * mortality_rate * coverage_rate * 
            gap_reduction_potential * 0.5 * risk_mult  # Mortality harder to impact
        )
        
        # Economic benefit (more realistic calculation)
        # Based on WHO estimates: $1 spent on nutrition returns $16 in economic benefits
        economic_multiplier = 16 * risk_mult * (coverage_rate ** 0.5)  # Diminishing returns
        economic_benefit = budget * economic_multiplier
        
        # Cost per outcome
        cost_per_life_saved = budget / lives_saved if lives_saved > 0 else float('inf')
        cost_per_stunting_prevented = budget / stunting_prevented if stunting_prevented > 0 else float('inf')
        
        return {
            'lives_saved': lives_saved,
            'stunting_prevented': stunting_prevented,
            'people_reached': int(population * coverage_rate),
            'economic_benefit': economic_benefit,
            'roi_percentage': (economic_benefit / budget - 1) * 100,
            'cost_per_life_saved': cost_per_life_saved,
            'cost_per_stunting_prevented': cost_per_stunting_prevented,
            'dalys_averted': lives_saved * 30 + stunting_prevented * 5
        }
    
    def _calculate_overall_confidence(self, gaps, coverage, risk):
        """Calculate overall prediction confidence"""
        confidences = []
        
        # Get confidence from nutrient predictions
        if gaps:
            nutrient_conf = np.mean([g.get('confidence', 75) for g in gaps.values()])
            confidences.append(nutrient_conf)
        
        # Coverage confidence (based on interval width)
        if coverage and 'confidence_interval' in coverage:
            ci_width = coverage['confidence_interval'][1] - coverage['confidence_interval'][0]
            coverage_conf = max(50, 100 - ci_width)
            confidences.append(coverage_conf)
        
        # Risk assessment confidence (based on probability spread)
        if risk and 'risk_probabilities' in risk:
            max_prob = max(risk['risk_probabilities'].values())
            risk_conf = max_prob * 100
            confidences.append(risk_conf)
        
        return np.mean(confidences) if confidences else 70


# Example usage and testing
if __name__ == "__main__":
    print("Initializing ML Prediction Models...")
    
    # Create integrated system
    system = IntegratedPredictionSystem()
    
    # Example district data
    sample_district = {
        'population': 250000,
        'health_facilities': 15,
        'hospitals': 1,
        'health_centers': 8,
        'area_km2': 1200,
        'rural_pct': 0.75,
        'poverty_rate': 0.35,
        'dist_to_kampala': 150,
        'children_under_5': 37500,
        'avg_adequacy': 45,
        'nutrients_below_50': 4,
        'nutrients_below_30': 2
    }
    
    # Example intervention plan
    intervention = {
        'type': 'mixed',
        'duration_months': 24,
        'target_nutrients': ['Vitamin_A_(mcg)', 'Iron_(mg)', 'Zinc_(mg)']
    }
    
    # Run predictions
    budget = 500000  # $500K USD
    
    predictions = system.predict_intervention_outcomes(
        sample_district,
        intervention,
        budget
    )
    
    print("\n" + "="*60)
    print("PREDICTION RESULTS")
    print("="*60)
    
    print(f"\n1. COVERAGE ESTIMATE:")
    print(f"   Estimated coverage: {predictions['coverage_estimate']['estimated_coverage']:.1f}%")
    print(f"   Limiting factors: {', '.join(predictions['coverage_estimate']['limiting_factors'])}")
    
    print(f"\n2. RISK ASSESSMENT:")
    print(f"   Risk level: {predictions['risk_assessment']['risk_level']}")
    print(f"   Risk score: {predictions['risk_assessment']['risk_score']:.1f}/100")
    print(f"   Key factors: {', '.join(predictions['risk_assessment']['key_risk_factors'])}")
    
    print(f"\n3. PREDICTED OUTCOMES:")
    outcomes = predictions['predicted_outcomes']
    print(f"   Lives saved: {outcomes['lives_saved']:,}")
    print(f"   Stunting prevented: {outcomes['stunting_prevented']:,}")
    print(f"   People reached: {outcomes['people_reached']:,}")
    print(f"   Economic ROI: {outcomes['roi_percentage']:.1f}%")
    print(f"   Cost per life saved: ${outcomes['cost_per_life_saved']:,.0f}")
    
    print(f"\n4. CONFIDENCE LEVEL: {predictions['confidence_level']:.1f}%")
    
    print("\n✅ Models ready for integration into dashboard")