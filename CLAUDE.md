# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a nutrition intervention analysis and simulation platform focusing on East African countries (Uganda and Kenya). The main application is an interactive Streamlit dashboard for analyzing nutrition deficiencies and modeling intervention strategies using real-world data.

## Key Development Commands

### Running the Main Application

```bash
# Main Uganda nutrition dashboard with all features
streamlit run uganda_nutrition_enhanced.py

# Alternative simulators
streamlit run iodine_intervention_simulator.py  # Kenya iodine interventions
streamlit run zinc_intervention_simulator.py     # Zinc deficiency simulator
```

### Testing and Validation

```bash
# Test dynamic data integration
python3 test_dynamic_values.py

# Test economic metrics calculations
python3 test_economic_metrics.py

# Run Uganda additional analysis
python3 uganda_additional_analysis.py
```

### Dependencies Installation

```bash
pip install streamlit pandas numpy plotly scipy scikit-learn networkx folium streamlit-folium reportlab python-dotenv twilio
```

## Architecture Overview

### Data Flow

1. **Real Data Sources** → `real_data_provider.py` → Provides actual Uganda/Kenya nutrition data
2. **Dynamic Integration** → `dynamic_data_integration.py` → Manages data source switching
3. **Configuration** → `uganda_nutrition_config.py` → Centralized settings and parameters
4. **Main Dashboard** → `uganda_nutrition_enhanced.py` → Interactive Streamlit interface
5. **Intervention Engine** → `uganda_intervention_engine.py` → Optimization algorithms

### Core Components

#### `uganda_nutrition_enhanced.py` (Main Dashboard)

- **Multi-page Streamlit app** with executive summary, intervention planning, monitoring, and reporting
- **Real-time data integration** from Uganda census, health facilities, and nutrition surveys
- **Advanced features**: Supply chain optimization, multi-nutrient synergies, PDF report generation
- **Interactive visualizations** using Plotly and Folium for geographic mapping

#### `real_data_provider.py`

- Loads actual data from:
  - `UGA_00003/`: FAO/WHO food consumption data (9,812 records)
  - `ug2/`: District-level population and health facility data
  - `latest/`: UN/UNICEF nutrition indicators
- Provides consistent API for accessing real metrics instead of simulated values

#### `uganda_intervention_engine.py`

- Optimization algorithms for intervention planning
- Cost-effectiveness calculations
- Multi-nutrient interaction modeling
- Supply chain network optimization/

### Data Sources

- **Population Data**: 47,840,590 (2025 projection) from Uganda census
- **Children Under 5**: 7,176,088 from demographic data
- **Stunting Rate**: 23.2% from UN 2024 data
- **Vitamin A Coverage**: 53.6% current projection from UNICEF
- **130 Districts**: Granular geographic data for targeted interventions

## Key Implementation Details

### Real vs Simulated Data

The system prioritizes real data over simulations:

```python
try:
    from real_data_provider import UgandaRealDataProvider
    real_provider = UgandaRealDataProvider()
    USE_REAL_DATA = True
except ImportError:
    USE_REAL_DATA = False  # Falls back to default values
```

### Intervention Effectiveness (Evidence-Based)

- Supplementation: 0.73 (77% improvement from Vitamin A programs)
- Fortification: 0.61 (based on fortified food consumption data)
- Education: 0.55 (conservative evidence-based estimate)
- Biofortification: 0.65 (from adoption rates)

### Cost Parameters (Per Person)

- Supplementation: $0.50 (UNICEF actual)
- Fortification: $15
- Education: $8
- Biofortification: $20

## Important Conventions

1. **Data Validation**: Always check if real data provider is available before using fallback values
2. **District-Level Granularity**: Use 130 districts for geographic analysis, not aggregated regions
3. **Multi-Nutrient Focus**: Consider interactions between Vitamin A, Iron, Zinc, B12, and Iodine
4. **Evidence-Based Metrics**: Use actual program outcomes, not theoretical estimates
5. **PDF Reports**: Generated using ReportLab with proper formatting for stakeholders

## Performance Considerations

- Dashboard loads ~10,000 consumption records - use caching where possible
- Geographic visualizations for 130 districts can be resource-intensive
- PDF generation includes charts and tables - may take several seconds
- Real-time monitoring updates should be throttled to prevent overload

## Security Notes

- Twilio credentials in `scripts/call_me.py` should use environment variables
- No sensitive health data should be exposed in public deployments
- District-level aggregation maintains privacy while enabling analysis
