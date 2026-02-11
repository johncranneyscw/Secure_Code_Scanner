# Critical File Counting Fix

## The Problem

**CRITICAL BUG**: Files were being counted multiple times when the same file appeared across different runs with run-specific path prefixes.

### Example of the Bug

Suppose you have CWE-89 (SQL Injection) in `main.py` found across 3 runs:

**JSON contains:**
```json
{
  "true_positive_files": [
    "run_1/src/main.py",
    "run_2/src/main.py", 
    "run_3/src/main.py"
  ]
}
```

**OLD CODE (WRONG):**
- Counted as: **3 unique files**
- Volume (Vol) = log₁₀(3 + 1) = 0.60
- **WRONG!** This is the SAME file, not 3 different files

**NEW CODE (CORRECT):**
- Normalized to: `["src/main.py", "src/main.py", "src/main.py"]`
- After deduplication: `["src/main.py"]`
- Counted as: **1 unique file**
- Volume (Vol) = log₁₀(1 + 1) = 0.30
- **CORRECT!** This properly reflects that only 1 file is affected

## Impact on Risk Scoring

The Volume (Vol) factor is used in risk score calculation:
```
Risk Score = V × I × L × Vol × C × 100
```

### Example Impact

For CWE-89 found in the same file across 10 runs:

**Before Fix (WRONG):**
- Files counted: 10 (run_1/main.py, run_2/main.py, ..., run_10/main.py)
- Vol = log₁₀(10 + 1) = **1.04**
- Risk Score = 1 × 0.8 × 1.0 × 1.04 × 1.0 × 100 = **83.2** (CRITICAL!)

**After Fix (CORRECT):**
- Files counted: 1 (main.py)
- Vol = log₁₀(1 + 1) = **0.30**
- Risk Score = 1 × 0.8 × 1.0 × 0.30 × 1.0 × 100 = **24.0** (LOW)

**The difference: 83.2 vs 24.0** - completely different risk category!

## The Solution

### New Function: `normalize_file_path()`

```python
def normalize_file_path(file_path, run_number=None):
    """
    Normalize file paths to remove run-specific prefixes.
    
    Removes patterns like:
    - run_1/, run-1/, run1/
    - /tmp/extract_123/run_2/
    - extract_456/
    - /tmp/tempdir123/
    """
    import re
    
    # Remove run-specific prefixes
    patterns = [
        r'^run[_-]?\d+/',           # run_1/, run-1/, run1/
        r'.*/run[_-]?\d+/',         # /path/to/run_1/
        r'^extract[_-]?\d+/',       # extract_123/
        r'.*/extract[_-]?\d+/',     # /tmp/extract_123/
    ]
    
    normalized = file_path
    for pattern in patterns:
        normalized = re.sub(pattern, '', normalized)
    
    # Remove temp directories
    normalized = re.sub(r'^/tmp/[^/]+/', '', normalized)
    normalized = re.sub(r'^temp[_-]?\d*/', '', normalized)
    
    return normalized
```

### Applied During JSON Analysis

```python
# In analyze_json_by_language()
raw_file_path = finding.get("file", "")

# CRITICAL FIX: Normalize before counting
file_path = normalize_file_path(raw_file_path, run_number)

# Now file_path is used for ALL subsequent operations:
# - Language detection
# - Unique file counting
# - CWE file tracking
# - Statistics
```

## Test Cases

### Test 1: Run Prefixes
```python
Input:  "run_1/src/main.py"
Output: "src/main.py"

Input:  "run-2/utils/helper.py"
Output: "utils/helper.py"

Input:  "run10/app.py"
Output: "app.py"
```

### Test 2: Extract Directories
```python
Input:  "extract_456/project/src/api.py"
Output: "project/src/api.py"

Input:  "/tmp/extract_123/run_2/code.py"
Output: "code.py"
```

### Test 3: Temp Directories
```python
Input:  "/tmp/tmpABC123/src/main.py"
Output: "src/main.py"

Input:  "temp_1/utils.py"
Output: "utils.py"
```

### Test 4: Already Normalized
```python
Input:  "src/main.py"
Output: "src/main.py"  (unchanged)

Input:  "package/module.py"
Output: "package/module.py"  (unchanged)
```

## Verification

After applying the fix, you should see:

1. **Lower file counts** for CWEs found in the same files across runs
2. **More accurate risk scores** that reflect actual code spread
3. **Correct Vol values** based on unique file count, not run count

### Before vs After Example

**Before Fix:**
```
CWE-89: SQL Injection
- Files: 30 (counted main.py 10 times, api.py 10 times, db.py 10 times)
- Vol: log₁₀(31) = 1.49
- Risk Score: 95.2 (CRITICAL!)
```

**After Fix:**
```
CWE-89: SQL Injection  
- Files: 3 (main.py, api.py, db.py - each counted once)
- Vol: log₁₀(4) = 0.60
- Risk Score: 38.4 (MEDIUM)
```

## Important Notes

1. **Likelihood (L)** still correctly reflects run frequency (runs_with_TP / total_runs)
2. **Volume (Vol)** now correctly reflects unique file spread (not inflated by run count)
3. **Risk scores** are now accurate and comparable across different CWEs
4. **This fix does NOT change the JSON file** - it only affects how files are counted

## Files Modified

- `app.py`:
  - Added `normalize_file_path()` function
  - Applied normalization in `analyze_json_by_language()` at line ~520
  - All file counting now uses normalized paths

This is a **CRITICAL FIX** for accurate risk scoring!
