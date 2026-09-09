from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

RAIZ = Path(__file__).resolve().parent

st.set_page_config(page_title="Dashboard de Gestão e Analytics de Energia", layout="wide")

@st.cache_data(show_spinner=False)
def carregar_dados():
    dados = RAIZ / "data"
    return {
        "medicoes": pd.read_csv(dados / "Fato_MedicoesEnergia.csv", parse_dates=["Timestamp", "Data"]),
        "custos": pd.read_csv(dados / "Fato_CustosEnergia.csv"),
        "unidades": pd.read_csv(dados / "Dim_Unidade.csv"),
        "setores": pd.read_csv(dados / "Dim_Setor.csv"),
        "alertas": pd.read_csv(dados / "Fato_Alertas.csv", parse_dates=["Timestamp"]),
        "oportunidades": pd.read_csv(dados / "Fato_Oportunidades.csv"),
        "producao": pd.read_csv(dados / "Fato_ProducaoMensal.csv"),
        "resumo": json.loads((RAIZ / "resumo_portfolio.json").read_text(encoding="utf-8")),
    }

d = carregar_dados()
med = d["medicoes"].merge(d["unidades"][["ID_Unidade", "Unidade", "TipoUnidade", "Cidade", "UF"]], on="ID_Unidade").merge(d["setores"][["ID_Setor", "Setor"]], on="ID_Setor")
custos = d["custos"].merge(d["unidades"][["ID_Unidade", "Unidade", "TipoUnidade"]], on="ID_Unidade")
unidades = d["unidades"]
setores = d["setores"]

st.title("Dashboard de Gestão e Analytics de Energia")
st.caption("Consumo • Demanda • Custos • Energia Solar • Eficiência • Anomalias")
st.info("Todos os dados, tarifas e fatores de emissão são sintéticos e usados somente para demonstração de portfólio.")

with st.sidebar:
    st.header("Filtros")
    pagina = st.radio("Navegação", ["Visão Executiva", "Análise de Consumo", "Gestão de Demanda", "Custos e Tarifas", "Energia Solar", "Eficiência Energética", "Alertas e Anomalias", "Detalhamento da Unidade"])
    tipo = st.multiselect("Tipo de unidade", sorted(med["TipoUnidade"].unique()), default=sorted(med["TipoUnidade"].unique()))
    unidade = st.multiselect("Unidade", sorted(med["Unidade"].unique()), default=sorted(med["Unidade"].unique()))
    setor = st.multiselect("Setor", sorted(med["Setor"].unique()), default=sorted(med["Setor"].unique()))
    data_ini = st.date_input("Data inicial", med["Data"].min().date())
    data_fim = st.date_input("Data final", med["Data"].max().date())
    dia_util = st.selectbox("Dia útil/fim de semana", ["Todos", "Dia útil", "Fim de semana"])
    ponta = st.selectbox("Horário de ponta", ["Todos", "Ponta", "Fora ponta"])

filtro = med[
    med["TipoUnidade"].isin(tipo)
    & med["Unidade"].isin(unidade)
    & med["Setor"].isin(setor)
    & (med["Data"].dt.date >= data_ini)
    & (med["Data"].dt.date <= data_fim)
].copy()
if dia_util == "Dia útil":
    filtro = filtro[filtro["DiaUtil"] == True]
elif dia_util == "Fim de semana":
    filtro = filtro[filtro["DiaUtil"] == False]
if ponta == "Ponta":
    filtro = filtro[filtro["HorarioPonta"] == True]
elif ponta == "Fora ponta":
    filtro = filtro[filtro["HorarioPonta"] == False]

meses = sorted(filtro["Timestamp"].dt.strftime("%Y-%m").unique())
custos_f = custos[custos["Unidade"].isin(unidade) & custos["TipoUnidade"].isin(tipo) & custos["MesAno"].isin(meses)].copy()
alertas_f = d["alertas"].merge(unidades[["ID_Unidade", "Unidade"]], on="ID_Unidade")
alertas_f = alertas_f[alertas_f["Unidade"].isin(unidade)]
opps_f = d["oportunidades"].merge(unidades[["ID_Unidade", "Unidade"]], on="ID_Unidade")
opps_f = opps_f[opps_f["Unidade"].isin(unidade)]

def br(v, dec=0):
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def brl(v):
    return "R$ " + br(v, 2)

def card(label, value, delta=None):
    st.metric(label, value, delta)

