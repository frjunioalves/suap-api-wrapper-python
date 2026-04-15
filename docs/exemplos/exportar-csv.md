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
    semestre = periodos[0]["semestre"]
    diarios = client.edu.get_diaries(semestre)

    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Disciplina", "Nota Etapa 1", "Nota Etapa 2", "Frequência (%)", "Situação"])

        for diario in diarios:
            disciplina = diario["disciplina"]
            notas = diario.get("notas", {})
            n1 = notas.get("nota_etapa_1", {}).get("nota", "")
            n2 = notas.get("nota_etapa_2", {}).get("nota", "")
            freq = diario.get("percentual_carga_horaria_frequentada", "")
            situacao = diario.get("situacao", "")

            writer.writerow([disciplina, n1, n2, freq, situacao])

print(f"Arquivo gerado: {ARQUIVO}")
```

---

## Arquivo gerado

```
Disciplina,Nota Etapa 1,Nota Etapa 2,Frequência (%),Situação
Algoritmos e Programação,8.5,7.0,92,Cursando
Banco de Dados,9.0,,88,Cursando
Estrutura de Dados,7.5,8.0,95,Cursando
```

!!! tip
    Abra o arquivo no LibreOffice Calc ou Google Sheets para visualizar e filtrar os dados com facilidade.
