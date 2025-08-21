"""
Supply Chain Optimization Module for Uganda Nutrition Interventions
Implements network optimization for distribution of nutrition supplements
"""

import numpy as np
import pandas as pd
import networkx as nx
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math

@dataclass
class DistributionHub:
    """Represents a distribution center or health facility"""
    name: str
    district: str
    location: Tuple[float, float]  # (lat, lon)
    capacity: int  # Storage capacity in units
    type: str  # 'national', 'regional', 'district', 'facility'
    cold_chain: bool = False
    staff_count: int = 0

@dataclass 
class Route:
    """Represents a distribution route between hubs"""
    from_hub: str
    to_hub: str
    distance_km: float
    transport_mode: str  # 'truck', 'motorcycle', 'bicycle', 'foot'
    cost_per_km: float
    time_hours: float
    reliability: float  # 0-1 score

class SupplyChainOptimizer:
    """Optimizes the supply chain network for nutrition interventions"""
    
    def __init__(self, facilities_data: pd.DataFrame, population_data: pd.DataFrame):
        self.facilities = facilities_data
        self.population = population_data
        self.network = nx.DiGraph()
        self.hubs = {}
        self.routes = []
        self._build_network()
        
    def _build_network(self):
        """Build the supply chain network from facility data"""
        
        # Create national hub (Kampala)
        national_hub = DistributionHub(
            name="National_Medical_Stores",
            district="KAMPALA",
            location=(0.3476, 32.5825),  # Kampala coordinates
            capacity=1000000,
            type="national",
            cold_chain=True,
            staff_count=50
        )
        self.hubs[national_hub.name] = national_hub
        self.network.add_node(national_hub.name, **national_hub.__dict__)
        
        # Create regional hubs (one per region)
        regions = {
            'Central': ('KAMPALA', (0.3476, 32.5825)),
            'Eastern': ('MBALE', (1.0821, 34.1758)),
            'Northern': ('GULU', (2.7809, 32.2995)),
            'Western': ('MBARARA', (-0.6118, 30.6587))
        }
        
        for region, (district, coords) in regions.items():
            hub = DistributionHub(
                name=f"{region}_Regional_Hub",
                district=district,
                location=coords,
                capacity=200000,
                type="regional",
                cold_chain=True,
                staff_count=20
            )
            self.hubs[hub.name] = hub
            self.network.add_node(hub.name, **hub.__dict__)
            
            # Connect to national hub
            distance = self._calculate_distance(national_hub.location, coords)
            self.network.add_edge(
                national_hub.name, 
                hub.name,
                distance=distance,
                cost=distance * 0.5,  # $0.5 per km for truck
                time=distance / 60,  # 60 km/h average
                reliability=0.95
            )
        
        # Create district hubs from facilities data
        if self.facilities is not None and not self.facilities.empty:
            for idx, row in self.facilities.iterrows():
                if idx >= 50:  # Limit to first 50 districts for performance
                    break
                    
                district_name = row.get('District', f'District_{idx}')
                if pd.isna(district_name):
                    continue
                    
                # Estimate location (would use real coordinates in production)
                lat = np.random.uniform(-1.5, 4.0)  # Uganda latitude range
                lon = np.random.uniform(29.5, 35.0)  # Uganda longitude range
                
                # Calculate capacity based on facilities
                total_facilities = 0
                for col in ['CLINIC', 'HC_II', 'HC_III', 'HC_IV', 'HOSPITAL']:
                    if col in row.index:
                        val = row[col]
                        if not pd.isna(val):
                            total_facilities += int(val) if isinstance(val, (int, float)) else 0
                
                hub = DistributionHub(
                    name=f"{district_name}_District_Hub",
                    district=district_name,
                    location=(lat, lon),
                    capacity=total_facilities * 1000,  # 1000 units per facility
                    type="district",
                    cold_chain=(total_facilities > 10),  # Cold chain if enough facilities
                    staff_count=max(2, total_facilities // 5)
                )
                self.hubs[hub.name] = hub
                self.network.add_node(hub.name, **hub.__dict__)
                
                # Connect to nearest regional hub
                nearest_region = self._find_nearest_regional_hub((lat, lon))
                if nearest_region:
                    distance = self._calculate_distance(
                        self.hubs[nearest_region].location, 
                        (lat, lon)
                    )
                    self.network.add_edge(
                        nearest_region,
                        hub.name,
                        distance=distance,
                        cost=distance * 0.3,  # Lower cost for shorter routes
                        time=distance / 40,  # 40 km/h for district roads
                        reliability=0.85
                    )
    
    def _calculate_distance(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        """Calculate distance between two locations using Haversine formula"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def _find_nearest_regional_hub(self, location: Tuple[float, float]) -> Optional[str]:
        """Find the nearest regional hub to a given location"""
        min_distance = float('inf')
        nearest_hub = None
        
        for hub_name, hub in self.hubs.items():
            if hub.type == 'regional':
                distance = self._calculate_distance(location, hub.location)
                if distance < min_distance:
                    min_distance = distance
                    nearest_hub = hub_name
        
        return nearest_hub
    
    def optimize_distribution(self, demand: Dict[str, int], 
                            budget: float, 
                            priority_districts: List[str]) -> Dict:
        """
        Optimize distribution plan given demand and constraints
        
        Args:
            demand: District -> units needed
            budget: Available budget for distribution
            priority_districts: Districts to prioritize
            
        Returns:
            Optimized distribution plan
        """
        
        distribution_plan = {
            'routes': [],
            'total_cost': 0,
            'total_time': 0,
            'coverage': 0,
            'unmet_demand': {}
        }
        
        # Sort districts by priority and demand
        sorted_districts = sorted(
            demand.items(),
            key=lambda x: (x[0] not in priority_districts, -x[1])
        )
        
        remaining_budget = budget
        
        for district, units_needed in sorted_districts:
            hub_name = f"{district}_District_Hub"
            
            if hub_name not in self.network:
                distribution_plan['unmet_demand'][district] = units_needed
                continue
            
            # Find shortest path from national hub
            try:
                path = nx.shortest_path(
                    self.network, 
                    "National_Medical_Stores",
                    hub_name,
                    weight='cost'
                )
                
                # Calculate route cost
                route_cost = 0
                route_time = 0
                
                for i in range(len(path) - 1):
                    edge_data = self.network[path[i]][path[i+1]]
                    route_cost += edge_data['cost']
                    route_time += edge_data['time']
                
                # Add handling costs
                handling_cost = units_needed * 0.1  # $0.1 per unit handling
                total_cost = route_cost + handling_cost
                
                if total_cost <= remaining_budget:
                    distribution_plan['routes'].append({
                        'district': district,
                        'path': path,
                        'units': units_needed,
                        'cost': total_cost,
                        'time_hours': route_time,
                        'priority': district in priority_districts
                    })
                    
                    remaining_budget -= total_cost
                    distribution_plan['total_cost'] += total_cost
                    distribution_plan['total_time'] = max(distribution_plan['total_time'], route_time)
                else:
                    # Partial fulfillment if budget limited
                    affordable_units = int((remaining_budget / total_cost) * units_needed)
                    if affordable_units > 0:
                        partial_cost = (affordable_units / units_needed) * total_cost
                        distribution_plan['routes'].append({
                            'district': district,
                            'path': path,
                            'units': affordable_units,
                            'cost': partial_cost,
                            'time_hours': route_time,
                            'priority': district in priority_districts,
                            'partial': True
                        })
                        distribution_plan['unmet_demand'][district] = units_needed - affordable_units
                        remaining_budget -= partial_cost
                        distribution_plan['total_cost'] += partial_cost
                    else:
                        distribution_plan['unmet_demand'][district] = units_needed
                        
            except nx.NetworkXNoPath:
                distribution_plan['unmet_demand'][district] = units_needed
        
        # Calculate coverage
        total_demand = sum(demand.values())
        met_demand = sum(r['units'] for r in distribution_plan['routes'])
        distribution_plan['coverage'] = (met_demand / total_demand * 100) if total_demand > 0 else 0
        
        return distribution_plan
    
    def analyze_bottlenecks(self) -> Dict:
        """Identify bottlenecks in the supply chain network"""
        
        bottlenecks = {
            'capacity_constraints': [],
            'connectivity_issues': [],
            'reliability_concerns': [],
            'cold_chain_gaps': []
        }
        
        # Check capacity constraints
        for hub_name, hub in self.hubs.items():
            if hub.type == 'district':
                # Check if district hub has adequate capacity
                if hub.capacity < 5000:  # Minimum viable capacity
                    bottlenecks['capacity_constraints'].append({
                        'hub': hub_name,
                        'current_capacity': hub.capacity,
                        'recommended': 5000,
                        'gap': 5000 - hub.capacity
                    })
        
        # Check connectivity
        for node in self.network.nodes():
            in_degree = self.network.in_degree(node)
            if self.hubs[node].type == 'district' and in_degree == 0:
                bottlenecks['connectivity_issues'].append({
                    'hub': node,
                    'issue': 'No incoming routes'
                })
        
        # Check reliability
        for u, v, data in self.network.edges(data=True):
            if data.get('reliability', 1.0) < 0.8:
                bottlenecks['reliability_concerns'].append({
                    'route': f"{u} -> {v}",
                    'reliability': data.get('reliability', 'unknown'),
                    'recommendation': 'Improve road conditions or add alternative route'
                })
        
        # Check cold chain coverage
        cold_chain_districts = sum(1 for h in self.hubs.values() 
                                 if h.type == 'district' and h.cold_chain)
        total_districts = sum(1 for h in self.hubs.values() if h.type == 'district')
        
        if total_districts > 0:
            cold_chain_coverage = cold_chain_districts / total_districts
            if cold_chain_coverage < 0.5:
                bottlenecks['cold_chain_gaps'].append({
                    'current_coverage': f"{cold_chain_coverage*100:.1f}%",
                    'target': "50%",
                    'districts_needing_cold_chain': total_districts - cold_chain_districts
                })
        
        return bottlenecks
    
    def recommend_improvements(self, budget: float) -> List[Dict]:
        """Recommend supply chain improvements within budget"""
        
        recommendations = []
        remaining_budget = budget
        
        # Get bottlenecks
        bottlenecks = self.analyze_bottlenecks()
        
        # Priority 1: Fix connectivity issues
        for issue in bottlenecks['connectivity_issues']:
            cost = 50000  # Estimated cost to establish route
            if cost <= remaining_budget:
                recommendations.append({
                    'type': 'connectivity',
                    'action': f"Establish distribution route to {issue['hub']}",
                    'cost': cost,
                    'impact': 'high',
                    'timeline': '1-2 months'
                })
                remaining_budget -= cost
        
        # Priority 2: Address capacity constraints
        for constraint in bottlenecks['capacity_constraints']:
            upgrade_cost = constraint['gap'] * 10  # $10 per unit capacity
            if upgrade_cost <= remaining_budget:
                recommendations.append({
                    'type': 'capacity',
                    'action': f"Upgrade storage at {constraint['hub']}",
                    'cost': upgrade_cost,
                    'impact': 'medium',
                    'timeline': '2-3 months'
                })
                remaining_budget -= upgrade_cost
        
        # Priority 3: Improve cold chain
        if bottlenecks['cold_chain_gaps']:
            gap = bottlenecks['cold_chain_gaps'][0]
            cold_chain_cost = gap['districts_needing_cold_chain'] * 25000
            if cold_chain_cost <= remaining_budget:
                recommendations.append({
                    'type': 'cold_chain',
                    'action': f"Install cold chain in {gap['districts_needing_cold_chain']} districts",
                    'cost': cold_chain_cost,
                    'impact': 'high',
                    'timeline': '3-6 months'
                })
                remaining_budget -= cold_chain_cost
        
        return recommendations

# Example usage
if __name__ == "__main__":
    print("Supply Chain Optimizer Module Loaded")
    print("="*60)
    
    # Test with sample data
    facilities_df = pd.DataFrame({
        'District': ['KAMPALA', 'WAKISO', 'MUKONO', 'JINJA', 'GULU'],
        'HOSPITAL': [5, 3, 2, 2, 1],
        'HC_IV': [10, 8, 5, 4, 3],
        'HC_III': [20, 15, 12, 10, 8],
        'HC_II': [30, 25, 20, 15, 12],
        'CLINIC': [15, 12, 10, 8, 5]
    })
    
    population_df = pd.DataFrame({
        'ADM2_EN': ['KAMPALA', 'WAKISO', 'MUKONO', 'JINJA', 'GULU'],
        'T_TL': [1650000, 2000000, 600000, 500000, 400000]
    })
    
    optimizer = SupplyChainOptimizer(facilities_df, population_df)
    
    # Test demand
    demand = {
        'KAMPALA': 10000,
        'WAKISO': 15000,
        'MUKONO': 5000,
        'JINJA': 4000,
        'GULU': 3000
    }
    
    # Optimize distribution
    plan = optimizer.optimize_distribution(
        demand=demand,
        budget=50000,
        priority_districts=['KAMPALA', 'GULU']
    )
    
    print(f"Distribution Coverage: {plan['coverage']:.1f}%")
    print(f"Total Cost: ${plan['total_cost']:,.2f}")
    print(f"Routes Planned: {len(plan['routes'])}")
    
    # Analyze bottlenecks
    bottlenecks = optimizer.analyze_bottlenecks()
    print(f"\nBottlenecks Found:")
    print(f"  Capacity Issues: {len(bottlenecks['capacity_constraints'])}")
    print(f"  Connectivity Issues: {len(bottlenecks['connectivity_issues'])}")
    
    # Get recommendations
    recommendations = optimizer.recommend_improvements(100000)
    print(f"\nRecommendations ({len(recommendations)}):")
    for rec in recommendations[:3]:
        print(f"  - {rec['action']}: ${rec['cost']:,.0f}")