def kpi_base():
    consumo = filtro["Consumo_kWh"].sum()
    custo = custos_f["CustoTotal_R"].sum()
    demanda = filtro.groupby(["Timestamp", "ID_Unidade"])["Demanda_kW"].sum().max()
    solar = filtro["GeracaoSolar_kWh"].sum()
    auto = filtro["AutoconsumoSolar_kWh"].sum()
    imp = filtro["ImportacaoRede_kWh"].sum()
    return consumo, custo, demanda, solar, auto, imp

consumo, custo, demanda, solar, auto, imp = kpi_base()

if filtro.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

if pagina == "Visão Executiva":
    c = st.columns(4)
    c[0].metric("Consumo Total", f"{br(consumo/1000,1)} MWh")
    c[1].metric("Custo Total", brl(custo))
    c[2].metric("Demanda Máxima", f"{br(demanda,0)} kW")
    c[3].metric("Custo Médio por kWh", brl(custo/consumo if consumo else 0))
    c = st.columns(4)
    c[0].metric("Geração Solar", f"{br(solar/1000,1)} MWh")
    c[1].metric("Economia Solar", brl(custos_f["EconomiaSolar_R"].sum()))
    c[2].metric("Emissões Evitadas", f"{br(filtro['EmissaoEvitadaSolar_tCO2e'].sum(),1)} tCO2e")
    c[3].metric("Economia Potencial", brl(opps_f["Economia_R_Ano"].sum()))
    st.caption(f"Última atualização dos dados: {d['resumo']['periodo']['ultima_medicao']}")
    mensal = filtro.assign(MesAno=filtro["Timestamp"].dt.strftime("%Y-%m")).groupby("MesAno", as_index=False).agg(Consumo_MWh=("Consumo_kWh", lambda s: s.sum()/1000), Geracao_MWh=("GeracaoSolar_kWh", lambda s: s.sum()/1000))
    st.plotly_chart(px.line(mensal, x="MesAno", y=["Consumo_MWh", "Geracao_MWh"], title="Consumo mensal e geração solar"), use_container_width=True)
    col1, col2 = st.columns(2)
    col1.plotly_chart(px.bar(filtro.groupby("Unidade", as_index=False)["Consumo_kWh"].sum(), x="Unidade", y="Consumo_kWh", title="Consumo por unidade"), use_container_width=True)
    col2.plotly_chart(px.bar(custos_f.groupby("Unidade", as_index=False)["CustoTotal_R"].sum(), x="Unidade", y="CustoTotal_R", title="Custo por unidade"), use_container_width=True)

elif pagina == "Análise de Consumo":
    c = st.columns(6)
    c[0].metric("Consumo Total", f"{br(consumo/1000,1)} MWh")
    c[1].metric("Consumo Médio Diário", f"{br(filtro.groupby('Data')['Consumo_kWh'].sum().mean(),0)} kWh")
    c[2].metric("Pico de Consumo", f"{br(filtro.groupby('Timestamp')['Consumo_kWh'].sum().max(),0)} kWh")
    c[3].metric("Carga Base", f"{br(filtro.groupby('Timestamp')['Demanda_kW'].sum().quantile(0.05),0)} kW")
    c[4].metric("Consumo Ponta", f"{br(filtro[filtro['HorarioPonta']]['Consumo_kWh'].sum()/1000,1)} MWh")
    c[5].metric("Consumo Fora Ponta", f"{br(filtro[~filtro['HorarioPonta']]['Consumo_kWh'].sum()/1000,1)} MWh")
    curva = filtro.groupby(["Hora", "DiaUtil"], as_index=False)["Consumo_kWh"].mean()
    curva["Tipo Dia"] = curva["DiaUtil"].map({True: "Dia útil", False: "Fim de semana"})
    st.plotly_chart(px.line(curva, x="Hora", y="Consumo_kWh", color="Tipo Dia", title="Curva média diária"), use_container_width=True)
    heat = filtro.groupby(["DiaSemana", "DiaSemanaNumero", "Hora"], as_index=False)["Consumo_kWh"].mean().sort_values("DiaSemanaNumero")
    fig = px.density_heatmap(heat, x="Hora", y="DiaSemana", z="Consumo_kWh", category_orders={"DiaSemana": DAY_ORDER}, title="Heatmap: dia da semana x hora")
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(px.bar(filtro.groupby("Setor", as_index=False)["Consumo_kWh"].sum().sort_values("Consumo_kWh"), x="Consumo_kWh", y="Setor", orientation="h", title="Consumo por setor"), use_container_width=True)

