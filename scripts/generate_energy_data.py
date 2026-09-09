from __future__ import annotations

import json
import math
import shutil
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SEED = 20250908
START = "2025-01-01 00:00:00"
END = "2025-12-31 23:00:00"
CO2_FACTOR = 0.0385


UNITS = [
    {
        "ID_Unidade": "U001",
        "Unidade": "Nexus Sao Paulo Manufacturing",
        "Cidade": "Sao Paulo",
        "UF": "SP",
        "TipoUnidade": "Fabrica",
        "PerfilOperacao": "industrial_shift",
        "Area_m2": 18500,
        "Funcionarios": 420,
        "PotenciaFV_kWp": 780,
        "DemandaContratada_kW": 1280,
        "TarifaPonta_R_kWh": 1.42,
        "TarifaForaPonta_R_kWh": 0.62,
        "TarifaDemanda_R_kW": 42.0,
        "PenalidadeUltrapassagem_R_kW": 84.0,
        "ImpostosPercentual": 0.245,
        "OutrosEncargos_R": 9800,
        "BaseLoad_kW": 210,
        "PeakLoad_kW": 1120,
        "ProductionBase": 15500,
        "DemandScenario": "adequada",
    },
    {
        "ID_Unidade": "U002",
        "Unidade": "Nexus Campinas Logistics",
        "Cidade": "Campinas",
        "UF": "SP",
        "TipoUnidade": "Centro logistico",
        "PerfilOperacao": "logistics",
        "Area_m2": 24000,
        "Funcionarios": 210,
        "PotenciaFV_kWp": 420,
        "DemandaContratada_kW": 720,
        "TarifaPonta_R_kWh": 1.35,
        "TarifaForaPonta_R_kWh": 0.58,
        "TarifaDemanda_R_kW": 39.0,
        "PenalidadeUltrapassagem_R_kW": 78.0,
        "ImpostosPercentual": 0.238,
        "OutrosEncargos_R": 6200,
        "BaseLoad_kW": 120,
        "PeakLoad_kW": 690,
        "ProductionBase": 9800,
        "DemandScenario": "ultrapassagem",
    },
    {
        "ID_Unidade": "U003",
        "Unidade": "Nexus Belo Horizonte Metals",
        "Cidade": "Belo Horizonte",
        "UF": "MG",
        "TipoUnidade": "Fabrica",
        "PerfilOperacao": "continuous",
        "Area_m2": 31000,
        "Funcionarios": 510,
        "PotenciaFV_kWp": 0,
        "DemandaContratada_kW": 2100,
        "TarifaPonta_R_kWh": 1.48,
        "TarifaForaPonta_R_kWh": 0.66,
        "TarifaDemanda_R_kW": 45.0,
        "PenalidadeUltrapassagem_R_kW": 90.0,
        "ImpostosPercentual": 0.252,
        "OutrosEncargos_R": 12400,
        "BaseLoad_kW": 820,
        "PeakLoad_kW": 1680,
        "ProductionBase": 22000,
        "DemandScenario": "superdimensionada",
    },
    {
        "ID_Unidade": "U004",
        "Unidade": "Nexus Vitoria Cold Chain",
        "Cidade": "Vitoria",
        "UF": "ES",
        "TipoUnidade": "Centro de distribuicao refrigerado",
        "PerfilOperacao": "cold_chain",
        "Area_m2": 16000,
        "Funcionarios": 165,
        "PotenciaFV_kWp": 310,
        "DemandaContratada_kW": 880,
        "TarifaPonta_R_kWh": 1.46,
        "TarifaForaPonta_R_kWh": 0.64,
        "TarifaDemanda_R_kW": 44.0,
        "PenalidadeUltrapassagem_R_kW": 88.0,
        "ImpostosPercentual": 0.247,
        "OutrosEncargos_R": 7600,
        "BaseLoad_kW": 390,
        "PeakLoad_kW": 830,
        "ProductionBase": 7600,
        "DemandScenario": "ultrapassagem",
    },
    {
        "ID_Unidade": "U005",
        "Unidade": "Nexus Curitiba Office",
        "Cidade": "Curitiba",
        "UF": "PR",
        "TipoUnidade": "Escritorio administrativo",
        "PerfilOperacao": "office",
        "Area_m2": 6800,
        "Funcionarios": 360,
        "PotenciaFV_kWp": 95,
        "DemandaContratada_kW": 420,
        "TarifaPonta_R_kWh": 1.25,
        "TarifaForaPonta_R_kWh": 0.54,
        "TarifaDemanda_R_kW": 35.0,
        "PenalidadeUltrapassagem_R_kW": 70.0,
        "ImpostosPercentual": 0.225,
        "OutrosEncargos_R": 3400,
        "BaseLoad_kW": 40,
        "PeakLoad_kW": 320,
        "ProductionBase": 0,
        "DemandScenario": "baixa_utilizacao",
    },
    {
        "ID_Unidade": "U006",
        "Unidade": "Nexus Ribeirao Preto Packaging",
        "Cidade": "Ribeirao Preto",
        "UF": "SP",
        "TipoUnidade": "Unidade industrial leve",
        "PerfilOperacao": "industrial_shift",
        "Area_m2": 12500,
        "Funcionarios": 240,
        "PotenciaFV_kWp": 520,
        "DemandaContratada_kW": 790,
        "TarifaPonta_R_kWh": 1.38,
        "TarifaForaPonta_R_kWh": 0.60,
        "TarifaDemanda_R_kW": 40.0,
        "PenalidadeUltrapassagem_R_kW": 80.0,
        "ImpostosPercentual": 0.240,
        "OutrosEncargos_R": 5600,
        "BaseLoad_kW": 145,
        "PeakLoad_kW": 760,
        "ProductionBase": 11800,
        "DemandScenario": "adequada",
    },
]

SECTORS = [
    ("S001", "Producao", ["Fabrica", "Unidade industrial leve"], 0.38),
    ("S002", "Refrigeracao", ["Centro de distribuicao refrigerado", "Centro logistico"], 0.31),
    ("S003", "Climatizacao", ["Fabrica", "Unidade industrial leve", "Centro logistico", "Escritorio administrativo", "Centro de distribuicao refrigerado"], 0.15),
    ("S004", "Iluminacao", ["Fabrica", "Unidade industrial leve", "Centro logistico", "Escritorio administrativo", "Centro de distribuicao refrigerado"], 0.08),
    ("S005", "Compressores", ["Fabrica", "Unidade industrial leve"], 0.16),
    ("S006", "Motores", ["Fabrica", "Unidade industrial leve", "Centro logistico"], 0.17),
    ("S007", "TI", ["Escritorio administrativo", "Centro logistico"], 0.08),
    ("S008", "Administrativo", ["Escritorio administrativo", "Fabrica", "Unidade industrial leve"], 0.05),
    ("S009", "Utilidades", ["Fabrica", "Unidade industrial leve", "Centro de distribuicao refrigerado"], 0.11),
    ("S010", "Carregamento de Veiculos", ["Centro logistico", "Centro de distribuicao refrigerado"], 0.09),
]


def ensure_clean_root() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    for sub in [
        "data",
        "scripts",
        "tests",
        "powerbi",
        "assets/mockups",
        "assets/screenshots",
        "assets/architecture",
        "docs",
    ]:
        (ROOT / sub).mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def seasonality(ts: pd.Timestamp) -> float:
    return 1 + 0.10 * math.sin(2 * math.pi * (ts.dayofyear - 18) / 365)


def temperature(ts: pd.Timestamp, rng: np.random.Generator, city: str) -> float:
    city_offset = {"Curitiba": -3.5, "Belo Horizonte": 0.5, "Vitoria": 2.0, "Ribeirao Preto": 1.5}.get(city, 0)
    daily = 4.2 * math.sin(2 * math.pi * (ts.hour - 14) / 24)
    annual = 5.5 * math.sin(2 * math.pi * (ts.dayofyear - 20) / 365)
    return round(23 + city_offset + daily + annual + rng.normal(0, 1.1), 1)


def operation_factor(profile: str, hour: int, weekday: int) -> float:
    weekend = weekday >= 5
    if profile == "continuous":
        return 0.78 + (0.20 if 7 <= hour <= 21 else 0.05)
    if profile == "industrial_shift":
        if weekend:
            return 0.30 if 7 <= hour <= 18 else 0.18
        return 0.92 if 7 <= hour <= 18 else (0.55 if 19 <= hour <= 22 else 0.26)
    if profile == "logistics":
        if weekend:
            return 0.45 if 8 <= hour <= 20 else 0.25
        return 0.88 if 6 <= hour <= 22 else 0.30
    if profile == "office":
        if weekend:
            return 0.16
        return 0.88 if 8 <= hour <= 18 else 0.18
    if profile == "cold_chain":
        return 0.82 + (0.10 if 10 <= hour <= 19 else 0.00)
    return 0.5


