from typing import Any, Optional

import keyring
import requests

from .config import load_config
from .exceptions import (
    SuapConnectionError,
    SuapForbiddenError,
    SuapNotFoundError,
    SuapNotLoggedInError,
    SuapRequestError,
    SuapServerError,
    SuapTokenExpiredError,
    SuapValidationError,
)
from .resources import CommonResource, EduResource, TokenResource

KEYRING_ACCESS = "suap_api_access"
KEYRING_REFRESH = "suap_api_refresh"


def _parse_error(response: requests.Response) -> str:
    """Extrai a mensagem de erro mais legível do corpo da resposta."""
    try:
        data = response.json()
    except ValueError:
        return response.text or f"HTTP {response.status_code} sem corpo."

    # Formato 422 do Ninja: {"detail": [{"type": ..., "loc": [...], "msg": "..."}]}
    if isinstance(data.get("detail"), list):
        parts = []
        for err in data["detail"]:
            loc = " -> ".join(str(x) for x in err.get("loc", []))
            msg = err.get("msg", "")
            parts.append(f"{loc}: {msg}" if loc else msg)
        return "; ".join(parts)

    # Formato ErrorSchema: {"message": "..."}
    if isinstance(data.get("message"), str):
        return data["message"]

    # Formato DRF genérico: {"detail": "..."}
    if isinstance(data.get("detail"), str):
        return data["detail"]

    return response.text or f"HTTP {response.status_code}"


def _raise_for_status(response: requests.Response) -> None:
    """Lança a exceção correta com base no status HTTP."""
    status = response.status_code
    msg = _parse_error(response)

    if status == 403:
        raise SuapForbiddenError(f"Acesso negado: {msg}")
    if status == 404:
        raise SuapNotFoundError(f"Recurso não encontrado: {msg}")
    if status == 422:
        raise SuapValidationError(f"Parâmetro inválido: {msg}")
    if status >= 500:
        raise SuapServerError(
            f"Erro interno do servidor SUAP (HTTP {status}). Tente novamente mais tarde."
        )
    raise SuapRequestError(f"HTTP {status}: {msg}")