elif pagina == "Gestão de Demanda":
    c = st.columns(6)
    c[0].metric("Demanda Máxima", f"{br(custos_f['DemandaMaxima_kW'].max(),0)} kW")
    c[1].metric("Demanda Contratada", f"{br(custos_f['DemandaContratada_kW'].max(),0)} kW")
    c[2].metric("Utilização", f"{br(custos_f['UtilizacaoDemandaPercentual'].max()*100,1)}%")
    c[3].metric("Excesso", f"{br(custos_f['ExcessoDemanda_kW'].sum(),0)} kW")
    c[4].metric("Custo Ultrapassagem", brl(custos_f["CustoUltrapassagem_R"].sum()))
    c[5].metric("Meses com Ultrapassagem", int((custos_f["ExcessoDemanda_kW"] > 0).sum()))
    st.plotly_chart(px.line(custos_f, x="MesAno", y=["DemandaMaxima_kW", "DemandaContratada_kW"], color="Unidade", title="Demanda máxima x contratada"), use_container_width=True)
    tabela = custos_f.groupby("Unidade", as_index=False).agg(**{"Demanda Contratada": ("DemandaContratada_kW","max"), "Demanda Máxima": ("DemandaMaxima_kW","max"), "Excesso": ("ExcessoDemanda_kW","sum"), "Utilização": ("UtilizacaoDemandaPercentual","max"), "Custo de Ultrapassagem": ("CustoUltrapassagem_R","sum")})
    st.dataframe(tabela, use_container_width=True)

elif pagina == "Custos e Tarifas":
    c = st.columns(7)
    c[0].metric("Custo Total", brl(custo))
    c[1].metric("Energia", brl(custos_f["CustoEnergia_R"].sum()))
    c[2].metric("Demanda", brl(custos_f["CustoDemanda_R"].sum()))
    c[3].metric("Ultrapassagem", brl(custos_f["CustoUltrapassagem_R"].sum()))
    c[4].metric("Médio/kWh", brl(custo/consumo if consumo else 0))
    c[5].metric("Ponta", brl(custos_f["CustoPonta_R"].sum()))
    c[6].metric("Fora Ponta", brl(custos_f["CustoForaPonta_R"].sum()))
    comp = custos_f[["CustoEnergia_R","CustoDemanda_R","CustoUltrapassagem_R","Impostos_R","OutrosCustos_R"]].sum().reset_index()
    comp.columns = ["Componente", "Valor"]
    st.plotly_chart(px.bar(comp, x="Componente", y="Valor", title="Composição do custo"), use_container_width=True)
    st.plotly_chart(px.line(custos_f.groupby("MesAno", as_index=False).agg(Custo=("CustoTotal_R","sum"), CustoMedio=("CustoMedio_R_kWh","mean")), x="MesAno", y=["Custo","CustoMedio"], title="Evolução de custo"), use_container_width=True)

elif pagina == "Energia Solar":
    c = st.columns(5)
    c[0].metric("Potência FV", f"{br(unidades[unidades['Unidade'].isin(unidade)]['PotenciaFV_kWp'].sum(),0)} kWp")
    c[1].metric("Geração Solar", f"{br(solar/1000,1)} MWh")
    c[2].metric("Autoconsumo", f"{br(auto/1000,1)} MWh")
    c[3].metric("Cobertura Solar", f"{br((auto/consumo if consumo else 0)*100,1)}%")
    c[4].metric("Dependência da Rede", f"{br((imp/consumo if consumo else 0)*100,1)}%")
    solar_m = filtro.assign(MesAno=filtro["Timestamp"].dt.strftime("%Y-%m")).groupby("MesAno", as_index=False)[["Consumo_kWh","GeracaoSolar_kWh","AutoconsumoSolar_kWh","ExportacaoRede_kWh","ImportacaoRede_kWh"]].sum()
    st.plotly_chart(px.line(solar_m, x="MesAno", y=["Consumo_kWh","GeracaoSolar_kWh"], title="Consumo x geração"), use_container_width=True)
    st.plotly_chart(px.bar(solar_m, x="MesAno", y=["AutoconsumoSolar_kWh","ExportacaoRede_kWh"], title="Autoconsumo x exportação"), use_container_width=True)

