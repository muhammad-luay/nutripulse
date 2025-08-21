"""
Enhanced Distribution Network Cards for Uganda Nutrition Dashboard
===================================================================
Distribution and supply chain metric cards with three-tier information hierarchy
Following the same UI implementation pattern as executive dashboard cards
"""

import streamlit as st
from typing import Dict, Optional

def create_distribution_network_cards(network_data: Dict) -> None:
    """Create the distribution network metric cards in a grid layout with three-tier information
    
    Args:
        network_data: Dictionary containing all distribution metrics including:
            - Main metrics: total_facilities, active_points, lead_time, turnover_rate, fill_rate
            - Context data for each metric (operational details, performance indicators, etc.)
    """
    
    # Create responsive grid layout - 3 columns for first row, 2 for second
    st.markdown("### 🚚 Distribution Network Performance")
    
    # First row - 3 primary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Total Facilities Card
        st.markdown(f"""
        <div class="metric-card" style="min-height: 200px;">
            <div class="card-icon">🏥</div>
            <div class="card-label">Total Facilities</div>
            <div class="card-value" style="font-size: 2.2rem; color: #D90000;">{network_data.get('total_facilities', '156')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem; color: #92400E;">Distribution network</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Health Centers:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('health_centers', '89')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Hospitals:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('hospitals', '42')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Warehouses:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('warehouses', '12')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Mobile Units:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('mobile_units', '13')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Active Distribution Points Card
        active_points = network_data.get('active_points', '72')
        total_points = network_data.get('total_points', '94')
        utilization = float(active_points) / float(total_points) * 100 if total_points else 0
        
        st.markdown(f"""
        <div class="metric-card" style="min-height: 200px;">
            <div class="card-icon">📍</div>
            <div class="card-label">Active Distribution Points</div>
            <div class="card-value" style="font-size: 2.2rem; color: #D90000;">{active_points}</div>
            <div class="card-subtitle" style="font-size: 0.85rem; color: #92400E;">Currently operational</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Total Points:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{total_points}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Utilization:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: {'#16A34A' if utilization > 75 else '#F59E0B' if utilization > 50 else '#DC2626'};">{utilization:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Urban:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('urban_points', '28')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Rural:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('rural_points', '44')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Average Lead Time Card
        lead_time = network_data.get('lead_time', '3.1 days')
        lead_time_value = float(lead_time.split()[0]) if isinstance(lead_time, str) else lead_time
        performance = "Excellent" if lead_time_value <= 2 else "Good" if lead_time_value <= 3.5 else "Fair" if lead_time_value <= 5 else "Poor"
        perf_color = "#16A34A" if performance == "Excellent" else "#22C55E" if performance == "Good" else "#F59E0B" if performance == "Fair" else "#DC2626"
        
        st.markdown(f"""
        <div class="metric-card" style="min-height: 200px;">
            <div class="card-icon">⏱️</div>
            <div class="card-label">Average Lead Time</div>
            <div class="card-value" style="font-size: 2.2rem; color: #D90000;">{lead_time}</div>
            <div class="card-subtitle" style="font-size: 0.85rem; color: #92400E;">Order to delivery</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Performance:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: {perf_color};">{performance}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Target:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('target_lead_time', '≤3 days')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Min Time:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('min_lead_time', '1.2 days')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Max Time:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('max_lead_time', '7.8 days')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row - 2 operational metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock Turnover Rate Card
        turnover = network_data.get('turnover_rate', '3.2x/month')
        turnover_value = float(turnover.split('x')[0]) if isinstance(turnover, str) and 'x' in turnover else 3.2
        efficiency = "High" if turnover_value >= 3 else "Medium" if turnover_value >= 2 else "Low"
        eff_color = "#16A34A" if efficiency == "High" else "#F59E0B" if efficiency == "Medium" else "#DC2626"
        
        st.markdown(f"""
        <div class="metric-card" style="min-height: 200px;">
            <div class="card-icon">🔄</div>
            <div class="card-label">Stock Turnover Rate</div>
            <div class="card-value" style="font-size: 2.2rem; color: #D90000;">{turnover}</div>
            <div class="card-subtitle" style="font-size: 0.85rem; color: #92400E;">Inventory efficiency</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Efficiency:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: {eff_color};">{efficiency}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Days on Hand:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('days_on_hand', '9.4 days')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Reorder Point:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('reorder_point', '14 days')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Waste Rate:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: {'#16A34A' if network_data.get('waste_rate', '2.1%') < '3%' else '#F59E0B'};">{network_data.get('waste_rate', '2.1%')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Fill Rate Card
        fill_rate = network_data.get('fill_rate', '90.7%')
        fill_value = float(fill_rate.rstrip('%')) if isinstance(fill_rate, str) else fill_rate
        service_level = "Excellent" if fill_value >= 95 else "Good" if fill_value >= 90 else "Fair" if fill_value >= 85 else "Poor"
        service_color = "#16A34A" if service_level == "Excellent" else "#22C55E" if service_level == "Good" else "#F59E0B" if service_level == "Fair" else "#DC2626"
        
        st.markdown(f"""
        <div class="metric-card" style="min-height: 200px;">
            <div class="card-icon">📦</div>
            <div class="card-label">Fill Rate</div>
            <div class="card-value" style="font-size: 2.2rem; color: #D90000;">{fill_rate}</div>
            <div class="card-subtitle" style="font-size: 0.85rem; color: #92400E;">Order fulfillment</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Service Level:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: {service_color};">{service_level}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Target:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('target_fill_rate', '95%')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Backorders:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: {'#DC2626' if int(network_data.get('backorders', '12')) > 20 else '#F59E0B' if int(network_data.get('backorders', '12')) > 10 else '#16A34A'};">{network_data.get('backorders', '12')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">On-Time:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{network_data.get('on_time_delivery', '88.3%')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_distribution_summary_card(summary_data: Dict) -> None:
    """Create a comprehensive distribution network summary card"""
    
    st.markdown("### 📊 Distribution Network Summary")
    
    # Create columns for the metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("NETWORK COVERAGE", summary_data.get('coverage_districts', '130/146'), help="Districts covered")
        st.metric("MONTHLY VOLUME", summary_data.get('monthly_volume', '2,847 MT'), help="Metric tons distributed")
    
    with col2:
        st.metric("EFFICIENCY SCORE", summary_data.get('efficiency_score', '87/100'), help="Overall performance")  
        st.metric("COST EFFICIENCY", summary_data.get('cost_per_mt', 'UGX 1.2M'), help="Per metric ton")
    
    # Key Challenges section
    st.markdown("#### KEY CHALLENGES")
    challenge_col1, challenge_col2 = st.columns(2)
    
    with challenge_col1:
        st.warning(f"⚠️ {summary_data.get('challenge_1', 'Remote area access (18 districts)')}")
        st.error(f"🔴 {summary_data.get('challenge_3', 'Stock-outs in 3 regions')}")
    
    with challenge_col2:
        st.warning(f"⚠️ {summary_data.get('challenge_2', 'Cold chain gaps (12 facilities)')}")
        st.success(f"✅ {summary_data.get('improvement', 'Fleet expanded by 15%')}")
    

def render_distribution_dashboard():
    """Render the complete distribution network dashboard with enhanced cards"""
    
    # Main metrics with full context
    network_data = {
        # Total Facilities
        'total_facilities': '156',
        'health_centers': '89',
        'hospitals': '42',
        'warehouses': '12',
        'mobile_units': '13',
        
        # Active Distribution Points
        'active_points': '72',
        'total_points': '94',
        'urban_points': '28',
        'rural_points': '44',
        
        # Lead Time
        'lead_time': '3.1 days',
        'target_lead_time': '≤3 days',
        'min_lead_time': '1.2 days',
        'max_lead_time': '7.8 days',
        
        # Turnover Rate
        'turnover_rate': '3.2x/month',
        'days_on_hand': '9.4 days',
        'reorder_point': '14 days',
        'waste_rate': '2.1%',
        
        # Fill Rate
        'fill_rate': '90.7%',
        'target_fill_rate': '95%',
        'backorders': '12',
        'on_time_delivery': '88.3%'
    }
    
    # Create the enhanced distribution cards
    create_distribution_network_cards(network_data)
    
    # Add summary card
    st.markdown("---")
    summary_data = {
        'coverage_districts': '130/146',
        'efficiency_score': '87/100',
        'monthly_volume': '2,847 MT',
        'cost_per_mt': 'UGX 1.2M',
        'challenge_1': 'Remote area access (18 districts)',
        'challenge_2': 'Cold chain gaps (12 facilities)',
        'challenge_3': 'Stock-outs in 3 regions',
        'improvement': 'Fleet expanded by 15%'
    }
    create_distribution_summary_card(summary_data)

if __name__ == "__main__":
    # Test the distribution network cards
    st.set_page_config(layout="wide", page_title="Distribution Network Dashboard")
    
    # Apply the card styling from the main components
    from uganda_card_components import apply_card_styling
    apply_card_styling()
    
    st.title("🚚 Uganda Nutrition - Distribution Network Dashboard")
    st.markdown("---")
    
    render_distribution_dashboard()