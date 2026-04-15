```python?code_reference&code_event_index=2
import os

content = """# Plano de Implementação: Modelos de Dados (Tipagem de Retorno)

## 1. Objetivo
Transformar os retornos atuais da API (que atualmente são objetos genéricos como `dict` e `list`) em objetos Python ricos, tipados e manipuláveis. 
Isso irá melhorar significativamente a Developer Experience (DX), fornecendo autocompletar (IntelliSense) nativo nas IDEs, verificação de tipos estática (Type Hinting) e acesso aos atributos via "ponto" (`diario.id` ao invés de `diario["id"]`).

## 2. Abordagem Escolhida: `dataclasses`
Para manter a biblioteca leve e não adicionar dependências pesadas ou obrigatórias (como Pydantic), utilizaremos o módulo nativo `dataclasses` do Python. Caso a resposta da API contenha atributos não previstos ou que mudem com o tempo, criaremos um construtor seguro.

## 3. Estrutura de Diretórios
Criar um novo pacote para os modelos dentro da biblioteca:
```
```text?code_stdout&code_event_index=2
File created successfully at specs/implementacao-modelos.md

```text
suap_api/
├── models/
│   ├── __init__.py
│   ├── comum.py     # Modelos do módulo comum (ex: DadosPessoais)
│   └── edu.py       # Modelos do módulo educacional (ex: Periodo, Diario, Aula)
```

## 4. Modelos a Serem Implementados

### `suap_api/models/comum.py`
* `DadosPessoais`: `id`, `matricula`, `nome_usual`, `cpf`, `rg`, `email`, `tipo_sanguineo`, `foto`, `data_nascimento`, `naturalidade`, `tipo_vinculo`.

### `suap_api/models/edu.py`
*(Baseado nos endpoints atuais documentados em `docs/biblioteca/recursos-edu.md`)*
* `Periodo`: `semestre`, `situacao`.
* `Diario`: `id`, `disciplina`, `componente_curricular`, `situacao`.
* `Professor`: `nome`, `email`.
* `Aula`: `data`, `quantidade`, `conteudo`, `faltas`.
* `Material`: `id`, `titulo`, `tipo`, `data_publicacao`, `descricao`.
* `Trabalho`: `id`, `titulo`, `descricao`, `data_entrega`.
* `Disciplina`: `disciplina`, `nota_etapa_1`, `nota_etapa_2`, `media`, `faltas`, `situacao`.
* `DadosAcademicos`: `curso`, `turma`, `situacao`.
* `RequisitosConclusao`: `ch_total`, `ch_cumprida`, `pendencias`.

## 5. Passos de Execução para o Claude Code

**Passo 1: Criar os arquivos de Modelo (`suap_api/models/`)**
- Implemente as `@dataclass` listadas acima.
- Dica: Crie um método de classe base ou auxiliar (ex: `from_dict(cls, data: dict)`) para iterar nas chaves recebidas da API e ignorar chaves inesperadas. O SUAP pode enviar campos novos e isso não deve quebrar o wrapper.

**Passo 2: Atualizar os Resources (`suap_api/resources/`)**
- Modifique `comum.py` e `edu.py` para converterem o retorno bruto da API (do método `_do_request`) para as novas `dataclasses`.
- Exemplo de conversão: `return [Periodo.from_dict(p) for p in data]`.
- Atualize os **Type Hints** dos métodos. Onde era `-> list` passará a ser `-> list[Periodo]`, etc.

**Passo 3: Atualizar a CLI (`suap_api/cli.py`)**
- A CLI depende da conversão do retorno para JSON formatado (`_print_json()`).
- Como os métodos agora retornarão objetos ao invés de dicionários, é preciso serializá-los. Você pode ajustar a função `_print_json` ou aplicar um `dataclasses.asdict(obj)` (ou conversor customizado) antes de imprimir os dados na tela para garantir que o formato JSON de saída permaneça inalterado para o usuário final.

**Passo 4: Atualizar os Testes (`tests/`)**
- No arquivo `tests/test_client.py`: Mude as asserções. Em vez de `assert dados["nome_usual"] == "João"`, teste `assert dados.nome_usual == "João"`.
- No arquivo `tests/test_cli.py`: Certifique-se de que a CLI continua respondendo e formatando a saída JSON corretamente.

**Passo 5: Atualizar a Documentação (`docs/`)**
- Altere os arquivos `docs/biblioteca/recursos-comum.md`, `docs/biblioteca/recursos-edu.md` e `docs/biblioteca/index.md`.
- Troque os exemplos de código que acessam dicionários (`print(dados["curso"])` ou `id_diario = diarios[0]["id"]`) pelas chamadas aos atributos do objeto (`print(dados.curso)` ou `id_diario = diarios[0].id`).
- Atualize a documentação de retorno dos endpoints para indicar o tipo correto do objeto.
"""

file_path = "specs/implementacao-modelos.md"
os.makedirs(os.path.dirname(file_path), exist_ok=True)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"File created successfully at {file_path}")


```
Criei um arquivo Markdown de implementação detalhando exatamente como transformar as respostas de dicionário (`dict`) em classes de dados manipuláveis no seu projeto. 

Seu arquivo Markdown está pronto
[file-tag: code-generated-file-0-1776274185124725134]

O plano especifica o uso de `dataclasses` nativas do Python, o que é ideal para manter a biblioteca leve. Ele também inclui instruções diretas que você pode passar para o Claude Code, cobrindo não apenas a criação dos modelos, mas também como atualizar a biblioteca (`resources`), a CLI, os testes e os arquivos de documentação do MkDocs (`docs/biblioteca/*.md`).