elif pagina == "Eficiência Energética":
    desvio = filtro["DesvioBaseline_kWh"].sum()
    c = st.columns(6)
    c[0].metric("Desvio do Baseline", f"{br(desvio/1000,1)} MWh")
    c[1].metric("Economia Potencial", brl(opps_f["Economia_R_Ano"].sum()))
    c[2].metric("Investimento", brl(opps_f["Investimento_R"].sum()))
    c[3].metric("Payback Médio", f"{br(opps_f['Investimento_R'].sum()/opps_f['Economia_R_Ano'].sum(),2)} anos")
    c[4].metric("kWh/m² ano", br(d["producao"][d["producao"]["ID_Unidade"].isin(unidades[unidades["Unidade"].isin(unidade)]["ID_Unidade"])]["kWh_m2_Ano"].mean(),1))
    c[5].metric("Oportunidades", len(opps_f))
    base = filtro.assign(MesAno=filtro["Timestamp"].dt.strftime("%Y-%m")).groupby("MesAno", as_index=False)[["Consumo_kWh","BaselineConsumo_kWh"]].sum()
    st.plotly_chart(px.line(base, x="MesAno", y=["Consumo_kWh","BaselineConsumo_kWh"], title="Baseline x consumo real"), use_container_width=True)
    st.plotly_chart(px.scatter(opps_f, x="Investimento_R", y="Economia_R_Ano", color="Prioridade", size="Economia_kWh_Ano", hover_name="Categoria", title="Investimento x economia"), use_container_width=True)
    st.dataframe(opps_f.sort_values(["Payback_Anos","Economia_R_Ano"]), use_container_width=True)

elif pagina == "Alertas e Anomalias":
    c = st.columns(8)
    c[0].metric("Total", len(alertas_f))
    c[1].metric("Críticos", int((alertas_f["Severidade"]=="Critica").sum()))
    c[2].metric("Altos", int((alertas_f["Severidade"]=="Alta").sum()))
    c[3].metric("Médios", int((alertas_f["Severidade"]=="Media").sum()))
    c[4].metric("Picos de Demanda", int(alertas_f["TipoAlerta"].str.contains("demanda", case=False).sum()))
    c[5].metric("Consumo Anormal", int(alertas_f["TipoAlerta"].str.contains("Consumo", case=False).sum()))
    c[6].metric("Baixo FP", int(alertas_f["TipoAlerta"].str.contains("potencia", case=False).sum()))
    c[7].metric("Anomalias Solares", int(alertas_f["TipoAlerta"].str.contains("solar", case=False).sum()))
    st.plotly_chart(px.histogram(alertas_f, x="TipoAlerta", color="Severidade", title="Alertas por tipo"), use_container_width=True)
    alertas_f["MesAno"] = alertas_f["Timestamp"].dt.strftime("%Y-%m")
    st.plotly_chart(px.density_heatmap(alertas_f, x="MesAno", y="TipoAlerta", z="DesvioPercentual", title="Heatmap temporal de alertas"), use_container_width=True)
    st.dataframe(alertas_f.rename(columns={"Timestamp": "Data/Hora", "ValorMedido": "Valor Medido", "ValorEsperado": "Valor Esperado"}), use_container_width=True)

else:
    unidade_det = st.selectbox("Selecionar unidade para detalhamento", sorted(unidades["Unidade"].unique()))
    uid = unidades.loc[unidades["Unidade"].eq(unidade_det), "ID_Unidade"].iloc[0]
    u = unidades[unidades["ID_Unidade"].eq(uid)].iloc[0]
    mf = med[med["ID_Unidade"].eq(uid)]
    cf = custos[custos["ID_Unidade"].eq(uid)]
    st.subheader(unidade_det)
    st.write(f"{u['Cidade']}/{u['UF']} • {u['TipoUnidade']} • Área: {br(u['Area_m2'])} m² • Funcionários: {br(u['Funcionarios'])}")
    cols = st.columns(6)
    cols[0].metric("Consumo", f"{br(mf['Consumo_kWh'].sum()/1000,1)} MWh")
    cols[1].metric("Demanda", f"{br(cf['DemandaMaxima_kW'].max(),0)} kW")
    cols[2].metric("Custo", brl(cf["CustoTotal_R"].sum()))
    cols[3].metric("Solar", f"{br(mf['GeracaoSolar_kWh'].sum()/1000,1)} MWh")
    cols[4].metric("Fator de Carga", f"{br((mf['Consumo_kWh'].sum()/(cf['DemandaMaxima_kW'].max()*8760))*100,1)}%")
    cols[5].metric("Fator de Potência", br(mf["FatorPotencia"].mean(),3))
    st.plotly_chart(px.line(mf.groupby("Hora", as_index=False)["Consumo_kWh"].mean(), x="Hora", y="Consumo_kWh", title="Curva de carga da unidade"), use_container_width=True)
    st.dataframe(opps_f[opps_f["ID_Unidade"].eq(uid)], use_container_width=True)
    st.dataframe(alertas_f[alertas_f["ID_Unidade"].eq(uid)], use_container_width=True)
