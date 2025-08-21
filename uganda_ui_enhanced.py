"""
Enhanced UI Components and Styling for Uganda Nutrition Dashboard
==================================================================
Professional UI with Uganda National Colors and Improved UX
"""

import streamlit as st

def apply_enhanced_styling():
    """Apply comprehensive UI enhancements with Uganda national colors"""
    
    st.markdown("""
    <style>
        /* ============================================
           UGANDA NATIONAL COLORS PALETTE
           ============================================ */
        :root {
            --uganda-red: #D90000;
            --uganda-yellow: #FCDC04;
            --uganda-black: #000000;
            --deep-blue: #1A365D;
            --forest-green: #22543D;
            --warm-orange: #ED8936;
            --success: #48BB78;
            --warning: #F6AD55;
            --danger: #FC8181;
            --info: #63B3ED;
            --gray-900: #1A202C;
            --gray-700: #4A5568;
            --gray-500: #718096;
            --gray-300: #CBD5E0;
            --gray-100: #F7FAFC;
            --gray-50: #F9FAFB;
        }
        
        /* ============================================
           MAIN HEADER WITH PROPER SPACING
           ============================================ */
        .main-header {
            background: linear-gradient(135deg, var(--uganda-red) 0%, var(--uganda-yellow) 35%, var(--deep-blue) 100%);
            padding: 3.5rem 2.5rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 5rem;
            box-shadow: 0 20px 50px rgba(0,0,0,0.25);
            position: relative;
            overflow: hidden;
            animation: headerGlow 3s ease-in-out infinite alternate;
        }
        
        @keyframes headerGlow {
            0% { box-shadow: 0 20px 50px rgba(217, 0, 0, 0.25); }
            100% { box-shadow: 0 20px 60px rgba(252, 220, 4, 0.35); }
        }
        
        /* Pattern overlay for texture */
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 15px,
                    rgba(255,255,255,0.03) 15px,
                    rgba(255,255,255,0.03) 30px
                ),
                repeating-linear-gradient(
                    -45deg,
                    transparent,
                    transparent 15px,
                    rgba(0,0,0,0.03) 15px,
                    rgba(0,0,0,0.03) 30px
                );
            pointer-events: none;
        }
        
        /* Visual separator after main header */
        .main-header::after {
            content: '';
            position: absolute;
            bottom: -3rem;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 6px;
            background: linear-gradient(90deg, 
                transparent, 
                var(--uganda-red) 20%, 
                var(--uganda-yellow) 50%, 
                var(--uganda-black) 80%, 
                transparent
            );
            border-radius: 3px;
        }
        
        .main-header h1 {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 0.75rem;
            text-shadow: 4px 4px 8px rgba(0,0,0,0.4);
            letter-spacing: -1px;
            position: relative;
            z-index: 1;
            line-height: 1.1;
        }
        
        .main-header p {
            font-size: 1.4rem;
            opacity: 0.95;
            margin-top: 0.5rem;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* ============================================
           DASHBOARD SUBTITLE SEPARATION FIX
           ============================================ */
        .dashboard-subtitle {
            margin-top: 4.5rem !important;
            padding-top: 3rem;
            border-top: 3px solid rgba(252, 220, 4, 0.4);
            position: relative;
        }
        
        .dashboard-subtitle::before {
            content: '◆';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 24px;
            color: var(--uganda-yellow);
            background: white;
            padding: 0 20px;
        }
        
        /* Investment Dashboard specific header */
        .investment-header {
            background: linear-gradient(135deg, var(--deep-blue) 0%, var(--forest-green) 50%, var(--warm-orange) 100%);
            padding: 2.5rem;
            border-radius: 12px;
            color: white;
            margin-top: 4rem;
            margin-bottom: 3rem;
            box-shadow: 0 15px 40px rgba(26, 54, 93, 0.3);
        }
        
        /* ============================================
           ENHANCED METRIC CARDS WITH CONTEXT
           ============================================ */
        .metric-card {
            background: linear-gradient(145deg, white 0%, var(--gray-50) 100%);
            padding: 2rem;
            border-radius: 14px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(0,0,0,0.06);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, var(--uganda-red), var(--uganda-yellow));
            transform: scaleX(0);
            transition: transform 0.4s ease;
            transform-origin: left;
        }
        
        .metric-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 40px rgba(217, 0, 0, 0.15);
            border-color: var(--uganda-yellow);
        }
        
        .metric-card:hover::before {
            transform: scaleX(1);
        }
        
        /* Metric components */
        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: var(--gray-700);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .metric-value {
            font-size: 2.8rem;
            font-weight: 800;
            color: var(--deep-blue);
            margin: 0.75rem 0;
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
            line-height: 1;
        }
        
        .metric-trend {
            font-size: 0.9rem;
            padding: 0.35rem 0.9rem;
            border-radius: 24px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }
        
        .metric-trend.positive {
            background: linear-gradient(135deg, rgba(72, 187, 120, 0.15) 0%, rgba(72, 187, 120, 0.1) 100%);
            color: var(--success);
            border: 1px solid rgba(72, 187, 120, 0.3);
        }
        
        .metric-trend.negative {
            background: linear-gradient(135deg, rgba(252, 129, 129, 0.15) 0%, rgba(252, 129, 129, 0.1) 100%);
            color: var(--danger);
            border: 1px solid rgba(252, 129, 129, 0.3);
        }
        
        .metric-context {
            margin-top: 1.25rem;
            padding-top: 1.25rem;
            border-top: 2px solid rgba(0,0,0,0.06);
            font-size: 0.85rem;
            color: var(--gray-700);
            line-height: 1.6;
        }
        
        .metric-context-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }
        
        .metric-context-label {
            color: var(--gray-500);
        }
        
        .metric-context-value {
            font-weight: 600;
            color: var(--gray-900);
        }
        
        /* ============================================
           ENHANCED DASHBOARD SECTIONS
           ============================================ */
        .dashboard-section {
            background: white;
            padding: 3rem;
            border-radius: 16px;
            margin-bottom: 3.5rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.05);
            position: relative;
        }
        
        .dashboard-section::before {
            content: '';
            position: absolute;
            top: -2px;
            left: 30px;
            right: 30px;
            height: 4px;
            background: linear-gradient(90deg, 
                var(--uganda-red) 0%, 
                var(--uganda-yellow) 33%, 
                var(--deep-blue) 66%, 
                var(--forest-green) 100%
            );
            border-radius: 2px;
        }
        
        .section-header {
            font-size: 2rem;
            font-weight: 800;
            color: var(--deep-blue);
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid var(--uganda-yellow);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .section-subtitle {
            font-size: 1.1rem;
            color: var(--gray-700);
            font-weight: 400;
            margin-top: 0.5rem;
            line-height: 1.6;
        }
        
        /* ============================================
           ENHANCED ACTION BUTTONS
           ============================================ */
        .stButton > button {
            background: linear-gradient(135deg, var(--uganda-red) 0%, var(--warm-orange) 100%);
            color: white;
            border: 2px solid transparent;
            padding: 1rem 2.5rem;
            font-weight: 700;
            border-radius: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.95rem;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 35px rgba(217, 0, 0, 0.35);
            background: linear-gradient(135deg, var(--warm-orange) 0%, var(--uganda-red) 100%);
            border-color: var(--uganda-yellow);
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* ============================================
           ENHANCED TABLES
           ============================================ */
        .dataframe {
            border: none !important;
            font-size: 0.95rem;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .dataframe thead tr th {
            background: linear-gradient(135deg, var(--deep-blue) 0%, var(--uganda-red) 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.75px;
            padding: 1.2rem !important;
            font-size: 0.85rem;
            border: none !important;
        }
        
        .dataframe tbody tr {
            transition: all 0.2s ease;
        }
        
        .dataframe tbody tr:nth-of-type(even) {
            background-color: rgba(252, 220, 4, 0.03) !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: rgba(252, 220, 4, 0.15) !important;
            transform: scale(1.01);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .dataframe tbody tr td {
            padding: 1rem !important;
            border-bottom: 1px solid rgba(0,0,0,0.06) !important;
            color: var(--gray-900);
        }
        
        /* ============================================
           TOOLTIPS AND INFO ICONS
           ============================================ */
        .info-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 20px;
            background: var(--info);
            color: white;
            border-radius: 50%;
            font-size: 0.75rem;
            font-weight: bold;
            cursor: help;
            transition: all 0.3s ease;
        }
        
        .info-icon:hover {
            transform: scale(1.2);
            background: var(--deep-blue);
        }
        
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 280px;
            background-color: var(--gray-900);
            color: white;
            text-align: left;
            border-radius: 10px;
            padding: 1rem;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -140px;
            opacity: 0;
            transition: opacity 0.3s, transform 0.3s;
            font-size: 0.85rem;
            line-height: 1.5;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            transform: translateY(10px);
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
            transform: translateY(0);
        }
        
        .tooltiptext::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -8px;
            border-width: 8px;
            border-style: solid;
            border-color: var(--gray-900) transparent transparent transparent;
        }
        
        /* ============================================
           RESPONSIVE GRID SYSTEM
           ============================================ */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 2.5rem 0;
        }
        
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(550px, 1fr));
            gap: 2.5rem;
            margin: 2.5rem 0;
        }
        
        /* ============================================
           ENHANCED TABS
           ============================================ */
        .stTabs {
            margin-top: 3.5rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.75rem;
            background: linear-gradient(90deg, rgba(217, 0, 0, 0.05), rgba(252, 220, 4, 0.05));
            padding: 0.75rem;
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.08);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: white;
            border-radius: 10px;
            color: var(--deep-blue);
            font-weight: 600;
            transition: all 0.3s ease;
            padding: 0.75rem 1.5rem;
            border: 2px solid transparent;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: var(--uganda-yellow);
            color: var(--gray-900);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(252, 220, 4, 0.3);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--uganda-red), var(--warm-orange));
            color: white;
            border-color: var(--uganda-yellow);
            box-shadow: 0 6px 20px rgba(217, 0, 0, 0.3);
        }
        
        /* ============================================
           PROGRESS BARS
           ============================================ */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, 
                var(--uganda-red) 0%, 
                var(--uganda-yellow) 50%, 
                var(--success) 100%
            );
            box-shadow: 0 3px 15px rgba(217, 0, 0, 0.3);
            border-radius: 12px;
            height: 12px;
        }
        
        /* ============================================
           ENHANCED SIDEBAR - MUTED PROFESSIONAL COLORS
           ============================================ */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2C3E50 0%, #34495E 50%, #2C3E50 100%);
            border-right: 2px solid rgba(252, 220, 4, 0.3);
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        }
        
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stNumberInput label {
            color: #ECF0F1;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.75rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }
        
        /* Sidebar header styling */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: var(--uganda-yellow) !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
            border-bottom: 1px solid rgba(252, 220, 4, 0.2);
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Sidebar expander styling */
        section[data-testid="stSidebar"] .streamlit-expanderHeader {
            background: rgba(52, 73, 94, 0.7) !important;
            color: #ECF0F1 !important;
            border: 1px solid rgba(252, 220, 4, 0.2);
            border-radius: 8px;
            font-weight: 600;
        }
        
        section[data-testid="stSidebar"] .streamlit-expanderHeader:hover {
            background: rgba(52, 73, 94, 0.9) !important;
            border-color: var(--uganda-yellow);
        }
        
        /* Sidebar input fields */
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] select {
            background: rgba(236, 240, 241, 0.95) !important;
            color: var(--gray-900) !important;
            border: 1px solid rgba(252, 220, 4, 0.3) !important;
            border-radius: 6px;
        }
        
        section[data-testid="stSidebar"] input:focus,
        section[data-testid="stSidebar"] select:focus {
            border-color: var(--uganda-yellow) !important;
            box-shadow: 0 0 0 2px rgba(252, 220, 4, 0.2) !important;
        }
        
        /* Sidebar slider styling */
        section[data-testid="stSidebar"] .stSlider > div > div {
            background: rgba(236, 240, 241, 0.2) !important;
        }
        
        section[data-testid="stSidebar"] .stSlider > div > div > div {
            background: var(--uganda-yellow) !important;
        }
        
        /* Sidebar text and paragraphs */
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] .stMarkdown {
            color: #BDC3C7 !important;
        }
        
        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, rgba(217, 0, 0, 0.8) 0%, rgba(252, 220, 4, 0.8) 100%);
            color: white;
            border: 1px solid rgba(252, 220, 4, 0.4);
            font-weight: 600;
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, rgba(252, 220, 4, 0.9) 0%, rgba(217, 0, 0, 0.9) 100%);
            border-color: var(--uganda-yellow);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(252, 220, 4, 0.3);
        }
        
        /* ============================================
           LOADING STATES
           ============================================ */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        .skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
        }
        
        /* ============================================
           MOBILE RESPONSIVE
           ============================================ */
        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2.2rem;
            }
            
            .main-header {
                padding: 2.5rem 1.5rem;
                margin-bottom: 3rem;
            }
            
            .metric-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .chart-grid {
                grid-template-columns: 1fr;
            }
            
            .dashboard-section {
                padding: 2rem 1.5rem;
            }
            
            .metric-value {
                font-size: 2.2rem;
            }
            
            .section-header {
                font-size: 1.6rem;
            }
            
            .stButton > button {
                padding: 0.8rem 1.5rem;
                font-size: 0.9rem;
            }
        }
        
        /* ============================================
           ULTRA-WIDE SCREENS
           ============================================ */
        @media (min-width: 1920px) {
            .main > div {
                max-width: 1800px;
                margin: 0 auto;
            }
            
            .metric-grid {
                grid-template-columns: repeat(5, 1fr);
            }
            
            .chart-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        /* ============================================
           PRINT STYLES
           ============================================ */
        @media print {
            .main-header {
                background: white !important;
                color: black !important;
                border: 2px solid black;
            }
            
            .stButton,
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_enhanced_metric_card(title, value, trend=None, context=None, icon=None):
    """
    Create an enhanced metric card with contextual information
    
    Args:
        title: Metric title
        value: Main metric value
        trend: Dict with 'value', 'direction' ('up'/'down'), 'period'
        context: Dict with additional context like 'benchmark', 'impact', 'source'
        icon: Optional icon emoji or symbol
    """
    
    trend_html = ""
    if trend:
        trend_class = "positive" if trend.get('direction') == 'up' else "negative"
        trend_icon = "↑" if trend.get('direction') == 'up' else "↓"
        trend_html = f"""
        <div class="metric-trend {trend_class}">
            {trend_icon} {trend['value']} from {trend.get('period', 'last period')}
        </div>
        """
    
    context_html = ""
    if context:
        context_items = ""
        if 'benchmark' in context:
            context_items += f"""
            <div class="metric-context-item">
                <span class="metric-context-label">vs National Avg:</span>
                <span class="metric-context-value">{context['benchmark']}</span>
            </div>
            """
        if 'impact' in context:
            context_items += f"""
            <div class="metric-context-item">
                <span class="metric-context-label">Impact:</span>
                <span class="metric-context-value">{context['impact']}</span>
            </div>
            """
        if 'source' in context:
            context_items += f"""
            <div class="metric-context-item">
                <span class="metric-context-label">Source:</span>
                <span class="metric-context-value">{context['source']}</span>
            </div>
            """
        
        if context_items:
            context_html = f"""
            <div class="metric-context">
                {context_items}
            </div>
            """
    
    icon_html = f"<span style='margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    
    card_html = f"""
    <div class="metric-card">
        <div class="metric-header">
            <div class="metric-label">
                {icon_html}{title}
                <span class="info-icon" title="Click for more details">i</span>
            </div>
        </div>
        <div class="metric-value">
            {value}
        </div>
        {trend_html}
        {context_html}
    </div>
    """
    
    return card_html

def create_section_header(title, subtitle=None):
    """Create a styled section header"""
    subtitle_html = f"<div class='section-subtitle'>{subtitle}</div>" if subtitle else ""
    
    return f"""
    <div class="dashboard-section">
        <div class="section-header">
            {title}
        </div>
        {subtitle_html}
    </div>
    """

def fix_title_spacing():
    """Specific fix for the title spacing issue"""
    st.markdown("""
    <style>
        /* Fix for title spacing between Command Center and Investment Dashboard */
        div[data-testid="stMarkdownContainer"] h1:contains("Investment Dashboard") {
            margin-top: 5rem !important;
            padding-top: 3rem !important;
        }
        
        /* Add breathing room between major sections */
        .element-container + .element-container {
            margin-top: 1.5rem;
        }
        
        /* Specific spacing for headers containing Uganda emojis */
        h1:has(.emoji), h2:has(.emoji) {
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)