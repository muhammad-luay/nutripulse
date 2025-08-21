"""
Streamlit UI Enhancement Module for Uganda Nutrition Dashboard
Provides custom styling and component improvements
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def apply_custom_theme():
    """Apply custom CSS theme to Streamlit app"""
    
    st.markdown("""
    <style>
        /* Import custom CSS */
        @import url('ui_improvements.css');
        
        /* Override Streamlit defaults */
        .stApp {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        }
        
        /* Dark theme for tabs - subtle and elegant */
        .stTabs [data-baseweb="tab-list"] {
            background-color: rgba(15, 23, 42, 0.6);
            border-bottom: 1px solid rgba(51, 65, 85, 0.5);
            gap: 2px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(30, 41, 59, 0.7);
            color: #CBD5E1;
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            border: 1px solid rgba(51, 65, 85, 0.5);
            border-bottom: none;
            font-weight: 500;
            transition: all 0.2s ease;
            font-size: 14px;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(51, 65, 85, 0.8);
            color: #E2E8F0;
            border-color: rgba(59, 130, 246, 0.4);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%) !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(59, 130, 246, 0.5) !important;
            border-bottom: 2px solid #3B82F6 !important;
            font-weight: 600;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #3B82F6;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            background-color: transparent;
            padding-top: 20px;
        }
        
        /* Metric containers */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        /* Metric labels */
        [data-testid="metric-container"] > div:first-child {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #CBD5E1;
        }
        
        /* Metric values */
        [data-testid="metric-container"] > div:nth-child(2) {
            font-size: 32px;
            font-weight: 700;
            color: #F8FAFC;
        }
        
        /* Metric deltas */
        [data-testid="metric-container"] > div:nth-child(3) {
            font-size: 14px;
            font-weight: 500;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: #1E293B;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
        }
        
        /* Progress bars */
        .stProgress > div > div {
            background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%);
        }
        
        /* Main content area dark theme */
        .main .block-container {
            background-color: rgba(15, 23, 42, 0.5);
            padding: 2rem;
            border-radius: 12px;
        }
        
        /* Section backgrounds */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.95);
        }
        
        section[data-testid="stSidebar"] > div {
            background-color: transparent;
        }
        
        /* Text color adjustments */
        p, span, div {
            color: #CBD5E1;
        }
        
        h1, h2, h3 {
            color: #F8FAFC;
        }
        
        /* Make tab icons and text brighter */
        .stTabs [data-baseweb="tab"] span {
            filter: brightness(1.2);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 8px;
            color: #F8FAFC;
        }
        
        /* Success/Warning/Error messages */
        .stAlert {
            border-radius: 12px;
            border-width: 1px;
        }
        
        /* Slider styling */
        .stSlider > div > div {
            background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%);
        }
        
        /* Select boxes */
        .stSelectbox > div > div {
            background: #1E293B;
            border: 1px solid rgba(148, 163, 184, 0.2);
            color: #F8FAFC;
        }
    </style>
    """, unsafe_allow_html=True)

def create_enhanced_metric_card(title, value, subtitle=None, delta=None, icon=None, color_theme="blue"):
    """Create an enhanced metric card with better styling"""
    
    color_themes = {
        "blue": {"bg": "#1E3A8A", "text": "#DBEAFE", "icon": "📊"},
        "green": {"bg": "#059669", "text": "#D1FAE5", "icon": "✅"},
        "red": {"bg": "#DC2626", "text": "#FEE2E2", "icon": "⚠️"},
        "gold": {"bg": "#F59E0B", "text": "#FEF3C7", "icon": "💰"}
    }
    
    theme = color_themes.get(color_theme, color_themes["blue"])
    if icon is None:
        icon = theme["icon"]
    
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, {theme['bg']}40 0%, {theme['bg']}20 100%);
        border: 1px solid {theme['bg']}40;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    ">
        <div style="display: flex; align-items: start; gap: 16px;">
            <div style="font-size: 32px;">{icon}</div>
            <div style="flex: 1;">
                <div style="
                    font-size: 14px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    color: #CBD5E1;
                    margin-bottom: 8px;
                ">{title}</div>
                <div style="
                    font-size: 32px;
                    font-weight: 700;
                    color: #F8FAFC;
                    margin-bottom: 4px;
                ">{value}</div>
                {f'<div style="font-size: 14px; color: #94A3B8;">{subtitle}</div>' if subtitle else ''}
                {f'<div style="font-size: 14px; color: {"#10B981" if delta and delta > 0 else "#EF4444"}; font-weight: 600; margin-top: 8px;">{"↑" if delta and delta > 0 else "↓"} {abs(delta) if delta else ""}%</div>' if delta is not None else ''}
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_intervention_mix_display(interventions_data):
    """Create a visually appealing intervention mix display"""
    
    html_content = """
    <div style="
        background: rgba(30, 41, 59, 0.6);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    ">
        <h3 style="color: #F8FAFC; margin-bottom: 20px;">Current Intervention Mix</h3>
    """
    
    for intervention in interventions_data:
        progress_width = intervention['percentage']
        html_content += f"""
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #F8FAFC; font-weight: 600;">{intervention['name']}</span>
                <span style="color: #3B82F6; font-weight: 700; font-size: 20px;">{intervention['percentage']}%</span>
            </div>
            <div style="
                height: 8px;
                background: rgba(148, 163, 184, 0.2);
                border-radius: 4px;
                overflow: hidden;
            ">
                <div style="
                    height: 100%;
                    width: {progress_width}%;
                    background: linear-gradient(90deg, #3B82F6 0%, #10B981 100%);
                    border-radius: 4px;
                    transition: width 0.5s ease;
                "></div>
            </div>
            <div style="color: #94A3B8; font-size: 12px; margin-top: 4px;">
                {intervention['cost_per_person']}
            </div>
        </div>
        """
    
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)

def create_status_badge(status, text):
    """Create a status badge with appropriate styling"""
    
    status_styles = {
        "success": {"bg": "rgba(16, 185, 129, 0.2)", "color": "#10B981", "icon": "✅"},
        "warning": {"bg": "rgba(245, 158, 11, 0.2)", "color": "#F59E0B", "icon": "⚠️"},
        "danger": {"bg": "rgba(239, 68, 68, 0.2)", "color": "#EF4444", "icon": "❌"},
        "info": {"bg": "rgba(59, 130, 246, 0.2)", "color": "#3B82F6", "icon": "ℹ️"}
    }
    
    style = status_styles.get(status, status_styles["info"])
    
    badge_html = f"""
    <span style="
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        gap: 6px;
        background: {style['bg']};
        color: {style['color']};
        border: 1px solid {style['color']}40;
    ">
        <span>{style['icon']}</span>
        <span>{text}</span>
    </span>
    """
    
    return badge_html

def create_enhanced_plotly_theme():
    """Create enhanced Plotly theme for better visualizations"""
    
    return {
        'layout': {
            'paper_bgcolor': 'rgba(30, 41, 59, 0.9)',
            'plot_bgcolor': 'rgba(30, 41, 59, 0.3)',
            'font': {'color': '#CBD5E1', 'family': 'Inter, sans-serif'},
            'title': {'font': {'color': '#F8FAFC', 'size': 20}},
            'xaxis': {
                'gridcolor': 'rgba(148, 163, 184, 0.1)',
                'linecolor': 'rgba(148, 163, 184, 0.2)',
                'tickfont': {'color': '#94A3B8'}
            },
            'yaxis': {
                'gridcolor': 'rgba(148, 163, 184, 0.1)',
                'linecolor': 'rgba(148, 163, 184, 0.2)',
                'tickfont': {'color': '#94A3B8'}
            },
            'colorway': ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'],
            'hovermode': 'x unified',
            'hoverlabel': {
                'bgcolor': 'rgba(30, 41, 59, 0.95)',
                'bordercolor': 'rgba(148, 163, 184, 0.3)',
                'font': {'color': '#F8FAFC'}
            }
        }
    }

def display_budget_constraint_warning(target_coverage, achievable_coverage, budget_limit):
    """Display an enhanced budget constraint warning"""
    
    warning_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    ">
        <div style="
            color: #F59E0B;
            font-weight: 600;
            margin-bottom: 12px;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            ⚠️ Budget Constraint Active
        </div>
        <div style="color: #CBD5E1; line-height: 1.6;">
            <ul style="margin: 8px 0; padding-left: 20px;">
                <li>Target coverage: <strong>{target_coverage}%</strong></li>
                <li>Achievable coverage with current budget: <strong>{achievable_coverage}%</strong></li>
                <li>People reached: <strong>{budget_limit:,}</strong> (limited by budget)</li>
            </ul>
            <p style="margin-top: 12px; color: #94A3B8; font-size: 14px;">
                💡 To reach your target coverage, increase the budget or reduce intervention costs.
            </p>
        </div>
    </div>
    """
    
    st.markdown(warning_html, unsafe_allow_html=True)

def add_loading_animation():
    """Add a loading animation for data processing"""
    
    loading_html = """
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
    ">
        <div style="
            border: 3px solid rgba(59, 130, 246, 0.1);
            border-top: 3px solid #3B82F6;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        "></div>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """
    
    return st.markdown(loading_html, unsafe_allow_html=True)