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

def test_no_solar_at_night():
    assert (fact.query('Hora < 6 or Hora > 18')['GeracaoSolar_kWh'] == 0).all()

def test_solar_coverage():
    coverage = fact['AutoconsumoSolar_kWh'].sum() / fact['Consumo_kWh'].sum()
    assert 0 <= coverage <= 1

def test_self_consumption():
    ratio = fact['AutoconsumoSolar_kWh'].sum() / fact['GeracaoSolar_kWh'].sum()
    assert 0 <= ratio <= 1
