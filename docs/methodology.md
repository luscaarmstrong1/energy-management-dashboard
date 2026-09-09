# Metodologia

Os dados são sintéticos e reproduzíveis. O consumo horário foi gerado por carga base, perfil operacional, dia útil/fim de semana, sazonalidade, temperatura, setor e ruído controlado. A demanda é tratada em kW e a energia em kWh/MWh. A geração solar utiliza potência instalada em kWp, janela diurna, sazonalidade, perdas térmicas e variabilidade de nuvens.

O baseline foi recalculado por Unidade + Setor + Dia da Semana + Hora, permitindo comparar consumo real e esperado sem tratar todo aumento de consumo como desperdício. Custos usam tarifas sintéticas parametrizáveis, incluindo ponta, fora ponta, demanda, ultrapassagem, impostos e encargos. Emissões usam fator sintético configurável de 0,0385 kgCO2e/kWh.

A detecção de anomalias usa z-score, média móvel de 24 horas e IQR. É uma abordagem estatística, não uma solução de inteligência artificial.
