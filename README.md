# 🐍 Python Automations

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![CLI](https://img.shields.io/badge/type-CLI%20tool-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

Collection of **practical, production-ready** automation scripts focused on real productivity: file management, API consumption, and automated email reporting.

## 🎯 Objective
Demonstrate real-world automations using Python, focusing on:
- Security
- Clarity
- Practical use
- Clean, reusable code

---

## 📦 Project Structure

```
python-automations/
├── scripts/
│   ├── file_renamer.py
│   ├── api_consumer.py
│   └── email_reporter.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Scripts

### 1️⃣ File Renamer
Automation for batch file renaming with safety features.

**Key Features**
- Prefix and suffix
- Text replacement
- Sequential numbering
- Date stamps
- Character sanitization
- Recursive processing
- Dry-run by default (safety)

**Example**
```
test file (3).txt → demo_test_file_3.txt
```

**Usage**
```bash
python file_renamer.py --dry-run
```

---

### 2️⃣ API Consumer

Consumes data from public APIs and exports results.

**Supported APIs**
- GitHub
- CoinGecko
- OpenWeatherMap (demo mode)

**Features**
- Formatted terminal output
- JSON and CSV export
- Error handling
- Basic rate limiting

**Usage**
```bash
python api_consumer.py github --user torvalds
```

---

### 3️⃣ Email Reporter

Automatic generation of HTML reports sent via email.

**Features**
- Professional HTML reports
- Preview without sending
- SMTP support (Gmail, Outlook)
- JSON or CSV data input
- Attachments and visual metrics

**Usage**
```bash
python email_reporter.py --preview
```

---

## ⚙️ Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧠 Technologies

- Python 3
- requests
- argparse
- SMTP / HTML

---

## ✅ Quality

- Type hints
- Docstrings
- Error handling
- User-friendly CLI
- Modular code

---

## 🎯 Use Cases

- File standardization
- API data collection
- Automated reporting
- Repetitive task automation

---

## 📌 Status

✔ Production-ready  
✔ Safe by default  
✔ Easy to extend
