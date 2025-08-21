"""
Enhanced Card Components for Uganda Nutrition Dashboard
========================================================
Professional card-based UI components for better information presentation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

def apply_card_styling():
    """Apply comprehensive card-based styling to the dashboard"""
    
    st.markdown("""
    <style>
        /* ============================================
           CARD FOUNDATION STYLES
           ============================================ */
        .card-container {
            display: grid;
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .card-grid-2 {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }
        
        .card-grid-3 {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        
        .card-grid-4 {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        .card-grid-6 {
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        }
        
        /* Base Card Style - Warm neutral with subtle Uganda colors */
        .metric-card {
            background: linear-gradient(145deg, #FEF9F3 0%, #FAF4ED 100%);
            border-radius: 16px;
            padding: 1.8rem;
            box-shadow: 0 4px 6px rgba(217, 0, 0, 0.08), 
                        0 1px 3px rgba(0, 0, 0, 0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(252, 220, 4, 0.2);
            position: relative;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px rgba(217, 0, 0, 0.12), 
                        0 4px 8px rgba(252, 220, 4, 0.15);
            border-color: rgba(252, 220, 4, 0.4);
            background: linear-gradient(145deg, #FFFBF7 0%, #FDF8F1 100%);
        }
        
        /* Card Header Accent */
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #D90000 0%, #FCDC04 50%, #1A365D 100%);
        }
        
        /* Card Icon */
        .card-icon {
            font-size: 2rem;
            margin-bottom: 0.75rem;
            display: inline-block;
        }
        
        /* Card Label */
        .card-label {
            font-size: 0.85rem;
            color: #7C2D12;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        /* Card Value */
        .card-value {
            font-size: 2rem;
            font-weight: 700;
            color: #D90000;
            line-height: 1.2;
            margin-bottom: 0.5rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.05);
        }
        
        .card-value.large {
            font-size: 2.5rem;
        }
        
        /* Card Subtitle */
        .card-subtitle {
            font-size: 0.9rem;
            color: #92400E;
            margin-top: 0.25rem;
            font-weight: 500;
        }
        
        /* Card Trend Indicator */
        .card-trend {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        .card-trend.positive {
            background: rgba(34, 197, 94, 0.1);
            color: #16A34A;
        }
        
        .card-trend.negative {
            background: rgba(239, 68, 68, 0.1);
            color: #DC2626;
        }
        
        .card-trend.neutral {
            background: rgba(107, 114, 128, 0.1);
            color: #6B7280;
        }
        
        /* Impact Card Specific - Same style as regular cards */
        .impact-card {
            background: linear-gradient(145deg, #FEF9F3 0%, #FAF4ED 100%);
            border: 1px solid rgba(252, 220, 4, 0.2);
        }
        
        .impact-card .card-value {
            color: #D90000;
        }
        
        /* Alert Card Styles */
        .alert-card {
            background: white;
            border-left: 4px solid;
            padding: 1rem 1.5rem;
            margin: 0.75rem 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .alert-card.critical {
            border-left-color: #DC2626;
            background: linear-gradient(90deg, rgba(220, 38, 38, 0.05) 0%, white 100%);
        }
        
        .alert-card.warning {
            border-left-color: #F59E0B;
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.05) 0%, white 100%);
        }
        
        .alert-card.success {
            border-left-color: #10B981;
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.05) 0%, white 100%);
        }
        
        .alert-icon {
            font-size: 1.5rem;
        }
        
        .alert-content {
            flex: 1;
        }
        
        .alert-title {
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 0.25rem;
        }
        
        .alert-message {
            font-size: 0.85rem;
            color: #6B7280;
        }
        
        /* Intervention Mix Card */
        .intervention-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #E5E7EB;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .intervention-card:hover {
            border-color: #FCDC04;
            box-shadow: 0 4px 12px rgba(252, 220, 4, 0.15);
        }
        
        .intervention-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .intervention-title {
            font-weight: 600;
            font-size: 1.1rem;
            color: #1F2937;
        }
        
        .intervention-percentage {
            font-size: 1.5rem;
            font-weight: 700;
            color: #D90000;
        }
        
        .intervention-cost {
            font-size: 0.9rem;
            color: #6B7280;
            margin-bottom: 0.5rem;
        }
        
        .intervention-bar {
            height: 8px;
            background: #E5E7EB;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .intervention-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #D90000 0%, #FCDC04 100%);
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        /* KPI Card with Progress Ring */
        .kpi-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }
        
        .kpi-ring {
            width: 120px;
            height: 120px;
            margin: 0 auto 1rem;
            position: relative;
        }
        
        .kpi-value-display {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.8rem;
            font-weight: 700;
        }
        
        .kpi-label {
            font-size: 0.95rem;
            color: #6B7280;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .kpi-trend {
            font-size: 0.85rem;
            color: #10B981;
            font-weight: 500;
        }
        
        /* Distribution Network Card */
        .network-card {
            background: linear-gradient(135deg, #EBF8FF 0%, #DBEAFE 100%);
            border: 1px solid #3B82F6;
            border-radius: 12px;
            padding: 1.5rem;
        }
        
        .network-stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2);
        }
        
        .network-stat:last-child {
            border-bottom: none;
        }
        
        .network-stat-label {
            font-size: 0.9rem;
            color: #1E40AF;
            font-weight: 500;
        }
        
        .network-stat-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E3A8A;
        }
        
        /* Financial Metrics Card */
        .financial-card {
            background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
            border: 2px solid #22C55E;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        }
        
        .financial-metric {
            margin-bottom: 1.5rem;
        }
        
        .financial-label {
            font-size: 0.85rem;
            color: #166534;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .financial-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: #15803D;
        }
        
        .financial-subtitle {
            font-size: 0.9rem;
            color: #16A34A;
            margin-top: 0.25rem;
        }
        
        /* Executive Dashboard Summary Card */
        .executive-card {
            background: linear-gradient(135deg, #1A365D 0%, #2563EB 100%);
            color: white;
            border-radius: 16px;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .executive-card::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .executive-metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .executive-metric:last-child {
            border-bottom: none;
        }
        
        .executive-label {
            font-size: 0.95rem;
            opacity: 0.9;
        }
        
        .executive-value {
            font-size: 1.3rem;
            font-weight: 700;
        }
        
        .executive-change {
            font-size: 0.85rem;
            opacity: 0.8;
            margin-left: 0.5rem;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .card-container {
                grid-template-columns: 1fr !important;
            }
            
            .card-value {
                font-size: 1.5rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_budget_coverage_cards(budget_data: Dict) -> None:
    """Create the budget and coverage metric cards in three columns with context
    
    Args:
        budget_data: Dictionary containing all card values including:
            - Main metrics: budget, duration, coverage, people, per_person, confidence
            - Context data: monthly_budget, health_budget_pct, funding_sources,
              children_under_5, pregnant_women, at_risk_adults, start_date, end_date,
              review_cycles, supplement_cost, fortification_cost, education_cost,
              current_coverage, coverage_gap, districts_covered, districts_total,
              data_sources, sample_size, margin_error
    """
    
    # Create three columns for better space utilization
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Budget Card with context
        st.markdown(f"""
        <div class="metric-card" style="min-height: 180px;">
            <div class="card-icon">💰</div>
            <div class="card-label">Total Budget</div>
            <div class="card-value" style="font-size: 1.8rem;">{budget_data.get('budget', 'UGX 178.0B')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem;">Annual allocation</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Monthly:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('monthly_budget', 'UGX 14.8B')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">vs Health Budget:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('health_budget_pct', '4.2%')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Sources:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('funding_sources', 'Gov+Donors')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # People Card with context
        st.markdown(f"""
        <div class="metric-card" style="min-height: 180px;">
            <div class="card-icon">👥</div>
            <div class="card-label">Target Population</div>
            <div class="card-value" style="font-size: 1.8rem;">{budget_data.get('people', '36.97M')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem;">Total beneficiaries</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Children <5:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('children_under_5', '7.2M')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Pregnant:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('pregnant_women', '1.8M')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">At-risk:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('at_risk_adults', '27.97M')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Duration Card with context
        st.markdown(f"""
        <div class="metric-card" style="min-height: 180px;">
            <div class="card-icon">📅</div>
            <div class="card-label">Duration</div>
            <div class="card-value" style="font-size: 1.8rem;">{budget_data.get('duration', '12 mo')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem;">Implementation period</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Start:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('start_date', 'Jan 2025')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">End:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('end_date', 'Dec 2025')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Reviews:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('review_cycles', 'Quarterly')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Per Person Card with context
        st.markdown(f"""
        <div class="metric-card" style="min-height: 180px;">
            <div class="card-icon">💵</div>
            <div class="card-label">Cost Per Person</div>
            <div class="card-value" style="font-size: 1.8rem;">{budget_data.get('per_person', 'UGX 5K')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem;">Average cost</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Supplement:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('supplement_cost', 'UGX 2K')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Fortification:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('fortification_cost', 'UGX 15K')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Education:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('education_cost', 'UGX 8K')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Coverage Card with context
        st.markdown(f"""
        <div class="metric-card" style="min-height: 180px;">
            <div class="card-icon">🎯</div>
            <div class="card-label">Coverage Target</div>
            <div class="card-value" style="font-size: 1.8rem;">{budget_data.get('coverage', '80%')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem;">Of vulnerable pop</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Current:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('current_coverage', '53.6%')}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Gap:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #F59E0B;">{budget_data.get('coverage_gap', '26.4%')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Districts:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('districts_covered', 130)}/{budget_data.get('districts_total', 146)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence Card with context
        st.markdown(f"""
        <div class="metric-card" style="min-height: 180px;">
            <div class="card-icon">📊</div>
            <div class="card-label">Confidence</div>
            <div class="card-value" style="font-size: 1.8rem;">{budget_data.get('confidence', '95%')}</div>
            <div class="card-subtitle" style="font-size: 0.85rem;">Model accuracy</div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Sources:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('data_sources', '12')} valid</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                    <span style="color: #92400E; font-size: 0.8rem;">Sample:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('sample_size', '9,812')}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #92400E; font-size: 0.8rem;">Error:</span>
                    <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{budget_data.get('margin_error', '±2.5%')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_target_strategy_card(strategy_data: Dict) -> None:
    """Create target strategy cards with the same style as budget cards, displayed on the left side"""
    
    # These will be displayed in the left column alongside intervention mix
    
    # Strategy Overview Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">🎯</div>
        <div class="card-label">Current Target Strategy</div>
        <div class="card-value" style="font-size: 1.3rem;">{strategy_data.get('strategy', 'Universal Coverage')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Implementation approach</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Type:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('strategy_type', 'Universal')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Priority:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('priority_level', 'High Impact')}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Phase:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('phase', 'Phase 1')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Target Population Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">👥</div>
        <div class="card-label">Target Population</div>
        <div class="card-value" style="font-size: 1.8rem;">{strategy_data.get('target_population', '46.2M')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Total requiring intervention</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Rural:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('rural_pop', '75%')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Urban:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('urban_pop', '25%')}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Risk Level:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #DC2626;">{strategy_data.get('vulnerability', 'High')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Coverage Target Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">📊</div>
        <div class="card-label">Coverage Target</div>
        <div class="card-value" style="font-size: 1.8rem;">{strategy_data.get('coverage_target', '80%')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Of vulnerable population</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Current:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('current_coverage', '53.6%')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Gap:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #F59E0B;">{strategy_data.get('coverage_gap', '26.4%')}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Timeline:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('timeline', '12 months')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Budget Allocation Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">💰</div>
        <div class="card-label">Budget Allocation</div>
        <div class="card-value" style="font-size: 1.8rem;">{strategy_data.get('total_budget', 'UGX 1.8T')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Per person: {strategy_data.get('per_person_budget', 'UGX 48K')}</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Interventions:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('intervention_budget', '70%')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Operations:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{strategy_data.get('operations_budget', '20%')}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">ROI:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #16A34A;">{strategy_data.get('expected_roi', '3.8x')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_impact_cards(impact_data: Dict) -> None:
    """Create health impact outcome cards matching the size of strategy cards"""
    
    # Lives Saved Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">❤️</div>
        <div class="card-label">Lives Saved</div>
        <div class="card-value" style="font-size: 1.8rem;">{impact_data.get('lives_saved', '10,697')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Estimated lives to be saved</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Confidence Interval:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{impact_data.get('lives_saved_ci', '7,552 - 13,841')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Impact Level:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #16A34A;">High</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Timeline:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">12 months</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stunting Prevented Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">📏</div>
        <div class="card-label">Stunting Prevented</div>
        <div class="card-value" style="font-size: 1.8rem;">{impact_data.get('stunting_prevented', '96,195')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Children protected from stunting</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Confidence Interval:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{impact_data.get('stunting_ci', '67,914 - 124,475')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Current Rate:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #F59E0B;">23.2%</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Target Rate:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #16A34A;">15%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # DALYs Averted Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">⏱️</div>
        <div class="card-label">DALYs Averted</div>
        <div class="card-value" style="font-size: 1.8rem;">{impact_data.get('dalys', '801,885')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Disability-adjusted life years saved</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Productivity Gain:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #16A34A;">2.2M work days</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">Healthcare Savings:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">UGX 890B</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Quality of Life:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #16A34A;">+15%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Economic Benefit Card
    st.markdown(f"""
    <div class="metric-card" style="min-height: 180px; margin-bottom: 1rem;">
        <div class="card-icon">💎</div>
        <div class="card-label">Economic Benefit</div>
        <div class="card-value" style="font-size: 1.8rem;">{impact_data.get('economic_benefit', 'UGX 5.9T')}</div>
        <div class="card-subtitle" style="font-size: 0.85rem;">Total economic value generated</div>
        <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid rgba(217, 0, 0, 0.15);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">NPV (5 years):</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">{impact_data.get('npv', 'UGX 28.4T')}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                <span style="color: #92400E; font-size: 0.8rem;">ROI:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #16A34A;">3.8x</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #92400E; font-size: 0.8rem;">Payback Period:</span>
                <span style="font-weight: 600; font-size: 0.85rem; color: #7C2D12;">18 months</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_intervention_mix_cards(interventions: List[Dict]) -> None:
    """Create intervention mix cards"""
    
    for intervention in interventions:
        percentage = intervention.get('percentage', 0)
        st.markdown(f"""
        <div class="intervention-card">
            <div class="intervention-header">
                <div class="intervention-title">{intervention.get('name', 'Intervention')}</div>
                <div class="intervention-percentage">{percentage}%</div>
            </div>
            <div class="intervention-cost">{intervention.get('cost', 'Cost not specified')}</div>
            <div class="intervention-bar">
                <div class="intervention-bar-fill" style="width: {percentage}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_executive_dashboard_card(exec_data: Dict) -> None:
    """Create executive dashboard summary card with properly formatted metrics"""
    
    # Create columns for better layout
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1A365D 0%, #2563EB 100%); 
                color: white; 
                border-radius: 16px; 
                padding: 2rem;
                margin-bottom: 1.5rem;">
        <h3 style="margin-bottom: 1.5rem; font-size: 1.5rem; color: white;">Executive Dashboard</h3>
    """, unsafe_allow_html=True)
    
    # Create metric cards in columns
    cols = st.columns(len(exec_data))
    
    for idx, (metric, data) in enumerate(exec_data.items()):
        with cols[idx]:
            value = data.get('value', 'N/A')
            change = data.get('change', 0)
            change_symbol = "+" if change >= 0 else ""
            change_color = "#10B981" if change >= 0 else "#EF4444"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem;">
                <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;">{metric}</div>
                <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.25rem;">{value}</div>
                <div style="font-size: 0.85rem; color: {change_color};">
                    {change_symbol}{change}{'%' if change != 0 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_alert_cards(alerts: List[Dict]) -> None:
    """Create real-time alert cards"""
    
    st.markdown('<h3>🚨 Real-Time Alerts</h3>', unsafe_allow_html=True)
    
    # Process alerts in pairs for 2-column layout
    for i in range(0, len(alerts), 2):
        col1, col2 = st.columns(2)
        
        # First alert in the pair
        with col1:
            alert = alerts[i]
            alert_type = alert.get('type', 'info')
            icon = alert.get('icon', '⚠️')
            
            type_class = 'warning'
            if alert_type == 'critical':
                type_class = 'critical'
            elif alert_type == 'success':
                type_class = 'success'
                
            st.markdown(f"""
            <div class="alert-card {type_class}">
                <div class="alert-icon">{icon}</div>
                <div class="alert-content">
                    <div class="alert-title">{alert.get('title', 'Alert')}</div>
                    <div class="alert-message">{alert.get('message', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Second alert in the pair (if exists)
        with col2:
            if i + 1 < len(alerts):
                alert = alerts[i + 1]
                alert_type = alert.get('type', 'info')
                icon = alert.get('icon', '⚠️')
                
                type_class = 'warning'
                if alert_type == 'critical':
                    type_class = 'critical'
                elif alert_type == 'success':
                    type_class = 'success'
                    
                st.markdown(f"""
                <div class="alert-card {type_class}">
                    <div class="alert-icon">{icon}</div>
                    <div class="alert-content">
                        <div class="alert-title">{alert.get('title', 'Alert')}</div>
                        <div class="alert-message">{alert.get('message', '')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def create_distribution_network_card(network_data: Dict) -> None:
    """Create distribution network statistics card"""
    
    stats_html = ""
    for stat, value in network_data.items():
        stats_html += f"""
        <div class="network-stat">
            <div class="network-stat-label">{stat}</div>
            <div class="network-stat-value">{value}</div>
        </div>
        """
    
    st.markdown(f"""
    <div class="network-card">
        <h3 style="color: #1E40AF; margin-bottom: 1.5rem;">Distribution Network</h3>
        {stats_html}
    </div>
    """, unsafe_allow_html=True)

def create_financial_metrics_card(financial_data: Dict) -> None:
    """Create financial metrics card"""
    
    st.markdown(f"""
    <div class="financial-card">
        <div class="financial-metric">
            <div class="financial-label">Net Present Value</div>
            <div class="financial-value">{financial_data.get('npv', 'UGX 66.5B')}</div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div>
                <div class="financial-label">IRR</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #15803D;">{financial_data.get('irr', '15.0%')}</div>
            </div>
            <div>
                <div class="financial-label">Payback</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #15803D;">{financial_data.get('payback', '4 years')}</div>
            </div>
        </div>
        <div style="margin-top: 1rem;">
            <div class="financial-label">Benefit-Cost Ratio</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #15803D;">{financial_data.get('bcr', '1.31')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_kpi_cards(kpi_data: List[Dict]) -> None:
    """Create KPI cards with trend indicators using native Streamlit components"""
    
    # Create columns based on number of KPIs
    num_kpis = len(kpi_data)
    
    # Arrange KPIs in rows of 3 for better display
    if num_kpis <= 3:
        cols = st.columns(num_kpis)
        for idx, kpi in enumerate(kpi_data):
            with cols[idx]:
                _render_single_kpi(kpi)
    else:
        # Create multiple rows with 3 columns each
        rows_needed = (num_kpis + 2) // 3  # Ceiling division
        kpi_idx = 0
        
        for row in range(rows_needed):
            cols = st.columns(min(3, num_kpis - kpi_idx))
            for col_idx in range(min(3, num_kpis - kpi_idx)):
                with cols[col_idx]:
                    _render_single_kpi(kpi_data[kpi_idx])
                kpi_idx += 1

def _render_single_kpi(kpi: Dict) -> None:
    """Render a single KPI metric"""
    trend = kpi.get('trend', 0)
    trend_symbol = '↑' if trend > 0 else '↓' if trend < 0 else '→'
    trend_text = f"{trend_symbol} {abs(trend)}%"
    
    # Use st.metric for native display
    st.metric(
        label=kpi.get('name', 'KPI'),
        value=kpi.get('value', 'N/A'),
        delta=trend_text if trend != 0 else None,
        delta_color="normal" if trend > 0 else "inverse" if trend < 0 else "off"
    )
    
    # Add subtitle if present
    if kpi.get('subtitle'):
        st.caption(kpi.get('subtitle'))

def create_progress_ring(value: float, max_value: float = 100, label: str = "", 
                         color: str = "#10B981", size: int = 120) -> str:
    """Create an SVG progress ring for KPI visualization"""
    
    percentage = (value / max_value) * 100
    radius = size / 2 - 10
    circumference = 2 * 3.14159 * radius
    stroke_dashoffset = circumference - (percentage / 100) * circumference
    
    return f"""
    <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
        <circle cx="{size/2}" cy="{size/2}" r="{radius}" 
                fill="none" stroke="#E5E7EB" stroke-width="8"/>
        <circle cx="{size/2}" cy="{size/2}" r="{radius}" 
                fill="none" stroke="{color}" stroke-width="8"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{stroke_dashoffset}"
                style="transition: stroke-dashoffset 0.5s ease;"/>
    </svg>
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
        <div style="font-size: 1.8rem; font-weight: 700;">{value:.0f}%</div>
        <div style="font-size: 0.75rem; color: #6B7280;">{label}</div>
    </div>
    """

def create_synergy_impact_card(base_impact: float, synergy_multiplier: float) -> None:
    """Create impact projection with synergies card"""
    
    total_impact = base_impact * synergy_multiplier
    additional_benefit = total_impact - base_impact
    
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%); border: 2px solid #A855F7;">
        <h3 style="color: #6B21A8; margin-bottom: 1rem;">Impact Projection with Synergies</h3>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center;">
            <div>
                <div class="card-label" style="color: #7C3AED;">Base Impact</div>
                <div class="card-value" style="font-size: 1.8rem; color: #6B21A8;">{base_impact:.0f} units</div>
            </div>
            <div>
                <div class="card-label" style="color: #7C3AED;">With Synergies</div>
                <div class="card-value" style="font-size: 1.8rem; color: #6B21A8;">{total_impact:.0f} units</div>
            </div>
            <div>
                <div class="card-label" style="color: #7C3AED;">Additional Benefit</div>
                <div class="card-value" style="font-size: 1.8rem; color: #6B21A8;">+{additional_benefit:.0f} units</div>
            </div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(168, 85, 247, 0.1); border-radius: 8px;">
            <div style="font-weight: 600; color: #6B21A8; margin-bottom: 0.5rem;">Synergy Multiplier: {synergy_multiplier:.2f}x</div>
            <div style="height: 8px; background: #E9D5FF; border-radius: 4px; overflow: hidden;">
                <div style="height: 100%; width: {min(synergy_multiplier * 50, 100)}%; background: linear-gradient(90deg, #A855F7 0%, #7C3AED 100%);"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sample usage function
def render_dashboard_with_cards():
    """Render the complete dashboard with all card components"""
    
    # Apply card styling
    apply_card_styling()
    
    # Budget & Coverage Section
    st.markdown("## 📊 Budget & Coverage Overview")
    budget_data = {
        'budget': 'UGX 178.0B',
        'duration': '12 mo',
        'coverage': '80%',
        'people': '11.09M',
        'per_person': 'UGX 16K',
        'confidence': '95%'
    }
    create_budget_coverage_cards(budget_data)
    
    # Target Strategy Section
    st.markdown("## 🎯 Targeting Strategy")
    strategy_data = {
        'strategy': 'High Burden Districts (Top 30)',
        'target_population': '13.9M',
        'coverage_target': '80%',
        'people_to_reach': '11,090,581',
        'budget': 'UGX 178.0B'
    }
    create_target_strategy_card(strategy_data)
    
    # Impact Section
    st.markdown("## 💪 Expected Health Outcomes")
    impact_data = {
        'lives_saved': '10,697',
        'lives_saved_ci': '7,552 - 13,841',
        'stunting_prevented': '96,195',
        'stunting_ci': '67,914 - 124,475',
        'dalys': '801,885',
        'economic_benefit': 'UGX 5.9T',
        'npv': 'UGX 28.4T'
    }
    create_impact_cards(impact_data)
    
    # Intervention Mix Section
    st.markdown("## 🔄 Intervention Mix")
    col1, col2 = st.columns(2)
    
    with col1:
        interventions = [
            {'name': 'Food Fortification Program', 'percentage': 60, 'cost': 'UGX 53K/person'},
            {'name': 'Direct Supplementation', 'percentage': 20, 'cost': 'UGX 2K/person'}
        ]
        create_intervention_mix_cards(interventions)
    
    with col2:
        interventions = [
            {'name': 'Nutrition Education', 'percentage': 10, 'cost': 'UGX 28K/person'},
            {'name': 'Biofortified Crops', 'percentage': 10, 'cost': 'UGX 71K/person'}
        ]
        create_intervention_mix_cards(interventions)
    
    # Executive Dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        exec_data = {
            'Critical Districts': {'value': '9', 'change': -3},
            'Affected Population': {'value': '15.1M', 'change': 0.2},
            'Avg Adequacy': {'value': '73.2%', 'change': 2.3},
            'Synergy Factor': {'value': '1.00x', 'change': 0},
            'Est. ROI': {'value': '3.2x', 'change': 0.3}
        }
        create_executive_dashboard_card(exec_data)
    
    with col2:
        # Financial Metrics
        financial_data = {
            'npv': 'UGX 66.5B',
            'irr': '15.0%',
            'payback': '4 years',
            'bcr': '1.31'
        }
        create_financial_metrics_card(financial_data)
    
    # Alerts Section
    alerts = [
        {'type': 'warning', 'icon': '⚠️', 'title': 'Stock Alert', 'message': 'Vitamin B12 supplies running low in 3 districts'},
        {'type': 'warning', 'icon': '⚠️', 'title': 'Coverage Gap', 'message': '15% below target in Eastern region'},
        {'type': 'success', 'icon': '✅', 'title': 'Milestone', 'message': '50,000 children reached this month'},
        {'type': 'success', 'icon': '✅', 'title': 'Quality', 'message': '98% compliance with protocols'}
    ]
    create_alert_cards(alerts)
    
    # Distribution Network
    st.markdown("## 🚚 Supply Chain & Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        network_data = {
            'Total Facilities': '156',
            'Active Distribution Points': '94',
            'Average Lead Time': '3.5 days',
            'Stock Turnover Rate': '2.1x/month',
            'Fill Rate': '90.0%'
        }
        create_distribution_network_card(network_data)
    
    with col2:
        # Synergy Impact
        create_synergy_impact_card(base_impact=100, synergy_multiplier=1.0)
    
    # KPIs Section
    st.markdown("## 📈 Key Performance Indicators")
    kpi_data = [
        {'name': 'Coverage Rate', 'value': '55.0%', 'trend': 5.2, 'subtitle': 'vs target: 80%'},
        {'name': 'Compliance', 'value': '72.0%', 'trend': 2.1},
        {'name': 'Stock Levels', 'value': '68%', 'trend': -3.5},
        {'name': 'Quality Score', 'value': '78/100', 'trend': 1.0},
        {'name': 'Feedback', 'value': '4.1/5.0', 'trend': 0.2},
        {'name': 'Efficiency', 'value': '0.92x', 'trend': 0.1}
    ]
    create_kpi_cards(kpi_data)

if __name__ == "__main__":
    # Test the card components
    st.set_page_config(layout="wide", page_title="Uganda Nutrition Cards")
    st.title("🇺🇬 Uganda Nutrition Dashboard - Card Components")
    render_dashboard_with_cards()