def solar_generation(ts: pd.Timestamp, kWp: float, temp_c: float, rng: np.random.Generator) -> float:
    if kWp <= 0 or ts.hour < 6 or ts.hour > 18:
        return 0.0
    sun = math.sin(math.pi * (ts.hour - 6) / 12)
    if sun <= 0:
        return 0.0
    seasonal = 0.87 + 0.17 * math.sin(2 * math.pi * (ts.dayofyear - 235) / 365)
    temp_loss = max(0.88, 1 - max(temp_c - 25, 0) * 0.004)
    cloud = rng.uniform(0.68, 1.04)
    return round(kWp * sun * seasonal * temp_loss * cloud * 0.82, 3)


def build_dimensions() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    dim_units = pd.DataFrame(UNITS)
    dim_setor = pd.DataFrame(
        [{"ID_Setor": s, "Setor": n, "TiposUnidadeAplicaveis": ", ".join(t), "PesoReferencia": w} for s, n, t, w in SECTORS]
    )
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    cal = pd.DataFrame({"Data": dates.date})
    cal["Ano"] = dates.year
    cal["Mes"] = dates.month_name(locale=None)
    cal["NumeroMes"] = dates.month
    cal["MesAno"] = dates.strftime("%Y-%m")
    cal["Trimestre"] = "Q" + dates.quarter.astype(str)
    cal["Semana"] = dates.isocalendar().week.astype(int).to_numpy()
    cal["Dia"] = dates.day
    cal["DiaSemana"] = dates.weekday
    cal["NomeDiaSemana"] = dates.day_name()
    cal["DiaUtil"] = dates.weekday < 5
    cal["FimSemana"] = dates.weekday >= 5
    cal["InicioMes"] = dates.is_month_start
    cal["FimMes"] = dates.is_month_end

    hours = list(range(24))
    dim_tempo = pd.DataFrame({"Hora": hours})
    dim_tempo["FaixaHoraria"] = dim_tempo["Hora"].map(lambda h: f"{h:02d}:00")
    dim_tempo["Turno"] = pd.cut(dim_tempo["Hora"], [-1, 5, 13, 21, 23], labels=["Madrugada", "Manha", "Tarde", "Noite"]).astype(str)
    dim_tempo["Ponta"] = dim_tempo["Hora"].between(18, 20)
    dim_tempo["PeriodoDia"] = dim_tempo["Turno"]

    dim_tarifa = dim_units[
        [
            "ID_Unidade",
            "TarifaPonta_R_kWh",
            "TarifaForaPonta_R_kWh",
            "DemandaContratada_kW",
            "TarifaDemanda_R_kW",
            "PenalidadeUltrapassagem_R_kW",
            "ImpostosPercentual",
            "OutrosEncargos_R",
        ]
    ].copy()
    dim_tarifa["InicioPonta"] = "18:00"
    dim_tarifa["FimPonta"] = "21:00"
    dim_tarifa["ModeloTarifario"] = "Time-of-use sintetico parametrizavel"
    return dim_units, dim_setor, cal, dim_tempo, dim_tarifa


