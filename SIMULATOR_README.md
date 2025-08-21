# 🧂 Kenya Iodine Intervention Simulator

## Interactive GUI for Modeling Iodine Deficiency Interventions

### Quick Start

1. **Run the simulator:**
```bash
streamlit run iodine_intervention_simulator.py
```

2. **Open in browser:** The app will automatically open at `http://localhost:8501`

### Features

## 📊 Interactive Controls

### Input Parameters (Tweakable):

1. **💵 Budget Allocation**
   - Total budget in KSH (Kenyan Shillings)
   - Automatically calculates budget per person
   - Range: 1 million to 10 billion KSH

2. **🎯 Intervention Mix (% of budget)**
   - **Salt Iodization:** Fix existing infrastructure (most cost-effective)
   - **Oil Fortification:** Longer iodine retention (6 months)
   - **Direct Supplementation:** Pills/drops for high-risk groups
   - **School Programs:** Iodized meals for children

3. **⚙️ Implementation Variables**
   - **Timeline:** 6-60 months implementation period
   - **Efficiency:** 30-95% (accounts for corruption, logistics, wastage)
   - **Target Groups:** Entire population or specific demographics

## 📈 Real-Time Outputs

### Immediate Effects (0-3 months):
- Urinary iodine normalization rate
- Thyroid function improvement
- Energy level increases

### Mid-term Effects (3-12 months):
- Goiter reduction percentage
- Pregnancy outcome improvements
- Child cognitive development gains

### Long-term Effects (1-5 years):
- Average IQ points gained per child
- Cretinism cases prevented
- Economic productivity increase

## 💡 Key Features

### Dynamic Calculations
- **Real-time updates:** All outputs change instantly when you adjust inputs
- **Coverage estimation:** Shows percentage of population reached
- **Cost per person:** Automatic calculation based on intervention mix

### Visual Analytics
- **Timeline graphs:** Shows intervention impact over months
- **Budget pie charts:** Visualizes resource allocation
- **ROI analysis:** Cost vs benefits over 5 years
- **Scenario comparison:** Compare different strategies

### Risk Assessment
- Supply chain reliability
- Quality control measures
- Community adoption rates
- Political stability factors

## 📋 Reports Generation
- Executive summary with all key metrics
- Downloadable reports in Markdown format
- Recommendations based on simulation results
- Scenario comparisons

## 🎮 How to Use

### Step 1: Set Your Budget
- Enter total available funds in KSH
- System calculates coverage potential

### Step 2: Allocate Interventions
- Use sliders to distribute budget (must total 100%)
- Each intervention has different cost/effectiveness ratios

### Step 3: Adjust Efficiency
- Set realistic implementation efficiency
- Accounts for real-world challenges

### Step 4: View Results
- Switch between tabs to see:
  - Health outcomes predictions
  - Cost-benefit analysis
  - Generated reports

## 📊 Example Scenarios

### Scenario 1: Emergency Response
- Budget: 1 billion KSH
- Focus: 60% direct supplementation, 40% salt fix
- Timeline: 6 months
- Result: Quick coverage but higher cost

### Scenario 2: Sustainable Solution
- Budget: 500 million KSH
- Focus: 70% salt iodization, 30% school programs
- Timeline: 24 months
- Result: Lower cost, gradual but lasting impact

### Scenario 3: Balanced Approach
- Budget: 750 million KSH
- Mix: 40% salt, 20% oil, 25% supplements, 15% schools
- Timeline: 18 months
- Result: Good coverage with risk diversification

## 🔍 Understanding the Model

### Cost Assumptions (per person/year):
- Salt iodization: 2.5 KSH
- Oil fortification: 30 KSH
- Direct supplements: 50 KSH
- School programs: 8 KSH

### Effectiveness Ratings:
- Direct supplements: 98% (highest)
- Oil fortification: 92%
- School programs: 88%
- Salt iodization: 85% (but most scalable)

### Coverage Formula:
```
Coverage = (Budget / (Avg_Cost × Population)) × Efficiency
```

## ⚠️ Important Notes

1. **Based on real data:** Uses Kenya National Micronutrient Survey 2011 showing 100% iodine deficiency

2. **Simplified model:** Real interventions have more complex dynamics

3. **Estimates only:** Results are projections, not guarantees

4. **Multiple interventions recommended:** No single solution addresses all aspects

## 🚀 Advanced Features

- **Risk factor monitoring:** Tracks implementation risks
- **ROI calculation:** Shows return on investment
- **Population segmentation:** Target specific groups
- **Timeline visualization:** See adoption curves
- **Scenario comparison:** Test multiple strategies

## 📈 Key Metrics Tracked

- Population coverage percentage
- Cost per IQ point gained
- Cost per life saved
- Economic productivity gains
- Health system cost savings

## 🎯 Optimization Tips

1. **Start with salt:** Most cost-effective for wide coverage
2. **Target high-risk:** Pregnant women and children first
3. **Mix strategies:** Diversify to reduce risk
4. **Monitor efficiency:** Address implementation bottlenecks
5. **Plan long-term:** Sustainable solutions over quick fixes

---

**Note:** This simulator is for educational and planning purposes. Actual intervention planning should involve public health experts and local stakeholders.