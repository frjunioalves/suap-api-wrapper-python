# 📊 Relatório de Notas

Script que busca os diários do semestre mais recente e imprime um resumo de notas e frequência no terminal.

---

## Código

```python
from suap_api import SuapClient

with SuapClient() as client:
    dados = client.comum.get_my_data()
    print(f"Aluno: {dados['nome_usual']} ({dados['matricula']})\n")

    periodos = client.edu.get_periods()
    semestre_atual = periodos[0]["semestre"]
    print(f"Semestre: {semestre_atual}")
    print("-" * 40)

    diarios = client.edu.get_diaries(semestre_atual)

    for diario in diarios:
        disciplina = diario["disciplina"]
        situacao = diario.get("situacao", "—")
        frequencia = diario.get("percentual_carga_horaria_frequentada", "—")

        notas = diario.get("notas", {})
        n1 = notas.get("nota_etapa_1", {}).get("nota", "—")
        n2 = notas.get("nota_etapa_2", {}).get("nota", "—")

        print(f"📘 {disciplina}")
        print(f"   Nota 1ª etapa : {n1}")
        print(f"   Nota 2ª etapa : {n2}")
        print(f"   Frequência    : {frequencia}%")
        print(f"   Situação      : {situacao}")
        print()
```

---

## Saída esperada

```
Aluno: João Silva (20221234)

Semestre: 2024.1
----------------------------------------
📘 Algoritmos e Programação
   Nota 1ª etapa : 8.5
   Nota 2ª etapa : 7.0
   Frequência    : 92%
   Situação      : Cursando

📘 Banco de Dados
   Nota 1ª etapa : 9.0
   Nota 2ª etapa : —
   Frequência    : 88%
   Situação      : Cursando
```
