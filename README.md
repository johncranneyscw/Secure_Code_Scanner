# Multi-Run Security Scanner with Language-Wise CWE Analysis

## 🚀 New Features Added

### Dual Mode Operation

The application now supports **two distinct modes**:

#### 1. **Scan Mode** (Original Functionality)
- Upload multiple ZIP files containing code projects
- Run security scanners (Semgrep, Bearer, Bandit, Trivy, OSV-Scanner)
- View and analyze scan results
- Export to various formats (DOCX, Excel, JSON)

#### 2. **Analysis Mode** (NEW)
- Upload existing results JSON files
- Perform comprehensive language-wise CWE analysis
- Track file impact and verdict distribution
- Generate detailed reports

---

## 📊 Analysis Mode Features

### Language-Wise CWE Grouping

The analysis automatically groups CWEs by programming language based on file extensions:

**Supported Languages:**
- C/C++
- Java
- JavaScript/TypeScript
- Python
- Ruby
- Go
- Rust
- PHP
- C#
- Swift
- Kotlin
- Scala
- Shell
- SQL
- YAML/JSON/XML
- HTML/CSS

### File Impact Analysis

For each CWE, the system tracks:
- **Total files affected** across all runs
- **Files per run** breakdown
- **Unique file list** showing all affected files
- **File count statistics** (average, min, max per run)

### Verdict Tracking

Comprehensive verdict analysis showing:
- ✅ **True Positives**: Actual security issues
- ❌ **False Positives**: Incorrectly flagged issues
- **Verdict distribution** per CWE, language, and globally

### Cross-Run Comparison

- Shows which runs each CWE appeared in
- Identifies consistent vs sporadic vulnerabilities
- Tracks CWE persistence across multiple code generations

### Tool Correlation

- Lists which security tools detected each CWE
- Shows tool agreement/disagreement
- Helps identify tool strengths and limitations

---

## 🎯 How to Use

### Starting the Application

```bash
python app.py
```

The server starts on `http://localhost:8080`

### Scan Mode Usage

1. Click **"Scan Mode (Upload ZIPs)"** button
2. Select multiple ZIP files (e.g., 10 code generations from same prompt)
3. Choose whether to clear previous runs
4. Click **"Run Security Scans"**
5. Monitor progress in real-time
6. View results when complete

### Analysis Mode Usage

1. Click **"Analysis Mode (Upload JSON)"** button
2. Upload a consolidated results JSON file (format must match the structure shown below)
3. Click **"Upload & Analyze JSON"**
4. View comprehensive analysis results

---

## 📁 Expected JSON Format

The JSON file should have this structure:

```json
{
  "total_runs": 10,
  "generated_at": "2026-01-13 10:58:02",
  "project": "gpt-5-mini_c-basic",
  "runs": [
    {
      "run_number": 1,
      "scan_timestamp": "N/A",
      "results": {
        "sast": {
          "semgrep": [
            {
              "scanner": "semgrep",
              "type": "SAST",
              "rule_id": "...",
              "cwe": "CWE-676",
              "severity": "WARNING",
              "file": "path/to/file.c",
              "line": 169,
              "message": "...",
              "stableId": "...",
              "verdict": "true_positive"
            }
          ],
          "bearer": [...],
          "bandit": [...]
        },
        "dep": {
          "trivy": [],
          "osv-scanner": []
        }
      }
    }
  ]
}
```

**Required Fields:**
- `runs` array containing run data
- Each run has `results.sast` with tool findings
- Each finding must have: `cwe`, `file`, `verdict`, `severity`, `scanner`

---

## 📈 Analysis Results Page

### Overview Tab

Shows global statistics:
- Total runs analyzed
- Total languages detected
- Total unique CWEs found
- Total findings (TP + FP breakdown)
- CWE distribution across all languages

### Language-Specific Tabs

Each language gets its own tab showing:

**Statistics Card:**
- Total CWEs for this language
- Total files affected
- True/False positive counts

**Detailed Table:**
- CWE ID and name
- Number of files affected
- Verdict breakdown (TP/FP)
- Severity levels
- Tools that detected it
- Runs where it appeared

**Expandable Details:**
- Full list of affected files
- File count per run
- Example findings with file locations
- Scanner messages

---

## 📥 Export Options

### From Scan Mode:
- **DOCX Report**: Individual run reports
- **Excel Checkmark Comparison**: CWE presence across runs
- **Excel Detailed Counts**: File counts per CWE per run
- **Consolidated JSON**: All runs in single JSON file
- **CWE Analysis JSON**: Comprehensive CWE statistics

### From Analysis Mode:
- **Language Analysis JSON**: Complete language-wise analysis
- **Language Analysis Excel**: Multi-sheet Excel with overview and per-language tabs

