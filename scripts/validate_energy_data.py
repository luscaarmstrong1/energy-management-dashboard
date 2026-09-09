from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
fact = pd.read_csv(ROOT / "data" / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp", "Data"])
costs = pd.read_csv(ROOT / "data" / "Fato_CustosEnergia.csv")

assert fact["Timestamp"].min().strftime("%Y-%m-%d %H:%M:%S") == "2025-01-01 00:00:00"
assert fact["Timestamp"].max().strftime("%Y-%m-%d %H:%M:%S") == "2025-12-31 23:00:00"
assert (fact.query("Hora < 6 or Hora > 18")["GeracaoSolar_kWh"] == 0).all()
assert (fact["ImportacaoRede_kWh"] >= -1e-6).all()
assert (fact["ExportacaoRede_kWh"] >= -1e-6).all()
assert (costs["CustoTotal_R"] > 0).all()
assert (costs["DemandaMaxima_kW"] > 0).all()
print("Validation passed")
