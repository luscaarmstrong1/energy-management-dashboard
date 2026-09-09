from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
fact = pd.read_csv(ROOT / "data" / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp"])
hourly = fact.groupby(["Timestamp", "ID_Unidade"], as_index=False).agg(Consumo_kWh=("Consumo_kWh", "sum"))
hourly["rolling_mean"] = hourly.groupby("ID_Unidade")["Consumo_kWh"].transform(lambda s: s.rolling(24, min_periods=12).mean())
hourly["rolling_std"] = hourly.groupby("ID_Unidade")["Consumo_kWh"].transform(lambda s: s.rolling(24, min_periods=12).std())
hourly["z_score"] = (hourly["Consumo_kWh"] - hourly["rolling_mean"]) / hourly["rolling_std"]
q = hourly.groupby("ID_Unidade")["Consumo_kWh"].quantile([0.25, 0.75]).unstack()
q["iqr"] = q[0.75] - q[0.25]
hourly = hourly.merge(q, left_on="ID_Unidade", right_index=True)
hourly["iqr_anomaly"] = hourly["Consumo_kWh"] > hourly[0.75] + 1.5 * hourly["iqr"]
anomalies = hourly[(hourly["z_score"].abs() > 3) | hourly["iqr_anomaly"]].copy()
anomalies.to_csv(ROOT / "data" / "Detected_Anomalies.csv", index=False)
print(f"Detected {len(anomalies)} anomalies")
