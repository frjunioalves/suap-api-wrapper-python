import json
import os
from pathlib import Path
from typing import TypedDict

from .exceptions import SuapNotLoggedInError

CONFIG_DIR = Path.home() / ".suap"
CONFIG_FILE = CONFIG_DIR / "config.json"


class Config(TypedDict):
    """Estrutura do ficheiro de configuração salvo em ``~/.suap/config.json``.

    Attributes:
        base_url: URL base da instância do SUAP (ex: ``https://suap.ifpi.edu.br``).
        username: Matrícula do utilizador autenticado.
    """

    base_url: str
    username: str


def normalize_url(url: str) -> str:
    """Normaliza a URL fornecida pelo aluno para o domínio base da API.

    Garante que a URL tenha o esquema ``https://``, remove barras finais e
    elimina o sufixo ``/api/v2`` caso o aluno o tenha incluído por engano.

    Args:
        url: URL digitada pelo aluno. Pode estar em qualquer um dos formatos::

                "suap.ifpi.edu.br"
                "https://suap.ifpi.edu.br/"
                "https://suap.ifpi.edu.br/api/v2"

    Returns:
        URL normalizada no formato ``https://<dominio>`` sem barra final,
        pronta para ser usada como ``base_url`` do cliente.

    Example:
        >>> normalize_url("suap.ifpi.edu.br")
        'https://suap.ifpi.edu.br'
        >>> normalize_url("https://suap.ifpi.edu.br/api/v2/")
        'https://suap.ifpi.edu.br'
    """
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    for suffix in ("/api/v2/", "/api/v2"):
        if url.endswith(suffix.rstrip("/")):
            url = url[: -len(suffix.rstrip("/"))]
            break
    return url


def save_config(base_url: str, username: str) -> None:
    """Persiste a configuração de sessão em ``~/.suap/config.json``.

    Cria o diretório ``~/.suap/`` caso não exista e define a permissão do
    ficheiro como ``600`` (leitura/escrita apenas pelo dono).

    Args:
        base_url: URL base da instância do SUAP normalizada.
        username: Matrícula do utilizador autenticado.
    """
    CONFIG_DIR.mkdir(exist_ok=True)
    data: Config = {"base_url": base_url, "username": username}
    CONFIG_FILE.write_text(json.dumps(data, indent=2))
    os.chmod(CONFIG_FILE, 0o600)


def load_config() -> Config:
    """Carrega a configuração de sessão salva em disco.

    Returns:
        Dicionário com ``base_url`` e ``username`` da sessão ativa.

    Raises:
        SuapNotLoggedInError: Se o ficheiro ``~/.suap/config.json`` não existir,
            indicando que nenhum login foi realizado.
    """
    if not CONFIG_FILE.exists():
        raise SuapNotLoggedInError(
            "Nenhuma sessão encontrada. Execute `suap login` primeiro."
        )
    return json.loads(CONFIG_FILE.read_text())


def clear_config() -> None:
    """Remove o ficheiro de configuração de sessão do disco.

    Não levanta exceção caso o ficheiro já não exista.
    """
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
