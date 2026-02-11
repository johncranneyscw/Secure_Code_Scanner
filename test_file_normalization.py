#!/usr/bin/env python3
"""
Test file path normalization to ensure files are counted correctly
"""

import re

def normalize_file_path(file_path, run_number=None):
    """
    Normalize file paths to remove run-specific prefixes for accurate unique file counting.
    """
    import re
    
    if not file_path:
        return file_path
    
    # Remove common run-specific prefixes
    patterns = [
        r'^run[_-]?\d+/',  # run_1/, run-1/, run1/
        r'.*/run[_-]?\d+/',  # /path/to/run_1/
        r'^extract[_-]?\d+/',  # extract_123/
        r'.*/extract[_-]?\d+/',  # /tmp/extract_123/
    ]
    
    normalized = file_path
    for pattern in patterns:
        normalized = re.sub(pattern, '', normalized)
    
    # Also remove leading temp directories
    normalized = re.sub(r'^/tmp/[^/]+/', '', normalized)
    normalized = re.sub(r'^temp[_-]?\d*/', '', normalized)
    
    return normalized


def run_tests():
    """Run test cases"""
    test_cases = [
        # Run prefixes
        ("run_1/src/main.py", "src/main.py"),
        ("run-2/utils/helper.py", "utils/helper.py"),
        ("run10/app.py", "app.py"),
        
        # Extract directories
        ("extract_456/project/src/api.py", "project/src/api.py"),
        ("/tmp/extract_123/run_2/code.py", "code.py"),
        
        # Temp directories
        ("/tmp/tmpABC123/src/main.py", "src/main.py"),
        ("temp_1/utils.py", "utils.py"),
        
        # Already normalized (should not change)
        ("src/main.py", "src/main.py"),
        ("package/module.py", "package/module.py"),
        
        # Complex nested paths
        ("/tmp/extract_999/run_5/project/src/controllers/api.py", "project/src/controllers/api.py"),
        
        # Edge cases
        ("", ""),
        ("main.py", "main.py"),
    ]
    
    print("Testing File Path Normalization\n" + "="*60)
    passed = 0
    failed = 0
    
    for input_path, expected in test_cases:
        result = normalize_file_path(input_path)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        print(f"{status}")
        print(f"  Input:    '{input_path}'")
        print(f"  Expected: '{expected}'")
        print(f"  Got:      '{result}'")
        print()
    
    print("="*60)
    print(f"Results: {passed} passed, {failed} failed")
    
    return failed == 0


def demonstrate_impact():
    """Demonstrate the impact on file counting and risk scores"""
    import math
    
    print("\n" + "="*60)
    print("Impact Demonstration: Same File Across 10 Runs")
    print("="*60 + "\n")
    
    # Same file in 10 runs - WITHOUT normalization
    files_without_norm = [
        "run_1/src/main.py",
        "run_2/src/main.py",
        "run_3/src/main.py",
        "run_4/src/main.py",
        "run_5/src/main.py",
        "run_6/src/main.py",
        "run_7/src/main.py",
        "run_8/src/main.py",
        "run_9/src/main.py",
        "run_10/src/main.py",
    ]
    
    # After normalization
    files_with_norm = [normalize_file_path(f) for f in files_without_norm]
    unique_files = list(set(files_with_norm))
    
    print("Without Normalization:")
    print(f"  File count: {len(files_without_norm)}")
    print(f"  Vol = log₁₀({len(files_without_norm)} + 1) = {math.log10(len(files_without_norm) + 1):.2f}")
    
    # Calculate risk score (example: V=1, I=0.8, L=1.0, C=1.0)
    vol_before = math.log10(len(files_without_norm) + 1)
    risk_before = 1 * 0.8 * 1.0 * vol_before * 1.0 * 100
    print(f"  Risk Score = 1 × 0.8 × 1.0 × {vol_before:.2f} × 1.0 × 100 = {risk_before:.1f}")
    
    print("\nWith Normalization:")
    print(f"  File count: {len(unique_files)}")
    print(f"  Unique files: {unique_files}")
    print(f"  Vol = log₁₀({len(unique_files)} + 1) = {math.log10(len(unique_files) + 1):.2f}")
    
    vol_after = math.log10(len(unique_files) + 1)
    risk_after = 1 * 0.8 * 1.0 * vol_after * 1.0 * 100
    print(f"  Risk Score = 1 × 0.8 × 1.0 × {vol_after:.2f} × 1.0 × 100 = {risk_after:.1f}")
    
    print(f"\n🎯 Difference: {risk_before:.1f} vs {risk_after:.1f}")
    print(f"   Impact: Risk score reduced by {risk_before - risk_after:.1f} points!")
    
    if risk_before >= 80:
        risk_level_before = "CRITICAL"
    elif risk_before >= 60:
        risk_level_before = "HIGH"
    elif risk_before >= 40:
        risk_level_before = "MEDIUM"
    else:
        risk_level_before = "LOW"
    
    if risk_after >= 80:
        risk_level_after = "CRITICAL"
    elif risk_after >= 60:
        risk_level_after = "HIGH"
    elif risk_after >= 40:
        risk_level_after = "MEDIUM"
    else:
        risk_level_after = "LOW"
    
    print(f"   Category changed: {risk_level_before} → {risk_level_after}")


if __name__ == "__main__":
    success = run_tests()
    demonstrate_impact()
    
    if success:
        print("\n✅ All tests passed! File normalization is working correctly.")
    else:
        print("\n❌ Some tests failed. Please review the implementation.")
