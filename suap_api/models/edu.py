import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class Periodo:
    id: Optional[int] = None
    semestre: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Periodo":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Horario:
    dia: Optional[str] = None
    horario: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Horario":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Local:
    id: Optional[int] = None
    sala: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Local":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Diario:
    id: Optional[int] = None
    disciplina: Optional[Any] = None
    professor: Optional[list] = None
    horario: Optional[list] = None
    local: Optional[Any] = None
    ambiente_virtual: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Diario":
        professor = [Professor.from_dict(p) for p in (data.get("professor") or [])]
        horario = [Horario.from_dict(h) for h in (data.get("horario") or [])]
        local = Local.from_dict(data["local"]) if data.get("local") else None
        known = {f.name for f in dataclasses.fields(cls)} - {"professor", "horario", "local"}
        return cls(**{k: v for k, v in data.items() if k in known}, professor=professor, horario=horario, local=local)


@dataclasses.dataclass
class Professor:
    id: Optional[int] = None
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
    faltas: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Aula":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Material:
    id: Optional[int] = None
    data: Optional[str] = None
    descricao: Optional[str] = None
    url: Optional[str] = None

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
class Nota:
    tipo: Optional[str] = None
    nota: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Nota":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclasses.dataclass
class Disciplina:
    id: Optional[int] = None
    nome: Optional[str] = None
    sigla: Optional[str] = None
    situacao: Optional[Any] = None
    ch_total_aula: Optional[int] = None
    ch_total_relogio: Optional[int] = None
    ch_cumprida_aula: Optional[int] = None
    qtd_faltas: Optional[int] = None
    qtd_avaliacoes: Optional[int] = None
    frequencia: Optional[float] = None
    notas: Optional[list] = None
    medias: Optional[list] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Disciplina":
        notas = [Nota.from_dict(n) for n in data.get("notas", [])]
        medias = [Nota.from_dict(m) for m in data.get("medias", [])]
        known = {f.name for f in dataclasses.fields(cls)} - {"notas", "medias"}
        return cls(**{k: v for k, v in data.items() if k in known}, notas=notas, medias=medias)


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
    ingresso: Optional[str] = None
    email_academico: Optional[str] = None
    email_escolar: Optional[str] = None
    cpf: Optional[str] = None
    periodo_referencia: Optional[int] = None
    ira: Optional[str] = None
    curso: Optional[str] = None
    matriz: Optional[str] = None
    qtd_periodos: Optional[int] = None
    situacao: Optional[str] = None
    data_migracao: Optional[str] = None
    impressao_digital: Optional[bool] = None
    emitiu_diploma: Optional[bool] = None
    educasenso: Optional[str] = None

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
