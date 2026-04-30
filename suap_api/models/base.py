import dataclasses


@dataclasses.dataclass
class RawMixin:
    _raw: dict = dataclasses.field(default_factory=dict, init=False, repr=False)

    @property
    def raw(self) -> dict:
        return self._raw
