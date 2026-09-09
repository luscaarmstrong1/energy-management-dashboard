from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
fact = pd.read_csv(ROOT / "data" / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp", "Data"])
costs = pd.read_csv(ROOT / "data" / "Fato_CustosEnergia.csv")
units = pd.read_csv(ROOT / "data" / "Dim_Unidade.csv")
opps = pd.read_csv(ROOT / "data" / "Fato_Oportunidades.csv")
alerts = pd.read_csv(ROOT / "data" / "Fato_Alertas.csv")
prod = pd.read_csv(ROOT / "data" / "Fato_ProducaoMensal.csv")

def test_load_factor_bounds():
    demand = fact.groupby(['Timestamp'])['Demanda_kW'].sum().max()
    lf = fact['Consumo_kWh'].sum() / (demand * fact['Timestamp'].nunique())
    assert 0 < lf <= 1
