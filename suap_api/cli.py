import dataclasses
import json
import sys
import termios
import tty
from contextlib import contextmanager
from typing import Generator

import click

from .client import SuapClient
from .config import clear_config, clear_tokens, load_config, normalize_url, save_config, save_tokens
from .exceptions import (
    SuapAuthError,
    SuapConnectionError,
    SuapForbiddenError,
    SuapNotFoundError,
    SuapNotLoggedInError,
    SuapRequestError,
    SuapServerError,
    SuapTokenExpiredError,
    SuapValidationError,
)


@contextmanager
def handle_errors() -> Generator[None, None, None]:
    """Trata todos os erros do wrapper com mensagens amigáveis."""
    try:
        yield
    except SuapConnectionError as e:
        click.echo(f"Erro de conexao: {e}", err=True)
        raise SystemExit(1)
    except SuapAuthError:
        click.echo(
            "Matricula ou senha incorretos. Verifique os dados e tente novamente.",
            err=True,
        )
        raise SystemExit(1)
    except SuapTokenExpiredError:
        click.echo("Sessao expirada. Execute `suap login` novamente.", err=True)
        raise SystemExit(1)
    except SuapNotLoggedInError:
        click.echo(
            "Nenhuma sessao encontrada. Execute `suap login` primeiro.", err=True
        )
        raise SystemExit(1)
    except SuapValidationError as e:
        click.echo(f"Parametro invalido: {e}", err=True)
        raise SystemExit(1)
    except SuapNotFoundError as e:
        click.echo(f"Nao encontrado: {e}", err=True)
        raise SystemExit(1)
    except SuapForbiddenError as e:
        click.echo(f"Acesso negado: {e}", err=True)
        raise SystemExit(1)
    except SuapServerError as e:
        click.echo(f"Erro no servidor SUAP: {e}", err=True)
        raise SystemExit(1)
    except SuapRequestError as e:
        click.echo(f"Erro na requisicao: {e}", err=True)
        raise SystemExit(1)


def _prompt_password(prompt: str = "Senha") -> str:
    """Lê a senha do terminal exibindo '*' para cada caractere digitado."""
    click.echo(f"{prompt}: ", nl=False)
    password: list[str] = []
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                break
            if ch == "\x03":
                raise KeyboardInterrupt
            if ch in ("\x7f", "\x08"):  # Backspace
                if password:
                    password.pop()
                    click.echo("\b \b", nl=False)
            else:
                password.append(ch)
                click.echo("*", nl=False)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    click.echo()
    return "".join(password)


def _to_serializable(data: object) -> object:
    if dataclasses.is_dataclass(data) and not isinstance(data, type):
        return dataclasses.asdict(data)  # type: ignore[arg-type]
    if isinstance(data, list):
        return [_to_serializable(item) for item in data]
    return data


def _print_json(data: object) -> None:
    click.echo(json.dumps(_to_serializable(data), indent=2, ensure_ascii=False))


@click.group()
def main() -> None:
    """SUAP API CLI — acesse o SUAP pela linha de comando."""


@main.command()
def login() -> None:
    """Realiza login no SUAP."""
    url = click.prompt("URL da sua instancia SUAP (ex: https://suap.ifpi.edu.br)")
    username = click.prompt("Matricula")
    password = _prompt_password()

    base_url = normalize_url(url)

    with handle_errors():
        client = SuapClient(base_url=base_url)
        access, refresh = client.token.authenticate(username, password)
        save_tokens(username, access, refresh)
        save_config(base_url, username)
        click.echo("Login realizado com sucesso.")


@main.command()
def logout() -> None:
    """Encerra a sessao atual."""
    try:
        config = load_config()
        clear_tokens(config["username"])
    except Exception:
        pass
    clear_config()
    click.echo("Sessao encerrada.")


# ------------------------------------------------------------------
# Comandos — comum
# ------------------------------------------------------------------

@main.command("meus-dados")
def my_data() -> None:
    """Exibe os dados pessoais do usuario logado."""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.comum.get_my_data())


# ------------------------------------------------------------------
# Comandos — edu
# ------------------------------------------------------------------

@main.command("periodos")
def periods() -> None:
    """Lista os semestres letivos do aluno."""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_periods())


@main.command("diarios")
@click.argument("semestre")
def diaries(semestre: str) -> None:
    """Lista os diarios do aluno em um semestre. Exemplo: suap diarios 2024.1"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_diaries(semestre))


@main.command("professores")
@click.argument("id_diario", type=int)
def diary_professors(id_diario: int) -> None:
    """Lista os professores de um diario. Exemplo: suap professores 42"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_diary_professors(id_diario))


@main.command("aulas")
@click.argument("id_diario", type=int)
def diary_classes(id_diario: int) -> None:
    """Lista as aulas de um diario. Exemplo: suap aulas 42"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_diary_classes(id_diario))


@main.command("materiais")
@click.argument("id_diario", type=int)
def diary_materials(id_diario: int) -> None:
    """Lista os materiais de um diario. Exemplo: suap materiais 42"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_diary_materials(id_diario))


@main.command("material")
@click.argument("id_material", type=int)
def material(id_material: int) -> None:
    """Exibe um material especifico. Exemplo: suap material 10"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_material(id_material))


@main.command("material-pdf")
@click.argument("id_diario", type=int)
@click.argument("id_material", type=int)
def material_pdf(id_diario: int, id_material: int) -> None:
    """Baixa o PDF de um material em arquivo temporario. Exemplo: suap material-pdf 42 10"""
    import tempfile

    with handle_errors():
        with SuapClient() as client:
            pdf_bytes = client.edu.get_material_pdf(id_diario, id_material)

        with tempfile.NamedTemporaryFile(
            suffix=".pdf", prefix=f"suap_material_{id_material}_", delete=False
        ) as tmp:
            tmp.write(pdf_bytes)
            click.echo(tmp.name)


@main.command("trabalhos")
@click.argument("id_diario", type=int)
def diary_assignments(id_diario: int) -> None:
    """Lista os trabalhos de um diario. Exemplo: suap trabalhos 42"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_diary_assignments(id_diario))


@main.command("disciplinas")
@click.argument("semestre")
def disciplines(semestre: str) -> None:
    """Lista as disciplinas do aluno em um semestre. Exemplo: suap disciplinas 2024.1"""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_disciplines(semestre))


@main.command("dados-aluno")
def student_data() -> None:
    """Exibe os dados academicos do aluno (curso, situacao, etc)."""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_student_data())


@main.command("conclusao")
def graduation_requirements() -> None:
    """Exibe os requisitos de conclusao do curso."""
    with handle_errors():
        with SuapClient() as client:
            _print_json(client.edu.get_graduation_requirements())
