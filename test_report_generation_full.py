"""
Comprehensive test for report generation functionality
Tests both standalone and dashboard integration
"""

import sys
import traceback
from io import BytesIO
import pandas as pd
from datetime import datetime

def test_report_generator():
    """Test the report generator module"""
    print("=" * 80)
    print("REPORT GENERATION VALIDATION TEST")
    print("=" * 80)
    
    results = {
        'module_import': False,
        'data_providers': False,
        'report_types': {},
        'data_collection': False,
        'pdf_generation': False,
        'dashboard_integration': False,
        'issues': []
    }
    
    # Test 1: Module Import
    print("\n1. Testing module import...")
    try:
        from report_generator import UgandaReportGenerator
        results['module_import'] = True
        print("✅ Report generator module imported successfully")
    except ImportError as e:
        results['issues'].append(f"Module import failed: {str(e)}")
        print(f"❌ Failed to import report generator: {str(e)}")
        return results
    
    # Test 2: Data Providers
    print("\n2. Testing data provider integration...")
    try:
        generator = UgandaReportGenerator()
        
        # Check if data providers are initialized
        if hasattr(generator, 'real_data_provider'):
            if generator.real_data_provider is not None:
                results['data_providers'] = True
                print("✅ Real data provider initialized")
            else:
                print("⚠️  Real data provider not available (using fallback)")
                results['issues'].append("Real data provider not initialized - using fallback data")
        
        # Check intervention engine
        if hasattr(generator, 'intervention_engine'):
            if generator.intervention_engine is not None:
                print("✅ Intervention engine initialized")
            else:
                print("⚠️  Intervention engine not available")
                results['issues'].append("Intervention engine not initialized")
                
    except Exception as e:
        results['issues'].append(f"Data provider initialization failed: {str(e)}")
        print(f"❌ Failed to initialize data providers: {str(e)}")
    
    # Test 3: Report Types
    print("\n3. Testing all report types...")
    report_types = ['executive', 'technical', 'donor', 'impact', 'financial', 'district']
    
    test_params = {
        'period': 'Q1 2024',
        'budget': 200000000,
        'districts': ['Kampala', 'Gulu', 'Mbarara'],
        'duration': 12,
        'include_sections': ['summary', 'metrics', 'recommendations']
    }
    
    for report_type in report_types:
        try:
            print(f"   Testing {report_type} report...")
            pdf_buffer = generator.generate_report(report_type, **test_params)
            
            if isinstance(pdf_buffer, BytesIO):
                pdf_size = len(pdf_buffer.getvalue())
                if pdf_size > 1000:  # Check if PDF has substantial content
                    results['report_types'][report_type] = {
                        'status': 'success',
                        'size': pdf_size
                    }
                    print(f"   ✅ {report_type}: Generated {pdf_size:,} bytes")
                else:
                    results['report_types'][report_type] = {
                        'status': 'minimal',
                        'size': pdf_size
                    }
                    results['issues'].append(f"{report_type} report has minimal content ({pdf_size} bytes)")
                    print(f"   ⚠️  {report_type}: Minimal content ({pdf_size} bytes)")
            else:
                results['report_types'][report_type] = {'status': 'failed'}
                results['issues'].append(f"{report_type} report did not return BytesIO object")
                print(f"   ❌ {report_type}: Invalid return type")
                
        except Exception as e:
            results['report_types'][report_type] = {
                'status': 'error',
                'error': str(e)
            }
            results['issues'].append(f"{report_type} report generation failed: {str(e)}")
            print(f"   ❌ {report_type}: {str(e)}")
    
    # Test 4: Data Collection
    print("\n4. Testing data collection...")
    try:
        data = generator.collect_report_data('executive', test_params)
        
        required_keys = ['metadata', 'population', 'nutrition_indicators', 
                        'coverage_metrics', 'financial_metrics', 'impact_metrics']
        
        missing_keys = [key for key in required_keys if key not in data]
        
        if not missing_keys:
            results['data_collection'] = True
            print("✅ All required data sections present")
            
            # Check data quality
            if data.get('population', {}).get('total', 0) > 0:
                print("✅ Population data loaded")
            else:
                print("⚠️  Population data missing or zero")
                results['issues'].append("Population data not properly loaded")
                
            if data.get('nutrition_indicators', {}):
                print("✅ Nutrition indicators loaded")
            else:
                print("⚠️  Nutrition indicators missing")
                results['issues'].append("Nutrition indicators not loaded")
                
        else:
            results['issues'].append(f"Missing data sections: {missing_keys}")
            print(f"❌ Missing data sections: {missing_keys}")
            
    except Exception as e:
        results['issues'].append(f"Data collection failed: {str(e)}")
        print(f"❌ Data collection failed: {str(e)}")
    
    # Test 5: Dashboard Integration
    print("\n5. Testing dashboard integration...")
    try:
        # Test the convenience function
        from report_generator import generate_report_from_dashboard
        
        pdf = generate_report_from_dashboard('executive', test_params)
        if isinstance(pdf, BytesIO) and len(pdf.getvalue()) > 1000:
            results['dashboard_integration'] = True
            print("✅ Dashboard integration function works")
        else:
            results['issues'].append("Dashboard integration returns invalid PDF")
            print("⚠️  Dashboard integration returns minimal content")
            
    except Exception as e:
        results['issues'].append(f"Dashboard integration failed: {str(e)}")
        print(f"❌ Dashboard integration failed: {str(e)}")
    
    # Test 6: Check for missing features
    print("\n6. Analyzing missing features...")
    missing_features = []
    
    # Check for chart integration
    if not hasattr(generator, 'embed_chart') and not hasattr(generator, '_embed_plotly_chart'):
        missing_features.append("Chart/visualization embedding")
    
    # Check for multi-language support
    if 'language' not in test_params or not hasattr(generator, 'translate'):
        missing_features.append("Multi-language support")
    
    # Check for custom branding
    if not hasattr(generator, 'add_logo') and not hasattr(generator, 'custom_branding'):
        missing_features.append("Custom branding/logo support")
    
    # Check for data validation
    if not hasattr(generator, 'validate_data'):
        missing_features.append("Data validation before report generation")
    
    # Check for export to other formats
    if not hasattr(generator, 'export_to_excel') and not hasattr(generator, 'export_to_word'):
        missing_features.append("Export to Excel/Word formats")
    
    # Check for email integration
    if not hasattr(generator, 'send_email') and not hasattr(generator, 'email_report'):
        missing_features.append("Email delivery integration")
    
    # Check for scheduling
    if not hasattr(generator, 'schedule_report'):
        missing_features.append("Scheduled report generation")
    
    # Check for templates customization
    if not hasattr(generator, 'custom_templates'):
        missing_features.append("Custom report templates")
    
    # Check for real-time data updates
    if not hasattr(generator, 'real_time_update'):
        missing_features.append("Real-time data updates")
    
    # Check for comparison reports
    if 'comparison' not in generator.templates:
        missing_features.append("Period-to-period comparison reports")
    
    if missing_features:
        results['issues'].extend([f"Missing feature: {f}" for f in missing_features])
        for feature in missing_features:
            print(f"   ⚠️  Missing: {feature}")
    else:
        print("   ✅ All expected features present")
    
    return results