def build_hourly_data(dim_units: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    timestamps = pd.date_range(START, END, freq="h")
    rows = []
    for unit in UNITS:
        sectors = [(sid, name, weight) for sid, name, types, weight in SECTORS if unit["TipoUnidade"] in types]
        weight_total = sum(w for _, _, w in sectors)
        normalized = [(sid, name, w / weight_total) for sid, name, w in sectors]
        for ts in timestamps:
            weekday = ts.weekday()
            op = operation_factor(unit["PerfilOperacao"], ts.hour, weekday)
            temp_c = temperature(ts, rng, unit["Cidade"])
            hvac_boost = max(temp_c - 25, 0) * 0.018
            weekend_boost = 0.0
            if unit["ID_Unidade"] == "U004" and weekday >= 5 and 9 <= ts.hour <= 17:
                weekend_boost = 0.10
            total_kw = unit["BaseLoad_kW"] + unit["PeakLoad_kW"] * op * seasonality(ts) * (1 + hvac_boost + weekend_boost)
            if unit["ID_Unidade"] == "U002" and ts.month in [3, 8, 11] and 18 <= ts.hour <= 20 and weekday < 5:
                total_kw *= 1.16
            if unit["ID_Unidade"] == "U004" and ts.month in [1, 2, 12] and 13 <= ts.hour <= 18:
                total_kw *= 1.11
            total_kw *= rng.normal(1, 0.045)
            gen_total = solar_generation(ts, unit["PotenciaFV_kWp"], temp_c, rng)
            for sid, sector, share in normalized:
                factor = 1.0
                if sector in ["Climatizacao", "Refrigeracao"]:
                    factor += hvac_boost * 2.2
                if sector == "Iluminacao" and (ts.hour < 6 or ts.hour > 18):
                    factor += 0.24
                if sector == "Carregamento de Veiculos" and 19 <= ts.hour <= 23:
                    factor += 0.40
                demand_kw = max(0, total_kw * share * factor * rng.normal(1, 0.035))
                gen_kwh = gen_total * share if sector in ["Producao", "Climatizacao", "Utilidades", "Administrativo"] else gen_total * share * 0.45
                import_kwh = max(demand_kw - gen_kwh, 0)
                export_kwh = max(gen_kwh - demand_kw, 0)
                fp = np.clip(rng.normal(0.955, 0.018), 0.86, 0.995)
                if unit["ID_Unidade"] == "U003" and sector in ["Motores", "Compressores"] and ts.month in [5, 6]:
                    fp -= 0.055
                voltage = rng.normal(380, 5.5)
                current = (demand_kw * 1000) / (math.sqrt(3) * voltage * max(fp, 0.7))
                rows.append(
                    {
                        "Timestamp": ts,
                        "Data": ts.date(),
                        "Hora": ts.hour,
                        "ID_Unidade": unit["ID_Unidade"],
                        "ID_Setor": sid,
                        "Consumo_kWh": round(demand_kw, 3),
                        "Demanda_kW": round(demand_kw, 3),
                        "GeracaoSolar_kWh": round(gen_kwh, 3),
                        "ImportacaoRede_kWh": round(import_kwh, 3),
                        "ExportacaoRede_kWh": round(export_kwh, 3),
                        "AutoconsumoSolar_kWh": round(min(demand_kw, gen_kwh), 3),
                        "EnergiaEvitadaRede_kWh": round(min(demand_kw, gen_kwh), 3),
                        "Temperatura_C": temp_c,
                        "DiaUtil": weekday < 5,
                        "HorarioPonta": 18 <= ts.hour < 21,
                        "FatorPotencia": round(float(fp), 4),
                        "Tensao_V": round(float(voltage), 1),
                        "Corrente_A": round(float(current), 2),
                        "StatusMedicao": "Valida",
                        "FatorEmissao_kgCO2_kWh": CO2_FACTOR,
                        "Emissao_kgCO2e": round(import_kwh * CO2_FACTOR, 4),
                        "Emissao_tCO2e": round(import_kwh * CO2_FACTOR / 1000, 6),
                        "EmissaoEvitadaSolar_tCO2e": round(min(demand_kw, gen_kwh) * CO2_FACTOR / 1000, 6),
                    }
                )
    df = pd.DataFrame(rows)
    monthly_sector = df.groupby(["ID_Unidade", pd.Grouper(key="Timestamp", freq="MS"), "ID_Setor"])["Consumo_kWh"].transform("mean")
    df["BaselineConsumo_kWh"] = monthly_sector.round(3)
    df["DesvioBaseline_kWh"] = (df["Consumo_kWh"] - df["BaselineConsumo_kWh"]).round(3)
    # Deterministic synthetic incidents for anomaly coverage.
    night_mask = (df["ID_Unidade"].eq("U005")) & (df["Timestamp"].between("2025-07-12 00:00", "2025-07-12 05:00")) & (df["ID_Setor"].eq("S003"))
    df.loc[night_mask, ["Consumo_kWh", "Demanda_kW", "ImportacaoRede_kWh"]] *= 2.6
    spike_mask = (df["ID_Unidade"].eq("U002")) & (df["Timestamp"].between("2025-08-19 18:00", "2025-08-19 20:00"))
    df.loc[spike_mask, ["Consumo_kWh", "Demanda_kW", "ImportacaoRede_kWh"]] *= 1.55
    solar_drop = (df["ID_Unidade"].eq("U006")) & (df["Timestamp"].between("2025-10-03 10:00", "2025-10-03 15:00"))
    df.loc[solar_drop, ["GeracaoSolar_kWh", "AutoconsumoSolar_kWh", "EnergiaEvitadaRede_kWh"]] *= 0.18
    df["AutoconsumoSolar_kWh"] = np.minimum(df["Consumo_kWh"], df["GeracaoSolar_kWh"]).round(3)
    df["EnergiaEvitadaRede_kWh"] = df["AutoconsumoSolar_kWh"]
    df["ImportacaoRede_kWh"] = np.maximum(df["Consumo_kWh"] - df["GeracaoSolar_kWh"], 0).round(3)
    df["ExportacaoRede_kWh"] = np.maximum(df["GeracaoSolar_kWh"] - df["Consumo_kWh"], 0).round(3)
    df["Emissao_kgCO2e"] = (df["ImportacaoRede_kWh"] * CO2_FACTOR).round(4)
    df["Emissao_tCO2e"] = (df["Emissao_kgCO2e"] / 1000).round(6)
    return df


def build_costs(fact: pd.DataFrame, dim_tarifa: pd.DataFrame) -> pd.DataFrame:
    merged = fact.merge(dim_tarifa, on="ID_Unidade", how="left")
    merged["MesAno"] = pd.to_datetime(merged["Timestamp"]).dt.strftime("%Y-%m")
    rows = []
    for (unit, mes), g in merged.groupby(["ID_Unidade", "MesAno"]):
        tariff = g.iloc[0]
        ponta = g.loc[g["HorarioPonta"], "ImportacaoRede_kWh"].sum()
        fora = g.loc[~g["HorarioPonta"], "ImportacaoRede_kWh"].sum()
        demand_max = g.groupby("Timestamp")["Demanda_kW"].sum().max()
        contracted = tariff["DemandaContratada_kW"]
        excess = max(demand_max - contracted, 0)
        custo_ponta = ponta * tariff["TarifaPonta_R_kWh"]
        custo_fora = fora * tariff["TarifaForaPonta_R_kWh"]
        custo_energia = custo_ponta + custo_fora
        custo_demanda = max(demand_max, contracted * 0.9) * tariff["TarifaDemanda_R_kW"]
        custo_ultra = excess * tariff["PenalidadeUltrapassagem_R_kW"]
        impostos = (custo_energia + custo_demanda + custo_ultra) * tariff["ImpostosPercentual"]
        outros = tariff["OutrosEncargos_R"]
        total = custo_energia + custo_demanda + custo_ultra + impostos + outros
        consumo = g["Consumo_kWh"].sum()
        solar_auto = g["AutoconsumoSolar_kWh"].sum()
        rows.append(
            {
                "MesAno": mes,
                "ID_Unidade": unit,
                "Consumo_kWh": round(consumo, 2),
                "Consumo_MWh": round(consumo / 1000, 2),
                "ImportacaoRede_kWh": round(g["ImportacaoRede_kWh"].sum(), 2),
                "GeracaoSolar_kWh": round(g["GeracaoSolar_kWh"].sum(), 2),
                "AutoconsumoSolar_kWh": round(solar_auto, 2),
                "ExportacaoRede_kWh": round(g["ExportacaoRede_kWh"].sum(), 2),
                "DemandaMaxima_kW": round(demand_max, 2),
                "DemandaContratada_kW": round(contracted, 2),
                "DemandaFaturavel_kW": round(max(demand_max, contracted * 0.9), 2),
                "ExcessoDemanda_kW": round(excess, 2),
                "UtilizacaoDemandaPercentual": round(demand_max / contracted, 4),
                "CustoPonta_R": round(custo_ponta, 2),
                "CustoForaPonta_R": round(custo_fora, 2),
                "CustoEnergia_R": round(custo_energia, 2),
                "CustoDemanda_R": round(custo_demanda, 2),
                "CustoUltrapassagem_R": round(custo_ultra, 2),
                "Impostos_R": round(impostos, 2),
                "OutrosCustos_R": round(outros, 2),
                "CustoTotal_R": round(total, 2),
                "CustoMedio_R_kWh": round(total / consumo, 4),
                "EconomiaSolar_R": round(solar_auto * tariff["TarifaForaPonta_R_kWh"], 2),
                "Emissao_tCO2e": round(g["Emissao_tCO2e"].sum(), 4),
                "EmissaoEvitadaSolar_tCO2e": round(g["EmissaoEvitadaSolar_tCO2e"].sum(), 4),
            }
        )
    return pd.DataFrame(rows)


def build_opportunities(costs: pd.DataFrame, fact: pd.DataFrame) -> pd.DataFrame:
    annual = costs.groupby("ID_Unidade").agg({"Consumo_kWh": "sum", "CustoMedio_R_kWh": "mean", "ExcessoDemanda_kW": "sum"}).reset_index()
    templates = [
        ("Iluminacao LED", "Substituir luminarias convencionais por LED industrial", 0.035, 185000, "Alta"),
        ("Gestao de demanda", "Reprogramar cargas flexiveis fora do horario de ponta", 0.020, 90000, "Alta"),
        ("Inversores de frequencia", "Aplicar VFDs em motores com carga variavel", 0.045, 260000, "Media"),
        ("Compressores", "Eliminar vazamentos e otimizar setpoints de ar comprimido", 0.028, 120000, "Alta"),
        ("Climatizacao", "Ajustar automacao, setpoints e manutencao preditiva", 0.025, 110000, "Media"),
        ("Solar FV", "Ampliar geracao fotovoltaica em area disponivel", 0.050, 620000, "Media"),
    ]
    rows = []
    idx = 1
    for _, u in annual.iterrows():
        unit = next(x for x in UNITS if x["ID_Unidade"] == u["ID_Unidade"])
        selected = templates[:4] if unit["PotenciaFV_kWp"] else templates[1:5]
        for cat, desc, pct, invest, prio in selected:
            saving_kwh = u["Consumo_kWh"] * pct
            saving_r = saving_kwh * u["CustoMedio_R_kWh"]
            if cat == "Gestao de demanda" and u["ExcessoDemanda_kW"] > 0:
                saving_r += min(u["ExcessoDemanda_kW"], 1200) * 55
            rows.append(
                {
                    "ID_Oportunidade": f"OPP{idx:03d}",
                    "ID_Unidade": u["ID_Unidade"],
                    "Categoria": cat,
                    "Descricao": desc,
                    "Investimento_R": round(invest * (0.75 + 0.5 * np.random.default_rng(SEED + idx).random()), 2),
                    "Economia_kWh_Ano": round(saving_kwh, 2),
                    "Economia_R_Ano": round(saving_r, 2),
                    "Payback_Anos": round((invest / max(saving_r, 1)), 2),
                    "Prioridade": prio,
                    "Status": "Priorizada" if prio == "Alta" else "Em avaliacao",
                }
            )
            idx += 1
    return pd.DataFrame(rows)


def build_alerts(fact: pd.DataFrame, costs: pd.DataFrame) -> pd.DataFrame:
    alerts = []
    idx = 1
    hourly_unit = fact.groupby(["Timestamp", "ID_Unidade"]).agg(
        Consumo=("Consumo_kWh", "sum"),
        Baseline=("BaselineConsumo_kWh", "sum"),
        Demanda=("Demanda_kW", "sum"),
        FP=("FatorPotencia", "mean"),
        Solar=("GeracaoSolar_kWh", "sum"),
    ).reset_index()
    hourly_unit["Desvio"] = (hourly_unit["Consumo"] - hourly_unit["Baseline"]) / hourly_unit["Baseline"].replace(0, np.nan)
    candidates = pd.concat(
        [
            hourly_unit.nlargest(16, "Desvio"),
            hourly_unit[hourly_unit["FP"] < 0.91].head(12),
            hourly_unit[(hourly_unit["Solar"] < 5) & (hourly_unit["Timestamp"].dt.hour.between(10, 15))].head(8),
        ],
        ignore_index=True,
    ).drop_duplicates(["Timestamp", "ID_Unidade"])
    for _, r in candidates.head(36).iterrows():
        if r["FP"] < 0.91:
            tipo, sev = "Fator de potencia baixo", "Media"
            measured, expected = r["FP"], 0.95
        elif r["Desvio"] > 0.40:
            tipo, sev = "Consumo anormal", "Alta" if r["Desvio"] > 0.65 else "Media"
            measured, expected = r["Consumo"], r["Baseline"]
        else:
            tipo, sev = "Geracao solar abaixo do esperado", "Media"
            measured, expected = r["Solar"], 80
        alerts.append(
            {
                "ID_Alerta": f"ALT{idx:03d}",
                "Timestamp": r["Timestamp"],
                "ID_Unidade": r["ID_Unidade"],
                "TipoAlerta": tipo,
                "Severidade": sev,
                "ValorMedido": round(float(measured), 3),
                "ValorEsperado": round(float(expected), 3),
                "DesvioPercentual": round(float((measured - expected) / expected), 4) if expected else 0,
                "Status": "Aberto" if sev == "Alta" else "Em analise",
                "Descricao": f"{tipo} identificado por regra estatistica sintetica.",
            }
        )
        idx += 1
    for _, r in costs[costs["ExcessoDemanda_kW"] > 0].nlargest(12, "ExcessoDemanda_kW").iterrows():
        alerts.append(
            {
                "ID_Alerta": f"ALT{idx:03d}",
                "Timestamp": pd.to_datetime(r["MesAno"] + "-01"),
                "ID_Unidade": r["ID_Unidade"],
                "TipoAlerta": "Ultrapassagem de demanda",
                "Severidade": "Critica" if r["ExcessoDemanda_kW"] > 80 else "Alta",
                "ValorMedido": r["DemandaMaxima_kW"],
                "ValorEsperado": r["DemandaContratada_kW"],
                "DesvioPercentual": round((r["DemandaMaxima_kW"] - r["DemandaContratada_kW"]) / r["DemandaContratada_kW"], 4),
                "Status": "Aberto",
                "Descricao": "Demanda maxima mensal acima da contratada.",
            }
        )
        idx += 1
    return pd.DataFrame(alerts)


def save_dataframes(dataframes: dict[str, pd.DataFrame]) -> None:
    for name, df in dataframes.items():
        df.to_csv(ROOT / "data" / f"{name}.csv", index=False, encoding="utf-8")
    with pd.ExcelWriter(ROOT / "Energy_Management_Data.xlsx", engine="openpyxl") as writer:
        for name, df in dataframes.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)


