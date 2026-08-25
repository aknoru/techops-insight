import pandas as pd
from src.analytics import prepare_incidents, kpis, service_summary

def sample():
    return pd.DataFrame([
        {"incident_id":"1","opened_at":"2026-01-01","closed_at":"2026-01-01",
         "service":"API","priority":"P2","severity":"High","status":"Resolved",
         "sla_hours":8,"resolution_hours":5,"downtime_hours":2},
        {"incident_id":"2","opened_at":"2026-01-02","closed_at":"2026-01-03",
         "service":"API","priority":"P1","severity":"Critical","status":"Resolved",
         "sla_hours":4,"resolution_hours":24,"downtime_hours":8},
    ])

def test_sla_flag():
    assert prepare_incidents(sample())["sla_breached"].tolist() == [False, True]

def test_kpis():
    result = kpis(sample())
    assert result["total_incidents"] == 2
    assert result["avg_mttr_hours"] == 14.5

def test_service_summary():
    assert service_summary(sample()).iloc[0]["service"] == "API"
