from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from ..client import SuapClient


class CommonResource:
    """Recurso de dados comuns da API do SUAP (``/api/comum/``).

    Contém endpoints relacionados a informações gerais do utilizador
    autenticado, independentes do módulo académico.
    Acedido via ``client.comum``.

    Example:
        >>> with SuapClient() as client:
        ...     dados = client.comum.get_my_data()
        ...     print(dados["nome"])
    """

    def __init__(self, client: "SuapClient") -> None:
        """Inicializa o recurso com uma referência ao cliente principal.

        Args:
            client: Instância de :class:`~suap_api.client.SuapClient` que
                fornece a sessão autenticada e a URL base.
        """
        self._client = client

    def get_my_data(self) -> Dict[str, Any]:
        """Obtém os dados pessoais do utilizador autenticado.

        Realiza um ``GET /api/comum/meus-dados/``.

        Returns:
            Dicionário com os dados do perfil, incluindo nome, matrícula,
            e-mail, foto e informações de vínculo institucional.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> dados = client.comum.get_my_data()
            >>> print(dados["nome"])
            'João da Silva'
        """
        return self._client._do_request("GET", "/api/comum/meus-dados/")
