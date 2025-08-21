"""
Integration module to replace hardcoded values with dynamic data
This connects the configuration system to the main application
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from uganda_nutrition_config import get_config
import streamlit as st

class DynamicDataProvider:
    """Provides dynamic data to replace hardcoded values in the main application"""
    
    def __init__(self):
        self.config = get_config()
        self.initialize_session_data()
    
    def initialize_session_data(self):
        """Initialize session-specific data"""
        if 'program_start_date' not in st.session_state:
            st.session_state.program_start_date = pd.Timestamp.now()
        
        if 'program_phase' not in st.session_state:
            st.session_state.program_phase = 'planning'
    
    def get_population_constants(self) -> Dict[str, int]:
        """Replace hardcoded population constants"""
        pop = self.config.get_population_estimate()
        age_dist = self.config.get_age_distribution()
        stunting_rate = self.config.get_stunting_rate()
        
        return {
            'UGANDA_POPULATION': pop,
            'STUNTED_CHILDREN': int(pop * age_dist['under_5'] * stunting_rate),
            'CHILDREN_UNDER_5': int(pop * age_dist['under_5']),
            'PREGNANT_WOMEN': int(pop * age_dist['pregnant_lactating']),
            'RURAL_POPULATION': int(pop * self.config.baseline_data['demographics']['urban_rural_split']['rural'])
        }
    
    def get_intervention_details(self) -> Dict[str, Dict[str, Any]]:
        """Get dynamic intervention details"""
        interventions = {}
        
        for intervention_type in ['fortification', 'supplementation', 'education', 'biofortification']:
            cost_data = self.config.get_intervention_costs(intervention_type)
            
            # Map to expected format
            interventions[intervention_type] = {
                'name': intervention_type.title().replace('_', ' '),
                'unit_cost': cost_data['unit_cost'],
                'effectiveness': cost_data['effectiveness'],
                'reach_time': self._get_reach_time(intervention_type),
                'coverage_potential': self._get_coverage_potential(intervention_type),
                'description': self._get_intervention_description(intervention_type),
                'policy_requirements': self._get_policy_requirements(intervention_type)
            }
        
        return interventions
    
    def _get_reach_time(self, intervention_type: str) -> int:
        """Get realistic reach times in months"""
        reach_times = {
            'fortification': 6,
            'supplementation': 3,
            'education': 12,
            'biofortification': 18
        }
        return reach_times.get(intervention_type, 9)
    
    def _get_coverage_potential(self, intervention_type: str) -> float:
        """Get realistic coverage potential"""
        # Based on program phase and intervention type
        phase = st.session_state.get('program_phase', 'planning')
        phase_multipliers = {
            'planning': 0.0,
            'pilot': 0.3,
            'implementation': 0.6,
            'scale_up': 0.8,
            'mature': 0.9
        }
        
        base_coverage = {
            'fortification': 0.85,
            'supplementation': 0.70,
            'education': 0.90,
            'biofortification': 0.75
        }
        
        phase_mult = phase_multipliers.get(phase, 0.5)
        base = base_coverage.get(intervention_type, 0.75)
        
        return min(base * phase_mult, base)
    
    def _get_intervention_description(self, intervention_type: str) -> str:
        """Get detailed intervention descriptions"""
        descriptions = {
            'fortification': """
                **What it is:** Adding essential nutrients to commonly consumed foods.
                
                **Coverage:** Reaches {coverage:.0%} of population through regular food consumption
                **Cost-effectiveness:** ${cost:.2f} per person per year
                **Impact timeline:** {timeline} months to measurable impact
                
                **Success factors:**
                • Government mandate and enforcement
                • Industry compliance monitoring
                • Consumer awareness campaigns
            """,
            'supplementation': """
                **What it is:** Direct provision of nutrient supplements to at-risk populations.
                
                **Target efficiency:** {effectiveness:.0%} reduction in deficiency
                **Delivery mechanism:** Health facilities and community workers
                **Compliance rate:** {compliance:.0%} with proper monitoring
                
                **Critical requirements:**
                • Cold chain for certain supplements
                • Regular distribution schedule
                • Beneficiary tracking system
            """,
            'education': """
                **What it is:** Community-based nutrition education and behavior change.
                
                **Sustainability:** Long-term behavior change
                **Cost efficiency:** ${cost:.2f} per person
                **Reach:** {coverage:.0%} of communities
                
                **Key components:**
                • Cooking demonstrations
                • Kitchen gardens
                • WASH integration
            """,
            'biofortification': """
                **What it is:** Nutrient-rich crop varieties through breeding.
                
                **Adoption rate:** {adoption:.0%} of farmers after 2 years
                **Yield impact:** Minimal to positive
                **Sustainability:** Self-sustaining after adoption
                
                **Available crops:**
                • Orange sweet potato (Vitamin A)
                • High-iron beans
                • Zinc maize
            """
        }
        
        desc_template = descriptions.get(intervention_type, "Standard intervention")
        cost_data = self.config.get_intervention_costs(intervention_type)
        
        return desc_template.format(
            coverage=self._get_coverage_potential(intervention_type),
            cost=cost_data['unit_cost'],
            effectiveness=cost_data['effectiveness'],
            timeline=self._get_reach_time(intervention_type),
            compliance=0.70 + np.random.uniform(-0.05, 0.05),
            adoption=0.60 + np.random.uniform(-0.10, 0.10)
        )
    
    def _get_policy_requirements(self, intervention_type: str) -> List[str]:
        """Get policy requirements for each intervention"""
        requirements = {
            'fortification': [
                "Mandatory fortification legislation",
                "Quality standards (UNBS certification)",
                "Industry compliance monitoring framework",
                "Import regulations for premix"
            ],
            'supplementation': [
                "National supplementation protocol",
                "Integration with child health days",
                "Supply chain management system",
                "Healthcare worker training program"
            ],
            'education': [
                "Behavior change communication strategy",
                "Community health worker deployment",
                "School curriculum integration",
                "Media campaign authorization"
            ],
            'biofortification': [
                "Seed certification standards",
                "Agricultural extension integration",
                "Farmer subsidy program",
                "Market linkage support"
            ]
        }
        return requirements.get(intervention_type, ["Standard requirements"])
    
    def calculate_health_outcomes(self, budget: float, population: int, 
                                 intervention_mix: Dict[str, float],
                                 selected_nutrients: List[str]) -> Dict[str, Any]:
        """Calculate health outcomes with dynamic parameters"""
        
        # Get dynamic multipliers
        impact_multipliers = self.config.get_health_impact_multipliers()
        health_indicators = self.config.baseline_data['health_indicators']
        
        # Calculate coverage based on budget and intervention mix
        total_cost = 0
        total_effectiveness = 0
        
        for intervention, percentage in intervention_mix.items():
            if percentage > 0:
                cost_data = self.config.get_intervention_costs(intervention)
                total_cost += (percentage / 100) * cost_data['unit_cost']
                total_effectiveness += (percentage / 100) * cost_data['effectiveness']
        
        # Realistic coverage calculation
        if total_cost > 0:
            coverage = min(0.95, (budget / (total_cost * population)))
        else:
            coverage = 0
        
        # Apply nutrient synergy bonus (if multiple nutrients selected)
        synergy_factor = 1.0 + (0.1 * max(0, len(selected_nutrients) - 1))
        synergy_factor = min(synergy_factor, 1.5)  # Cap at 50% bonus
        
        total_effectiveness *= synergy_factor
        
        # Calculate realistic health impacts
        pop_constants = self.get_population_constants()
        
        # Lives saved calculation (more conservative)
        u5_mortality = self.config.get_u5_mortality()
        baseline_deaths = int(pop_constants['CHILDREN_UNDER_5'] * (u5_mortality / 1000))
        mortality_reduction = min(0.25, total_effectiveness * 0.20)  # Max 25% reduction
        lives_saved = int(coverage * baseline_deaths * mortality_reduction)
        
        # Stunting prevention (gradual impact)
        stunting_rate = health_indicators['stunting_rate']
        stunted_children = int(pop_constants['CHILDREN_UNDER_5'] * stunting_rate)
        stunting_reduction = min(0.30, total_effectiveness * 0.25)  # Max 30% reduction
        stunting_prevented = int(coverage * stunted_children * stunting_reduction)
        
        # Anemia reduction
        anemia_rates = self.config.get_anemia_prevalence()
        anemia_baseline = int(pop_constants['CHILDREN_UNDER_5'] * anemia_rates['children_under_5'])
        anemia_reduction = min(0.40, total_effectiveness * 0.35)  # Max 40% reduction
        anemia_reduced = int(coverage * anemia_baseline * anemia_reduction)
        
        # Economic benefits
        healthcare_savings = coverage * population * total_effectiveness * impact_multipliers['healthcare_cost_saved_per_beneficiary']
        productivity_gains = stunting_prevented * impact_multipliers['productivity_gain_per_stunting_prevented']
        economic_benefit = healthcare_savings + productivity_gains
        
        # DALYs calculation
        dalys_averted = (
            lives_saved * impact_multipliers['daly_per_life_saved'] +
            stunting_prevented * impact_multipliers['daly_per_stunting_prevented'] +
            anemia_reduced * impact_multipliers['daly_per_anemia_case_prevented']
        )
        
        # Health impact score (0-100)
        max_possible_impact = population * 0.3  # Maximum 30% of population impacted
        actual_impact = lives_saved + stunting_prevented + anemia_reduced
        health_impact = min(100, (actual_impact / max_possible_impact) * 100)
        
        return {
            'lives_saved': lives_saved,
            'stunting_prevented': stunting_prevented,
            'anemia_reduced': anemia_reduced,
            'coverage': coverage * 100,
            'effectiveness': total_effectiveness * 100,
            'economic_benefit': economic_benefit,
            'dalys_averted': int(dalys_averted),
            'health_impact': health_impact,
            'cost_per_daly': budget / max(dalys_averted, 1),
            'cost_per_life_saved': budget / max(lives_saved, 1)
        }
    
    def get_monitoring_metrics(self, intervention_data: Dict[str, Any], 
                              time_period: str) -> Dict[str, Any]:
        """Get realistic monitoring metrics based on program maturity"""
        
        # Determine program phase based on time
        if hasattr(st.session_state, 'program_start_date'):
            days_elapsed = (pd.Timestamp.now() - st.session_state.program_start_date).days
            if days_elapsed < 90:
                phase = 'pilot'
            elif days_elapsed < 365:
                phase = 'implementation'
            elif days_elapsed < 730:
                phase = 'scale_up'
            else:
                phase = 'mature'
        else:
            phase = 'implementation'
        
        return self.config.get_monitoring_metrics(phase)
    
    def get_staffing_requirements(self, coverage_population: int) -> Dict[str, int]:
        """Get dynamic staffing requirements"""
        return self.config.get_staffing_requirements(coverage_population)
    
    def get_kpi_targets(self) -> Dict[str, Any]:
        """Get dynamic KPI targets"""
        # Calculate based on program duration
        if hasattr(st.session_state, 'program_start_date'):
            years = (pd.Timestamp.now() - st.session_state.program_start_date).days / 365
        else:
            years = 1
        
        targets = self.config.get_kpi_targets(int(years))
        
        # Format for display
        return {
            'Coverage Rate': f"{targets['coverage_rate']*100:.0f}%",
            'Supplement Compliance': f"{targets['compliance_rate']*100:.0f}%",
            'Fortification Standards Met': f"{targets['fortification_standards']*100:.0f}%",
            'Stock-out Rate': f"<{targets['stock_out_rate']*100:.0f}%",
            'Cost per Beneficiary': f"<${targets['cost_per_beneficiary']:.0f}",
            'Stunting Reduction Rate': f"{targets['stunting_reduction']*100:.0f}%",
            'Anemia Reduction': f"{targets['anemia_reduction']*100:.0f}%",
            'B12 Deficiency Reduction': f"{targets['b12_deficiency_reduction']*100:.0f}%"
        }
    
    def get_financial_projections(self, base_budget: float, years: int = 5) -> Dict[str, Any]:
        """Get realistic financial projections"""
        return self.config.get_financial_projections(base_budget, years)
    
    def get_scenario_analysis(self) -> Dict[str, Dict[str, Any]]:
        """Get scenario analysis parameters"""
        scenarios = self.config.get_scenario_probabilities()
        
        # Format for display
        formatted = {}
        for scenario_name, params in scenarios.items():
            formatted[scenario_name.replace('_', ' ').title()] = {
                'probability': params['probability'],
                'impact': params['impact_multiplier'],
                'cost': params['cost_multiplier'],
                'timeline': params['timeline_multiplier'],
                'color': {'best_case': 'green', 'expected_case': 'blue', 'worst_case': 'red'}[scenario_name]
            }
        
        return formatted
    
    def get_gauge_values(self) -> Dict[str, float]:
        """Get current gauge values based on actual metrics"""
        metrics = self.get_monitoring_metrics({}, 'current')
        
        return {
            'coverage_rate': metrics['coverage_rate'],
            'compliance': metrics['compliance_rate'],
            'quality_score': metrics['quality_scores'],
            'cost_per_person': 20 - (metrics['cost_efficiency'] * 5)  # Inverse relationship
        }
    
    def get_success_metrics_table(self) -> pd.DataFrame:
        """Get success metrics with realistic baselines and targets"""
        
        current_year = pd.Timestamp.now().year
        baseline_year = 2020
        target_year = 2025
        
        # Calculate current values based on trends
        years_passed = current_year - baseline_year
        years_to_target = target_year - current_year
        
        health_indicators = self.config.baseline_data['health_indicators']
        
        # Stunting trajectory
        stunting_baseline = 29.0
        stunting_annual_reduction = 0.75  # 0.75% per year
        stunting_current = max(20, stunting_baseline - (stunting_annual_reduction * years_passed))
        stunting_target = max(15, stunting_current - (stunting_annual_reduction * years_to_target))
        
        # Similar calculations for other indicators
        metrics_data = {
            'Indicator': ['Stunting Reduction', 'Anemia Reduction', 'B12 Improvement', 'Coverage Achieved', 'Cost Efficiency'],
            'Baseline (2020)': [f'{stunting_baseline:.0f}%', '28%', '37% deficient', '0%', 'N/A'],
            'Current ({})'.format(current_year): [
                f'{stunting_current:.0f}%',
                f'{max(15, 28 - years_passed * 1.0):.0f}%',
                f'{max(20, 37 - years_passed * 1.5):.0f}% deficient',
                f'{min(60, years_passed * 12):.0f}%',
                f'${max(15, 25 - years_passed * 1.5):.0f}/person'
            ],
            'Target (2025)': [f'{stunting_target:.0f}%', '15%', '20% deficient', '80%', '$15/person'],
            'Progress': self._calculate_progress_indicators(
                [stunting_current, 28 - years_passed * 1.0, 37 - years_passed * 1.5, 
                 years_passed * 12, 25 - years_passed * 1.5],
                [stunting_target, 15, 20, 80, 15]
            )
        }
        
        return pd.DataFrame(metrics_data)
    
    def _calculate_progress_indicators(self, current_values: List[float], 
                                      target_values: List[float]) -> List[str]:
        """Calculate progress indicators for metrics"""
        progress = []
        for current, target in zip(current_values, target_values):
            if isinstance(current, (int, float)) and isinstance(target, (int, float)):
                achievement = (target - current) / max(abs(target), 1) * 100
                if achievement < 30:
                    progress.append('🟢 Good')
                elif achievement < 60:
                    progress.append('🟡 On track')
                else:
                    progress.append('🔴 Behind')
            else:
                progress.append('🟡 On track')
        return progress
    
    def get_live_data_feed(self) -> pd.DataFrame:
        """Generate realistic live data feed"""
        
        # Get current metrics
        metrics = self.get_monitoring_metrics({}, 'current')
        coverage = metrics['coverage_rate'] / 100
        
        # Calculate realistic ranges based on coverage
        pop_constants = self.get_population_constants()
        daily_reach = int(pop_constants['UGANDA_POPULATION'] * coverage / 365)
        
        return pd.DataFrame({
            'Metric': ['New Beneficiaries', 'Supplements Distributed', 'Districts Active', 'Staff Deployed'],
            'Value': [
                np.random.randint(int(daily_reach * 0.8), int(daily_reach * 1.2)),
                np.random.randint(int(daily_reach * 3), int(daily_reach * 5)),  # Multiple supplements per person
                np.random.randint(40, 80),  # Active districts
                np.random.randint(100, 300)  # Staff on duty
            ],
            'Status': ['Active', 'Normal', 'Operational', 'Deployed']
        })
    
    def get_district_data(self, district_name: str) -> Dict[str, Any]:
        """Get district-specific dynamic data"""
        return self.config.get_district_specific_data(district_name)

# Singleton instance
_provider_instance = None

def get_data_provider() -> DynamicDataProvider:
    """Get or create the data provider instance"""
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = DynamicDataProvider()
    return _provider_instance