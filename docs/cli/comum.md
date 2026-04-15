# CLI — Módulo Comum

Comandos relacionados a dados gerais do usuário autenticado.

---

## `suap meus-dados`

Exibe os dados pessoais do usuário logado.

```bash
suap meus-dados
```

**Exemplo de saída:**

```json
{
  "id": 1234,
  "matricula": "20221234TADS0014",
  "nome_usual": "João da Silva",
  "cpf": "***.***.***-**",
  "rg": "1234567",
  "email": "joao.silva@academico.ifpi.edu.br",
  "tipo_sanguineo": "O+",
  "foto": "https://suap.ifpi.edu.br/media/foto.jpg",
  "data_nascimento": "2000-01-01",
  "naturalidade": "Teresina",
  "tipo_vinculo": "Aluno"
}
```

!!! tip
    Use `suap meus-dados | jq '.email'` para extrair campos individuais.
