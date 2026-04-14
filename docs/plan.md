# Especificação de Projeto: SUAP API Python Wrapper (Versão Flexível)

## Objetivo
Criar uma biblioteca Python e uma CLI para interagir com a API v2 do SUAP. O diferencial desta versão é a **não dependência de uma URL fixa**, permitindo que alunos de diferentes instituições (como IFPI, IFRN, etc.) utilizem a mesma ferramenta apenas informando a sua instância no login.

## Stack Tecnológica
- **Linguagem:** Python 3.8+
- **Requisições:** `requests`
- **CLI:** `click` (recomendado pela facilidade com prompts)
- **Segurança:** `keyring` (para o token) e `getpass` (para a senha)
- **Configuração:** `json` ou `toml` para guardar a URL da instância.
- **Testes:** `pytest` + `responses` (mock de requisições HTTP)
- **Tipos:** Type hints em todo o código, validados com `mypy`
- **Empacotamento:** `pyproject.toml` com `[project.scripts]` para expor o comando `suap`

## Requisitos de Arquitetura e UX

### 1. Fluxo de Login Dinâmico (CLI)
O comando `suap login` deve ser interativo e solicitar:
1.  **URL da instância:** O aluno informa a URL completa do seu SUAP (ex: `https://suap.ifpi.edu.br`).
    - *Lógica interna:* Normalizar a URL removendo barras finais e anexar `/api/v2/` para formar a `base_url`.
2.  **Utilizador/Matrícula:** Matrícula padrão do SUAP.
3.  **Senha:** Input escondido (utilizando `getpass` ou o modo `hide_input=True` do Click).

### 2. Gestão de Configuração e Sessão
- **Localização:** Criar uma pasta oculta no diretório home do utilizador (ex: `~/.suap/`).
- **Configuração (`config.json`):** Guardar a `base_url` validada e o utilizador atual. O arquivo deve ser criado com permissão `600` (somente leitura/escrita do próprio utilizador).
- **Token:** O Token JWT **nunca** deve ser guardado no ficheiro JSON. Deve ser armazenado de forma segura via `keyring.set_password("suap_api", username, token)`.

### 3. Classe Core: `SuapClient`
A classe principal deve ser capaz de:
- Identificar automaticamente a `base_url` e o `token` a partir dos ficheiros de configuração e do `keyring`.
- Permitir override manual: `SuapClient(base_url="...", token="...")`.
- Implementar um método privado `_do_request` que gere erros de autenticação (401) e injete o header `Authorization: JWT <token>`.
- Definir um **timeout padrão** para todas as requisições (ex: `timeout=10`) para evitar que a CLI trave em redes instáveis.
- Suportar uso como **context manager** (`with SuapClient() as client:`) para garantir o fechamento da `Session`.

## Endpoints Prioritários (v2)
Com base na estrutura do SUAP v2, implementar métodos para:
- `POST /autenticacao/token/` (Obtenção do token inicial).
- `POST /autenticacao/token/refresh/` (Renovação do token — usado automaticamente pelo `_do_request` ao receber 401).
- `GET /minhas-informacoes/meus-dados/` (Dados do perfil e vínculo).
- `GET /minhas-informacoes/meus-periodos-letivos/` (Histórico de períodos).
- `GET /minhas-informacoes/boletim/{ano}/{periodo}/` (Notas e faltas).
- `GET /minhas-informacoes/turmas-virtuais/{ano}/{periodo}/` (Lista de disciplinas).
- `GET /minhas-informacoes/turma-virtual/{id}/` (Detalhes da disciplina, participantes e materiais).

## Requisitos de Segurança
1.  **Validação de SSL:** Por lidar com dados académicos, nunca desativar a verificação de certificados SSL nas requisições.
2.  **Permissões de arquivo:** O `~/.suap/config.json` deve ser criado com `os.chmod(..., 0o600)` imediatamente após a escrita.
3.  **Limpeza de Sessão:** O comando `suap logout` deve obrigatoriamente remover o token do `keyring` e limpar o ficheiro de configuração.
4.  **Tratamento de Exceções:** Criar exceções específicas como `SuapTokenExpiredError` para orientar o utilizador a realizar um novo login.
5.  **Timeout obrigatório:** Toda chamada via `requests` deve ter timeout definido para prevenir travamentos.

## Guia de Implementação para o Agente
1.  Crie a estrutura de pastas do pacote e o `pyproject.toml` com dependências e `[project.scripts]` mapeando `suap = "suap_api.cli:main"`.
2.  Implemente a lógica de normalização de URL (remoção de barra final + append de `/api/v2/`).
3.  Configure o `click` para o comando `login` com os prompts necessários.
4.  Desenvolva a classe `SuapClient` com suporte a `requests.Session`, timeout padrão e context manager.
5.  Implemente o fluxo de refresh automático de token no `_do_request` ao receber 401.
6.  Adicione type hints em todos os métodos públicos e verifique com `mypy`.
7.  Adicione testes unitários usando `pytest` + `responses` para mockar as chamadas HTTP (exemplo de URL base: `https://suap.ifpi.edu.br/api/v2/`).