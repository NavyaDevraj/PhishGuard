# 🛡️ PhishGuard — Phishing URL Risk Analyzer

PhishGuard is a Python-based web application that analyzes website URLs and identifies potentially suspicious patterns using rule-based detection.

It provides a security dashboard, risk classification, scan history and downloadable reports through an interactive Streamlit interface.

## ✨ Features

- **URL Security Scanner:** Analyze website URLs for suspicious characteristics.
- **Risk Classification:** Categorize analyzed URLs as LOW, MEDIUM or HIGH risk.
- **Risk Score:** Calculate a heuristic risk score based on detected indicators.
- **Security Analysis Report:** Display detected indicators and safety recommendations.
- **Security Dashboard:** View total scans and risk distribution.
- **Scan History:** Store and review previously analyzed URLs.
- **Search and Filters:** Find scans by URL and risk classification.
- **CSV Export:** Download scan history for further analysis.
- **Interactive Charts:** Visualize scan statistics using Plotly.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| SQLite | Scan history database |
| Pandas | Data processing |
| Plotly | Interactive charts |

## 🔍 Detection Indicators

PhishGuard checks URL characteristics such as:

- Unusually long URLs
- Insecure HTTP connections
- IP addresses used instead of domain names
- Presence of the `@` symbol
- Suspicious keywords such as `login`, `verify`, `banking`, `password`, `account` and `secure`

The application assigns points to detected indicators and classifies the resulting score:

| Risk Score | Classification |
|---|---|
| 0–1 | LOW |
| 2–4 | MEDIUM |
| 5 or above | HIGH |

These are heuristic rules for educational analysis, not verified phishing probabilities.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd PhishGuard
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser, usually at:

`http://localhost:8501`

## 📁 Project Structure

```text
PhishGuard/
│
├── app.py
├── analyzer.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── phishguard.db  (created locally when the app runs)
```

## 📸 Application Screenshots

Screenshots of the dashboard, URL scanner and scan history will be added here.

## ⚠️ Disclaimer

PhishGuard is an educational project that uses rule-based URL analysis. It does not connect to a live threat-intelligence service and cannot guarantee that a website is safe or malicious.

Always verify website authenticity before entering passwords, payment information or other sensitive data.

## 👩‍💻 Project

**PhishGuard — Phishing URL Risk Analyzer**

Built using Python, Streamlit, SQLite, Pandas and Plotly.