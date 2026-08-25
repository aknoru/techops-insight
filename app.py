import os
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

from src.analytics import prepare_incidents, kpis, service_summary, monthly_summary

st.set_page_config(page_title="TechOps Insight", layout="wide")
st.title("TechOps Insight")
st.caption("IT Operations Analytics — incident, SLA, MTTR and downtime intelligence")

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "incidents.csv"

@st.cache_data
def load_csv():
    if not CSV_PATH.exists():
        raise FileNotFoundError("Run python scripts/generate_data.py first.")
    return pd.read_csv(CSV_PATH)

@st.cache_data
def load_postgres(url):
    engine = create_engine(url)
    return pd.read_sql("SELECT * FROM incidents", engine)

db_url = os.getenv("TECHOPS_DATABASE_URL")
try:
    raw = load_postgres(db_url) if db_url else load_csv()
except Exception as exc:
    st.error(str(exc))
    st.stop()

df = prepare_incidents(raw)

with st.sidebar:
    st.header("Filters")
    services = st.multiselect("Service", sorted(df.service.unique()), default=sorted(df.service.unique()))
    priorities = st.multiselect("Priority", sorted(df.priority.unique()), default=sorted(df.priority.unique()))

filtered = df[df.service.isin(services) & df.priority.isin(priorities)]
m = kpis(filtered)

a,b,c,d = st.columns(4)
a.metric("Incidents", f"{m['total_incidents']:,}")
b.metric("SLA breach rate", f"{m['sla_breach_rate']:.1%}")
c.metric("Average MTTR", f"{m['avg_mttr_hours']:.1f} h")
d.metric("Downtime", f"{m['total_downtime_hours']:.1f} h")

left, right = st.columns(2)
with left:
    monthly = monthly_summary(filtered)
    st.plotly_chart(px.line(monthly, x="month", y="incidents", markers=True,
                             title="Monthly Incident Volume"), use_container_width=True)
with right:
    service = service_summary(filtered)
    fig = px.bar(service, x="service", y="sla_breach_rate", title="SLA Breach Rate by Service")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Service Performance")
st.dataframe(service, use_container_width=True)
st.subheader("Recent Incidents")
st.dataframe(filtered.sort_values("opened_at", ascending=False).head(50), use_container_width=True)
