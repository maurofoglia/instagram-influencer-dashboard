# 📊 Instagram Influencer Analytics & Segmentation Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](INSERISCI_QUI_IL_TUO_LINK_STREAMLIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Live Interactive Dashboard:** [👉 Launch Streamlit App]
https://instagram-influencer-dashboard-zlqozbbxpram9eer24ycbz.streamlit.app/
---

## 📌 Project Overview

This project is an end-to-end Data Science and Machine Learning workflow designed to analyze, clean, and segment a dataset of top global Instagram influencers. 

By combining **Exploratory Data Analysis (EDA)**, **K-Means Clustering**, and an interactive **Streamlit Web Dashboard**, this project explores how follower volume relates to real audience engagement, uncovers geographic distributions, and detects engagement anomalies (such as potential bot activity).

---

## 🧭 Project Workflow (PACE Framework)

The project follows the standard **PACE** (Plan, Analyze, Construct, Execute) data methodology:

### 1. Plan
- **Dataset Structure:** Examined raw columns (`rank`, `influencer_insta_name`, `category_1`, `category_2`, `followers`, `audience_country`, `authentic_engagement`, `engagement_avg`).
- **Data Cleaning:**
  - Standardized column names to snake_case.
  - Converted string formatted metrics with shorthand units (e.g., `18.8M` $\rightarrow$ `18,800,000`, `383.1K` $\rightarrow$ `383,100`).
  - Handled missing categories and imputed missing country data.

### 2. Analyze (EDA)
- Analyzed follower count distributions (power-law / heavy-tailed distribution).
- Discovered inverse correlation trends between total follower volume and engagement percentage.
- Identified geographic clusters and leading content categories (Music, Cinema, Sports, Lifestyle).

### 3. Construct (Feature Engineering & Unsupervised ML)
- **Feature Engineering:** Calculated `engagement_rate` ($\frac{\text{engagement\_avg}}{\text{followers}}$) and `authenticity_score` ($\frac{\text{authentic\_engagement}}{\text{engagement\_avg}}$).
- **Feature Scaling:** Applied `StandardScaler` to prevent dominant features (followers in tens of millions) from biasing Euclidean distance calculations.
- **K-Means Clustering:** Segmented creators into 4 actionable clusters based on standardized features:
  - **Mega-Celebrities:** Extremely high reach, moderate to low relative engagement.
  - **Active Niche Creators:** Smaller follower bases with exceptionally high audience engagement.
  - **Mid-Tier Influencers:** Balanced audience size with consistent interactions.
  - **Emerging High-Potential Creators:** Rapidly growing engagement profiles.

### 4. Execute
- Exported cleaned, segmented data to `data/processed/influencers_segmented.csv`.
- Built and deployed a production-ready, interactive web application using **Streamlit** and **Plotly**.

---

## 🖥️ Dashboard Features

- **Dynamic KPI Cards:** Instant visibility into filtered creators, average engagement rate, total follower reach, and average authenticity score.
- **Multidimensional Filters:** Filter by creator category, audience country, and K-Means segment.
- **Interactive Global Choropleth Map:** Visualizes influencer concentration across countries with hover metrics.
- **Followers vs. Engagement Scatterplot:** Logarithmic scale scatterplot with color-coded clusters to identify high-value creators and detect outliers/bot inflation.
- **Audience Authenticity Inspector:** Highlights creators with low authentic engagement ratios.
- **Interactive Data Table & CSV Export:** Filtered records can be inspected and exported directly from the browser.

---

## 🛠️ Tech Stack & Libraries

- **Language:** Python 3.10+
- **Data Analysis & Preprocessing:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (`KMeans`, `StandardScaler`)
- **Data Visualization:** Plotly Express, Matplotlib, Seaborn
- **Web Application & Cloud Deployment:** Streamlit Community Cloud

---

## 📁 Repository Structure

```text
eda-dashboard/
│
├── data/
│   ├── raw/
│   │   └── top_influencers.csv            # Original raw dataset
│   └── processed/
│       └── influencers_segmented.csv      # Cleaned and clustered dataset
│
├── notebooks/
│   └── 01_EDA_and_Preprocessing.ipynb     # Step-by-step EDA & ML pipeline (PACE)
│
├── src/
│   └── app.py                             # Interactive Streamlit application
│
├── .gitignore                             # Git ignore rules
├── requirements.txt                       # Project dependencies
└── README.md                              # Project documentation
```

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/maurofoglia/instagram-influencer-dashboard.git
cd instagram-influencer-dashboard
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run src/app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
