from unittest.mock import MagicMock

import pytest
import responses as rsps_lib

from suap_api.client import SuapClient
from suap_api.exceptions import SuapAuthError, SuapRequestError, SuapTokenExpiredError
from suap_api.models import (
    Aula,
    DadosAcademicos,
    DadosPessoais,
    Diario,
    Disciplina,
    Material,
    Periodo,
    Professor,
    RequisitosConclusao,
    Trabalho,
)

BASE_URL = "https://suap.ifpi.edu.br"


def make_client(access: str = "access-token", refresh: str = "refresh-token") -> SuapClient:
    client = SuapClient(base_url=BASE_URL, token=access)
    client._refresh_token = refresh
    return client


# ------------------------------------------------------------------
# token
# ------------------------------------------------------------------

class TestTokenResource:
    @rsps_lib.activate
    def test_authenticate_returns_pair(self) -> None:
        rsps_lib.add(
            rsps_lib.POST,
            f"{BASE_URL}/api/token/pair",
            json={"access": "acc123", "refresh": "ref123", "username": "20221234"},
            status=200,
        )
        client = SuapClient(base_url=BASE_URL)
        access, refresh = client.token.authenticate("20221234", "senha")
        assert access == "acc123"
        assert refresh == "ref123"
        assert client._access_token == "acc123"
        assert client._refresh_token == "ref123"

    @rsps_lib.activate
    def test_authenticate_raises_on_401(self) -> None:
        rsps_lib.add(
            rsps_lib.POST,
            f"{BASE_URL}/api/token/pair",
            json={"detail": "No active account"},
            status=401,
        )
        client = SuapClient(base_url=BASE_URL)
        with pytest.raises(SuapAuthError):
            client.token.authenticate("20221234", "errada")

    @rsps_lib.activate
    def test_verify_returns_true_when_valid(self) -> None:
        rsps_lib.add(rsps_lib.POST, f"{BASE_URL}/api/token/verify", status=200)
        assert make_client().token.verify("some-token") is True

    @rsps_lib.activate
    def test_verify_returns_false_when_invalid(self) -> None:
        rsps_lib.add(rsps_lib.POST, f"{BASE_URL}/api/token/verify", status=401)
        assert make_client().token.verify("bad-token") is False


# ------------------------------------------------------------------
# _do_request (maquinaria interna)
# ------------------------------------------------------------------

class TestDoRequest:
    @rsps_lib.activate
    def test_injects_bearer_header(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/comum/meus-dados/",
            json={"nome_usual": "Aluno"},
            status=200,
        )
        make_client().comum.get_my_data()
        assert rsps_lib.calls[0].request.headers["Authorization"] == "Bearer access-token"

    @rsps_lib.activate
    def test_retries_with_refresh_on_401(self) -> None:
        rsps_lib.add(rsps_lib.GET, f"{BASE_URL}/api/comum/meus-dados/", status=401)
        rsps_lib.add(
            rsps_lib.POST,
            f"{BASE_URL}/api/token/refresh",
            json={"access": "new-access", "refresh": "new-refresh"},
            status=200,
        )
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/comum/meus-dados/",
            json={"nome_usual": "Aluno"},
            status=200,
        )
        client = make_client()
        data = client.comum.get_my_data()
        assert isinstance(data, DadosPessoais)
        assert client._access_token == "new-access"

    @rsps_lib.activate
    def test_raises_token_expired_when_refresh_fails(self) -> None:
        rsps_lib.add(rsps_lib.GET, f"{BASE_URL}/api/comum/meus-dados/", status=401)
        rsps_lib.add(rsps_lib.POST, f"{BASE_URL}/api/token/refresh", status=401)
        with pytest.raises(SuapTokenExpiredError):
            make_client().comum.get_my_data()

    @rsps_lib.activate
    def test_raises_request_error_on_404(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/comum/meus-dados/",
            json={"message": "Not found"},
            status=404,
        )
        with pytest.raises(SuapRequestError):
            make_client().comum.get_my_data()


# ------------------------------------------------------------------
# comum
# ------------------------------------------------------------------

class TestCommonResource:
    @rsps_lib.activate
    def test_get_my_data(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/comum/meus-dados/",
            json={"nome_usual": "Aluno Teste", "matricula": "20221234"},
            status=200,
        )
        dados = make_client().comum.get_my_data()
        assert isinstance(dados, DadosPessoais)
        assert dados.nome_usual == "Aluno Teste"
        assert dados.matricula == "20221234"


# ------------------------------------------------------------------
# edu
# ------------------------------------------------------------------

