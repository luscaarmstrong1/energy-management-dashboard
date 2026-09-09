# Dicionário de KPIs

| KPI | Definição | Fórmula | Unidade | Interpretação |
| --- | --- | --- | --- | --- |
| Consumo Total | Soma da energia consumida | `SUM(Consumo_kWh)` | kWh/MWh | Volume total consumido |
| Demanda Máxima | Maior potência horária do período | `MAX(Demanda_kW)` | kW | Pico de demanda |
| Fator de Carga | Energia / (demanda máxima x horas) | `Consumo / (Demanda Máxima x Horas)` | % | Uso da infraestrutura elétrica |
| Fator de Potência | Relação elétrica sintética da medição | `Média(FatorPotencia)` | adimensional | Indicador elétrico, não mede eficiência energética |
| Custo Total | Soma dos componentes da fatura sintética | `Energia + Demanda + Ultrapassagem + Impostos + Encargos` | R$ | Gasto total |
| Custo Médio | Custo total dividido pelo consumo | `Custo Total / Consumo` | R$/kWh | Custo unitário de energia |
| Cobertura Solar | Autoconsumo solar dividido pelo consumo | `Autoconsumo / Consumo` | % | Quanto do consumo foi coberto por solar |
| Autoconsumo Solar | Solar usada localmente | `MIN(Consumo, Geração)` | kWh | Energia FV consumida no local |
| Autoconsumo % | Autoconsumo dividido pela geração | `Autoconsumo / Geração` | % | Uso local da geração FV |
| Dependência da Rede | Importação dividida pelo consumo | `Importação / Consumo` | % | Exposição ao suprimento da rede |
| Intensidade Energética | Consumo por denominador físico | `kWh / m², funcionário, unidade produzida ou tonelada` | variável | Eficiência operacional relativa |
