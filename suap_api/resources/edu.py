from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from ..client import SuapClient


class EduResource:
    """Recurso do módulo académico da API do SUAP (``/api/edu/``).

    Centraliza todos os endpoints relacionados à vida académica do aluno:
    períodos letivos, diários, aulas, materiais, trabalhos, disciplinas
    e dados de conclusão de curso.
    Acedido via ``client.edu``.

    Example:
        >>> with SuapClient() as client:
        ...     periodos = client.edu.get_periods()
        ...     diarios = client.edu.get_diaries("2024.1")
        ...     aulas = client.edu.get_diary_classes(diarios[0]["id"])
    """

    def __init__(self, client: "SuapClient") -> None:
        """Inicializa o recurso com uma referência ao cliente principal.

        Args:
            client: Instância de :class:`~suap_api.client.SuapClient` que
                fornece a sessão autenticada e a URL base.
        """
        self._client = client

    def get_periods(self) -> List[Any]:
        """Lista os semestres letivos do aluno.

        Realiza um ``GET /api/edu/periodos``.

        Returns:
            Lista de dicionários, cada um representando um período letivo
            com informações como ano, semestre e situação.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> periodos = client.edu.get_periods()
            >>> print(periodos[0]["semestre"])
            '2024.1'
        """
        return self._client._do_request("GET", "/api/edu/periodos")

    def get_diaries(self, semestre: str) -> List[Any]:
        """Lista os diários do aluno em um semestre letivo.

        Realiza um ``GET /api/edu/diarios/{semestre}``.

        Args:
            semestre: Identificador do semestre no formato ``"AAAA.P"``
                (ex: ``"2024.1"``).

        Returns:
            Lista de diários, cada um contendo o ``id`` do diário,
            nome da disciplina e demais informações académicas.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapNotFoundError: Se o semestre informado não existir.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> diarios = client.edu.get_diaries("2024.1")
            >>> id_diario = diarios[0]["id"]
        """
        return self._client._do_request("GET", f"/api/edu/diarios/{semestre}")

    def get_diary_professors(self, id_diario: int) -> List[Any]:
        """Lista os professores de um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/professores``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de dicionários com nome e dados de cada professor.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> professores = client.edu.get_diary_professors(42)
        """
        return self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/professores")

    def get_diary_classes(self, id_diario: int) -> List[Any]:
        """Lista as aulas registradas em um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/aulas``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de aulas com data, conteúdo e número de faltas.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> aulas = client.edu.get_diary_classes(42)
        """
        return self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/aulas")

    def get_diary_materials(self, id_diario: int) -> List[Any]:
        """Lista os materiais disponíveis em um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/materiais``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de materiais, cada um com ``id``, título e tipo de arquivo.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> materiais = client.edu.get_diary_materials(42)
            >>> id_material = materiais[0]["id"]
        """
        return self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/materiais")

    def get_material(self, id_material: int) -> Dict[str, Any]:
        """Obtém os detalhes de um material específico.

        Realiza um ``GET /api/edu/materiais/{id_material}``.

        Args:
            id_material: Identificador numérico do material, obtido via
                :meth:`get_diary_materials`.

        Returns:
            Dicionário com título, tipo, data de publicação e demais
            metadados do material.

        Raises:
            SuapNotFoundError: Se o material com o ID fornecido não existir.
            SuapValidationError: Se ``id_material`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> material = client.edu.get_material(10)
            >>> print(material["titulo"])
        """
        return self._client._do_request("GET", f"/api/edu/materiais/{id_material}")

    def get_material_pdf(self, id_diario: int, id_material: int) -> bytes:
        """Baixa o conteúdo PDF de um material.

        Realiza um ``GET /api/edu/materiais/{id_diario}/{id_material}/pdf/``
        para obter a URL do arquivo e, em seguida, faz o download e retorna
        os bytes brutos do PDF.

        Args:
            id_diario: Identificador numérico do diário ao qual o material
                pertence, obtido via :meth:`get_diaries`.
            id_material: Identificador numérico do material, obtido via
                :meth:`get_diary_materials`.

        Returns:
            Conteúdo binário do PDF.

        Raises:
            SuapNotFoundError: Se o material ou diário não existirem.
            SuapValidationError: Se algum dos IDs não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> pdf_bytes = client.edu.get_material_pdf(42, 10)
            >>> with open("aula.pdf", "wb") as f:
            ...     f.write(pdf_bytes)
        """
        url: str = self._client._do_request(
            "GET", f"/api/edu/materiais/{id_diario}/{id_material}/pdf/"
        )
        if url.startswith("http://"):
            url = "https://" + url[7:]
        return self._client._do_request_binary("GET", url, _absolute=True)

    def get_diary_assignments(self, id_diario: int) -> List[Any]:
        """Lista os trabalhos de um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/trabalhos``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de trabalhos com título, descrição e prazo de entrega.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> trabalhos = client.edu.get_diary_assignments(42)
        """
        return self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/trabalhos")

    def get_disciplines(self, semestre: str) -> List[Any]:
        """Lista as disciplinas do aluno com notas e situação em um semestre.

        Realiza um ``GET /api/edu/disciplinas/{semestre}``.

        Args:
            semestre: Identificador do semestre no formato ``"AAAA.P"``
                (ex: ``"2024.1"``).

        Returns:
            Lista de disciplinas com notas por etapa, faltas e situação
            final do aluno em cada uma.

        Raises:
            SuapNotFoundError: Se o semestre informado não existir.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> disciplinas = client.edu.get_disciplines("2024.1")
        """
        return self._client._do_request("GET", f"/api/edu/disciplinas/{semestre}")

    def get_student_data(self) -> Dict[str, Any]:
        """Obtém os dados académicos do aluno com foco no curso.

        Realiza um ``GET /api/edu/meus-dados-aluno/``.

        Returns:
            Dicionário com informações do curso, turma, situação de matrícula
            e dados académicos relevantes do aluno autenticado.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> dados = client.edu.get_student_data()
            >>> print(dados["curso"])
        """
        return self._client._do_request("GET", "/api/edu/meus-dados-aluno/")

    def get_graduation_requirements(self) -> Dict[str, Any]:
        """Obtém os requisitos de conclusão do curso do aluno autenticado.

        Realiza um ``GET /api/edu/requisitos-conclusao/``.

        Returns:
            Dicionário com carga horária total exigida, carga horária
            cumprida, componentes pendentes e situação geral de conclusão.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> conclusao = client.edu.get_graduation_requirements()
            >>> print(conclusao["ch_total"])
        """
        return self._client._do_request("GET", "/api/edu/requisitos-conclusao/")