class TestEduResource:
    @rsps_lib.activate
    def test_get_periods(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/periodos",
            json=[{"semestre": "2024.1", "situacao": "Concluído"}],
            status=200,
        )
        periodos = make_client().edu.get_periods()
        assert isinstance(periodos[0], Periodo)
        assert periodos[0].semestre == "2024.1"

    @rsps_lib.activate
    def test_get_diaries(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/diarios/2024.1",
            json=[{"id": 1, "disciplina": "Algoritmos"}],
            status=200,
        )
        diarios = make_client().edu.get_diaries("2024.1")
        assert isinstance(diarios[0], Diario)
        assert diarios[0].id == 1

    @rsps_lib.activate
    def test_get_diary_professors(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/diarios/42/professores",
            json=[{"nome": "Prof", "email": "prof@ifpi.edu.br"}],
            status=200,
        )
        professores = make_client().edu.get_diary_professors(42)
        assert isinstance(professores[0], Professor)
        assert professores[0].nome == "Prof"

    @rsps_lib.activate
    def test_get_diary_classes(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/diarios/42/aulas",
            json=[{"data": "2024-03-01", "quantidade": 2, "faltas": 0}],
            status=200,
        )
        aulas = make_client().edu.get_diary_classes(42)
        assert isinstance(aulas[0], Aula)
        assert aulas[0].data == "2024-03-01"

    @rsps_lib.activate
    def test_get_diary_materials(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/diarios/42/materiais",
            json=[{"id": 5, "data": "2024-03-01", "descricao": "Slide 1", "url": None}],
            status=200,
        )
        materiais = make_client().edu.get_diary_materials(42)
        assert isinstance(materiais[0], Material)
        assert materiais[0].id == 5

    @rsps_lib.activate
    def test_get_material(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/materiais/5",
            json={"id": 5, "data": "2024-03-01", "descricao": "Slide 1", "url": None},
            status=200,
        )
        material = make_client().edu.get_material(5)
        assert isinstance(material, Material)
        assert material.descricao == "Slide 1"

    @rsps_lib.activate
    def test_get_material_pdf(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/materiais/42/5/pdf/",
            body=b"%PDF-1.4 fake",
            status=200,
        )
        assert make_client().edu.get_material_pdf(42, 5) == b"%PDF-1.4 fake"

    @rsps_lib.activate
    def test_get_diary_assignments(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/diarios/42/trabalhos",
            json=[{"id": 1, "titulo": "T1"}],
            status=200,
        )
        trabalhos = make_client().edu.get_diary_assignments(42)
        assert isinstance(trabalhos[0], Trabalho)
        assert trabalhos[0].titulo == "T1"

    @rsps_lib.activate
    def test_get_disciplines(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/disciplinas/2024.1",
            json=[{
                "id": 1,
                "nome": "Algoritmos",
                "sigla": "TEC.0001",
                "situacao": {"rotulo": "Cursando", "status": "info"},
                "ch_total_aula": 60,
                "qtd_faltas": 2,
                "frequencia": 90.0,
                "notas": [{"tipo": "N1", "nota": None}],
                "medias": [{"tipo": "MD", "nota": None}],
            }],
            status=200,
        )
        disciplinas = make_client().edu.get_disciplines("2024.1")
        assert isinstance(disciplinas[0], Disciplina)
        assert disciplinas[0].nome == "Algoritmos"
        assert disciplinas[0].id == 1
        assert disciplinas[0].qtd_faltas == 2

    @rsps_lib.activate
    def test_get_student_data(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/meus-dados-aluno/",
            json={"curso": "TADS", "turma": "2022.1"},
            status=200,
        )
        dados = make_client().edu.get_student_data()
        assert isinstance(dados, DadosAcademicos)
        assert dados.curso == "TADS"

    @rsps_lib.activate
    def test_get_graduation_requirements(self) -> None:
        rsps_lib.add(
            rsps_lib.GET,
            f"{BASE_URL}/api/edu/requisitos-conclusao/",
            json={"ch_total": 3200, "ch_cumprida": 1600},
            status=200,
        )
        conclusao = make_client().edu.get_graduation_requirements()
        assert isinstance(conclusao, RequisitosConclusao)
        assert conclusao.ch_total == 3200


# ------------------------------------------------------------------
# context manager
# ------------------------------------------------------------------

class TestContextManager:
    def test_closes_session_on_exit(self) -> None:
        client = make_client()
        client._session.close = MagicMock()
        with client:
            pass
        client._session.close.assert_called_once()
