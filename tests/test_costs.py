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

def test_cost_components_reconcile():
    parts = costs[['CustoEnergia_R','CustoDemanda_R','CustoUltrapassagem_R','Impostos_R','OutrosCustos_R']].sum(axis=1)
    assert ((parts - costs['CustoTotal_R']).abs() < 1.0).all()
