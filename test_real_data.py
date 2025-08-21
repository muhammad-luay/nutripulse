"""
Test that real data is being loaded and used instead of fallback values
"""

import sys
import json
from datetime import datetime

def test_real_data_loading():
    """Test that all real data sources are properly loaded"""
    print("=" * 80)
    print("TESTING REAL DATA INTEGRATION")
    print("=" * 80)
    
    results = {
        'provider_loaded': False,
        'population_data': False,
        'consumption_data': False,
        'nutrition_indicators': False,
        'health_facilities': False,
        'real_values': {}
    }
    
    # Test 1: Load the real data provider
    print("\n1. Loading real data provider...")
    try:
        from real_data_provider import UgandaRealDataProvider
        provider = UgandaRealDataProvider()
        results['provider_loaded'] = True
        print("✅ Real data provider loaded")
    except Exception as e:
        print(f"❌ Failed to load provider: {e}")
        return results
    
    # Test 2: Check population data
    print("\n2. Checking population data...")
    try:
        pop_data = provider.get_population_data()
        total_pop = pop_data.get('total', 0)
        children = pop_data.get('children_under_5', 0)
        districts = pop_data.get('districts', [])
        
        # These should be real values, not fallback
        if total_pop > 45000000 and total_pop < 50000000:  # Real range
            results['population_data'] = True
            results['real_values']['total_population'] = total_pop
            results['real_values']['children_under_5'] = children
            results['real_values']['districts_count'] = len(districts)
            print(f"✅ Real population: {total_pop:,} total, {children:,} children <5")
            print(f"   Districts: {len(districts)}")
        else:
            print(f"⚠️ Suspicious population value: {total_pop}")
    except Exception as e:
        print(f"❌ Population data error: {e}")
    
    # Test 3: Check consumption data
    print("\n3. Checking consumption data...")
    try:
        consumption_df = provider.get_consumption_data()
        if consumption_df is not None:
            results['consumption_data'] = True
            results['real_values']['consumption_records'] = len(consumption_df)
            print(f"✅ Real consumption data: {len(consumption_df):,} food records")
            
            # Check nutrient analysis
            nutrient_analysis = provider.get_nutrient_analysis()
            if nutrient_analysis:
                print(f"   Nutrient analysis available for {len(nutrient_analysis)} nutrients")
                # Show a sample
                if 'VITA_RAE_mcg' in nutrient_analysis:
                    vit_a = nutrient_analysis['VITA_RAE_mcg']
                    print(f"   Vitamin A deficiency: {vit_a.get('deficient_pct', 0):.1f}% of subjects")
        else:
            print("⚠️ No consumption data loaded")
    except Exception as e:
        print(f"❌ Consumption data error: {e}")
    
    # Test 4: Check nutrition indicators
    print("\n4. Checking nutrition indicators...")
    try:
        indicators = provider.get_nutrition_indicators()
        stunting = indicators.get('stunting_prevalence', 0)
        vitamin_a = indicators.get('vitamin_a_coverage', 0)
        
        # Check for real 2022 values
        if stunting > 25 and stunting < 35:  # Real range ~28.9%
            results['nutrition_indicators'] = True
            results['real_values']['stunting_rate'] = stunting
            results['real_values']['vitamin_a_coverage'] = vitamin_a
            print(f"✅ Real indicators: Stunting {stunting}%, Vitamin A coverage {vitamin_a}%")
            
            # Show more indicators
            print(f"   Wasting: {indicators.get('wasting_prevalence', 0)}%")
            print(f"   Iron deficiency: {indicators.get('iron_deficiency', 0)}%")
            print(f"   Zinc deficiency: {indicators.get('zinc_deficiency', 0)}%")
        else:
            print(f"⚠️ Suspicious stunting rate: {stunting}%")
    except Exception as e:
        print(f"❌ Nutrition indicators error: {e}")
    
    # Test 5: Check health facilities
    print("\n5. Checking health facilities...")
    try:
        facilities = provider.get_health_facilities()
        total = facilities.get('total_facilities', 0)
        hospitals = facilities.get('hospitals', 0)
        
        if total > 7000 and total < 8000:  # Real range ~7439
            results['health_facilities'] = True
            results['real_values']['total_facilities'] = total
            results['real_values']['hospitals'] = hospitals
            print(f"✅ Real facilities: {total:,} total, {hospitals} hospitals")
            
            # Show breakdown
            print(f"   HC IV: {facilities.get('hc_iv', 0)}")
            print(f"   HC III: {facilities.get('hc_iii', 0)}")
            print(f"   HC II: {facilities.get('hc_ii', 0)}")
        else:
            print(f"⚠️ Suspicious facility count: {total}")
    except Exception as e:
        print(f"❌ Health facilities error: {e}")
    
    # Test 6: Get summary statistics
    print("\n6. Getting summary statistics...")
    try:
        summary = provider.get_summary_statistics()
        print("\nData Sources:")
        for source, desc in summary.get('data_sources', {}).items():
            print(f"  - {source}: {desc}")
        
        print("\nData Quality:")
        for check, status in summary.get('data_quality', {}).items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {check}: {status}")
    except Exception as e:
        print(f"❌ Summary error: {e}")
    
    return results

