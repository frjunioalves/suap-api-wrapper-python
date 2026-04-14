from unittest.mock import MagicMock, patch

import responses as rsps_lib
from click.testing import CliRunner

from suap_api.cli import main

BASE_URL = "https://suap.ifpi.edu.br"


class TestLoginCommand:
    @rsps_lib.activate
    def test_successful_login(self) -> None:
        rsps_lib.add(
            rsps_lib.POST,
            f"{BASE_URL}/api/token/pair",
            json={"access": "acc123", "refresh": "ref123", "username": "20221234"},
            status=200,
        )
        runner = CliRunner()
        with (
            patch("suap_api.cli.save_config") as mock_save,
            patch("suap_api.cli.keyring.set_password") as mock_keyring,
        ):
            result = runner.invoke(
                main,
                ["login"],
                input="https://suap.ifpi.edu.br\n20221234\nsenha123\n",
            )

        assert result.exit_code == 0, result.output
        assert "sucesso" in result.output
        mock_save.assert_called_once_with(BASE_URL, "20221234")
        assert mock_keyring.call_count == 2

    @rsps_lib.activate
    def test_login_with_wrong_credentials(self) -> None:
        rsps_lib.add(
            rsps_lib.POST,
            f"{BASE_URL}/api/token/pair",
            json={"detail": "No active account"},
            status=401,
        )
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["login"],
            input="https://suap.ifpi.edu.br\n20221234\nsenha_errada\n",
        )
        assert result.exit_code == 1
        assert "Matricula ou senha incorretos" in result.output


class TestLogoutCommand:
    def test_logout_clears_both_tokens(self) -> None:
        runner = CliRunner()
        with (
            patch(
                "suap_api.cli.load_config",
                return_value={"username": "20221234", "base_url": BASE_URL},
            ),
            patch("suap_api.cli.keyring.delete_password") as mock_del,
            patch("suap_api.cli.clear_config") as mock_clear,
        ):
            result = runner.invoke(main, ["logout"])

        assert result.exit_code == 0
        assert "encerrada" in result.output
        assert mock_del.call_count == 2
        mock_clear.assert_called_once()


def _make_mock_client() -> MagicMock:
    """Cria um mock de SuapClient com recursos (comum, edu) acessíveis."""
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    return mock_client


class TestMyDataCommand:
    def test_outputs_json(self) -> None:
        mock = _make_mock_client()
        mock.comum.get_my_data.return_value = {"nome": "Aluno Teste"}

        with patch("suap_api.cli.SuapClient", return_value=mock):
            result = CliRunner().invoke(main, ["meus-dados"])

        assert result.exit_code == 0
        assert "Aluno Teste" in result.output


class TestNewCommands:
    def test_periodos(self) -> None:
        mock = _make_mock_client()
        mock.edu.get_periods.return_value = [{"semestre": "2024.1"}]
        with patch("suap_api.cli.SuapClient", return_value=mock):
            result = CliRunner().invoke(main, ["periodos"])
        assert result.exit_code == 0
        assert "2024.1" in result.output

    def test_diarios(self) -> None:
        mock = _make_mock_client()
        mock.edu.get_diaries.return_value = [{"id": 1}]
        with patch("suap_api.cli.SuapClient", return_value=mock):
            result = CliRunner().invoke(main, ["diarios", "2024.1"])
        assert result.exit_code == 0

    def test_dados_aluno(self) -> None:
        mock = _make_mock_client()
        mock.edu.get_student_data.return_value = {"curso": "TADS"}
        with patch("suap_api.cli.SuapClient", return_value=mock):
            result = CliRunner().invoke(main, ["dados-aluno"])
        assert result.exit_code == 0
        assert "TADS" in result.output

    def test_conclusao(self) -> None:
        mock = _make_mock_client()
        mock.edu.get_graduation_requirements.return_value = {"ch_total": 3200}
        with patch("suap_api.cli.SuapClient", return_value=mock):
            result = CliRunner().invoke(main, ["conclusao"])
        assert result.exit_code == 0
        assert "3200" in result.output
