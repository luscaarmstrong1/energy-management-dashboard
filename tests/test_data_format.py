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

def test_integrity_and_duplicates():
    assert fact[['Timestamp','ID_Unidade','ID_Setor']].duplicated().sum() == 0
    assert fact[['Timestamp','ID_Unidade','ID_Setor','Consumo_kWh']].notna().all().all()
    assert set(fact['ID_Unidade']).issubset(set(units['ID_Unidade']))
    assert (fact[['Consumo_kWh','Demanda_kW','ImportacaoRede_kWh','ExportacaoRede_kWh']] >= 0).all().all()
