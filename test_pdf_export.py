#!/usr/bin/env python3
"""
Test script to verify PDF export functionality with ReportLab.
"""
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import logging
from exports.export_utils import REPORTLAB_AVAILABLE, export_comparison_pdf, export_comparison_csv

# Configure logging to see the startup messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_reportlab_detection():
    """Test that ReportLab is properly detected."""
    print("=" * 60)
    print("TEST 1: ReportLab Detection")
    print("=" * 60)
    print(f"REPORTLAB_AVAILABLE: {REPORTLAB_AVAILABLE}")
    
    if REPORTLAB_AVAILABLE:
        print("✅ PASS: ReportLab is detected and available")
    else:
        print("❌ FAIL: ReportLab is not available")
        return False
    
    return True

def test_csv_export():
    """Test that CSV export works (should always work)."""
    print("\n" + "=" * 60)
    print("TEST 2: CSV Export (Always Available)")
    print("=" * 60)
    
    try:
        import pandas as pd
        
        # Create sample data
        sample_df = pd.DataFrame({
            'player_name': ['Player 1', 'Player 2'],
            'sporta_score': [85.5, 78.2],
            'goals': [25, 18],
            'shots': [45, 38],
            'total_xg': [22.5, 16.8],
            'assists': [10, 8],
            'passes': [1200, 1150],
            'dribbles': [85, 72],
            'carries': [450, 420],
            'recoveries': [180, 165],
            'pressures': [220, 195],
            'tackles': [45, 52],
            'interceptions': [38, 41]
        })
        
        csv_data = export_comparison_csv(sample_df)
        
        if csv_data and len(csv_data) > 0:
            print(f"✅ PASS: CSV export generated {len(csv_data)} bytes")
            print(f"   First 100 chars: {csv_data[:100].decode('utf-8')}")
            return True
        else:
            print("❌ FAIL: CSV export returned empty data")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: CSV export failed with error: {e}")
        return False

def test_pdf_export():
    """Test that PDF export works when ReportLab is available."""
    print("\n" + "=" * 60)
    print("TEST 3: PDF Export (Requires ReportLab)")
    print("=" * 60)
    
    if not REPORTLAB_AVAILABLE:
        print("⚠️  SKIP: ReportLab not available, PDF export test skipped")
        return True  # Not a failure, just unavailable
    
    try:
        import pandas as pd
        
        # Create sample player profiles
        player1_profile = {
            'player_name': 'Lionel Messi',
            'nickname': 'La Pulga',
            'jersey_number': '10',
            'sporta_score': 95.5,
            'team': 'Inter Miami',
            'nationality': 'Argentina',
            'position': 'Forward',
            'age': 36,
            'height': '170 cm',
            'preferred_foot': 'Left',
            'matches_played': 800,
            'goals': 850,
            'total_xg': 78.5,
            'passes': 15000,
            'dribbles': 450,
            'recoveries': 1200,
            'pressures': 1800
        }
        
        player2_profile = {
            'player_name': 'Cristiano Ronaldo',
            'nickname': 'CR7',
            'jersey_number': '7',
            'sporta_score': 93.2,
            'team': 'Al-Nassr',
            'nationality': 'Portugal',
            'position': 'Forward',
            'age': 39,
            'height': '187 cm',
            'preferred_foot': 'Right',
            'matches_played': 900,
            'goals': 890,
            'total_xg': 95.2,
            'passes': 12000,
            'dribbles': 320,
            'recoveries': 950,
            'pressures': 1500
        }
        
        # Create sample stats as Series
        player1_stats = pd.Series({
            'sporta_score': 95.5,
            'goals': 850,
            'shots': 1200,
            'total_xg': 78.5,
            'assists': 320,
            'passes': 15000,
            'dribbles': 450,
            'carries': 8500,
            'recoveries': 1200,
            'pressures': 1800,
            'tackles': 180,
            'interceptions': 150
        })
        
        player2_stats = pd.Series({
            'sporta_score': 93.2,
            'goals': 890,
            'shots': 1400,
            'total_xg': 95.2,
            'assists': 250,
            'passes': 12000,
            'dribbles': 320,
            'carries': 7200,
            'recoveries': 950,
            'pressures': 1500,
            'tackles': 220,
            'interceptions': 180
        })
        
        # Generate PDF
        pdf_data = export_comparison_pdf(player1_profile, player2_profile, 
                                        player1_stats, player2_stats)
        
        if pdf_data and len(pdf_data) > 0:
            print(f"✅ PASS: PDF export generated {len(pdf_data)} bytes")
            
            # Save to file for verification
            output_file = PROJECT_ROOT / "test_output.pdf"
            with open(output_file, 'wb') as f:
                f.write(pdf_data)
            print(f"   PDF saved to: {output_file}")
            
            # Verify it's a valid PDF
            if pdf_data[:4] == b'%PDF':
                print("   ✅ Valid PDF header detected")
                return True
            else:
                print("   ❌ Invalid PDF header")
                return False
        else:
            print("❌ FAIL: PDF export returned None or empty data")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: PDF export failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PDF EXPORT FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("ReportLab Detection", test_reportlab_detection()))
    results.append(("CSV Export", test_csv_export()))
    results.append(("PDF Export", test_pdf_export()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! PDF export is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())