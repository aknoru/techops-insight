from pathlib import Path
import numpy as np
import pandas as pd

def main():
    rng = np.random.default_rng(42)
    rows = 1200
    services = ["Payments", "Identity", "API Gateway", "Database", "Web", "Messaging"]
    priorities = ["P1", "P2", "P3", "P4"]
    severity_map = {"P1": "Critical", "P2": "High", "P3": "Medium", "P4": "Low"}
    sla_map = {"P1": 4, "P2": 8, "P3": 24, "P4": 48}

    opened = pd.date_range("2025-01-01", "2026-06-30", periods=rows)
    priority = rng.choice(priorities, rows, p=[.08, .27, .45, .20])
    resolution = np.clip(rng.gamma(2.0, 4.0, rows), .2, 72)
    sla = np.array([sla_map[p] for p in priority])
    downtime = np.clip(resolution * rng.uniform(.05, .45, rows), 0, resolution)

    df = pd.DataFrame({
        "incident_id": [f"INC-{i:05d}" for i in range(1, rows + 1)],
        "opened_at": opened,
        "service": rng.choice(services, rows),
        "priority": priority,
        "severity": [severity_map[p] for p in priority],
        "status": rng.choice(["Resolved", "Closed"], rows, p=[.75, .25]),
        "sla_hours": sla,
        "resolution_hours": np.round(resolution, 2),
        "downtime_hours": np.round(downtime, 2),
    })
    df["closed_at"] = df["opened_at"] + pd.to_timedelta(df["resolution_hours"], unit="h")
    cols = ["incident_id","opened_at","closed_at","service","priority","severity",
            "status","sla_hours","resolution_hours","downtime_hours"]
    out = Path(__file__).resolve().parents[1] / "data" / "incidents.csv"
    out.parent.mkdir(exist_ok=True)
    df[cols].to_csv(out, index=False)
    print(f"Wrote {len(df)} synthetic incidents to {out}")

if __name__ == "__main__":
    main()