def generate_validation_report(results):
    """Generate a comprehensive validation report"""
    print("\n" + "=" * 80)
    print("VALIDATION REPORT SUMMARY")
    print("=" * 80)
    
    # Overall status
    total_tests = 6
    passed_tests = sum([
        results['module_import'],
        results['data_providers'],
        len([r for r in results['report_types'].values() if r.get('status') == 'success']) >= 5,
        results['data_collection'],
        results['pdf_generation'] if 'pdf_generation' in results else False,
        results['dashboard_integration']
    ])
    
    print(f"\nOverall Status: {passed_tests}/{total_tests} tests passed")
    
    # Report generation status
    print("\nReport Generation Status:")
    for report_type, status in results['report_types'].items():
        status_icon = "✅" if status.get('status') == 'success' else "⚠️" if status.get('status') == 'minimal' else "❌"
        print(f"  {status_icon} {report_type.capitalize()}: {status.get('status', 'unknown')}")
    
    # Issues found
    if results['issues']:
        print("\nIssues Identified:")
        for i, issue in enumerate(results['issues'], 1):
            print(f"  {i}. {issue}")
    else:
        print("\n✅ No critical issues found!")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS FOR ENHANCEMENT")
    print("=" * 80)
    
    recommendations = []
    
    if not results['data_providers']:
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Data Integration',
            'recommendation': 'Ensure real_data_provider.py is properly configured with actual Uganda data sources'
        })
    
    if any(r.get('status') == 'minimal' for r in results['report_types'].values()):
        recommendations.append({
            'priority': 'MEDIUM',
            'area': 'Content Generation',
            'recommendation': 'Expand report sections with more detailed content and analysis'
        })
    
    if 'Chart/visualization embedding' in str(results['issues']):
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Visualizations',
            'recommendation': 'Implement chart embedding using plotly/matplotlib to image conversion'
        })
    
    if 'Multi-language support' in str(results['issues']):
        recommendations.append({
            'priority': 'MEDIUM',
            'area': 'Localization',
            'recommendation': 'Add translation support for local languages (Luganda, Swahili, etc.)'
        })
    
    if 'Export to Excel/Word' in str(results['issues']):
        recommendations.append({
            'priority': 'LOW',
            'area': 'Export Formats',
            'recommendation': 'Implement converters for Excel/Word using openpyxl/python-docx'
        })
    
    if 'Email delivery' in str(results['issues']):
        recommendations.append({
            'priority': 'MEDIUM',
            'area': 'Distribution',
            'recommendation': 'Add email integration for automatic report distribution'
        })
    
    if 'Real-time data updates' in str(results['issues']):
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Data Freshness',
            'recommendation': 'Implement real-time data fetching from APIs/databases'
        })
    
    if 'comparison reports' in str(results['issues']):
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Analytics',
            'recommendation': 'Add period-over-period comparison functionality'
        })
    
    # Always recommend these
    recommendations.extend([
        {
            'priority': 'HIGH',
            'area': 'Data Validation',
            'recommendation': 'Add comprehensive data validation before report generation'
        },
        {
            'priority': 'MEDIUM',
            'area': 'Error Handling',
            'recommendation': 'Implement robust error handling with user-friendly messages'
        },
        {
            'priority': 'LOW',
            'area': 'Performance',
            'recommendation': 'Add caching for frequently generated reports'
        }
    ])
    
    # Sort by priority
    priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    recommendations.sort(key=lambda x: priority_order[x['priority']])
    
    for rec in recommendations:
        print(f"\n[{rec['priority']}] {rec['area']}:")
        print(f"  → {rec['recommendation']}")
    
    return recommendations

