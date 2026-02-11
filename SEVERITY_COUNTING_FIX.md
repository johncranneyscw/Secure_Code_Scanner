# Severity-Based Counting Fix

## Problem Statement
The original code was counting CWEs by **calculated risk score ranges** (0-100 scale), 
not by the **actual severity reported by security scanners**.

### What Was Wrong
```python
# OLD - WRONG: Counted by risk score
'critical_cwes': len([c for c in sorted_cwes if c[1]['risk_score'] >= 80]),
'high_cwes': len([c for c in sorted_cwes if 60 <= c[1]['risk_score'] < 80]),
'medium_cwes': len([c for c in sorted_cwes if 40 <= c[1]['risk_score'] < 60])
```

This would show 0 Critical CWEs even if you had findings with CRITICAL/HIGH severity,
because the risk score calculation might not reach 80.

## Solution Applied

### New Approach: Count by Actual Severity from JSON

```python
# NEW - CORRECT: Count by actual scanner severity
severity_counts = {
    'critical': set(),
    'high': set(),
    'medium': set(),
    'low': set()
}

for cwe_id, cwe_data in scored_cwes.items():
    severities = [s.upper() for s in cwe_data.get('severities', [])]
    
    # Semgrep mapping: ERROR=HIGH, WARNING=MEDIUM, INFO=LOW
    if 'CRITICAL' in severities:
        severity_counts['critical'].add(cwe_id)
    elif any(s in ['HIGH', 'ERROR'] for s in severities):
        severity_counts['high'].add(cwe_id)
    elif any(s in ['MEDIUM', 'WARNING'] for s in severities):
        severity_counts['medium'].add(cwe_id)
    elif any(s in ['LOW', 'INFO'] for s in severities):
        severity_counts['low'].add(cwe_id)

return {
    'metrics': {
        'critical_cwes': len(severity_counts['critical']),
        'high_cwes': len(severity_counts['high']),
        'medium_cwes': len(severity_counts['medium']),
        'low_cwes': len(severity_counts['low'])
    }
}
```

## Severity Mappings

### Semgrep
- `ERROR` → **HIGH** (counted as High CWE)
- `WARNING` → **MEDIUM** (counted as Medium CWE)
- `INFO` → **LOW** (counted as Low CWE)

### Bearer / Bandit
- `CRITICAL` → **CRITICAL** (counted as Critical CWE)
- `HIGH` → **HIGH** (counted as High CWE)
- `MEDIUM` → **MEDIUM** (counted as Medium CWE)
- `LOW` → **LOW** (counted as Low CWE)

## What Changed in the UI

### Before (WRONG)
```
Critical CWEs (≥80)    0
High CWEs (60-79)      0
Medium CWEs (40-59)    3
```
*Based on calculated risk score ranges*

### After (CORRECT)
```
Critical CWEs          2    (Severity: CRITICAL)
High CWEs             15    (Severity: HIGH/ERROR)
Medium CWEs            8    (Severity: MEDIUM/WARNING)
Low CWEs               3    (Severity: LOW/INFO)
```
*Based on actual scanner severity from JSON*

## Key Benefits

1. **Accurate Representation**: Shows what scanners actually found
2. **Scanner Alignment**: Matches Semgrep's ERROR/WARNING/INFO terminology
3. **Consistent Interpretation**: Severity = what scanner says, not calculated metric
4. **Added Low Category**: Now tracks low-severity findings too

## Files Modified

1. **app.py** - `calculate_model_score()` function
   - Changed metrics counting logic
   - Now reads `severities` field from scored CWE data
   - Maps scanner-specific severities to standard categories

2. **analysis_results.html** - Metrics display section
   - Updated labels to show "By Actual Severity from Scanners"
   - Added descriptions: "(Severity: HIGH/ERROR)" etc.
   - Added Low CWEs card (was missing before)
   - Moved vulnerability density to full-width card below

## Important Notes

- **Risk Score** (0-100) is still calculated and used for overall model score
- **Severity** from scanners is now used for the metric counts
- These are two different things:
  - Risk Score = calculated metric (V × I × L × Vol × C × 100)
  - Severity = what the scanner reported (CRITICAL, HIGH, ERROR, WARNING, etc.)

The dashboard now correctly shows both!
