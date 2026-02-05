# 🚀 Quick Start Guide

## Installation

1. **Install Python Dependencies**
```bash
pip install flask werkzeug python-docx openpyxl
```

2. **Directory Structure**
```
your-project/
├── app.py
├── scanners.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── progress.html
│   ├── results.html
│   └── analysis_results.html
└── static/
    └── style.css
```

3. **Start the Server**
```bash
python app.py
```

4. **Open Browser**
Navigate to: `http://localhost:8080`

---

## Quick Usage - Analysis Mode (NEW!)

### Step 1: Upload Your JSON
1. Click **"Analysis Mode (Upload JSON)"** button on home page
2. Click **"Choose File"** and select your consolidated JSON file
3. Click **"Upload & Analyze JSON"**

### Step 2: View Results
You'll see:
- **Overview Tab**: All CWEs across all languages
- **Language Tabs**: C, JavaScript, Python, etc. - click to see language-specific CWEs

### Step 3: Explore the Data

#### View File Impact
- Look at "Files Affected" column
- Click **"View Files"** button to see complete list of affected files

#### Check Verdicts
- Green badge = True Positives (real issues)
- Red badge = False Positives (false alarms)

#### See Details
- Click **"Show"** button to see:
  - File count per run
  - Example findings with line numbers
  - Scanner messages

### Step 4: Export Reports
- **📥 Download Full Analysis JSON**: Complete data in JSON format
- **📊 Download Excel Report**: Multi-sheet Excel with all details

---

## Quick Usage - Scan Mode (Original)

### Step 1: Upload ZIPs
1. Stay on **"Scan Mode"** (default)
2. Click **"Choose Files"** and select multiple .zip files
3. Check/uncheck "Clear previous runs" option
4. Click **"Run Security Scans"**

### Step 2: Monitor Progress
- Watch real-time progress bar
- See which file is currently being scanned
- View log messages

### Step 3: View Results
- Click **"View Results"** when complete
- Navigate between runs using buttons
- See SAST and dependency findings

### Step 4: Export Data
- Download DOCX reports
- Download Excel comparisons
- Download consolidated JSON
- **Switch to Analysis Mode** and upload the JSON for language analysis!

---

## 🎯 Example Workflow

### Scenario: Analyzing 10 AI-Generated Code Samples

1. **Generate Data** (if needed)
   - Upload 10 ZIPs in Scan Mode
   - Wait for scanning to complete
   - Download "📦 Download All Runs JSON"

2. **Analyze by Language**
   - Switch to Analysis Mode
   - Upload the JSON file
   - View results

3. **Answer Questions**
   - "Which CWEs affect C code?" → Click **C** tab
   - "How many files have CWE-787?" → Look at "Files Affected" column
   - "What's the false positive rate?" → Compare TP vs FP badges
   - "Which runs have this CWE?" → Check "Runs" column

4. **Export for Report**
   - Download Excel for tables
   - Download JSON for further processing

---

## 📊 Understanding the Results

### Overview Tab
Shows **global statistics** across all languages:
- Total unique CWEs found
- Which languages each CWE affects
- File count across all runs

### Language Tabs
Shows **language-specific** data:
- CWEs only found in this language
- Files written in this language
- Language-specific statistics

### Metrics Explained

| Metric | Meaning |
|--------|---------|
| **Files Affected** | Total unique files with this CWE |
| **TP** (True Positive) | Confirmed vulnerabilities |
| **FP** (False Positive) | Incorrectly flagged issues |
| **Severities** | ERROR, WARNING, HIGH, MEDIUM, LOW, INFO |
| **Tools** | Which scanners detected it |
| **Runs** | Which runs (1-10) had this CWE |

---

## 🔍 Example Queries

### "Show me all C security issues"
1. Click **C** tab
2. See all CWEs in C code
3. Sorted by files affected (most impactful first)

### "How widespread is CWE-787?"
1. Go to Overview tab OR any language tab
2. Find CWE-787 row
3. Look at "Files Affected" and "Runs Found"

### "What are the false alarm rates?"
1. Compare green (TP) vs red (FP) badges
2. Higher FP = tool may need tuning
3. Export Excel for detailed analysis

### "Which files have buffer overflows?"
1. Find CWE-787 (Out-of-bounds Write) or CWE-125 (Out-of-bounds Read)
2. Click **"View Files"** button
3. See complete list of affected files

---

## ⚡ Pro Tips

### 🎨 Better Visualizations
- Use the Excel export for pivot tables
- JSON export for custom scripts/charts
- Language tabs to focus analysis

### 🔄 Workflow Optimization
- Keep scan results, re-analyze anytime
- Compare different JSON files by switching uploads
- Export multiple formats for different audiences

### 📈 Statistical Analysis
- Track TP/FP ratios by language
- Compare CWE consistency across runs
- Identify tool agreement patterns

### 🐛 Debugging Issues
- Check browser console for errors
- Verify JSON structure matches expected format
- Look for file extension mismatches

---

## 🆘 Common Issues

### "No analysis data available"
**Solution**: Upload a JSON file first in Analysis Mode

### "Invalid JSON structure"
**Solution**: Check that JSON has `"runs"` array with proper structure

### Language shows as "unknown"
**Solution**: File extension not recognized - check `get_language_from_file()` mapping

### Can't see all files
**Solution**: UI shows first 20, full list in Excel/JSON exports

---

## 📞 Need Help?

1. Check the **README.md** for detailed documentation
2. Review the example JSON structure
3. Verify all dependencies are installed
4. Check console output for error messages

---

**Happy Analyzing! 🎉**
