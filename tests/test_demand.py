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

def test_demand_monthly_peak_matches_hourly():
    tmp = fact.copy()
    tmp['MesAno'] = tmp['Timestamp'].dt.strftime('%Y-%m')
    hourly = tmp.groupby(['MesAno', 'ID_Unidade', 'Timestamp'])['Demanda_kW'].sum().reset_index(name='Demanda')
    peaks = hourly.groupby(['MesAno', 'ID_Unidade'])['Demanda'].max()
    for _, row in costs.iterrows():
        assert abs(row['DemandaMaxima_kW'] - peaks.loc[(row['MesAno'], row['ID_Unidade'])]) < 0.02

def test_excess_demand_formula():
    expected = (costs['DemandaMaxima_kW'] - costs['DemandaContratada_kW']).clip(lower=0)
    assert ((expected - costs['ExcessoDemanda_kW']).abs() < 0.02).all()