if __name__ == "__main__":
    print("Starting comprehensive report generation validation...\n")
    
    try:
        # Run tests
        results = test_report_generator()
        
        # Generate report
        recommendations = generate_validation_report(results)
        
        # Save results to file
        with open('REPORT_GENERATION_VALIDATION.md', 'w') as f:
            f.write("# Report Generation Validation Results\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Test Results\n\n")
            f.write(f"- Module Import: {'✅ Passed' if results['module_import'] else '❌ Failed'}\n")
            f.write(f"- Data Providers: {'✅ Initialized' if results['data_providers'] else '⚠️ Using Fallback'}\n")
            f.write(f"- Data Collection: {'✅ Complete' if results['data_collection'] else '❌ Incomplete'}\n")
            f.write(f"- Dashboard Integration: {'✅ Working' if results['dashboard_integration'] else '❌ Not Working'}\n\n")
            
            f.write("## Report Types Status\n\n")
            for report_type, status in results['report_types'].items():
                f.write(f"- **{report_type.capitalize()}**: {status.get('status', 'unknown')}")
                if status.get('size'):
                    f.write(f" ({status['size']:,} bytes)")
                f.write("\n")
            
            if results['issues']:
                f.write("\n## Issues Found\n\n")
                for issue in results['issues']:
                    f.write(f"- {issue}\n")
            
            f.write("\n## Recommendations\n\n")
            for rec in recommendations:
                f.write(f"### [{rec['priority']}] {rec['area']}\n")
                f.write(f"{rec['recommendation']}\n\n")
        
        print("\n" + "=" * 80)
        print("✅ Validation complete! Results saved to REPORT_GENERATION_VALIDATION.md")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Critical error during validation: {str(e)}")
        traceback.print_exc()
        sys.exit(1)