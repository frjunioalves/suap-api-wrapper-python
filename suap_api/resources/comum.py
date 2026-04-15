from typing import TYPE_CHECKING

from ..models.comum import DadosPessoais

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
        ...     print(dados.nome_usual)
    """

    def __init__(self, client: "SuapClient") -> None:
        self._client = client

    def get_my_data(self) -> DadosPessoais:
        """Obtém os dados pessoais do utilizador autenticado.

        Realiza um ``GET /api/comum/meus-dados/``.

        Returns:
            :class:`~suap_api.models.comum.DadosPessoais` com os dados do perfil.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> dados = client.comum.get_my_data()
            >>> print(dados.nome_usual)
            'João da Silva'
        """
        data = self._client._do_request("GET", "/api/comum/meus-dados/")
        return DadosPessoais.from_dict(data)
