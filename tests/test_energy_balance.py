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

def test_energy_balance():
    assert (fact['Consumo_kWh'] - fact['AutoconsumoSolar_kWh'] - fact['ImportacaoRede_kWh']).abs().max() < 0.01
    assert (fact['GeracaoSolar_kWh'] - fact['AutoconsumoSolar_kWh'] - fact['ExportacaoRede_kWh']).abs().max() < 0.01