def insights(costs: pd.DataFrame, fact: pd.DataFrame, opps: pd.DataFrame, alerts: pd.DataFrame, dim_units: pd.DataFrame) -> list[str]:
    unit_names = dim_units.set_index("ID_Unidade")["Unidade"].to_dict()
    annual = costs.groupby("ID_Unidade").agg(
        Consumo_kWh=("Consumo_kWh", "sum"),
        CustoTotal_R=("CustoTotal_R", "sum"),
        DemandaMaxima_kW=("DemandaMaxima_kW", "max"),
        DemandaContratada_kW=("DemandaContratada_kW", "max"),
        EconomiaSolar_R=("EconomiaSolar_R", "sum"),
        GeracaoSolar_kWh=("GeracaoSolar_kWh", "sum"),
        ImportacaoRede_kWh=("ImportacaoRede_kWh", "sum"),
        EmissaoEvitadaSolar_tCO2e=("EmissaoEvitadaSolar_tCO2e", "sum"),
    )
    annual["FatorCarga"] = annual["Consumo_kWh"] / (annual["DemandaMaxima_kW"] * 8760)
    annual["GridDependency"] = annual["ImportacaoRede_kWh"] / annual["Consumo_kWh"]
    total_consumption = annual["Consumo_kWh"].sum()
    top_consumer = annual["Consumo_kWh"].idxmax()
    top_cost = annual["CustoTotal_R"].idxmax()
    low_lf = annual["FatorCarga"].idxmin()
    over = ((annual["DemandaMaxima_kW"] / annual["DemandaContratada_kW"]) - 1).idxmax()
    under = (annual["DemandaMaxima_kW"] / annual["DemandaContratada_kW"]).idxmin()
    top_solar = annual["EconomiaSolar_R"].idxmax()
    top_grid = annual["GridDependency"].idxmax()
    alert_top = alerts["ID_Unidade"].value_counts().idxmax()
    opp_top = opps.groupby("ID_Unidade")["Economia_R_Ano"].sum().idxmax()
    return [
        f"{unit_names[top_consumer]} concentra {annual.loc[top_consumer, 'Consumo_kWh'] / total_consumption:.1%} do consumo anual.",
        f"{unit_names[top_cost]} apresenta o maior custo anual: R$ {annual.loc[top_cost, 'CustoTotal_R']:,.0f}.",
        f"{unit_names[over]} tem o maior risco de demanda, com pico {annual.loc[over, 'DemandaMaxima_kW'] / annual.loc[over, 'DemandaContratada_kW']:.1%} da demanda contratada.",
        f"{unit_names[under]} mostra baixa utilizacao contratada: {annual.loc[under, 'DemandaMaxima_kW'] / annual.loc[under, 'DemandaContratada_kW']:.1%}.",
        f"{unit_names[low_lf]} tem o menor fator de carga anual: {annual.loc[low_lf, 'FatorCarga']:.2f}.",
        f"{unit_names[top_solar]} gera a maior economia solar anual: R$ {annual.loc[top_solar, 'EconomiaSolar_R']:,.0f}.",
        f"A geracao solar evitou {annual['EmissaoEvitadaSolar_tCO2e'].sum():,.1f} tCO2e no ano sintetico.",
        f"{unit_names[top_grid]} possui a maior dependencia da rede: {annual.loc[top_grid, 'GridDependency']:.1%}.",
        f"{unit_names[opp_top]} tem o maior potencial financeiro em oportunidades: R$ {opps.groupby('ID_Unidade')['Economia_R_Ano'].sum().loc[opp_top]:,.0f}/ano.",
        f"{unit_names[alert_top]} concentra o maior numero de alertas operacionais: {alerts['ID_Unidade'].value_counts().loc[alert_top]} eventos.",
    ]


def draw_mockup(path: Path, title: str, accent: tuple[int, int, int]) -> None:
    img = Image.new("RGB", (1440, 900), (246, 248, 247))
    d = ImageDraw.Draw(img)
    try:
        font_big = ImageFont.truetype("arial.ttf", 42)
        font_med = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font_big = font_med = font_small = ImageFont.load_default()
    d.rectangle([0, 0, 1440, 76], fill=(22, 45, 52))
    d.text((42, 20), title, fill=(255, 255, 255), font=font_big)
    d.rectangle([0, 76, 210, 900], fill=(33, 55, 62))
    nav = ["Executive", "Consumption", "Demand", "Cost", "Solar", "Efficiency", "Alerts", "Unit Detail"]
    for i, n in enumerate(nav):
        y = 120 + i * 54
        fill = accent if n.lower().split()[0] in title.lower() else (54, 76, 83)
        d.rounded_rectangle([22, y, 188, y + 38], radius=6, fill=fill)
        d.text((38, y + 9), n, fill=(255, 255, 255), font=font_small)
    card_w = 270
    for i, label in enumerate(["Consumo", "Custo", "Demanda", "Solar"]):
        x = 250 + i * 292
        d.rounded_rectangle([x, 112, x + card_w, 228], radius=8, fill=(255, 255, 255), outline=(218, 224, 224))
        d.text((x + 22, 132), label, fill=(70, 80, 84), font=font_small)
        d.text((x + 22, 166), ["28.4 GWh", "R$ 23.1M", "1,982 kW", "3.2 GWh"][i], fill=(23, 43, 49), font=font_med)
    # chart panels
    panels = [(250, 270, 820, 565), (850, 270, 1365, 565), (250, 610, 760, 850), (790, 610, 1365, 850)]
    for p in panels:
        d.rounded_rectangle(p, radius=8, fill=(255, 255, 255), outline=(218, 224, 224))
    rng = np.random.default_rng(abs(hash(title)) % 10000)
    for p in panels[:2]:
        x0, y0, x1, y1 = p
        pts = []
        for i in range(12):
            x = x0 + 40 + i * ((x1 - x0 - 80) / 11)
            y = y1 - 45 - (rng.random() * 0.65 + 0.2) * (y1 - y0 - 95)
            pts.append((x, y))
        d.line(pts, fill=accent, width=5)
        for x, y in pts:
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=accent)
    for p in panels[2:]:
        x0, y0, x1, y1 = p
        for i in range(10):
            h = int((rng.random() * 0.7 + 0.15) * (y1 - y0 - 80))
            x = x0 + 40 + i * 44
            d.rectangle([x, y1 - 35 - h, x + 28, y1 - 35], fill=accent)
    d.text((250, 70), "Nexus Industrial Group | Dados sinteticos 2025", fill=(101, 114, 118), font=font_small)
    img.save(path)


