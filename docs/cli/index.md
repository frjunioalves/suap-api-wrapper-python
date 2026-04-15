# CLI — Visão Geral

Após [instalar](../instalacao.md) o pacote e fazer [login](../autenticacao.md), o comando `suap` estará disponível no terminal.

## Todos os comandos

| Comando | Descrição |
|---|---|
| `suap login` | Realiza login no SUAP |
| `suap logout` | Encerra a sessão atual |
| `suap meus-dados` | Dados pessoais do usuário logado |
| `suap periodos` | Lista os semestres letivos |
| `suap diarios <semestre>` | Diários de um semestre |
| `suap disciplinas <semestre>` | Disciplinas com notas e faltas |
| `suap dados-aluno` | Dados acadêmicos (curso, situação) |
| `suap conclusao` | Requisitos de conclusão do curso |
| `suap professores <id_diario>` | Professores de um diário |
| `suap aulas <id_diario>` | Aulas registradas em um diário |
| `suap materiais <id_diario>` | Materiais disponíveis em um diário |
| `suap material <id_material>` | Detalhes de um material |
| `suap material-pdf <id_diario> <id_material>` | Baixa o PDF de um material |
| `suap trabalhos <id_diario>` | Trabalhos de um diário |

---

## Formato da saída

Todos os comandos retornam **JSON formatado** (`indent=2`). Isso facilita o uso com ferramentas como `jq`:

```bash
# Pegar só o nome do primeiro diário
suap diarios 2024.1 | jq '.[0].disciplina'

# Listar todos os IDs de diário de um semestre
suap diarios 2024.1 | jq '.[].id'
```

---

## Fluxo típico de uso

```bash
# 1. Login
suap login

# 2. Ver semestres disponíveis
suap periodos

# 3. Listar diários de um semestre (anote o "id" dos diários)
suap diarios 2024.1

# 4. Com o ID de um diário, consulte aulas, materiais e trabalhos
suap aulas 42
suap materiais 42
suap trabalhos 42

# 5. Ver detalhes de um material específico
suap material 10

# 6. Baixar o PDF de um material
suap material-pdf 42 10

# 7. Ver notas e faltas por disciplina
suap disciplinas 2024.1

# 8. Ver dados acadêmicos do curso
suap dados-aluno
suap conclusao
```

---

## Tratamento de erros

Erros são exibidos em `stderr` com mensagens em português e o processo encerra com código `1`:

```
$ suap diarios 2024.1
Nenhuma sessao encontrada. Execute `suap login` primeiro.

$ echo $?
1
```
