import dataclasses
from typing import Any, List, Optional

# Strings que a API retorna no lugar de ausência de dados real
_GARBAGE_STRINGS = {"NoneNone", "None - / -", "-", ""}


def _sanitize_str(value: Optional[str]) -> Optional[str]:
    """Converte strings-lixo da API (ex: ``"NoneNone"``) em ``None``."""
    if value is None:
        return None
    return None if value.strip() in _GARBAGE_STRINGS else value


@dataclasses.dataclass
class Vinculo:
    id: Optional[int] = None
    matricula: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    turno: Optional[str] = None
    curso: Optional[str] = None
    campus: Optional[str] = None
    situacao: Optional[str] = None
    cota_sistec: Optional[str] = None
    cota_mec: Optional[str] = None
    situacao_sistemica: Optional[str] = None
    matricula_regular: Optional[bool] = None
    linha_pesquisa: Optional[str] = None
    curriculo_lattes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Vinculo":
        known = {f.name for f in dataclasses.fields(cls)}
        filtered = {k: v for k, v in data.items() if k in known}
        filtered["linha_pesquisa"] = _sanitize_str(filtered.get("linha_pesquisa"))
        filtered["curriculo_lattes"] = _sanitize_str(filtered.get("curriculo_lattes"))
        return cls(**filtered)


@dataclasses.dataclass
class DadosPessoais:
    id: Optional[int] = None
    matricula: Optional[str] = None
    nome_usual: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    email: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    url_foto_75x100: Optional[str] = None
    url_foto_150x200: Optional[str] = None
    foto: Optional[str] = None  # mantido por compatibilidade
    data_nascimento: Optional[str] = None
    naturalidade: Optional[str] = None
    tipo_vinculo: Optional[str] = None
    filiacao: List[Optional[str]] = dataclasses.field(default_factory=list)
    vinculo: Optional[Vinculo] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DadosPessoais":
        known = {f.name for f in dataclasses.fields(cls)}
        filtered: dict[str, Any] = {k: v for k, v in data.items() if k in known}

        # Trata strings-lixo em campos de texto simples
        for field in ("rg", "tipo_sanguineo", "naturalidade", "email"):
            if field in filtered:
                filtered[field] = _sanitize_str(filtered[field])

        # Garante que filiacao seja uma lista (mesmo com elementos nulos)
        if "filiacao" in filtered and not isinstance(filtered["filiacao"], list):
            filtered["filiacao"] = []

        # Desserializa o sub-objeto vinculo, se presente
        raw_vinculo = filtered.get("vinculo")
        if isinstance(raw_vinculo, dict):
            filtered["vinculo"] = Vinculo.from_dict(raw_vinculo)

        return cls(**filtered)
