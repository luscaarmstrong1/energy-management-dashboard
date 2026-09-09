# Modelo de Dados

Grãos:
- `Fato_MedicoesEnergia`: Timestamp + Unidade + Setor.
- `Fato_CustosEnergia`: Mês + Unidade.
- `Fato_Oportunidades`: Oportunidade.
- `Fato_Alertas`: Evento.
- `Fato_ProducaoMensal`: Mês + Unidade.

Relacionamentos recomendados: dimensões filtram fatos em direção única, com cardinalidade 1:N sempre que aplicável.