def create_mockups() -> None:
    pages = {
        "executive": ("Executive Overview", (0, 106, 92)),
        "consumption": ("Consumption Analytics", (0, 121, 145)),
        "demand": ("Demand Management", (27, 94, 132)),
        "cost": ("Cost & Tariff", (82, 101, 112)),
        "solar": ("Solar & Renewables", (30, 132, 73)),
        "efficiency": ("Energy Efficiency", (71, 124, 95)),
        "alerts": ("Alerts & Anomalies", (202, 92, 30)),
        "unit_detail": ("Unit Detail", (0, 106, 92)),
    }
    for file, (title, accent) in pages.items():
        draw_mockup(ROOT / "assets" / "mockups" / f"{file}.png", title, accent)
    screenshot_map = {
        "executive_dashboard.png": "Executive Overview",
        "load_profile.png": "Consumption Analytics",
        "demand_management.png": "Demand Management",
        "cost_analysis.png": "Cost & Tariff",
        "solar_dashboard.png": "Solar & Renewables",
        "efficiency_dashboard.png": "Energy Efficiency",
        "alerts_dashboard.png": "Alerts & Anomalies",
    }
    for filename, source in screenshot_map.items():
        source_file = source.lower().replace(" & ", "_").replace(" ", "_")
        lookup = {
            "executive_overview": "executive.png",
            "consumption_analytics": "consumption.png",
            "demand_management": "demand.png",
            "cost_tariff": "cost.png",
            "solar_renewables": "solar.png",
            "energy_efficiency": "efficiency.png",
            "alerts_anomalies": "alerts.png",
        }
        shutil.copy(ROOT / "assets" / "mockups" / lookup[source_file], ROOT / "assets" / "screenshots" / filename)
    draw_data_model()


def draw_data_model() -> None:
    img = Image.new("RGB", (1400, 850), (248, 250, 249))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small = ImageFont.truetype("arial.ttf", 17)
    except OSError:
        font = small = ImageFont.load_default()
    d.text((40, 30), "Modelo estrela - Energy Management Dashboard", fill=(21, 44, 51), font=font)
    facts = [("Fato_MedicoesEnergia", 530, 205), ("Fato_CustosEnergia", 540, 460), ("Fato_Oportunidades", 910, 465), ("Fato_Alertas", 200, 465)]
    dims = [("Dim_Calendario", 130, 145), ("Dim_Tempo", 520, 95), ("Dim_Unidade", 920, 145), ("Dim_Setor", 170, 680), ("Dim_Tarifa", 930, 680), ("Dim_Status", 540, 695)]
    for name, x, y in dims:
        d.rounded_rectangle([x, y, x + 245, y + 90], radius=8, fill=(234, 241, 239), outline=(157, 179, 175), width=2)
        d.text((x + 18, y + 30), name, fill=(22, 45, 52), font=small)
    for name, x, y in facts:
        d.rounded_rectangle([x, y, x + 300, y + 110], radius=8, fill=(22, 45, 52), outline=(0, 106, 92), width=3)
        d.text((x + 22, y + 40), name, fill=(255, 255, 255), font=small)
    for x1, y1, x2, y2 in [(375, 190, 530, 250), (642, 185, 665, 205), (920, 190, 830, 250), (395, 725, 530, 285), (930, 725, 690, 570), (665, 695, 665, 570)]:
        d.line([x1, y1, x2, y2], fill=(94, 121, 124), width=3)
    img.save(ROOT / "assets" / "architecture" / "data_model.png")


