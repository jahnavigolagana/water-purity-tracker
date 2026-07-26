# Water Purity Tracker for Hostel 💧

A commercial SaaS-style full-stack web application designed for monitoring hostel water quality, calculating purity scores, executing rule-based treatment recommendations, storing historical CSV logs, visualizing analytical trends, and generating reports.

Developed as a college mini-project integrating **Engineering Chemistry**, **Programming**, **IT Workshop**, **Python Programming**, **CSV File Handling**, **Web Development**, and an **AI Rule Engine**.

---

## 🌟 Key Features

- **Modern Glassmorphism UI**: Water-inspired deep ocean blue theme, glass cards, dynamic page backgrounds, Google Fonts (Poppins), and FontAwesome icons.
- **Engineering Chemistry Analysis**: Computes weighted Purity Scores (0–100) based on pH (6.5–8.5), TDS (0–500 ppm), Turbidity (0–5 NTU), and Temperature (20–35°C).
- **Python AI Rule Engine**: Recommends treatment actions (Reverse Osmosis, Calcite Neutralization, Sand Filtration, UV Treatment, Chemical Balancing).
- **CSV Data Storage**: Automatically logs all entries into `data/water_readings.csv` with search, multi-filter, pagination, and export capabilities.
- **Interactive Dashboards & Analytics**: Live Chart.js visualizations (Daily Trend line chart, Safe vs Unsafe distribution, Tank parameter comparison bar chart, multi-axis weekly trends).
- **Automated Quality Alerts**: Automatically flags unsafe water test logs and alerts administrators with severity levels.
- **Official Compliance Reports**: Daily, Weekly, Monthly, and Yearly audit reports with print support and CSV download options.
- **Multi-Role User Management**: Support for Admin, Hostel Staff, and Student accounts.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Vanilla + Bootstrap 5 CDN), JavaScript (ES6), Chart.js, Font Awesome 6, Google Fonts.
- **Backend**: Python Flask REST API server.
- **Storage**: `water_readings.csv` (Mandatory CSV Datastore) + SQLite (Users, Alerts & Settings).

---

## 🚀 Quick Setup & Installation

### 1. Requirements
Ensure Python 3.8+ is installed on your machine.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Flask Server
```bash
python backend/app.py
```

### 4. Access Web Interface
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Demo Credentials
- **Admin**: `admin` / `admin123`
- **Hostel Staff**: `staff` / `staff123`
- **Student**: `student` / `student123`

---

## 📁 Project Structure

```
water-purity-tracker/
├── backend/
│   ├── app.py                 # Flask server & REST API
│   ├── rules.py               # Python AI Rule Engine
│   ├── csv_handler.py         # CSV file handling & queries
│   ├── report_generator.py    # Analytical reports engine
│   ├── database.py            # SQLite users & alerts database
│   └── utils.py               # Purity score & standards validator
├── data/
│   └── water_readings.csv     # Historical readings database
├── static/
│   ├── css/
│   │   ├── style.css          # Core design system
│   │   ├── glassmorphism.css  # Glass UI components
│   │   └── backgrounds.css   # Dynamic page animated backgrounds
│   └── js/
│       ├── main.js            # App controller & toasts
│       ├── charts.js          # Chart.js visualizations
│       └── rule_engine.js     # Live real-time frontend score preview
├── templates/
│   ├── layout.html            # Base master layout
│   ├── authentication.html    # Login screen
│   ├── dashboard.html         # Executive SaaS dashboard
│   ├── water_test.html        # Chemistry test entry form
│   ├── analysis.html          # Detailed standards comparison
│   ├── ai_suggestions.html    # AI Rule Engine treatment advice
│   ├── reports.html           # Compliance audit generator
│   ├── history.html           # Searchable CSV data table
│   ├── analytics.html         # Parameter correlation charts
│   ├── alerts.html            # Water safety alerts log
│   ├── users.html             # User role management
│   ├── profile.html           # User profile & credentials
│   ├── settings.html          # System preferences
│   ├── about.html             # Project details & academic info
│   └── help.html              # FAQs & support form
├── requirements.txt
└── README.md
```
