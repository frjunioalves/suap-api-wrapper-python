class SuapError(Exception):
    """Exceção base para todos os erros do wrapper.

    Todas as exceções específicas herdam desta classe, permitindo capturar
    qualquer erro do wrapper com um único ``except SuapError``.
    """


class SuapAuthError(SuapError):
    """Credenciais inválidas.

    Levantada quando a matrícula ou senha fornecidas são rejeitadas pela API
    (resposta HTTP 401 no endpoint de obtenção de token).
    """


class SuapTokenExpiredError(SuapError):
    """Token de acesso expirado.

    Levantada quando o access token expirou e não foi possível renová-lo
    usando o refresh token. O utilizador deve executar ``suap login`` novamente.
    """


class SuapNotLoggedInError(SuapError):
    """Nenhuma sessão ativa encontrada.

    Levantada quando o cliente tenta realizar uma operação autenticada mas
    não existe configuração ou token salvo. O utilizador deve executar
    ``suap login`` antes de usar os demais comandos.
    """


class SuapRequestError(SuapError):
    """Erro HTTP genérico retornado pela API.

    Levantada para respostas HTTP de erro que não se enquadram nas
    categorias mais específicas (4xx que não sejam 401/403/404/422 e 5xx).

    Attributes:
        args: Mensagem descrevendo o código HTTP e o corpo da resposta.
    """


class SuapValidationError(SuapRequestError):
    """Parâmetro inválido enviado à API (HTTP 422).

    Levantada quando a API rejeita a requisição por um parâmetro de tipo
    ou formato incorreto. A mensagem inclui o campo problemático e a razão,
    extraídos do corpo de resposta do Ninja/FastAPI.

    Example:
        Passar uma string onde a API espera um inteiro::

            client.edu.get_diary_classes("2024.1")
            # SuapValidationError: Parâmetro inválido: path -> id_diario: ...
    """


class SuapNotFoundError(SuapRequestError):
    """Recurso não encontrado (HTTP 404).

    Levantada quando o ID fornecido não corresponde a nenhum registro
    existente ou acessível pelo utilizador autenticado.
    """


class SuapForbiddenError(SuapRequestError):
    """Acesso negado ao recurso (HTTP 403).

    Levantada quando o utilizador autenticado não possui permissão para
    acessar o recurso solicitado.
    """


class SuapServerError(SuapRequestError):
    """Erro interno do servidor SUAP (HTTP 5xx).

    Levantada quando o servidor retorna um erro 5xx, indicando uma falha
    no lado do SUAP. Geralmente transitório; tentar novamente mais tarde
    pode resolver.
    """


class SuapConnectionError(SuapError):
    """Falha de rede ao tentar contactar o servidor.

    Levantada em situações de conectividade: host não encontrado (URL errada),
    timeout da requisição, erro de certificado SSL ou conexão recusada.
    """
