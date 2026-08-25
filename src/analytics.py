import pandas as pd

REQUIRED_COLUMNS = {
    "incident_id", "opened_at", "closed_at", "service", "priority",
    "severity", "status", "sla_hours", "resolution_hours", "downtime_hours"
}

def validate_incidents(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

def prepare_incidents(df: pd.DataFrame) -> pd.DataFrame:
    validate_incidents(df)
    out = df.copy()
    out["opened_at"] = pd.to_datetime(out["opened_at"])
    out["closed_at"] = pd.to_datetime(out["closed_at"])
    out["sla_breached"] = out["resolution_hours"] > out["sla_hours"]
    out["month"] = out["opened_at"].dt.to_period("M").astype(str)
    return out

def kpis(df: pd.DataFrame) -> dict:
    df = prepare_incidents(df)
    return {
        "total_incidents": int(len(df)),
        "sla_breach_rate": float(df["sla_breached"].mean()),
        "avg_mttr_hours": float(df["resolution_hours"].mean()),
        "total_downtime_hours": float(df["downtime_hours"].sum()),
    }

def service_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = prepare_incidents(df)
    return (
        df.groupby("service", as_index=False)
        .agg(
            incidents=("incident_id", "count"),
            avg_mttr_hours=("resolution_hours", "mean"),
            downtime_hours=("downtime_hours", "sum"),
            sla_breach_rate=("sla_breached", "mean"),
        )
        .sort_values(["sla_breach_rate", "incidents"], ascending=[False, False])
    )

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = prepare_incidents(df)
    return (
        df.groupby("month", as_index=False)
        .agg(
            incidents=("incident_id", "count"),
            downtime_hours=("downtime_hours", "sum"),
            avg_mttr_hours=("resolution_hours", "mean"),
        )
        .sort_values("month")
    )
