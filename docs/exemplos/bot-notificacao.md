# 🤖 Bot de Notificação via Telegram

Script que verifica as notas do semestre atual e envia um resumo para um chat do Telegram.

---

## Pré-requisitos

```bash
pip install requests
```

Você também precisa de um bot do Telegram e do seu `chat_id`.
Consulte a [documentação oficial do BotFather](https://core.telegram.org/bots#botfather) para criar o bot e obter o token.

---

## Código

```python
import os
import requests
from suap_api import SuapClient

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def enviar_mensagem(texto: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": texto, "parse_mode": "Markdown"})


with SuapClient() as client:
    periodos = client.edu.get_periods()
    semestre = periodos[0]["semestre"]
    diarios = client.edu.get_diaries(semestre)

    linhas = [f"📋 *Notas — {semestre}*\n"]

    for diario in diarios:
        disciplina = diario["disciplina"]
        notas = diario.get("notas", {})
        n1 = notas.get("nota_etapa_1", {}).get("nota", "—")
        n2 = notas.get("nota_etapa_2", {}).get("nota", "—")
        freq = diario.get("percentual_carga_horaria_frequentada", "—")

        linhas.append(f"📘 *{disciplina}*")
        linhas.append(f"   Etapa 1: `{n1}` | Etapa 2: `{n2}` | Freq: `{freq}%`")

    enviar_mensagem("\n".join(linhas))
    print("Mensagem enviada!")
```

---

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `TELEGRAM_TOKEN` | Token do bot obtido no BotFather |
| `TELEGRAM_CHAT_ID` | ID do chat para receber as mensagens |

!!! tip "Automatizar"
    Adicione este script a um `cron` ou serviço agendado para receber notificações automáticas no início de cada semana.
