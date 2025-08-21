"""
Integration script to apply UI enhancements to the Uganda Nutrition Dashboard
"""

import streamlit as st
from streamlit_ui_enhancements import (
    apply_custom_theme,
    create_enhanced_metric_card,
    create_intervention_mix_display,
    create_status_badge,
    create_enhanced_plotly_theme,
    display_budget_constraint_warning
)

def integrate_ui_enhancements():
    """
    Add this function call at the beginning of your uganda_nutrition_enhanced.py file
    after the st.set_page_config() call
    """
    
    # Apply the custom theme
    apply_custom_theme()
    
    # Example usage in your main dashboard:
    
    # Instead of st.metric(), use:
    # create_enhanced_metric_card(
    #     title="PEOPLE TO REACH",
    #     value="36,968,606",
    #     subtitle="Total beneficiaries",
    #     icon="👥",
    #     color_theme="blue"
    # )
    
    # For intervention mix display:
    # interventions_data = [
    #     {"name": "Food Fortification Program", "percentage": 35, "cost_per_person": "UGX 53K/person"},
    #     {"name": "Direct Supplementation", "percentage": 30, "cost_per_person": "UGX 2K/person"},
    #     {"name": "Nutrition Education", "percentage": 20, "cost_per_person": "UGX 28K/person"},
    #     {"name": "Biofortified Crops", "percentage": 15, "cost_per_person": "UGX 71K/person"}
    # ]
    # create_intervention_mix_display(interventions_data)
    
    # For status badges in your UI:
    # st.markdown(create_status_badge("success", "Valid intervention mix!"), unsafe_allow_html=True)
    
    # For budget warnings:
    # display_budget_constraint_warning(
    #     target_coverage=80,
    #     achievable_coverage=10.8,
    #     budget_limit=5000000
    # )

# HOW TO INTEGRATE INTO YOUR EXISTING APP:
# ==========================================
# 
# 1. In uganda_nutrition_enhanced.py, add at the top after imports:
#    from integrate_ui_enhancements import integrate_ui_enhancements
#    from streamlit_ui_enhancements import *
#
# 2. After st.set_page_config(), add:
#    integrate_ui_enhancements()
#
# 3. Replace existing st.metric() calls with create_enhanced_metric_card()
#
# 4. For Plotly charts, apply the theme:
#    theme = create_enhanced_plotly_theme()
#    fig.update_layout(theme['layout'])
#
# 5. Use the provided UI components throughout your app for consistency

# EXAMPLE MODIFICATION FOR uganda_nutrition_enhanced.py:
def example_enhanced_kpi_display(col1, col2, col3, col4):
    """Example of how to replace the existing KPI display"""
    
    with col1:
        create_enhanced_metric_card(
            title="PEOPLE TO REACH",
            value="36,968,606",
            subtitle="Total beneficiaries",
            delta=5.2,  # Year-over-year change
            icon="👥",
            color_theme="blue"
        )
    
    with col2:
        create_enhanced_metric_card(
            title="LIVES SAVED",
            value="3,867",
            subtitle="CI: 2,730 - 5,003",
            icon="❤️",
            color_theme="green"
        )
    
    with col3:
        create_enhanced_metric_card(
            title="STUNTING PREVENTED",
            value="34,776",
            subtitle="CI: 24,552 - 44,999",
            icon="📈",
            color_theme="gold"
        )
    
    with col4:
        create_enhanced_metric_card(
            title="ECONOMIC BENEFIT",
            value="UGX 3565.6T",
            subtitle="NPV: UGX 17161.6T",
            delta=12.3,
            icon="💰",
            color_theme="green"
        )