class SuapClient:
    """Cliente principal para a API do SUAP.

    Organiza o acesso à API por módulos, espelhando a estrutura do JSON
    de endpoints:

    Attributes:
        token (TokenResource): Endpoints de autenticação (``/api/token/``).
        comum (CommonResource): Endpoints de dados comuns (``/api/comum/``).
        edu (EduResource): Endpoints do módulo académico (``/api/edu/``).
        base_url (str): URL base da instância do SUAP.
        TIMEOUT (int): Tempo limite em segundos para todas as requisições.

    Example:
        Uso com sessão salva (após ``suap login``)::

            with SuapClient() as client:
                dados = client.comum.get_my_data()
                periodos = client.edu.get_periods()
                diarios = client.edu.get_diaries("2024.1")

        Uso manual sem configuração salva::

            with SuapClient(base_url="https://suap.ifpi.edu.br") as client:
                client.token.authenticate("20221234", "senha")
                dados = client.comum.get_my_data()
    """

    TIMEOUT = 10

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """Inicializa o cliente, carregando a sessão salva ou usando credenciais manuais.

        Se ``base_url`` for omitido, as configurações são lidas de
        ``~/.suap/config.json`` e os tokens são recuperados do keyring do sistema.

        Args:
            base_url: URL base da instância do SUAP
                (ex: ``"https://suap.ifpi.edu.br"``). Se ``None``, carrega
                da configuração salva.
            token: Access token JWT para uso imediato. Útil para testes ou
                integração direta sem sessão salva.

        Raises:
            SuapNotLoggedInError: Se ``base_url`` for ``None`` e não houver
                configuração salva ou token no keyring.
        """
        if base_url is not None:
            self.base_url = base_url.rstrip("/")
            self._access_token: Optional[str] = token
            self._refresh_token: Optional[str] = None
            self._username: Optional[str] = None
        else:
            config = load_config()
            self.base_url = config["base_url"].rstrip("/")
            self._username = config["username"]
            self._access_token = keyring.get_password(KEYRING_ACCESS, self._username)
            self._refresh_token = keyring.get_password(KEYRING_REFRESH, self._username)
            if not self._access_token:
                raise SuapNotLoggedInError(
                    "Token não encontrado. Execute `suap login`."
                )

        self._session = requests.Session()

        # Recursos organizados por módulo da API
        self.token = TokenResource(self)
        self.comum = CommonResource(self)
        self.edu = EduResource(self)

    def __enter__(self) -> "SuapClient":
        """Suporte a context manager — retorna a própria instância."""
        return self

    def __exit__(self, *_: Any) -> None:
        """Fecha a sessão HTTP ao sair do bloco ``with``."""
        self._session.close()

    # ------------------------------------------------------------------
    # Maquinaria interna — não faz parte da API pública
    # ------------------------------------------------------------------

    def _do_refresh(self) -> None:
        """Renova o access token usando o refresh token armazenado.

        Chamado automaticamente por :meth:`_do_request` ao receber HTTP 401.
        Atualiza ``_access_token`` e ``_refresh_token`` na instância e no keyring.

        Raises:
            SuapTokenExpiredError: Se não houver refresh token disponível ou
                se o servidor rejeitar o refresh (token completamente expirado).
        """
        if not self._refresh_token:
            raise SuapTokenExpiredError(
                "Sessão expirada. Execute `suap login` novamente."
            )
        try:
            response = self._session.post(
                f"{self.base_url}/api/token/refresh",
                json={"refresh": self._refresh_token},
                timeout=self.TIMEOUT,
            )
        except requests.exceptions.RequestException:
            raise SuapTokenExpiredError(
                "Sessão expirada e não foi possível renová-la. Execute `suap login` novamente."
            )
        if response.status_code in (400, 401):
            raise SuapTokenExpiredError(
                "Sessão expirada. Execute `suap login` novamente."
            )
        response.raise_for_status()
        data = response.json()
        self._access_token = data["access"]
        self._refresh_token = data["refresh"]
        if self._username:
            keyring.set_password(KEYRING_ACCESS, self._username, self._access_token)
            keyring.set_password(KEYRING_REFRESH, self._username, self._refresh_token)

    def _do_request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Executa uma requisição autenticada e retorna o JSON."""
        if not self._access_token:
            raise SuapNotLoggedInError("Token ausente. Execute `suap login`.")

        kwargs.setdefault("timeout", self.TIMEOUT)
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        try:
            response = self._session.request(
                method, f"{self.base_url}{path}", headers=headers, **kwargs
            )
        except requests.exceptions.SSLError:
            raise SuapConnectionError(
                "Erro de certificado SSL. Verifique se a URL usa HTTPS corretamente."
            )
        except requests.exceptions.ConnectionError:
            raise SuapConnectionError(
                "Não foi possível conectar ao servidor. Verifique sua conexão."
            )
        except requests.exceptions.Timeout:
            raise SuapConnectionError(
                "A requisição demorou demais. Verifique sua conexão e tente novamente."
            )

        if response.status_code == 401:
            self._do_refresh()
            headers["Authorization"] = f"Bearer {self._access_token}"
            response = self._session.request(
                method, f"{self.base_url}{path}", headers=headers, **kwargs
            )

        if not response.ok:
            _raise_for_status(response)

        if not response.content:
            return {}

        try:
            return response.json()
        except ValueError:
            raise SuapRequestError(
                f"A API retornou uma resposta inesperada (não-JSON): {response.text[:200]}"
            )

    def _do_request_binary(self, method: str, path: str, _absolute: bool = False, **kwargs: Any) -> bytes:
        """Executa uma requisição autenticada e retorna bytes (PDFs, etc.)."""
        if not self._access_token:
            raise SuapNotLoggedInError("Token ausente. Execute `suap login`.")

        kwargs.setdefault("timeout", self.TIMEOUT)
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self._access_token}"

        url = path if _absolute else f"{self.base_url}{path}"

        try:
            response = self._session.request(method, url, headers=headers, **kwargs)
        except requests.exceptions.SSLError:
            raise SuapConnectionError(
                "Erro de certificado SSL. Verifique se a URL usa HTTPS corretamente."
            )
        except requests.exceptions.ConnectionError:
            raise SuapConnectionError(
                "Não foi possível conectar ao servidor. Verifique sua conexão."
            )
        except requests.exceptions.Timeout:
            raise SuapConnectionError(
                "A requisição demorou demais. Verifique sua conexão e tente novamente."
            )

        if response.status_code == 401:
            self._do_refresh()
            headers["Authorization"] = f"Bearer {self._access_token}"
            response = self._session.request(method, url, headers=headers, **kwargs)

        if not response.ok:
            _raise_for_status(response)

        return response.content
