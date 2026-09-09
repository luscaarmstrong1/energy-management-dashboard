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

def test_emissions_are_non_negative_and_consistent():
    assert (fact['Emissao_tCO2e'] >= 0).all()
    assert ((fact['Emissao_tCO2e'] - fact['ImportacaoRede_kWh'] * 0.0385 / 1000).abs() < 0.00001).all()
