# Evaluare Națională 2024 - Scraper

This Python script automatically scrapes the **evaluation results** of 8th-grade students from the official Romanian Ministry of Education website:  
📎 https://evaluare.edu.ro

It collects **all candidate data** from **all counties (`județe`)**, page by page, and stores the results in `.csv` files.

---

## ✅ What It Does

- Loops through every **county ID (`Jud=1` to `Jud=52`)**
- Extracts all pages of results for each county
- Parses detailed candidate data including:
  - Candidate code
  - National ranking
  - School name
  - Exam grades: Romanian, Math, and optionally Mother Tongue
- Adds a `"Județul"` column with the full name of the county
- Saves each county's data as a CSV file under `/data`

---

## 📁 Output Structure

All `.csv` files are saved in a `/data` subfolder relative to the script.  
Each file is named:

```
data/evaluare_<jud_code>_<judet_name>.csv
```

Example:
```
data/evaluare_38_TIMIȘ.csv
data/evaluare_03_ARAD.csv
```

Each CSV file has the following columns:
```
Index, Codul candidatului, Poziția în ierarhia Evaluare Națională 2025,
Școala de proveniență,
Limba şi literatura română - Notă,
Limba şi literatura română - Contestație,
Limba şi literatura română - Notă finală,
Matematică - Notă,
Matematică - Contestație,
Matematică - Notă finală,
Limba şi literatura maternă - Denumire,
Limba şi literatura maternă - Notă,
Limba şi literatura maternă - Contestație,
Limba şi literatura maternă - Notă finală,
Media la evaluarea națională,
Județul
```

---

## 🚀 How to Use

### 1. ✅ Install Python packages

Make sure you have **Python 3.8+** installed.

Then install required libraries:

```
pip install selenium beautifulsoup4 pandas
```

### 2. ✅ Download ChromeDriver

You'll need **ChromeDriver** matching your installed Chrome version.

- Download from: https://googlechromelabs.github.io/chrome-for-testing/#stable
- Extract it, and make sure `chromedriver.exe` is on your system `PATH` or in the same folder as the script.

---

### 3. ▶️ Run the Script

```
python main.py
```

You'll see output like:

```
🔍 Scraping JUD_CODE=1
  🔄 Page 1 - https://evaluare.edu.ro/Evaluare/CandFromJudAlfa.aspx?Jud=1&PageN=1
  🔄 Page 2 ...
  💾 Saved 1324 rows to data/evaluare_01_ALBA.csv
...
✅ All counties processed.
```

---

## 🧠 What Each Library Does

| Library          | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `selenium`       | Automates browser interaction to load JavaScript-rendered pages         |
| `beautifulsoup4` | Parses HTML content and extracts table data                             |
| `pandas`         | Handles structured data and exports CSVs                                |
| `os`, `time`     | Utility modules (folder creation, delays, filename handling)            |

---

## 📌 Notes

- Some counties (e.g., `Jud=47` or higher) may not exist — the script skips them automatically.
- Mother tongue sections may contain blanks if the candidate didn't take that exam.
- The script runs headlessly (no Chrome window appears) using `--headless` mode.

---

## 📬 Feedback or Issues?

Feel free to open a GitHub issue or message the developer for fixes or improvements.