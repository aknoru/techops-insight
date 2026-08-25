
# TechOps Insight — IT Operations Analytics Platform

A portfolio-ready IT operations analytics application using Python, SQL, PostgreSQL and Streamlit.

## Demonstrates
- Incident and SLA analytics
- MTTR and downtime analysis
- Operational bottleneck identification
- PostgreSQL data modeling
- SQL KPI aggregation
- Interactive Streamlit dashboard
- Synthetic data generation
- Automated tests

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py
streamlit run app.py
```

The app runs from a generated CSV by default. PostgreSQL is optional.

For PostgreSQL:
```text
TECHOPS_DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/techops
```

Then:
```bash
python scripts/load_postgres.py
streamlit run app.py
```

## Structure
```text
techops-insight/
├── app.py
├── requirements.txt
├── README.md
├── data/.gitkeep
├── sql/kpis.sql
├── scripts/generate_data.py
├── scripts/load_postgres.py
├── src/analytics.py
└── tests/test_analytics.py
```

Synthetic records are generated locally; no proprietary or personal data is included.
=======
# techops-insight