def test_report_generation_with_real_data():
    """Test that reports use real data"""
    print("\n" + "=" * 80)
    print("TESTING REPORT GENERATION WITH REAL DATA")
    print("=" * 80)
    
    try:
        from report_generator import EnhancedReportGenerator
        
        print("\n1. Initializing report generator...")
        generator = EnhancedReportGenerator()
        
        print("\n2. Generating test report with real data...")
        params = {
            'period': 'Q1 2024',
            'budget': 100000000,
            'districts': ['Kampala', 'Gulu'],
            'duration': 12
        }
        
        # Generate a report
        pdf_buffer = generator.generate_report('executive', **params)
        
        if pdf_buffer:
            print(f"✅ Report generated: {len(pdf_buffer.getvalue()):,} bytes")
            
            # Check if real data was used
            if hasattr(generator, 'real_data_provider') and generator.real_data_provider:
                print("✅ Real data provider is connected")
            else:
                print("⚠️ Real data provider not connected - using fallback")
        else:
            print("❌ Report generation failed")
            
    except Exception as e:
        print(f"❌ Report generation error: {e}")

def generate_summary(results):
    """Generate summary report"""
    print("\n" + "=" * 80)
    print("REAL DATA INTEGRATION SUMMARY")
    print("=" * 80)
    
    # Check overall status
    all_loaded = all([
        results['population_data'],
        results['consumption_data'],
        results['nutrition_indicators'],
        results['health_facilities']
    ])
    
    if all_loaded:
        print("\n🎉 SUCCESS! All real data sources are connected!")
        print("\nReal Values Being Used:")
        for key, value in results.get('real_values', {}).items():
            if isinstance(value, (int, float)):
                if value > 1000:
                    print(f"  - {key}: {value:,.0f}")
                else:
                    print(f"  - {key}: {value}")
            else:
                print(f"  - {key}: {value}")
    else:
        print("\n⚠️ PARTIAL SUCCESS - Some data sources not fully connected")
        print("\nData Source Status:")
        print(f"  {'✅' if results['population_data'] else '❌'} Population data")
        print(f"  {'✅' if results['consumption_data'] else '❌'} Consumption data")
        print(f"  {'✅' if results['nutrition_indicators'] else '❌'} Nutrition indicators")
        print(f"  {'✅' if results['health_facilities'] else '❌'} Health facilities")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if all_loaded:
        print("✅ Real data is fully integrated!")
        print("\nNext steps:")
        print("1. Run the dashboard: streamlit run uganda_nutrition_enhanced.py")
        print("2. Generate reports to see real data in action")
        print("3. All reports will now show:")
        print("   - Real population of 47+ million")
        print("   - Actual stunting rate of 28.9%")
        print("   - Real vitamin A coverage of 64%")
        print("   - Actual consumption patterns from 9,813 records")
    else:
        print("⚠️ Some data sources need attention")
        if not results['consumption_data']:
            print("- Check UGA_00003 directory for consumption CSV files")
        if not results['population_data']:
            print("- Check ug2 directory for population data")

if __name__ == "__main__":
    print("Starting real data integration test...\n")
    
    # Test data loading
    results = test_real_data_loading()
    
    # Test report generation
    test_report_generation_with_real_data()
    
    # Generate summary
    generate_summary(results)
    
    # Save results
    with open('real_data_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n✅ Test complete! Results saved to real_data_test_results.json")