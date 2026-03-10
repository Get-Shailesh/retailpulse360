<div align="center">

# 🛍️ RetailPulse 360

### End-to-End Retail Analytics Platform · NovaMart Chain (25 Stores · 5 Regions)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![SQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Excel](https://img.shields.io/badge/Excel-openpyxl-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)](https://openpyxl.readthedocs.io)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](docs/PowerBI_Implementation_Guide.html)

<br/>

> **A complete data analyst capstone project** covering the full analytics stack:
> synthetic data generation → SQL star schema → Python ML pipeline → Excel management report → Power BI dashboard → AI-powered insights

<br/>

**[📊 Live Interactive Dashboard](https://get-shailesh.github.io/retailpulse360/)** · **[🗄️ SQL Schema](docs/retailpulse360_schema_queries.sql)** · **[📈 Power BI Guide](docs/PowerBI_Implementation_Guide.html)**

</div>

---

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [📁 Project Structure](#-project-structure)
- [📊 Dataset Overview](#-dataset-overview)
- [🚀 Quick Start](#-quick-start)
- [🐍 Python Scripts](#-python-scripts)
- [🗄️ SQL Database](#️-sql-database)
- [📊 Excel Report](#-excel-report)
- [📈 Power BI Dashboard](#-power-bi-dashboard)
- [🤖 ML Models & Results](#-ml-models--results)
- [🔍 Key Business Insights](#-key-business-insights)
- [📤 GitHub Setup Guide](#-github-setup-guide)
- [💻 VS Code Setup Guide](#-vs-code-setup-guide)

---

## 🎯 Project Overview

RetailPulse 360 is a full-stack data analytics platform built for **NovaMart**, a fictional retail chain with 25 stores across 5 US regions. The project simulates a real-world data analyst role — from raw data to board-level insights.

| Metric           | Value                         |
| ---------------- | ----------------------------- |
| 📅 Date Range    | Jan 2022 – Dec 2024 (3 years) |
| 💰 Total Revenue | $160.9M                       |
| 📈 GP Margin     | 42.5%                         |
| 🛒 Transactions  | 151,687                       |
| 👥 Customers     | 10,000                        |
| 🏪 Stores        | 25 (5 regions)                |
| 🧾 Products      | 226 SKUs                      |
| ⭐ Reviews       | 8,000                         |

### Tech Stack

```
Data Layer     →  Python (pandas, numpy) · CSV datasets
SQL Layer      →  PostgreSQL star schema · 4 views · stored procedures
ML Layer       →  scikit-learn · Random Forest · Ridge Regression · Isolation Forest
Reporting      →  openpyxl Excel · Power BI DAX · HTML live dashboard
```

---

## 📁 Project Structure

```
retailpulse360/
│
├── 📂 data/                        ← All datasets (CSV)
│   ├── transactions.csv            ← 151,687 rows · core fact table
│   ├── customers.csv               ← 10,000 customer profiles
│   ├── products.csv                ← 226 product SKUs
│   ├── stores.csv                  ← 25 store locations
│   ├── inventory.csv               ← 3,375 stock records
│   ├── reviews.csv                 ← 8,000 customer reviews
│   ├── rfm_scores.csv              ← ML output: RFM segments
│   └── churn_scores.csv            ← ML output: churn predictions
│
├── 📂 scripts/                     ← Python source code
│   ├── 01_generate_data.py         ← Synthetic data generator
│   ├── 02_analytics_pipeline.py    ← EDA + ML pipeline (run this)
│   └── 03_build_excel.py           ← Excel workbook builder
│
├── 📂 outputs/                     ← Generated files
│   ├── RetailPulse360_Management_Report.xlsx
│   └── figures/                    ← 7 analysis charts (PNG)
│       ├── 01_revenue_overview.png
│       ├── 02_store_product_analysis.png
│       ├── 03_rfm_segmentation.png
│       ├── 04_churn_model.png
│       ├── 05_sales_forecast.png
│       ├── 06_anomaly_detection.png
│       └── 07_sentiment_analysis.png
│
├── 📂 docs/                        ← Reference documentation
│   ├── retailpulse360_schema_queries.sql
│   └── PowerBI_Implementation_Guide.html
│
├── 📂 dashboard/                   ← Interactive HTML demo
│   └── RetailPulse360_LiveDemo.html
│
├── requirements.txt
├── .gitignore
└── README.md                       ← You are here
```

---

## 📊 Dataset Overview

### `transactions.csv` — 151,687 rows

| Column             | Type   | Description                  |
| ------------------ | ------ | ---------------------------- |
| `transaction_id`   | string | Unique ID (T0000001…)        |
| `date`             | date   | 2022-01-01 to 2024-12-31     |
| `store_id`         | string | FK → stores.csv              |
| `customer_id`      | string | FK → customers.csv           |
| `product_id`       | string | FK → products.csv            |
| `quantity`         | int    | Units purchased              |
| `unit_price`       | float  | Shelf price                  |
| `discount_amount`  | float  | Discount applied             |
| `final_unit_price` | float  | Price after discount         |
| `total_revenue`    | float  | quantity × final_unit_price  |
| `total_cost`       | float  | quantity × unit_cost         |
| `gross_profit`     | float  | total_revenue − total_cost   |
| `payment_method`   | string | Credit/Debit/Mobile Pay/Cash |
| `channel`          | string | In-Store / Online            |

### `customers.csv` — 10,000 rows

| Column                     | Type   | Description                  |
| -------------------------- | ------ | ---------------------------- |
| `customer_id`              | string | C00001 – C10000              |
| `first_name` / `last_name` | string | Full name                    |
| `email`                    | string | Contact email                |
| `age`                      | int    | 18–75                        |
| `gender`                   | string | M / F / Other                |
| `city`                     | string | US city                      |
| `registration_date`        | date   | Account created              |
| `loyalty_tier`             | string | New / Bronze / Silver / Gold |
| `email_opt_in`             | bool   | Marketing consent            |

### `products.csv` — 226 rows

| Column         | Type   | Description                                                  |
| -------------- | ------ | ------------------------------------------------------------ |
| `product_id`   | string | P0001 – P0226                                                |
| `product_name` | string | Brand + subcategory + SKU#                                   |
| `category`     | string | Electronics / Clothing / Groceries / Home & Kitchen / Sports |
| `brand`        | string | NovaBrand / TechEdge / AlphaLine etc.                        |
| `unit_cost`    | float  | Supplier cost                                                |
| `unit_price`   | float  | Retail price                                                 |
| `margin_pct`   | float  | Gross margin %                                               |

### `stores.csv` — 25 rows

| Column       | Description                           |
| ------------ | ------------------------------------- |
| `store_id`   | S001 – S025                           |
| `region`     | North / South / East / West / Central |
| `store_type` | Flagship / Standard / Express         |
| `city`       | US city                               |
| `sqft`       | Store size                            |

### `rfm_scores.csv` — ML Output

> Generated by `02_analytics_pipeline.py` — do not edit manually

| Column          | Description                                           |
| --------------- | ----------------------------------------------------- |
| `recency`       | Days since last purchase                              |
| `frequency`     | Total transactions                                    |
| `monetary`      | Total spend                                           |
| `R` / `F` / `M` | Quintile scores (1–5)                                 |
| `RFM`           | Combined score                                        |
| `segment`       | Champions / Loyal / Potential / At Risk / Hibernating |

### `churn_scores.csv` — ML Output

| Column              | Description                 |
| ------------------- | --------------------------- |
| `churn_probability` | Model score 0.0–1.0         |
| `churn_risk_label`  | Low / Medium / High Risk    |
| `segment`           | RFM segment cross-reference |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git
- VS Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/retailpulse360.git
cd retailpulse360
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Pipeline

```bash
# Step 1: Generate all datasets (skip if using existing data/)
python scripts/01_generate_data.py

# Step 2: Run the full ML analytics pipeline
python scripts/02_analytics_pipeline.py

# Step 3: Build the Excel management report
python scripts/03_build_excel.py
```

### 5. View the Dashboard

Open `dashboard/RetailPulse360_LiveDemo.html` in any browser — **no server needed**.

---

## 🐍 Python Scripts

### `01_generate_data.py` — Data Generator

Generates all synthetic datasets from scratch using `numpy` and `pandas`.

```python
# Key sections:
# ── STORES        → 25 stores across 5 regions
# ── PRODUCTS      → 226 SKUs across 5 categories
# ── CUSTOMERS     → 10,000 profiles with loyalty tiers
# ── TRANSACTIONS  → 151,687 rows (3 years, seasonal patterns)
# ── INVENTORY     → Stock levels with reorder alerts
# ── REVIEWS       → 8,000 ratings with sentiment labels
```

**Run time:** ~15 seconds  
**Output:** 6 CSV files in `data/`

---

### `02_analytics_pipeline.py` — ML Pipeline

The core analytics script. Runs 7 analysis modules end-to-end.

```
[1/7] Load Data         → Read all 6 CSVs
[2/7] Revenue EDA       → Monthly trends, regional breakdown
[3/7] Store Analysis    → Top 10 stores, product scatter
[4/7] RFM Segments      → 5-segment customer classification
[5/7] Churn Model       → Random Forest (AUC = 1.000)
[6/7] Sales Forecast    → Ridge Regression + 90-day projection
[7/7] Anomaly Detection → Isolation Forest (55 anomalies)
```

**Models used:**

| Model                | Library | Purpose               | Result           |
| -------------------- | ------- | --------------------- | ---------------- |
| Random Forest        | sklearn | Churn prediction      | AUC = 1.000      |
| Ridge Regression     | sklearn | Sales forecasting     | $123,559/day avg |
| Isolation Forest     | sklearn | Anomaly detection     | 55 anomalies     |
| RFM Quintile Scoring | pandas  | Customer segmentation | 5 segments       |

**Run time:** ~45 seconds  
**Output:** 7 PNG charts + `rfm_scores.csv` + `churn_scores.csv`

---

### `03_build_excel.py` — Excel Report Builder

Builds a professional 6-sheet Excel workbook using `openpyxl`.

| Sheet                    | Contents                                 |
| ------------------------ | ---------------------------------------- |
| 📊 Executive Summary     | KPI cards + regional breakdown table     |
| 📅 Monthly KPIs          | 36-month trend + embedded line chart     |
| 📦 Product Performance   | Top 50 products + pie chart              |
| 👥 Customer Intelligence | RFM segments + at-risk customer list     |
| 📋 Inventory Status      | Reorder alerts with red/amber formatting |
| 🗄️ SQL Query Library     | Reference queries for analysts           |

**Run time:** ~10 seconds  
**Output:** `outputs/RetailPulse360_Management_Report.xlsx`

---

## 🗄️ SQL Database

The full star schema is defined in `docs/retailpulse360_schema_queries.sql`.

### Schema Design

```sql
-- FACT TABLE
fact_transactions     (151,687 rows)
  ├── date           → dim_date
  ├── store_id       → dim_stores
  ├── customer_id    → dim_customers
  └── product_id     → dim_products

-- DIMENSION TABLES
dim_date              (date spine with year/month/quarter)
dim_stores            (25 stores with region, type, city)
dim_customers         (10,000 customers with loyalty tier)
dim_products          (226 SKUs with category, margin)
```

### Pre-Built Views

```sql
vw_monthly_revenue    -- Revenue + GP by month/region
vw_product_performance -- Units, revenue, margin per SKU
vw_customer_rfm       -- Recency/frequency/monetary scores
vw_store_scorecard    -- KPIs per store with rankings
```

### Sample Queries

```sql
-- YoY Revenue Growth
SELECT year, month,
  SUM(total_revenue) AS revenue,
  LAG(SUM(total_revenue)) OVER (PARTITION BY month ORDER BY year) AS prev_yr,
  ROUND(
    (SUM(total_revenue) - LAG(SUM(total_revenue)) OVER (PARTITION BY month ORDER BY year))
    / NULLIF(LAG(SUM(total_revenue)) OVER (PARTITION BY month ORDER BY year), 0) * 100, 2
  ) AS yoy_growth_pct
FROM vw_monthly_revenue
GROUP BY year, month ORDER BY year, month;

-- Top 10 Products
SELECT RANK() OVER (ORDER BY SUM(total_revenue) DESC) AS rank,
  p.product_name, p.category,
  SUM(quantity) AS units_sold,
  SUM(total_revenue) AS revenue
FROM fact_transactions t
JOIN dim_products p ON t.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY revenue DESC LIMIT 10;
```

---

## 📊 Excel Report

### Opening the Report

1. Download `outputs/RetailPulse360_Management_Report.xlsx`
2. Open in **Microsoft Excel 2016+** or **LibreOffice Calc**
3. Enable macros if prompted (needed for chart refresh)

### Key Features

- **Color-scale conditional formatting** on revenue columns
- **Data bars** on product ranking table
- **Embedded charts** that update with data
- **Live formulas** — no hardcoded values anywhere
- **Red/amber alerts** on inventory reorder rows

---

## 📈 Power BI Dashboard

Full setup guide: `docs/PowerBI_Implementation_Guide.html`

### Quick Setup

```
1. Open Power BI Desktop
2. Get Data → Text/CSV → import all files from data/
3. Model View → create relationships:
      transactions[store_id]    → stores[store_id]
      transactions[product_id]  → products[product_id]
      transactions[customer_id] → customers[customer_id]
4. Add DAX measures (see guide for full list)
5. Build 5 report pages from the guide
```

### Core DAX Measures

```dax
Total Revenue = SUM(transactions[total_revenue])

GP Margin % = DIVIDE(SUM(transactions[gross_profit]), SUM(transactions[total_revenue]))

YoY Growth =
VAR CurrentYear = SUM(transactions[total_revenue])
VAR PriorYear = CALCULATE(SUM(transactions[total_revenue]),
    SAMEPERIODLASTYEAR(dim_date[date]))
RETURN DIVIDE(CurrentYear - PriorYear, PriorYear)

Rolling 3M Revenue =
CALCULATE([Total Revenue],
    DATESINPERIOD(dim_date[date], LASTDATE(dim_date[date]), -3, MONTH))
```

---

## 🤖 ML Models & Results

### Model 1: Churn Prediction (Random Forest)

```
Algorithm:     RandomForestClassifier (100 trees, max_depth=8)
Target:        churned = 1 if recency > 90 days
Features:      recency, frequency, monetary, R/F/M scores,
               age, loyalty_tier_score, email_opt_in
Train/Test:    80% / 20% (stratified)

Results:
  AUC Score:   1.000
  High Risk:   1,985 customers flagged
  At-Risk Revenue: ~$3.4M annual
```

### Model 2: Sales Forecasting (Ridge Regression)

```
Algorithm:     Ridge(alpha=1.0) with seasonal month dummies
Features:      time index (t), month one-hot encoding
Horizon:       90 days forward

Results:
  Avg Forecast:     $123,559/day
  Q1 2025 Proj:     ~$11.1M
  Confidence Band:  ±15%
```

### Model 3: Anomaly Detection (Isolation Forest)

```
Algorithm:     IsolationForest(contamination=0.05)
Features:      daily_revenue, pct_vs_7day_rolling_avg

Results:
  Anomalies:    55 detected (5% of days)
  Notable:      12 likely data errors for investigation
```

### RFM Segmentation Results

| Segment                | Count | % of Base | Avg Revenue |
| ---------------------- | ----- | --------- | ----------- |
| 🏆 Champions           | 1,664 | 16.6%     | $186        |
| 💙 Loyal Customers     | 2,843 | 28.4%     | $168        |
| 🌱 Potential Loyalists | 3,062 | 30.6%     | $136        |
| ⚠️ At Risk             | 1,507 | 15.1%     | $98         |
| 💤 Hibernating         | 924   | 9.2%      | $72         |

---

## 🔍 Key Business Insights

> Generated from the actual ML pipeline run on 151,687 transactions

### 💰 Revenue

- **$160.9M** total 3-year revenue at **42.5% GP margin**
- Electronics leads revenue (**38%** share) but below-average margin (38.2%)
- November–December = **22% of annual revenue** — peak season critical
- Online channel: **18% of transactions** but **24% higher AOV** ($217 vs $175)

### 🏪 Regional Performance

- **West region** underperforms: revenue per store **15% below network average**
- **Central region** highest revenue despite fewest stores
- **South region** lowest customer sentiment: **3.41★** vs 3.98★ North

### 👥 Customers

- **1,664 Champions** generate ~31% of revenue (top 16.6%)
- **1,985 high-risk churners** — $3.4M annual revenue at risk
- Win-back campaign recommended within **7 days** for At Risk segment

### 📦 Inventory

- **341 SKU-store combos** below reorder level
- **142 fully out of stock** — Electronics worst affected
- Los Angeles Smartphone stockout estimated **$84K lost revenue**

---

## 📤 GitHub Setup Guide

> Step-by-step instructions to publish this project to GitHub

### Step 1: Install Git

```bash
# Windows — download from:
https://git-scm.com/download/win

# macOS
brew install git

# Linux (Ubuntu/Debian)
sudo apt install git
```

Verify: `git --version`

---

### Step 2: Configure Git (first time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

### Step 3: Create a GitHub Account & Repository

1. Go to **[github.com](https://github.com)** → Sign up or log in
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name:** `retailpulse360`
   - **Description:** `End-to-end retail analytics platform with ML pipeline, SQL, Excel & Power BI`
   - **Visibility:** Public ✅ _(so employers can see it)_
   - **DO NOT** tick "Add a README" _(we have our own)_
4. Click **Create repository**
5. **Copy the repository URL** shown — it looks like:
   `https://github.com/YOUR_USERNAME/retailpulse360.git`

---

### Step 4: Initialize Git in Your Project Folder

```bash
# Navigate to your project folder
cd path/to/retailpulse360

# Initialize git
git init

# Add all files
git add .

# Check what's staged
git status
```

---

### Step 5: Make Your First Commit

```bash
git commit -m "🚀 Initial commit — RetailPulse 360 full analytics project

- 151,687 transaction synthetic dataset
- Python ML pipeline: RFM, Churn (AUC=1.0), Forecast, Anomaly Detection
- PostgreSQL star schema with 4 views
- Excel management report (6 sheets)
- Power BI implementation guide
- Interactive HTML dashboard"
```

---

### Step 6: Connect to GitHub and Push

```bash
# Connect your local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/retailpulse360.git

# Set the default branch name
git branch -M main

# Push to GitHub
git push -u origin main
```

Enter your **GitHub username** and **Personal Access Token** when prompted.

> **⚠️ Note on `transactions.csv` (15MB)**
> GitHub has a 25MB file limit. The transactions file is 15MB — it will upload fine.
> If you ever regenerate it and it grows, add it to `.gitignore` and use Git LFS:
>
> ```bash
> git lfs install
> git lfs track "data/transactions.csv"
> git add .gitattributes
> ```

---

### Step 7: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/retailpulse360`
2. You should see all folders and your README rendered beautifully
3. Pin it to your profile: **Profile page → Customize profile → Pin repository**

---

### Step 8: Future Updates (daily workflow)

```bash
# After making changes:
git add .
git commit -m "✨ Add: short description of what changed"
git push
```

---

## 💻 VS Code Setup Guide

> Step-by-step instructions to open and work on this project in VS Code

### Step 1: Install VS Code

Download from **[code.visualstudio.com](https://code.visualstudio.com)**

---

### Step 2: Install Recommended Extensions

Open VS Code → press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)

Install these extensions:

| Extension          | Publisher   | Why                         |
| ------------------ | ----------- | --------------------------- |
| **Python**         | Microsoft   | Run .py files, IntelliSense |
| **Pylance**        | Microsoft   | Type checking, autocomplete |
| **Jupyter**        | Microsoft   | Notebook support            |
| **Rainbow CSV**    | mechatroner | Colour-code CSV columns     |
| **Excel Viewer**   | GrapeCity   | Preview .xlsx in VS Code    |
| **GitLens**        | GitKraken   | Git blame, history          |
| **SQLTools**       | mtxr        | Run SQL queries inline      |
| **indent-rainbow** | oderwat     | Visualise Python indents    |

---

### Step 3: Open the Project

```bash
# From terminal
cd path/to/retailpulse360
code .
```

Or: VS Code → **File → Open Folder** → select `retailpulse360/`

---

### Step 4: Set Up the Python Interpreter

1. Press `Ctrl+Shift+P` → type **"Python: Select Interpreter"**
2. Choose the interpreter from your virtual environment:
   - Windows: `.\venv\Scripts\python.exe`
   - Mac/Linux: `./venv/bin/python`
3. You'll see it in the bottom-left status bar ✅

---

### Step 5: Create a VS Code Workspace Settings File

Create `.vscode/settings.json` in your project root:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.associations": {
    "*.csv": "csv"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "python.terminal.activateEnvironment": true
}
```

---

### Step 6: Run Scripts in VS Code

**Option A — Run button:**
Open any `.py` file → click the ▶ **Run Python File** button (top right)

**Option B — Terminal:**

```bash
# Open integrated terminal: Ctrl+` (backtick)
python scripts/02_analytics_pipeline.py
```

**Option C — Debug mode:**

1. Open `02_analytics_pipeline.py`
2. Press `F5` → select **Python File**
3. Set breakpoints by clicking the left margin
4. Step through code with `F10`

---

### Step 7: View Data Files

- Click any `.csv` file → VS Code shows it as a **colour-coded table** (with Rainbow CSV)
- Click `.xlsx` file → Opens in **Excel Viewer** preview panel
- Click `.html` file → Right-click → **Open with Live Server** (if installed)

---

### Step 8: Use the Integrated Git Panel

1. Click the **Source Control icon** (left sidebar, looks like a branch)
2. See all changed files listed
3. Click `+` to stage files
4. Type a commit message in the box
5. Click **✓ Commit** then **⟳ Sync** to push to GitHub

---

### Recommended VS Code Layout

```
┌─────────────────────────────────────────────────────┐
│  EXPLORER          │  02_analytics_pipeline.py       │
│  ├ data/           │                                 │
│  ├ scripts/        │  # ── RFM SEGMENTATION ──       │
│  ├ outputs/        │  rfm = trans.groupby(...)       │
│  └ docs/           │                                 │
│                    ├─────────────────────────────────┤
│  OUTLINE           │  TERMINAL                       │
│  ├ Load Data       │  $ python scripts/02_...py      │
│  ├ RFM Segments    │  [4/7] RFM Segmentation...      │
│  └ Churn Model     │  ✓ Completed in 43.2s           │
└─────────────────────────────────────────────────────┘
```

---

## 📄 License

This project is for educational and portfolio purposes.
Dataset is 100% synthetic — no real customer data.

---

<div align="center">

**Built with ❤️ as a Data Analyst Capstone Project**

_RetailPulse 360 · NovaMart Analytics Platform_

</div>
