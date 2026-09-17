# Customer Retention Analytics Pro

An enterprise-grade Streamlit application for analyzing customer churn and
retention patterns across a banking customer base.

## Features

- **Executive Overview** — headline KPIs (churn rate, active member rate,
  average balance, relationship score) with deltas against the full dataset,
  plus retention donut, tenure-churn curve, geography churn bar, and age
  distribution charts.
- **Segment Analysis** — geography x product-tier churn heatmap, relationship
  tier breakdown, balance-vs-credit-score scatter, and a configurable
  group-by summary table.
- **Customer Explorer** — searchable, sortable, exportable customer-level
  table with a relationship-score progress column.
- **Data Health** — dataset diagnostics: row/column counts, duplicate IDs,
  column types, null counts, descriptive statistics.
- **Global Filters** — geography, gender, engagement status, product count,
  and age range, all persisted via `st.session_state`.
- **Custom Dataset Upload** — replace the sample dataset with your own CSV
  (validated against the required schema).
- Premium dark theme (slate / navy background, emerald accent), custom CSS,
  cached data processing, and clean error handling throughout.

## Project Structure

```
customer_retention_analytics_pro/
├── app.py                        # Main application entry point
├── components/
│   ├── __init__.py
│   ├── sidebar.py                # Navigation + global filters
│   ├── kpi_cards.py               # KPI metric card rendering
│   ├── charts.py                  # Plotly chart builders (themed)
│   ├── page_overview.py           # Overview page
│   ├── page_segments.py           # Segment analysis page
│   ├── page_explorer.py           # Customer explorer page
│   └── page_data_health.py        # Data health / diagnostics page
├── utils/
│   ├── __init__.py
│   ├── data.py                    # Loading, validation, enrichment
│   ├── metrics.py                 # KPI + segment computations
│   └── style.css                  # Custom CSS theme
├── data/
│   └── European_Bank.csv          # Sample dataset
├── .streamlit/
│   └── config.toml                # Theme + server configuration
├── requirements.txt
└── README.md
```

## Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:

   ```bash
   streamlit run app.py
   ```

4. Open the URL Streamlit prints (typically `http://localhost:8501`).

## Using Your Own Data

Upload a CSV from the sidebar under **Data Source**. The file must contain
these columns:

```
CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure,
Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited
```

If validation fails, the app displays a clear error and falls back to the
bundled sample dataset.

## Notes on the Relationship Score

`RelationshipStrength` is a transparent, rules-based index (weighted
combination of activity status, product count, credit card ownership, and
tenure) intended purely for descriptive segmentation. It is **not** a
predictive churn model.

## Deployment

The app is stateless aside from `st.session_state` (filters, uploaded file),
so it deploys directly to Streamlit Community Cloud, Docker, or any host
that runs `streamlit run app.py`. No external API keys are required.