def write_project_files(dataframes: dict[str, pd.DataFrame], insight_lines: list[str]) -> None:
    readme = f"""
    # Energy Management Dashboard

    Electrical Engineering • Energy Analytics • Power BI • Energy Efficiency

    ## Overview

    Professional portfolio case for energy management using synthetic hourly data for Nexus Industrial Group. The project combines electrical engineering concepts, demand management, solar generation, cost analytics, anomaly detection, and Power BI-ready modeling.

    ## Business Problem

    Industrial and commercial sites need to understand when, where, and why energy consumption, demand peaks, tariff exposure, and operational inefficiencies occur.

    ## Objective

    Build a reproducible analytics project that answers energy, demand, cost, solar, emissions, and efficiency questions with a star-schema dataset, documented DAX, Power Query guidance, dashboard mockups, and a Streamlit demo.

    ## Dashboard Preview

    See `assets/mockups/` and `assets/screenshots/` for the designed pages.

    ## Dataset

    The dataset covers {START[:10]} to {END[:10]} at hourly grain. All records are synthetic and technically plausible. No real invoices, contracts, customer identifiers, or confidential data are used.

    ## Data Model

    Star schema with `Fato_MedicoesEnergia`, `Fato_CustosEnergia`, `Fato_Oportunidades`, and `Fato_Alertas`, connected to calendar, time, unit, sector, and tariff dimensions.

    ## KPIs

    Main KPIs include total consumption, monthly consumption, maximum demand, contracted demand utilization, load factor, total cost, average cost per kWh, peak/off-peak cost, solar coverage, self-consumption, grid dependency, avoided emissions, baseline deviation, and potential savings.

    ## Technologies

    Python, pandas, NumPy, Power BI, DAX, Power Query, Streamlit, Plotly, pytest, Excel.

    ## How to Run

    ```bash
    pip install -r requirements.txt
    python scripts/generate_energy_data.py
    python scripts/validate_energy_data.py
    pytest -q
    streamlit run app.py
    ```

    ## Privacy

    All data is synthetic. Tariff values, operating profiles, solar generation, emissions, and savings assumptions are modeled for portfolio demonstration and should not be treated as official regulatory values.

    ## Disclaimer

    This project is an engineering analytics case. It does not replace a certified energy audit, utility invoice validation, regulatory tariff study, or electrical design.

    ## Author

    Portfolio project by Lucas.
    """
    write_text(ROOT / "README.md", readme)
    write_text(ROOT / "README_PT-BR.md", readme.replace("# Energy Management Dashboard", "# Dashboard de Gestão e Analytics de Energia").replace("Overview", "Visão Geral").replace("Business Problem", "Problema de Negócio"))
    write_text(ROOT / "LICENSE", "MIT License\n\nCopyright (c) 2026 Lucas\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files.")
    write_text(ROOT / ".gitignore", "__pycache__/\n.pytest_cache/\n.streamlit/\n*.pyc\n.env\n")
    write_text(ROOT / "requirements.txt", "pandas>=2.0\nnumpy>=1.24\nopenpyxl>=3.1\nstreamlit>=1.32\nplotly>=5.18\npytest>=8.0\nPillow>=10.0\n")

    write_text(ROOT / "docs" / "insights.md", "# Insights\n\n" + "\n".join(f"{i+1}. {line}" for i, line in enumerate(insight_lines)))
    write_text(ROOT / "docs" / "recommendations.md", """
    # Executive Recommendations

    | Prioridade | Problema identificado | Evidência | Ação sugerida | Impacto esperado |
    | --- | --- | --- | --- | --- |
    | Alta | Ultrapassagem de demanda em unidades operacionais | Alertas e custos de ultrapassagem concentrados em logística e refrigeração | Revisar demanda contratada e deslocar cargas flexíveis | Redução de penalidades e melhor previsibilidade |
    | Alta | Base load elevado em operação contínua | Menor fator de carga e consumo noturno relevante | Investigar cargas permanentes, compressores e utilidades | Redução de consumo fora do horário produtivo |
    | Média | Dependência elevada da rede em unidades sem FV | Baixa cobertura solar anual | Avaliar expansão fotovoltaica com estudo técnico-financeiro | Redução de importação, custo e emissões |
    | Média | Fator de potência baixo em eventos simulados | Alertas de FP abaixo de referência | Inspecionar banco de capacitores e cargas indutivas | Redução de risco operacional e melhoria elétrica |
    | Alta | Oportunidades com payback curto | Carteira anual de economia por unidade | Priorizar LED, demanda, compressores e automação | Captura rápida de economia operacional |
    """)
    write_text(ROOT / "docs" / "methodology.md", """
    # Methodology

    The dataset is synthetic and reproducible. Hourly load is generated from unit-specific base load, operating profile, weekday/weekend behavior, seasonality, temperature sensitivity, sector allocation, and controlled noise. Solar generation uses installed kWp, daylight hours, seasonal irradiance proxy, temperature losses, and cloud variability. Costs are calculated from configurable peak/off-peak energy tariffs, contracted demand, demand charge, exceedance penalty, taxes, and fixed charges. Baseline consumption is estimated by unit, month, and sector average and used for deviation analysis. Alerts combine engineered synthetic incidents and statistical signals.
    """)
    write_text(ROOT / "docs" / "assumptions.md", """
    # Assumptions

    | Premissa | Valor | Unidade | Tipo | Editável | Descrição |
    | --- | ---: | --- | --- | --- | --- |
    | Período dos dados | 2025 | ano | Synthetic Assumption | Sim | Ano completo em granularidade horária |
    | Horário de ponta | 18h-21h | hora | Synthetic Assumption | Sim | Parâmetro usado para separar custo ponta e fora ponta |
    | Fator de emissão | 0.0385 | kgCO2e/kWh | Synthetic Assumption | Sim | Valor demonstrativo, não oficial |
    | Tarifa energia | por unidade | R$/kWh | Synthetic Assumption | Sim | Valores plausíveis para simulação |
    | Demanda contratada | por unidade | kW | Synthetic Assumption | Sim | Criada para cobrir cenários adequado, excedido e superdimensionado |
    """)
    write_text(ROOT / "docs" / "executive_summary.md", """
    # Executive Summary

    ## Energy Performance
    The synthetic portfolio shows distinct load profiles by industrial, logistics, office, refrigerated, and continuous operations.

    ## Cost Performance
    Cost is driven by imported grid energy, demand charges, taxes, and exceedance penalties.

    ## Demand Performance
    The model intentionally includes adequate, exceeded, and oversized contracted demand scenarios.

    ## Solar Performance
    Solar generation is limited to daylight hours and allocated to autoconsumption and export.

    ## Efficiency
    Baseline deviations, specific consumption, and opportunities identify where action has the highest operational value.

    ## Risks
    Main risks include peak demand exceedance, low power factor events, weekend consumption, and solar underperformance.

    ## Opportunities
    Prioritized measures include demand management, lighting, compressor optimization, variable frequency drives, HVAC controls, and FV expansion.
    """)
    write_text(ROOT / "docs" / "portfolio_description.md", """
    # Portfolio Description

    Energy Management Dashboard is a professional analytics case that combines electrical engineering, energy management, renewable generation, efficiency diagnostics, Python data engineering, and Power BI modeling. It uses synthetic hourly data to analyze consumption, demand, costs, solar generation, emissions, anomalies, and savings opportunities across multiple fictitious facilities.
    """)
    write_text(ROOT / "docs" / "linkedin_project.md", """
    # LinkedIn Project

    Short description:
    Energy Management Dashboard: projeto de analytics energético com dados horários sintéticos, Power BI, Python e modelo estrela para analisar consumo, demanda, custos, geração solar, emissões, anomalias e oportunidades de eficiência em unidades industriais e comerciais.

    Top skills:
    1. Energy Management
    2. Microsoft Power BI
    3. Data Analytics
    4. Electrical Engineering
    5. Energy Efficiency
    """)
    write_text(ROOT / "docs" / "linkedin_post.md", """
    # LinkedIn Post

    Desenvolvi um projeto de portfólio para responder uma pergunta comum em operações industriais: como transformar medições de energia em decisões práticas?

    O Energy Management Dashboard usa dados horários sintéticos para analisar consumo, demanda máxima, custo de energia, horário de ponta, geração fotovoltaica, autoconsumo, emissões evitadas, baseline, anomalias e oportunidades de eficiência energética.

    A solução combina Python para geração e validação dos dados, modelo estrela para BI, medidas DAX documentadas, Power Query, tema visual, mockups e uma versão Streamlit para demonstração.

    Principais aprendizados: separar corretamente kW de kWh, modelar demanda contratada, evitar conclusões sem baseline e conectar indicadores técnicos a impacto financeiro.

    [LINK GITHUB]
    [LINK DEMO]
    """)
    write_text(ROOT / "docs" / "resume_bullet_points.md", """
    # Resume Bullet Points

    ## Versão curta
    - Desenvolvi dashboard de gestão energética com dados horários sintéticos, integrando consumo, demanda, custos, geração fotovoltaica, emissões e oportunidades de eficiência.

    ## Versão ATS
    - Desenvolveu projeto de Business Intelligence em Power BI para Energy Management, utilizando Python, modelo estrela, DAX e Power Query para análise de consumo kWh, demanda kW, tarifas, custos, geração solar, baseline, anomalias e eficiência energética.

    ## English
    - Built an Energy Management Dashboard using synthetic hourly energy data, Python, star-schema modeling, DAX, and Power BI specifications to analyze consumption, demand, cost, solar generation, emissions, anomalies, and energy efficiency opportunities.
    """)
    write_text(ROOT / "docs" / "interview_case.md", """
    # Interview Case

    1. The project solves the lack of integrated visibility over energy consumption, demand, cost, solar generation, and efficiency opportunities.
    2. Data is structured as a star schema with hourly and monthly fact tables connected to calendar, time, unit, sector, and tariff dimensions.
    3. The load curve is generated from operating profiles, base load, peak load, seasonality, temperature, weekday/weekend behavior, and sector weights.
    4. Energy is measured in kWh and represents consumption over time. Demand is measured in kW and represents power at a point or interval.
    5. Load factor is energy divided by maximum demand times period hours.
    6. Contracted demand is analyzed by comparing monthly maximum demand with the contracted value and calculating utilization and exceedance.
    7. Energy cost is calculated from imported grid energy split by peak/off-peak tariffs, demand charge, exceedance penalty, taxes, and fixed charges.
    8. Peak hours are modeled as configurable parameters, not hardcoded regulation.
    9. Solar generation is modeled from installed kWp, daylight, seasonality, temperature loss, and cloud variability.
    10. Self-consumption is the portion of solar generation used by the site instead of exported.
    11. Solar Coverage equals self-consumed solar energy divided by total consumption.
    12. Anomalies are detected with statistical rules such as z-score, rolling mean, and IQR.
    13. Baseline is built by historical average by unit, month, and sector.
    14. Insights are calculated in `docs/insights.md`.
    15. In a real company, the dashboard would support tariff review, demand management, maintenance prioritization, efficiency projects, and executive reporting.
    """)
    write_text(ROOT / "docs" / "data_dictionary.md", build_data_dictionary(dataframes))
    write_text(ROOT / "docs" / "kpi_dictionary.md", build_kpi_dictionary())
    write_text(ROOT / "powerbi" / "data_model.md", build_data_model_doc())
    write_text(ROOT / "powerbi" / "dashboard_specification.md", build_dashboard_spec())
    write_text(ROOT / "powerbi" / "power_query.md", build_power_query_doc())
    write_text(ROOT / "powerbi" / "dax_measures.md", build_dax())
    write_text(ROOT / "powerbi" / "theme.json", json.dumps(build_theme(), indent=2, ensure_ascii=False))
    write_scripts_and_tests()
    write_streamlit_app()


def build_data_dictionary(dataframes: dict[str, pd.DataFrame]) -> str:
    rows = ["# Data Dictionary\n", "| Tabela | Campo | Tipo | Unidade | Descrição | Exemplo |", "| --- | --- | --- | --- | --- | --- |"]
    unit_map = {"kWh": "kWh", "kW": "kW", "_R": "R$", "Percentual": "%", "CO2": "CO2e", "Temperatura": "C", "Tensao": "V", "Corrente": "A"}
    for table, df in dataframes.items():
        for col in df.columns:
            unit = next((v for k, v in unit_map.items() if k in col), "")
            example = str(df[col].iloc[0])[:45] if len(df) else ""
            rows.append(f"| {table} | {col} | {df[col].dtype} | {unit} | Campo de {table}. | {example} |")
    return "\n".join(rows)


def build_kpi_dictionary() -> str:
    kpis = [
        ("Consumo Total", "Soma de Consumo_kWh", "SUM(Fato_MedicoesEnergia[Consumo_kWh])", "kWh", "Volume total consumido"),
        ("Demanda Maxima", "Maior demanda no periodo", "MAXX(SUMMARIZE(...), [Demanda])", "kW", "Pico de potência"),
        ("Fator de Carga", "Energia / (demanda maxima x horas)", "[Consumo Total kWh] / ([Demanda Maxima kW] * [Horas Periodo])", "%", "Uso da infraestrutura"),
        ("Custo Total", "Energia + demanda + penalidades + impostos", "SUM(Fato_CustosEnergia[CustoTotal_R])", "R$", "Gasto total"),
        ("Custo Medio kWh", "Custo total dividido por consumo", "[Custo Total] / [Consumo Total kWh]", "R$/kWh", "Custo unitário"),
        ("Solar Coverage", "Autoconsumo solar / consumo", "[Autoconsumo Solar] / [Consumo Total kWh]", "%", "Cobertura solar"),
        ("Grid Dependency", "Importação da rede / consumo", "[Importacao Rede] / [Consumo Total kWh]", "%", "Dependência da rede"),
        ("CO2 Evitado", "Autoconsumo solar x fator de emissão", "SUM(Fato_MedicoesEnergia[EmissaoEvitadaSolar_tCO2e])", "tCO2e", "Emissões evitadas"),
    ]
    rows = ["# KPI Dictionary\n", "| Nome | Definição | Fórmula | Unidade | Interpretação | Uso gerencial |", "| --- | --- | --- | --- | --- | --- |"]
    for k in kpis:
        rows.append(f"| {k[0]} | {k[1]} | `{k[2]}` | {k[3]} | {k[4]} | Apoia priorização e acompanhamento. |")
    return "\n".join(rows)


