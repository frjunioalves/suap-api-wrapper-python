import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class DadosPessoais:
    id: Optional[int] = None
    matricula: Optional[str] = None
    nome_usual: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    email: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    foto: Optional[str] = None
    data_nascimento: Optional[str] = None
    naturalidade: Optional[str] = None
    tipo_vinculo: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DadosPessoais":
        known = {f.name for f in dataclasses.fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})
