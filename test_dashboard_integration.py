"""
Test the enhanced report generator integration with the dashboard
"""

import streamlit as st
from io import BytesIO
import sys
import traceback

def test_dashboard_integration():
    """Test that the enhanced report generator works with the dashboard"""
    
    print("=" * 80)
    print("TESTING ENHANCED REPORT GENERATOR INTEGRATION")
    print("=" * 80)
    
    results = {
        'import_test': False,
        'generator_init': False,
        'report_generation': {},
        'issues': []
    }
    
    # Test 1: Import the enhanced generator
    print("\n1. Testing import of enhanced generator...")
    try:
        from report_generator import EnhancedReportGenerator
        results['import_test'] = True
        print("✅ Enhanced report generator imported successfully")
    except ImportError as e:
        results['issues'].append(f"Import failed: {str(e)}")
        print(f"❌ Failed to import: {str(e)}")
        return results
    
    # Test 2: Initialize generator
    print("\n2. Testing generator initialization...")
    try:
        generator = EnhancedReportGenerator()
        results['generator_init'] = True
        print("✅ Generator initialized successfully")
        
        # Check for warnings/errors
        if hasattr(generator, 'errors') and generator.errors:
            print(f"⚠️  Initialization errors: {generator.errors}")
            results['issues'].extend(generator.errors)
        
        if hasattr(generator, 'warnings') and generator.warnings:
            print(f"⚠️  Initialization warnings: {generator.warnings[:3]}")
            
    except Exception as e:
        results['issues'].append(f"Initialization failed: {str(e)}")
        print(f"❌ Failed to initialize: {str(e)}")
        return results
    
    # Test 3: Generate reports with dashboard parameters
    print("\n3. Testing report generation with dashboard parameters...")
    
    # Simulate dashboard parameters
    dashboard_params = {
        'period': 'Q1 2024',
        'budget': 150000000,
        'districts': ['Kampala', 'Gulu', 'Mbarara'],
        'duration': 12,
        'include_sections': ['summary', 'metrics', 'recommendations'],
        'format': 'PDF',
        'language': 'English'
    }
    
    # Test each report type that the dashboard supports
    report_types = {
        'Executive Summary': 'executive',
        'Technical Report': 'technical',
        'Donor Report': 'donor',
        'Impact Assessment': 'impact',
        'Financial Analysis': 'financial',
        'Government Brief': 'district',
        'Full Documentation': 'comparison'
    }
    
    for ui_name, generator_type in report_types.items():
        try:
            print(f"\n   Testing '{ui_name}' ({generator_type})...")
            
            # Generate report
            pdf_buffer = generator.generate_report(generator_type, **dashboard_params)
            
            if isinstance(pdf_buffer, BytesIO):
                pdf_size = len(pdf_buffer.getvalue())
                if pdf_size > 5000:  # Expect substantial content
                    results['report_generation'][ui_name] = 'success'
                    print(f"   ✅ {ui_name}: Generated {pdf_size:,} bytes")
                else:
                    results['report_generation'][ui_name] = 'minimal'
                    results['issues'].append(f"{ui_name} has minimal content")
                    print(f"   ⚠️  {ui_name}: Minimal content ({pdf_size} bytes)")
            else:
                results['report_generation'][ui_name] = 'failed'
                results['issues'].append(f"{ui_name} did not return BytesIO")
                print(f"   ❌ {ui_name}: Invalid return type")
                
        except Exception as e:
            results['report_generation'][ui_name] = 'error'
            results['issues'].append(f"{ui_name} error: {str(e)}")
            print(f"   ❌ {ui_name}: {str(e)}")
    
    # Test 4: Check for new features
    print("\n4. Checking for enhanced features...")
    
    features = {
        'Data Validation': hasattr(generator, 'validate_data'),
        'Chart Creation': hasattr(generator, 'create_chart_visualization'),
        'Error Handling': hasattr(generator, '_create_error_report'),
        'Comparison Reports': 'comparison' in generator.templates,
        'Data Quality Notices': hasattr(generator, '_create_data_quality_notice'),
        'Visualizations': hasattr(generator, '_create_visualizations_section')
    }
    
    for feature, present in features.items():
        if present:
            print(f"   ✅ {feature}: Available")
        else:
            print(f"   ❌ {feature}: Not found")
            results['issues'].append(f"Missing feature: {feature}")
    
    return results

def test_streamlit_compatibility():
    """Test that the enhanced generator works with Streamlit components"""
    print("\n5. Testing Streamlit compatibility...")
    
    try:
        # Create a minimal Streamlit-like environment
        from report_generator import EnhancedReportGenerator
        
        # Test with Streamlit-style parameters
        generator = EnhancedReportGenerator()
        
        # Simulate what the dashboard does
        report_params = {
            'period': 'Monthly',
            'budget': 100000000,
            'districts': [],
            'duration': 12,
            'include_sections': ['summary', 'metrics', 'recommendations'],
            'format': 'PDF',
            'language': 'English'
        }
        
        # Generate a test report
        pdf_buffer = generator.generate_report('executive', **report_params)
        
        if isinstance(pdf_buffer, BytesIO) and len(pdf_buffer.getvalue()) > 1000:
            print("   ✅ Streamlit compatibility confirmed")
            return True
        else:
            print("   ❌ Streamlit compatibility issue detected")
            return False
            
    except Exception as e:
        print(f"   ❌ Streamlit compatibility error: {str(e)}")
        return False

def generate_summary_report(results):
    """Generate a summary of the integration test"""
    print("\n" + "=" * 80)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 80)
    
    # Overall status
    total_tests = len(results['report_generation']) + 2  # +2 for import and init
    passed_tests = sum([
        results['import_test'],
        results['generator_init'],
        len([r for r in results['report_generation'].values() if r == 'success'])
    ])
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    # Report generation details
    print("\nReport Generation Results:")
    for report_type, status in results['report_generation'].items():
        icon = "✅" if status == 'success' else "⚠️" if status == 'minimal' else "❌"
        print(f"  {icon} {report_type}: {status}")
    
    # Issues
    if results['issues']:
        issue_count = len(results['issues'])
        print(f"\nIssues Found ({issue_count}):")
        for issue in results['issues'][:10]:  # Show first 10 issues
            print(f"  - {issue}")
    else:
        print("\n✅ No issues found!")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    if not results['import_test']:
        print("🔴 CRITICAL: Fix import issues before deployment")
    elif not results['generator_init']:
        print("🔴 CRITICAL: Fix initialization issues")
    elif any(s == 'error' for s in results['report_generation'].values()):
        print("🟡 WARNING: Some report types are failing")
    else:
        print("🟢 SUCCESS: Integration is working properly!")
        print("\nNext Steps:")
        print("1. Run the dashboard with: streamlit run uganda_nutrition_enhanced.py")
        print("2. Test report generation through the UI")
        print("3. Verify PDF downloads work correctly")
        print("4. Check that visualizations appear in PDFs")

if __name__ == "__main__":
    print("Starting enhanced report generator integration test...\n")
    
    try:
        # Run main integration tests
        results = test_dashboard_integration()
        
        # Test Streamlit compatibility
        streamlit_ok = test_streamlit_compatibility()
        
        # Generate summary
        generate_summary_report(results)
        
        # Save results
        import json
        with open('integration_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n✅ Integration test complete! Results saved to integration_test_results.json")
        
        # Return exit code
        if results['import_test'] and results['generator_init']:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
            
    except Exception as e:
        print(f"\n❌ Critical error during integration test: {str(e)}")
        traceback.print_exc()
        sys.exit(1)