def build_dax() -> str:
    measures = {
        "Consumo Total kWh": "SUM(Fato_MedicoesEnergia[Consumo_kWh])",
        "Consumo Total MWh": "DIVIDE([Consumo Total kWh], 1000)",
        "Demanda Maxima kW": "MAXX(SUMMARIZE(Fato_MedicoesEnergia, Fato_MedicoesEnergia[Timestamp], Dim_Unidade[ID_Unidade], \"DemandaHora\", SUM(Fato_MedicoesEnergia[Demanda_kW])), [DemandaHora])",
        "Demanda Contratada kW": "MAX(Dim_Tarifa[DemandaContratada_kW])",
        "Excesso de Demanda kW": "MAX(0, [Demanda Maxima kW] - [Demanda Contratada kW])",
        "Utilizacao da Demanda %": "DIVIDE([Demanda Maxima kW], [Demanda Contratada kW])",
        "Horas Periodo": "DISTINCTCOUNT(Fato_MedicoesEnergia[Timestamp])",
        "Fator de Carga": "DIVIDE([Consumo Total kWh], [Demanda Maxima kW] * [Horas Periodo])",
        "Custo Total": "SUM(Fato_CustosEnergia[CustoTotal_R])",
        "Custo Medio kWh": "DIVIDE([Custo Total], [Consumo Total kWh])",
        "Custo Demanda": "SUM(Fato_CustosEnergia[CustoDemanda_R])",
        "Custo Energia": "SUM(Fato_CustosEnergia[CustoEnergia_R])",
        "Custo Ponta": "SUM(Fato_CustosEnergia[CustoPonta_R])",
        "Custo Fora Ponta": "SUM(Fato_CustosEnergia[CustoForaPonta_R])",
        "Geracao Solar": "SUM(Fato_MedicoesEnergia[GeracaoSolar_kWh])",
        "Autoconsumo Solar": "SUM(Fato_MedicoesEnergia[AutoconsumoSolar_kWh])",
        "% Energia Solar": "DIVIDE([Autoconsumo Solar], [Consumo Total kWh])",
        "Economia Solar": "SUM(Fato_CustosEnergia[EconomiaSolar_R])",
        "CO2 Evitado": "SUM(Fato_MedicoesEnergia[EmissaoEvitadaSolar_tCO2e])",
        "Importacao Rede": "SUM(Fato_MedicoesEnergia[ImportacaoRede_kWh])",
        "Grid Dependency %": "DIVIDE([Importacao Rede], [Consumo Total kWh])",
        "% Variacao Consumo MoM": "DIVIDE([Consumo Total kWh] - CALCULATE([Consumo Total kWh], DATEADD(Dim_Calendario[Data], -1, MONTH)), CALCULATE([Consumo Total kWh], DATEADD(Dim_Calendario[Data], -1, MONTH)))",
        "% Variacao Custo MoM": "DIVIDE([Custo Total] - CALCULATE([Custo Total], DATEADD(Dim_Calendario[Data], -1, MONTH)), CALCULATE([Custo Total], DATEADD(Dim_Calendario[Data], -1, MONTH)))",
    }
    parts = ["# DAX Measures\n"]
    for name, code in measures.items():
        parts.append(f"## [{name}]\n\n```DAX\n{name} =\n{code}\n```\n\nUnidade/finalidade: medida principal para análise energética e financeira no modelo estrela.\n")
    return "\n".join(parts)


def build_power_query_doc() -> str:
    return """
    # Power Query

    1. Importar todos os CSVs da pasta `data/`.
    2. Definir tipos: datas como Date, Timestamp como DateTime, métricas como Decimal Number, flags como True/False.
    3. Não mesclar fatos entre si no Power Query. Relacionar pelo modelo.
    4. Relacionar `Fato_MedicoesEnergia[Data]` com `Dim_Calendario[Data]`.
    5. Relacionar `Fato_MedicoesEnergia[Hora]` com `Dim_Tempo[Hora]`.
    6. Relacionar fatos a `Dim_Unidade` por `ID_Unidade`.
    7. Relacionar `Fato_MedicoesEnergia` a `Dim_Setor` por `ID_Setor`.
    8. Relacionar `Fato_CustosEnergia` e `Dim_Tarifa` por `ID_Unidade`.

    Example M pattern:

    ```powerquery
    let
        Source = Csv.Document(File.Contents("data/Fato_MedicoesEnergia.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
        PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
        ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {{"Timestamp", type datetime}, {"Data", type date}, {"Consumo_kWh", type number}})
    in
        ChangedTypes
    ```
    """


def build_data_model_doc() -> str:
    return """
    # Data Model

    Grain:
    - `Fato_MedicoesEnergia`: one row per timestamp, unit, and sector.
    - `Fato_CustosEnergia`: one row per month and unit.
    - `Fato_Oportunidades`: one row per simulated opportunity.
    - `Fato_Alertas`: one row per alert event.

    Relationships:
    - `Dim_Calendario[Data]` 1:N `Fato_MedicoesEnergia[Data]`
    - `Dim_Tempo[Hora]` 1:N `Fato_MedicoesEnergia[Hora]`
    - `Dim_Unidade[ID_Unidade]` 1:N all fact tables
    - `Dim_Setor[ID_Setor]` 1:N `Fato_MedicoesEnergia[ID_Setor]`
    - `Dim_Tarifa[ID_Unidade]` 1:1 `Dim_Unidade[ID_Unidade]`

    Use single-direction filters from dimensions to facts. Avoid bidirectional relationships unless a specific drill-through behavior requires it.
    """


def build_dashboard_spec() -> str:
    return """
    # Dashboard Specification

    ## Page 1: Executive Overview
    Cards: Consumo Total, Custo Total, Demanda Máxima, Custo Médio/kWh, Geração Solar, Economia Solar, Emissões Evitadas. Charts: monthly consumption, monthly cost, unit consumption, solar vs consumption, demand by unit.

    ## Page 2: Consumption Analytics
    Load curve, weekday-hour heatmap, consumption by hour, day, sector, unit, peak/off-peak and weekday/weekend.

    ## Page 3: Demand Management
    Demand maximum, contracted demand, utilization, exceedance, demand cost, demand vs contracted, histogram, unit table.

    ## Page 4: Cost & Tariff
    Total cost, energy cost, demand cost, peak/off-peak, exceedance, taxes, average R$/kWh and bill composition.

    ## Page 5: Solar & Renewables
    Installed kWp, generation, self-consumption, export, grid import, avoided energy, financial savings and avoided CO2.

    ## Page 6: Energy Efficiency
    Specific consumption, baseline, actual consumption, deviation, potential savings, investment, payback, opportunity matrix.

    ## Page 7: Alerts & Anomalies
    Alert counts, critical alerts, demand spikes, abnormal consumption, low power factor, solar drop, timeline and operational table.

    ## Page 8: Unit Detail
    Drill-through with unit profile, consumption, demand, cost, tariff, FV, CO2, load factor, intensity, alerts, opportunities and load curve.
    """


def build_theme() -> dict:
    return {
        "name": "Energy Management Executive",
        "dataColors": ["#006A5C", "#007991", "#1B5E84", "#54706F", "#F2A900", "#C0392B"],
        "background": "#F6F8F7",
        "foreground": "#172D34",
        "tableAccent": "#006A5C",
        "visualStyles": {
            "*": {"*": {"fontFamily": "Segoe UI", "color": {"solid": {"color": "#172D34"}}}},
            "card": {"*": {"labels": [{"color": {"solid": {"color": "#172D34"}}, "fontSize": 18}]}},
            "slicer": {"*": {"items": [{"fontSize": 11}], "header": [{"fontSize": 12, "fontColor": {"solid": {"color": "#172D34"}}}]}},
        },
    }


