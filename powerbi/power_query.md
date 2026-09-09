# Power Query

Importe todos os CSVs da pasta `data/` em UTF-8. Defina `Timestamp` como DateTime, `Data` como Date, horas como número inteiro, métricas como número decimal e flags como True/False.

Não mescle fatos entre si. Use relacionamentos no modelo estrela. As tarifas são premissas sintéticas parametrizáveis e devem permanecer em `Dim_Tarifa`.
