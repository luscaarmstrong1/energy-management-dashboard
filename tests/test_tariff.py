from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
fact = pd.read_csv(ROOT / "data" / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp"])
costs = pd.read_csv(ROOT / "data" / "Fato_CustosEnergia.csv")

def test_peak_and_offpeak_costs_exist():
    assert (costs['CustoPonta_R'] >= 0).all()
    assert (costs['CustoForaPonta_R'] > 0).all()
