# Customer Retention Analytics Pro

Enterprise-grade Streamlit application for analyzing customer churn and retention across a banking customer base — engagement, product utilization, and relationship-strength analytics for data-driven retention strategy.

**© 2026 Yuvraj Singh. All Rights Reserved.**

---

## Owner

**Yuvraj Singh**
All rights, title, and interest in and to this software, including all source code, documentation, design assets, and associated intellectual property, are owned exclusively by Yuvraj Singh.

## License

All Rights Reserved.

This software and its source code are the proprietary property of Yuvraj Singh. No part of this repository may be copied, modified, distributed, sublicensed, publicly displayed, reverse-engineered, or used in any form — commercial or non-commercial — without the prior express written permission of the owner.

Unauthorized use, reproduction, or distribution of this application or any portion of it is strictly prohibited and may result in legal action.

For licensing inquiries or permission requests, contact Yuvraj Singh directly.

---

## Features

- **Executive Overview** — headline KPIs (churn rate, active members, product mix) with delta indicators
- **Segment Analysis** — churn cross-cuts by geography, age, balance tier, and product count
- **Customer Explorer** — searchable, sortable, exportable customer-level table
- **Data Health** — dataset diagnostics and data-quality summary
- Custom dark corporate theme with responsive layout
- Cached data loading and metric computation for fast reruns

## Project Structure

```
customer_retention_analytics_pro/
├── app.py                 # Main application entry point
├── requirements.txt       # Pip dependencies
├── README.md              # This file
├── .streamlit/
│   └── config.toml        # Theme configuration
├── data/
│   └── European_Bank.csv  # Bundled sample dataset
├── components/             # UI modules (sidebar, charts, KPI cards, pages)
└── utils/                  # Data loading, validation, and metric helpers
```

## Setup

1. **Extract** this archive and open a terminal in the project folder.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. The app opens automatically at `http://localhost:8501`. If it doesn't, open that URL in your browser manually.

## Deployment

To host a public link via **Streamlit Community Cloud**:

1. Push this project to a GitHub repository (owned by or authorized by Yuvraj Singh).
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repository.
3. Set the entry point to `app.py` and deploy.
4. You'll receive a public `*.streamlit.app` URL.

## Data

The bundled dataset (`data/European_Bank.csv`) is provided for demonstration purposes. To use your own data, replace this file with a CSV matching the same column schema, or upload a file directly within the app.

## Disclaimer

This application is provided "as is" without warranty of any kind. The owner is not liable for any damages or losses resulting from the use of this software.

---

**Contact:** Yuvraj Singh — Owner & Author
