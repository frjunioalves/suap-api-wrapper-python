from .base import RawMixin
from .comum import DadosPessoais, Vinculo
from .edu import (
    Aula,
    DadosAcademicos,
    Diario,
    Disciplina,
    Horario,
    Local,
    Material,
    Mensagem,
    Nota,
    Periodo,
    Professor,
    RequisitosConclusao,
    Trabalho,
)

__all__ = [
    "RawMixin",
    "DadosPessoais",
    "Vinculo",
    "Periodo",
    "Diario",
    "Horario",
    "Local",
    "Professor",
    "Aula",
    "Material",
    "Trabalho",
    "Disciplina",
    "Nota",
    "Mensagem",
    "DadosAcademicos",
    "RequisitosConclusao",
]
