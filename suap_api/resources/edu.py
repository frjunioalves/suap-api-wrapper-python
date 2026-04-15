from typing import TYPE_CHECKING

from ..models.edu import (
    Aula,
    DadosAcademicos,
    Diario,
    Disciplina,
    Material,
    Periodo,
    Professor,
    RequisitosConclusao,
    Trabalho,
)

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
        ...     aulas = client.edu.get_diary_classes(diarios[0].id)
    """

    def __init__(self, client: "SuapClient") -> None:
        self._client = client

    def get_periods(self) -> list[Periodo]:
        """Lista os semestres letivos do aluno.

        Realiza um ``GET /api/edu/periodos``.

        Returns:
            Lista de :class:`~suap_api.models.edu.Periodo`.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> periodos = client.edu.get_periods()
            >>> print(periodos[0].semestre)
            '2024.1'
        """
        data = self._client._do_request("GET", "/api/edu/periodos")
        return [Periodo.from_dict(p) for p in data]

    def get_diaries(self, semestre: str) -> list[Diario]:
        """Lista os diários do aluno em um semestre letivo.

        Realiza um ``GET /api/edu/diarios/{semestre}``.

        Args:
            semestre: Identificador do semestre no formato ``"AAAA.P"``
                (ex: ``"2024.1"``).

        Returns:
            Lista de :class:`~suap_api.models.edu.Diario`.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapNotFoundError: Se o semestre informado não existir.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> diarios = client.edu.get_diaries("2024.1")
            >>> id_diario = diarios[0].id
        """
        data = self._client._do_request("GET", f"/api/edu/diarios/{semestre}")
        return [Diario.from_dict(d) for d in data]

    def get_diary_professors(self, id_diario: int) -> list[Professor]:
        """Lista os professores de um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/professores``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de :class:`~suap_api.models.edu.Professor`.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> professores = client.edu.get_diary_professors(42)
            >>> print(professores[0].nome)
        """
        data = self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/professores")
        return [Professor.from_dict(p) for p in data]

    def get_diary_classes(self, id_diario: int) -> list[Aula]:
        """Lista as aulas registradas em um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/aulas``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de :class:`~suap_api.models.edu.Aula`.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> aulas = client.edu.get_diary_classes(42)
            >>> print(aulas[0].data)
        """
        data = self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/aulas")
        return [Aula.from_dict(a) for a in data]

    def get_diary_materials(self, id_diario: int) -> list[Material]:
        """Lista os materiais disponíveis em um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/materiais``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de :class:`~suap_api.models.edu.Material`.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> materiais = client.edu.get_diary_materials(42)
            >>> id_material = materiais[0].id
        """
        data = self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/materiais")
        return [Material.from_dict(m) for m in data]

    def get_material(self, id_material: int) -> Material:
        """Obtém os detalhes de um material específico.

        Realiza um ``GET /api/edu/materiais/{id_material}``.

        Args:
            id_material: Identificador numérico do material, obtido via
                :meth:`get_diary_materials`.

        Returns:
            :class:`~suap_api.models.edu.Material` com os metadados do arquivo.

        Raises:
            SuapNotFoundError: Se o material com o ID fornecido não existir.
            SuapValidationError: Se ``id_material`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> material = client.edu.get_material(10)
            >>> print(material.titulo)
        """
        data = self._client._do_request("GET", f"/api/edu/materiais/{id_material}")
        return Material.from_dict(data)

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

    def get_diary_assignments(self, id_diario: int) -> list[Trabalho]:
        """Lista os trabalhos de um diário.

        Realiza um ``GET /api/edu/diarios/{id_diario}/trabalhos``.

        Args:
            id_diario: Identificador numérico do diário, obtido via
                :meth:`get_diaries`.

        Returns:
            Lista de :class:`~suap_api.models.edu.Trabalho`.

        Raises:
            SuapNotFoundError: Se o diário com o ID fornecido não existir.
            SuapValidationError: Se ``id_diario`` não for um inteiro válido.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> trabalhos = client.edu.get_diary_assignments(42)
            >>> print(trabalhos[0].titulo)
        """
        data = self._client._do_request("GET", f"/api/edu/diarios/{id_diario}/trabalhos")
        return [Trabalho.from_dict(t) for t in data]

    def get_disciplines(self, semestre: str) -> list[Disciplina]:
        """Lista as disciplinas do aluno com notas e situação em um semestre.

        Realiza um ``GET /api/edu/disciplinas/{semestre}``.

        Args:
            semestre: Identificador do semestre no formato ``"AAAA.P"``
                (ex: ``"2024.1"``).

        Returns:
            Lista de :class:`~suap_api.models.edu.Disciplina`.

        Raises:
            SuapNotFoundError: Se o semestre informado não existir.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> disciplinas = client.edu.get_disciplines("2024.1")
            >>> print(disciplinas[0].disciplina)
        """
        data = self._client._do_request("GET", f"/api/edu/disciplinas/{semestre}")
        return [Disciplina.from_dict(d) for d in data]

    def get_student_data(self) -> DadosAcademicos:
        """Obtém os dados académicos do aluno com foco no curso.

        Realiza um ``GET /api/edu/meus-dados-aluno/``.

        Returns:
            :class:`~suap_api.models.edu.DadosAcademicos` com curso, turma e situação.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> dados = client.edu.get_student_data()
            >>> print(dados.curso)
        """
        data = self._client._do_request("GET", "/api/edu/meus-dados-aluno/")
        return DadosAcademicos.from_dict(data)

    def get_graduation_requirements(self) -> RequisitosConclusao:
        """Obtém os requisitos de conclusão do curso do aluno autenticado.

        Realiza um ``GET /api/edu/requisitos-conclusao/``.

        Returns:
            :class:`~suap_api.models.edu.RequisitosConclusao` com carga horária e pendências.

        Raises:
            SuapNotLoggedInError: Se não houver sessão ativa.
            SuapTokenExpiredError: Se o token expirar e não puder ser renovado.
            SuapConnectionError: Se não for possível conectar ao servidor.

        Example:
            >>> conclusao = client.edu.get_graduation_requirements()
            >>> print(conclusao.ch_total)
        """
        data = self._client._do_request("GET", "/api/edu/requisitos-conclusao/")
        return RequisitosConclusao.from_dict(data)