---

## 🔍 Example Use Cases

### Research Scenario
You've generated 10 code samples from the same AI prompt and want to analyze:

**Scan Mode Flow:**
1. Upload all 10 ZIP files
2. Wait for scanning to complete
3. Download consolidated JSON
4. Switch to Analysis Mode
5. Upload the JSON for detailed CWE analysis

**Direct Analysis Flow:**
1. Already have results JSON from previous scans
2. Go to Analysis Mode
3. Upload JSON
4. Immediately see language-wise breakdown

### Questions the Analysis Answers

1. **"Which CWEs affect C code vs JavaScript code?"**
   - Navigate to language-specific tabs

2. **"How many files does CWE-787 affect across all runs?"**
   - Check overview or language tab, expand "View Files"

3. **"What's the true positive rate for CWE-732?"**
   - View verdict counts in the detailed table

4. **"Which CWEs appear consistently across runs vs only once?"**
   - Look at "Runs Found" column

5. **"Which security tools are most effective?"**
   - Check "Tools" column to see detection correlation

---

## 🛠️ Technical Details

### File Extension to Language Mapping

The `get_language_from_file()` function maps extensions:
```python
'.c' → 'c'
'.cpp', '.cc', '.cxx' → 'cpp'
'.js', '.jsx' → 'javascript'
'.py' → 'python'
# ... and more
```

### Analysis Algorithm

1. **Parse JSON**: Load and validate structure
2. **Iterate Runs**: Process each run's findings
3. **Group by Language**: Use file extension to categorize
4. **Track Files**: Build sets of affected files per CWE
5. **Count Verdicts**: Separate TP from FP
6. **Aggregate**: Calculate totals and statistics
7. **Sort**: Order by impact (files affected)

### Performance Considerations

- Uses sets for efficient unique file tracking
- Processes findings in single pass
- Converts to lists only for serialization
- Limits examples to 5 per CWE to keep JSON size reasonable

---

## 📊 Understanding the Statistics

### Per-Language Statistics

- **Total CWEs**: Unique CWE IDs found in this language
- **Total Files**: Unique files affected in this language
- **True Positives**: Actual vulnerabilities confirmed
- **False Positives**: Incorrectly flagged issues

### Per-CWE Statistics

- **Total Files Affected**: Unique files across ALL runs
- **File Counts Per Run**: How many files in each individual run
- **Average Files Per Run**: Mean file count
- **Max/Min Files**: Range across runs

---

## 🎨 UI Features

### Modern Dark Theme
- Gradient backgrounds
- Glass-morphism cards
- Responsive design
- Bootstrap 5 components

### Interactive Elements
- Tabbed navigation per language
- Collapsible file lists
- Expandable detail views
- Color-coded severity badges
- Real-time progress tracking (Scan Mode)

### Accessibility
- High contrast text
- Clear visual hierarchy
- Responsive on mobile devices
- Keyboard navigation support

---

## 📋 Dependencies

Make sure you have these installed:

```bash
pip install flask werkzeug python-docx openpyxl
```

For scanning functionality, also need:
```bash
# Install security scanners
semgrep
bearer
bandit
trivy
osv-scanner
```

---

## 🔧 Configuration

Edit these constants in `app.py`:

```python
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
REPORT_DIR = BASE_DIR / "reports"
```

---

## 🐛 Troubleshooting

### "No analysis data available"
- Make sure you uploaded a JSON file in Analysis Mode first
- Check that JSON structure matches expected format

### "Invalid JSON structure"
- Verify JSON has `"runs"` array at top level
- Each run must have `"results"` → `"sast"` structure

### Language shows as "unknown"
- File extension not in mapping
- Add new extension to `get_language_from_file()` function

### Missing files in analysis
- Check that file paths are present in JSON
- Verify files have valid extensions

---

## 📝 Notes

- Analysis is performed in-memory (no database)
- Data persists until server restart or new upload
- Large JSON files (>100MB) may take longer to process
- Excel exports limited to 31 characters for sheet names
- File lists truncated to first 20 in UI (full list in exports)

---

## 🎯 Future Enhancements

Potential additions:
- Database persistence
- Multi-project comparison
- Time-series analysis
- Custom CWE filtering
- Severity weighting
- Risk scoring
- PDF reports
- Chart visualizations

---

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Verify JSON format matches expected structure
3. Ensure all dependencies are installed
4. Check file permissions for uploads/reports directories

---

## 📜 License

This tool is for research and security analysis purposes.

---

**Version**: 2.0  
**Last Updated**: January 2026  
**Author**: Enhanced Security Scanner with Language Analysis