def write_scripts_and_tests() -> None:
    generator = Path(__file__).read_text(encoding="utf-8")
    write_text(ROOT / "scripts" / "generate_energy_data.py", generator)
    write_text(ROOT / "scripts" / "validate_energy_data.py", """
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
    """)
    write_text(ROOT / "scripts" / "detect_anomalies.py", """
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
    """)
    test_common = """from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
fact = pd.read_csv(ROOT / "data" / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp"])
costs = pd.read_csv(ROOT / "data" / "Fato_CustosEnergia.csv")
"""
    tests = {
        "test_energy_balance.py": test_common + "\ndef test_energy_balance():\n    diff = (fact['Consumo_kWh'] - fact['AutoconsumoSolar_kWh'] - fact['ImportacaoRede_kWh'] + fact['ExportacaoRede_kWh']).abs().max()\n    assert diff < 1.0\n",
        "test_demand.py": test_common + "\ndef test_demand_monthly_peak_positive():\n    assert (costs['DemandaMaxima_kW'] > 0).all()\n    assert (costs['UtilizacaoDemandaPercentual'] > 0).all()\n",
        "test_costs.py": test_common + "\ndef test_costs_reconcile():\n    parts = costs[['CustoEnergia_R','CustoDemanda_R','CustoUltrapassagem_R','Impostos_R','OutrosCustos_R']].sum(axis=1)\n    assert ((parts - costs['CustoTotal_R']).abs() < 1.0).all()\n",
        "test_solar.py": test_common + "\ndef test_no_solar_at_night():\n    assert (fact.query('Hora < 6 or Hora > 18')['GeracaoSolar_kWh'] == 0).all()\n",
        "test_tariff.py": test_common + "\ndef test_peak_and_offpeak_costs_exist():\n    assert (costs['CustoPonta_R'] >= 0).all()\n    assert (costs['CustoForaPonta_R'] > 0).all()\n",
        "test_emissions.py": test_common + "\ndef test_emissions_non_negative():\n    assert (fact['Emissao_tCO2e'] >= 0).all()\n    assert (fact['EmissaoEvitadaSolar_tCO2e'] >= 0).all()\n",
        "test_anomalies.py": test_common + "\ndef test_alerts_exist():\n    alerts = pd.read_csv(ROOT / 'data' / 'Fato_Alertas.csv')\n    assert len(alerts) >= 20\n    assert {'Alta','Critica','Media'} & set(alerts['Severidade'])\n",
    }
    for name, content in tests.items():
        write_text(ROOT / "tests" / name, content)


def write_streamlit_app() -> None:
    write_text(ROOT / "app.py", """
    from pathlib import Path
    import pandas as pd
    import plotly.express as px
    import streamlit as st

    ROOT = Path(__file__).resolve().parent
    st.set_page_config(page_title="Energy Management Dashboard", layout="wide")
    st.title("Energy Management Dashboard")

    fact = pd.read_csv(ROOT / "data" / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp", "Data"])
    costs = pd.read_csv(ROOT / "data" / "Fato_CustosEnergia.csv")
    units = pd.read_csv(ROOT / "data" / "Dim_Unidade.csv")
    alerts = pd.read_csv(ROOT / "data" / "Fato_Alertas.csv")
    opps = pd.read_csv(ROOT / "data" / "Fato_Oportunidades.csv")

    unit_options = ["All"] + units["Unidade"].tolist()
    selected_unit = st.sidebar.selectbox("Unidade", unit_options)
    page = st.sidebar.radio("Page", ["Executive", "Consumption", "Demand", "Cost", "Solar", "Efficiency", "Alerts"])
    if selected_unit != "All":
        uid = units.loc[units["Unidade"].eq(selected_unit), "ID_Unidade"].iloc[0]
        fact = fact[fact["ID_Unidade"].eq(uid)]
        costs = costs[costs["ID_Unidade"].eq(uid)]
        alerts = alerts[alerts["ID_Unidade"].eq(uid)]
        opps = opps[opps["ID_Unidade"].eq(uid)]

    def cards(values):
        cols = st.columns(len(values))
        for col, (label, value) in zip(cols, values):
            col.metric(label, value)

    if page == "Executive":
        cards([
            ("Consumo", f"{fact['Consumo_kWh'].sum()/1000:,.1f} MWh"),
            ("Custo", f"R$ {costs['CustoTotal_R'].sum()/1_000_000:,.2f}M"),
            ("Demanda Max", f"{costs['DemandaMaxima_kW'].max():,.0f} kW"),
            ("Solar", f"{fact['GeracaoSolar_kWh'].sum()/1000:,.1f} MWh"),
        ])
        monthly = costs.groupby("MesAno", as_index=False)[["Consumo_MWh", "CustoTotal_R"]].sum()
        st.plotly_chart(px.line(monthly, x="MesAno", y="Consumo_MWh", title="Consumo mensal (MWh)"), use_container_width=True)
        by_unit = costs.groupby("ID_Unidade", as_index=False)["CustoTotal_R"].sum().merge(units[["ID_Unidade", "Unidade"]])
        st.plotly_chart(px.bar(by_unit, x="Unidade", y="CustoTotal_R", title="Custo por unidade"), use_container_width=True)
    elif page == "Consumption":
        curve = fact.groupby("Hora", as_index=False)["Consumo_kWh"].mean()
        st.plotly_chart(px.line(curve, x="Hora", y="Consumo_kWh", title="Curva de carga media horaria"), use_container_width=True)
        heat = fact.assign(DiaSemana=fact["Timestamp"].dt.day_name()).groupby(["DiaSemana","Hora"], as_index=False)["Consumo_kWh"].mean()
        st.plotly_chart(px.density_heatmap(heat, x="Hora", y="DiaSemana", z="Consumo_kWh", title="Heatmap dia da semana x hora"), use_container_width=True)
    elif page == "Demand":
        st.plotly_chart(px.bar(costs, x="MesAno", y=["DemandaMaxima_kW","DemandaContratada_kW"], barmode="group", title="Demanda maxima x contratada"), use_container_width=True)
        st.dataframe(costs[["MesAno","ID_Unidade","DemandaContratada_kW","DemandaMaxima_kW","ExcessoDemanda_kW","UtilizacaoDemandaPercentual"]])
    elif page == "Cost":
        comp = costs[["CustoEnergia_R","CustoDemanda_R","CustoUltrapassagem_R","Impostos_R","OutrosCustos_R"]].sum().reset_index()
        comp.columns = ["Componente", "Valor_R"]
        st.plotly_chart(px.bar(comp, x="Componente", y="Valor_R", title="Composicao do custo"), use_container_width=True)
    elif page == "Solar":
        solar = costs.groupby("MesAno", as_index=False)[["GeracaoSolar_kWh","AutoconsumoSolar_kWh","ExportacaoRede_kWh"]].sum()
        st.plotly_chart(px.line(solar, x="MesAno", y=["GeracaoSolar_kWh","AutoconsumoSolar_kWh","ExportacaoRede_kWh"], title="Solar mensal"), use_container_width=True)
    elif page == "Efficiency":
        st.dataframe(opps.sort_values("Payback_Anos")[["ID_Unidade","Categoria","Investimento_R","Economia_R_Ano","Payback_Anos","Prioridade","Status"]])
    else:
        st.plotly_chart(px.histogram(alerts, x="TipoAlerta", color="Severidade", title="Alertas por tipo"), use_container_width=True)
        st.dataframe(alerts)
    """)


def main() -> None:
    ensure_clean_root()
    dim_units, dim_setor, dim_cal, dim_tempo, dim_tarifa = build_dimensions()
    fact = build_hourly_data(dim_units)
    costs = build_costs(fact, dim_tarifa)
    opps = build_opportunities(costs, fact)
    alerts = build_alerts(fact, costs)
    dataframes = {
        "Fato_MedicoesEnergia": fact,
        "Fato_CustosEnergia": costs,
        "Fato_Oportunidades": opps,
        "Fato_Alertas": alerts,
        "Dim_Unidade": dim_units,
        "Dim_Setor": dim_setor,
        "Dim_Calendario": dim_cal,
        "Dim_Tempo": dim_tempo,
        "Dim_Tarifa": dim_tarifa,
    }
    save_dataframes(dataframes)
    insight_lines = insights(costs, fact, opps, alerts, dim_units)
    create_mockups()
    write_project_files(dataframes, insight_lines)
    print(ROOT)
    print(f"hourly_rows={len(fact)}")
    print(f"monthly_cost_rows={len(costs)}")
    print(f"alerts={len(alerts)} opportunities={len(opps)}")


if __name__ == "__main__":
    main()
