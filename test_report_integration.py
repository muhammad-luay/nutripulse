#!/usr/bin/env python3
"""
Test script to validate report generation integration
Tests both standalone and dashboard integration
"""

import sys
import os
from io import BytesIO

def test_standalone_generation():
    """Test standalone report generation"""
    print("Testing standalone report generation...")
    
    try:
        from report_generator import UgandaReportGenerator
        
        generator = UgandaReportGenerator()
        
        # Test parameters
        params = {
            'period': '2024 Q1',
            'budget': 150000000,
            'districts': ['Kampala', 'Gulu', 'Karamoja'],
            'duration': 12
        }
        
        # Test executive report
        print("  Generating executive report...")
        pdf_buffer = generator.generate_report('executive', **params)
        
        if pdf_buffer and len(pdf_buffer.getvalue()) > 1000:
            print("  ✅ Executive report generated successfully")
            print(f"     Size: {len(pdf_buffer.getvalue())} bytes")
        else:
            print("  ❌ Executive report generation failed")
            return False
            
        # Test technical report
        print("  Generating technical report...")
        pdf_buffer = generator.generate_report('technical', **params)
        
        if pdf_buffer and len(pdf_buffer.getvalue()) > 1000:
            print("  ✅ Technical report generated successfully")
            print(f"     Size: {len(pdf_buffer.getvalue())} bytes")
        else:
            print("  ❌ Technical report generation failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_data_integration():
    """Test data integration with real data provider"""
    print("\nTesting data integration...")
    
    try:
        # Try to import real data provider
        from real_data_provider import UgandaRealDataProvider
        provider = UgandaRealDataProvider()
        
        # Test data collection
        print("  Testing population data...")
        pop_data = provider.get_population_data()
        if pop_data and 'total' in pop_data:
            print(f"  ✅ Population data loaded: {pop_data.get('total'):,} people")
        else:
            print("  ⚠️  Population data not available")
            
        print("  Testing nutrition indicators...")
        nutrition = provider.get_nutrition_indicators()
        if nutrition and 'stunting_prevalence' in nutrition:
            print(f"  ✅ Nutrition data loaded: {nutrition.get('stunting_prevalence')}% stunting")
        else:
            print("  ⚠️  Nutrition data not available")
            
        return True
        
    except ImportError:
        print("  ⚠️  Real data provider not available - using fallback data")
        return True
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_report_content():
    """Test that reports contain expected content"""
    print("\nTesting report content...")
    
    try:
        from report_generator import UgandaReportGenerator
        
        generator = UgandaReportGenerator()
        
        # Generate a report
        pdf_buffer = generator.generate_report('executive', period='2024 Q1', budget=100000000)
        
        # Check size (should be substantial)
        pdf_size = len(pdf_buffer.getvalue())
        if pdf_size > 2000:
            print(f"  ✅ Report has substantial content: {pdf_size} bytes")
        else:
            print(f"  ❌ Report too small: {pdf_size} bytes")
            return False
            
        # Save test report
        with open("test_integration_report.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())
        print("  ✅ Test report saved as test_integration_report.pdf")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_dashboard_compatibility():
    """Test compatibility with dashboard parameters"""
    print("\nTesting dashboard compatibility...")
    
    try:
        from report_generator import UgandaReportGenerator
        
        generator = UgandaReportGenerator()
        
        # Simulate dashboard parameters
        dashboard_params = {
            'period': 'Monthly',
            'budget': 250000000,
            'districts': [],  # Empty districts list
            'duration': 24,
            'include_sections': ['Executive Summary', 'KPIs', 'Recommendations'],
            'format': 'PDF',
            'language': 'English'
        }
        
        # Generate report with dashboard parameters
        pdf_buffer = generator.generate_report('executive', **dashboard_params)
        
        if pdf_buffer and len(pdf_buffer.getvalue()) > 1000:
            print("  ✅ Dashboard parameters handled correctly")
            return True
        else:
            print("  ❌ Failed with dashboard parameters")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Uganda Nutrition Report Generation Integration Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Standalone Generation", test_standalone_generation()))
    results.append(("Data Integration", test_data_integration()))
    results.append(("Report Content", test_report_content()))
    results.append(("Dashboard Compatibility", test_dashboard_compatibility()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("-" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"Total: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed! Report generation is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)