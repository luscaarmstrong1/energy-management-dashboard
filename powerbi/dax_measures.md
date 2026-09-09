# Medidas DAX

## [Consumo Total kWh]
```DAX
Consumo Total kWh =
SUM(Fato_MedicoesEnergia[Consumo_kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Consumo Total MWh]
```DAX
Consumo Total MWh =
DIVIDE([Consumo Total kWh], 1000)
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Demanda Máxima kW]
```DAX
Demanda Máxima kW =
MAXX(SUMMARIZE(Fato_MedicoesEnergia, Fato_MedicoesEnergia[Timestamp], Dim_Unidade[ID_Unidade], "Demanda Horária", SUM(Fato_MedicoesEnergia[Demanda_kW])), [Demanda Horária])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Demanda Contratada kW]
```DAX
Demanda Contratada kW =
MAX(Dim_Tarifa[DemandaContratada_kW])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Excesso de Demanda kW]
```DAX
Excesso de Demanda kW =
MAX(0, [Demanda Máxima kW] - [Demanda Contratada kW])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Utilização da Demanda %]
```DAX
Utilização da Demanda % =
DIVIDE([Demanda Máxima kW], [Demanda Contratada kW])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Horas do Período]
```DAX
Horas do Período =
DISTINCTCOUNT(Fato_MedicoesEnergia[Timestamp])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Fator de Carga]
```DAX
Fator de Carga =
DIVIDE([Consumo Total kWh], [Demanda Máxima kW] * [Horas do Período])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Custo Total]
```DAX
Custo Total =
SUM(Fato_CustosEnergia[CustoTotal_R])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Custo Médio por kWh]
```DAX
Custo Médio por kWh =
DIVIDE([Custo Total], [Consumo Total kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Custo de Energia]
```DAX
Custo de Energia =
SUM(Fato_CustosEnergia[CustoEnergia_R])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Custo de Demanda]
```DAX
Custo de Demanda =
SUM(Fato_CustosEnergia[CustoDemanda_R])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Custo de Ultrapassagem]
```DAX
Custo de Ultrapassagem =
SUM(Fato_CustosEnergia[CustoUltrapassagem_R])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Geração Solar kWh]
```DAX
Geração Solar kWh =
SUM(Fato_MedicoesEnergia[GeracaoSolar_kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Autoconsumo Solar kWh]
```DAX
Autoconsumo Solar kWh =
SUM(Fato_MedicoesEnergia[AutoconsumoSolar_kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Cobertura Solar %]
```DAX
Cobertura Solar % =
DIVIDE([Autoconsumo Solar kWh], [Consumo Total kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Autoconsumo Solar %]
```DAX
Autoconsumo Solar % =
DIVIDE([Autoconsumo Solar kWh], [Geração Solar kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Dependência da Rede %]
```DAX
Dependência da Rede % =
DIVIDE(SUM(Fato_MedicoesEnergia[ImportacaoRede_kWh]), [Consumo Total kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [CO2 Evitado t]
```DAX
CO2 Evitado t =
SUM(Fato_MedicoesEnergia[EmissaoEvitadaSolar_tCO2e])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Desvio do Baseline kWh]
```DAX
Desvio do Baseline kWh =
SUM(Fato_MedicoesEnergia[DesvioBaseline_kWh])
```
Unidade e uso: medida documentada para análise de gestão energética.

## [Economia Potencial]
```DAX
Economia Potencial =
SUM(Fato_Oportunidades[Economia_R_Ano])
```
Unidade e uso: medida documentada para análise de gestão energética.
