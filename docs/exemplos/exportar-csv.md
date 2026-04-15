# 📁 Exportar para CSV

Script que exporta os diários do semestre atual para um arquivo `.csv`, útil para análise em planilhas.

---

## Código

```python
import csv
from suap_api import SuapClient

ARQUIVO = "notas_suap.csv"

with SuapClient() as client:
    periodos = client.edu.get_periods()
    semestre = periodos[0].semestre
    disciplinas = client.edu.get_disciplines(semestre)

    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Disciplina", "Nota Etapa 1", "Nota Etapa 2", "Média", "Faltas", "Situação"])

        for d in disciplinas:
            writer.writerow([d.disciplina, d.nota_etapa_1, d.nota_etapa_2, d.media, d.faltas, d.situacao])

print(f"Arquivo gerado: {ARQUIVO}")
```

---

## Arquivo gerado

```
Disciplina,Nota Etapa 1,Nota Etapa 2,Média,Faltas,Situação
Algoritmos e Programação,8.5,7.0,7.8,2,Cursando
Banco de Dados,9.0,,,,Cursando
Estrutura de Dados,7.5,8.0,7.8,0,Cursando
```

!!! tip
    Abra o arquivo no LibreOffice Calc ou Google Sheets para visualizar e filtrar os dados com facilidade.
