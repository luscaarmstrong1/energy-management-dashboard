# Dicionário de Dados

| Tabela | Campo | Tipo | Unidade | Descrição |
| --- | --- | --- | --- | --- |
| Fato_MedicoesEnergia | Timestamp | datetime64[us] |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Data | datetime64[us] |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Hora | int64 |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | ID_Setor | str |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Consumo_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Demanda_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | GeracaoSolar_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | ImportacaoRede_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | ExportacaoRede_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | AutoconsumoSolar_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | EnergiaEvitadaRede_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Temperatura_C | float64 |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | DiaUtil | bool |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | HorarioPonta | bool |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | FatorPotencia | float64 |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Tensao_V | float64 |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Corrente_A | float64 |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | StatusMedicao | str |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | FatorEmissao_kgCO2_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Emissao_kgCO2e | float64 | CO2e | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | Emissao_tCO2e | float64 | CO2e | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | EmissaoEvitadaSolar_tCO2e | float64 | CO2e | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | BaselineConsumo_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | DesvioBaseline_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | DiaSemanaNumero | int32 |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | DiaSemana | str |  | Campo utilizado no modelo analítico. |
| Fato_MedicoesEnergia | DesvioBaseline_Percentual | float64 | % | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | MesAno | str |  | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | Consumo_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | Consumo_MWh | float64 |  | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | ImportacaoRede_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | GeracaoSolar_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | AutoconsumoSolar_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | ExportacaoRede_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | DemandaMaxima_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | DemandaContratada_kW | int64 | kW/kWp | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | DemandaFaturavel_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | ExcessoDemanda_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | UtilizacaoDemandaPercentual | float64 | % | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoPonta_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoForaPonta_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoEnergia_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoDemanda_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoUltrapassagem_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | Impostos_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | OutrosCustos_R | int64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoTotal_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | CustoMedio_R_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | EconomiaSolar_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | Emissao_tCO2e | float64 | CO2e | Campo utilizado no modelo analítico. |
| Fato_CustosEnergia | EmissaoEvitadaSolar_tCO2e | float64 | CO2e | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | ID_Oportunidade | str |  | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Categoria | str |  | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Descricao | str |  | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Investimento_R | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Economia_kWh_Ano | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Economia_R_Ano | float64 | R$ | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Payback_Anos | float64 |  | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Prioridade | str |  | Campo utilizado no modelo analítico. |
| Fato_Oportunidades | Status | str |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | ID_Alerta | str |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | Timestamp | datetime64[us] |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | TipoAlerta | str |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | Severidade | str |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | ValorMedido | float64 |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | ValorEsperado | float64 |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | DesvioPercentual | float64 | % | Campo utilizado no modelo analítico. |
| Fato_Alertas | Status | str |  | Campo utilizado no modelo analítico. |
| Fato_Alertas | Descricao | str |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | MesAno | str |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | Producao_Unidades | float64 |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | Producao_t | float64 |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | Area_m2 | int64 |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | Funcionarios | int64 |  | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | ConsumoAnualReferencia_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | kWh_m2_Ano | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | kWh_Funcionario_Ano | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | kWh_UnidadeProduzida | float64 | kWh | Campo utilizado no modelo analítico. |
| Fato_ProducaoMensal | kWh_t | float64 | kWh | Campo utilizado no modelo analítico. |
| Dim_Unidade | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | Unidade | str |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | Cidade | str |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | UF | str |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | TipoUnidade | str |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | PerfilOperacao | str |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | Area_m2 | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | Funcionarios | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | PotenciaFV_kWp | int64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Unidade | DemandaContratada_kW | int64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Unidade | TarifaPonta_R_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Dim_Unidade | TarifaForaPonta_R_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Dim_Unidade | TarifaDemanda_R_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Unidade | PenalidadeUltrapassagem_R_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Unidade | ImpostosPercentual | float64 | % | Campo utilizado no modelo analítico. |
| Dim_Unidade | OutrosEncargos_R | int64 | R$ | Campo utilizado no modelo analítico. |
| Dim_Unidade | BaseLoad_kW | int64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Unidade | PeakLoad_kW | int64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Unidade | ProductionBase | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Unidade | DemandScenario | str |  | Campo utilizado no modelo analítico. |
| Dim_Setor | ID_Setor | str |  | Campo utilizado no modelo analítico. |
| Dim_Setor | Setor | str |  | Campo utilizado no modelo analítico. |
| Dim_Setor | TiposUnidadeAplicaveis | str |  | Campo utilizado no modelo analítico. |
| Dim_Setor | PesoReferencia | float64 |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | Data | str |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | Ano | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | Mes | str |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | NumeroMes | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | MesAno | str |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | Trimestre | str |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | Semana | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | Dia | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | DiaSemana | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | NomeDiaSemana | str |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | DiaUtil | bool |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | FimSemana | bool |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | InicioMes | bool |  | Campo utilizado no modelo analítico. |
| Dim_Calendario | FimMes | bool |  | Campo utilizado no modelo analítico. |
| Dim_Tempo | Hora | int64 |  | Campo utilizado no modelo analítico. |
| Dim_Tempo | FaixaHoraria | str |  | Campo utilizado no modelo analítico. |
| Dim_Tempo | Turno | str |  | Campo utilizado no modelo analítico. |
| Dim_Tempo | Ponta | bool |  | Campo utilizado no modelo analítico. |
| Dim_Tempo | PeriodoDia | str |  | Campo utilizado no modelo analítico. |
| Dim_Tarifa | ID_Unidade | str |  | Campo utilizado no modelo analítico. |
| Dim_Tarifa | TarifaPonta_R_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Dim_Tarifa | TarifaForaPonta_R_kWh | float64 | kWh | Campo utilizado no modelo analítico. |
| Dim_Tarifa | DemandaContratada_kW | int64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Tarifa | TarifaDemanda_R_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Tarifa | PenalidadeUltrapassagem_R_kW | float64 | kW/kWp | Campo utilizado no modelo analítico. |
| Dim_Tarifa | ImpostosPercentual | float64 | % | Campo utilizado no modelo analítico. |
| Dim_Tarifa | OutrosEncargos_R | int64 | R$ | Campo utilizado no modelo analítico. |
| Dim_Tarifa | InicioPonta | str |  | Campo utilizado no modelo analítico. |
| Dim_Tarifa | FimPonta | str |  | Campo utilizado no modelo analítico. |
| Dim_Tarifa | ModeloTarifario | str |  | Campo utilizado no modelo analítico. |
