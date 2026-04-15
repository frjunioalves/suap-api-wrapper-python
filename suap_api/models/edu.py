import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class Periodo:
    semestre: Optional[str] = None
    situacao: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Periodo":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Diario:
    id: Optional[int] = None
    disciplina: Optional[str] = None
    componente_curricular: Optional[str] = None
    situacao: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Diario":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Professor:
    nome: Optional[str] = None
    email: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Professor":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Aula:
    id: Optional[int] = None
    etapa: Optional[str] = None
    data: Optional[str] = None
    conteudo: Optional[str] = None
    qtd_aulas: Optional[int] = None
    quantidade: Optional[int] = None  # mantido por compatibilidade
    faltas: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Aula":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Material:
    id: Optional[int] = None
    titulo: Optional[str] = None
    tipo: Optional[str] = None
    data_publicacao: Optional[str] = None
    descricao: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Material":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Trabalho:
    id: Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_entrega: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Trabalho":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Disciplina:
    id_diario: Optional[int] = None
    disciplina: Optional[str] = None
    carga_horaria: Optional[int] = None
    nota_etapa_1: Optional[Any] = None
    nota_etapa_2: Optional[Any] = None
    media: Optional[Any] = None
    faltas: Optional[int] = None
    situacao: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Disciplina":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Mensagem:
    id: Optional[int] = None
    assunto: Optional[str] = None
    remetente: Optional[str] = None
    data_envio: Optional[str] = None
    lida: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Mensagem":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class DadosAcademicos:
    curso: Optional[str] = None
    turma: Optional[str] = None
    situacao: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DadosAcademicos":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class RequisitosConclusao:
    ch_total: Optional[int] = None
    ch_cumprida: Optional[int] = None
    pendencias: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RequisitosConclusao":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})
