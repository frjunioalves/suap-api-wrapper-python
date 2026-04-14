from typing import TYPE_CHECKING, Tuple

import requests

from ..exceptions import SuapAuthError, SuapConnectionError

if TYPE_CHECKING:
    from ..client import SuapClient


class TokenResource:
    """Recurso de autenticação da API do SUAP (``/api/token/``).

    Responsável pela obtenção e verificação de tokens JWT.
    Acedido via ``client.token``.

    Note:
        A renovação automática do access token (refresh) é gerida
        internamente pelo :class:`~suap_api.client.SuapClient` e não
        está exposta neste recurso.

    Example:
        >>> with SuapClient(base_url="https://suap.ifpi.edu.br") as client:
        ...     access, refresh = client.token.authenticate("20221234", "senha")
    """

    def __init__(self, client: "SuapClient") -> None:
        """Inicializa o recurso com uma referência ao cliente principal.

        Args:
            client: Instância de :class:`~suap_api.client.SuapClient` que
                fornece a sessão HTTP e a URL base.
        """
        self._client = client

    def authenticate(self, username: str, password: str) -> Tuple[str, str]:
        """Obtém o par de tokens JWT via credenciais.

        Realiza um ``POST /api/token/pair`` com as credenciais fornecidas
        e armazena os tokens resultantes no cliente para uso nas
        requisições subsequentes.

        Args:
            username: Matrícula do aluno (ex: ``"20221234TADS0014"``).
            password: Senha da conta SUAP.

        Returns:
            Tupla ``(access_token, refresh_token)`` com os tokens JWT.

        Raises:
            SuapAuthError: Se a matrícula ou senha forem inválidas (HTTP 401).
            SuapConnectionError: Se não for possível conectar ao servidor
                (URL errada, sem internet, timeout ou erro SSL).

        Example:
            >>> access, refresh = client.token.authenticate("20221234", "senha")
        """
        try:
            response = self._client._session.post(
                f"{self._client.base_url}/api/token/pair",
                json={"username": username, "password": password},
                timeout=self._client.TIMEOUT,
            )
        except requests.exceptions.SSLError:
            raise SuapConnectionError(
                "Erro de certificado SSL. Verifique se a URL usa HTTPS corretamente."
            )
        except requests.exceptions.ConnectionError:
            raise SuapConnectionError(
                f"Não foi possível conectar a '{self._client.base_url}'. "
                "Verifique se a URL está correta e se há conexão com a internet."
            )
        except requests.exceptions.Timeout:
            raise SuapConnectionError(
                "A requisição demorou demais. Verifique sua conexão e tente novamente."
            )

        if response.status_code == 401:
            raise SuapAuthError("Matrícula ou senha incorretos.")
        response.raise_for_status()

        data = response.json()
        self._client._access_token = data["access"]
        self._client._refresh_token = data["refresh"]
        return data["access"], data["refresh"]

    def verify(self, token: str) -> bool:
        """Verifica se um token JWT é válido junto ao servidor.

        Realiza um ``POST /api/token/verify``. Em caso de falha de rede,
        retorna ``False`` sem levantar exceção.

        Args:
            token: Token JWT (access ou refresh) a ser verificado.

        Returns:
            ``True`` se o token for válido, ``False`` caso contrário.

        Example:
            >>> is_valid = client.token.verify(access_token)
        """
        try:
            response = self._client._session.post(
                f"{self._client.base_url}/api/token/verify",
                json={"token": token},
                timeout=self._client.TIMEOUT,
            )
        except requests.exceptions.RequestException:
            return False
        return response.ok
