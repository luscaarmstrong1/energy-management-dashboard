# Case para Entrevistas

## 1. Qual problema o projeto resolve?
Ele transforma 315.360 medições horárias sintéticas em indicadores e recomendações de gestão energética.

## 2. Como os dados foram estruturados?
Usei modelo estrela com fatos de medições, custos, alertas, oportunidades e produção mensal conectados a dimensões.

## 3. Como foi criada a curva de carga?
A curva combina carga base, perfil operacional, sazonalidade, temperatura, dia útil e setor.

## 4. Qual a diferença entre energia e demanda?
Energia é kWh ao longo do tempo; demanda é kW de potência em um intervalo.

## 5. O que é fator de carga?
É o consumo dividido por demanda máxima vezes horas do período.

## 6. O que é fator de potência?
É um indicador elétrico adimensional e não deve ser confundido com fator de carga.

## 7. Como analisar demanda contratada?
Comparando demanda máxima, contratada, excesso, utilização e custo de ultrapassagem.

## 8. Como foi calculado custo de energia?
Com tarifas sintéticas de ponta/fora ponta, demanda, ultrapassagem, impostos e encargos.

## 9. Como foi modelado horário de ponta?
Como parâmetro configurável, sem afirmar regra regulatória universal.

## 10. Como a geração solar foi incorporada?
Por potência FV em kWp, daylight, sazonalidade, perdas e autoconsumo/exportação.

## 11. O que é autoconsumo?
É a energia solar consumida localmente.

## 12. Como foi calculada a cobertura solar?
Autoconsumo solar dividido pelo consumo total.

## 13. Como foi calculada a dependência da rede?
Importação da rede dividida pelo consumo total.

## 14. Como foram identificadas anomalias?
Com z-score, média móvel e IQR.

## 15. Como foi construído o baseline?
Por unidade, setor, dia da semana e hora.

## 16. Como avaliar intensidade energética?
Só uso denominadores positivos, como área, funcionários, produção e toneladas.

## 17. Como priorizar oportunidades?
Por economia anual, investimento, payback e prioridade operacional.

## 18. Como o payback foi calculado?
Investimento dividido pela economia anual estimada.

## 19. Quais cuidados foram tomados com dados sintéticos?
Todos os valores são fictícios e documentados como premissas sintéticas.

## 20. Quais insights apareceram?
Nexus Belo Horizonte Metals concentra 42,1% do consumo anual.

## 21. Qual unidade merece atenção?
A unidade com maior risco de demanda é Nexus Vitoria Cold Chain.

## 22. Como esse dashboard apoiaria uma empresa real?
Apoiaria revisão tarifária, gestão de demanda, eficiência, manutenção e reporte executivo.

## 23. O que entraria em uma V2?
Dados de 15 minutos, IoT, previsão, medidores inteligentes e tarifas reais.

## 24. Como você montaria isso no Power BI?
Importaria CSVs, criaria relacionamentos 1:N e aplicaria medidas DAX e tema.

## 25. Por que usar modelo estrela?
Porque separa dimensões e fatos, melhora clareza, filtros e performance.

## 26. Como validar que solar não aparece à noite?
Com teste automatizado sobre horas fora de 6h a 18h.

## 27. Como validar custo total?
Somando energia, demanda, ultrapassagem, impostos e encargos.

## 28. Como validar demanda máxima?
Comparando o custo mensal com o máximo horário agregado por unidade.

## 29. Qual a principal limitação?
Os dados são sintéticos e não substituem auditoria real.

## 30. O que o projeto demonstra tecnicamente?
Demonstra Engenharia Elétrica, Data Analytics, Power BI, Python e Gestão de Energia.
