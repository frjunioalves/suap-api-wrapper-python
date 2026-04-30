# Especificação: Retorno de Resposta Bruta (Raw JSON)

Esta especificação descreve as abordagens para permitir que o utilizador da biblioteca aceda ao JSON original retornado pela API do SUAP, sem o tratamento de dados realizado pelos modelos (DataClasses).

## Contexto

Atualmente, o `SuapClient` utiliza recursos (como `EduResource` e `CommonResource`) que consomem a API e convertem o JSON em objetos Python tipados. Embora isso facilite o uso, alguns utilizadores precisam do JSON original para fins de depuração, log ou acesso a campos não mapeados.

## Propostas de Implementação

### 1. Atributo `raw` nos Modelos (Recomendado)

Adicionar um atributo privado `_raw` em cada classe de modelo que armazena o dicionário original antes de qualquer limpeza ou conversão.

#### Prós:
- **Não quebra o código existente:** O retorno dos métodos continua sendo um único objeto.
- **Acesso sob demanda:** O utilizador só acede ao JSON se precisar.
- **Consistência:** O JSON fica "atachado" ao dado que ele representa.

#### Exemplo de Estrutura:
```python
@dataclasses.dataclass
class ModeloBase:
    _raw: dict = dataclasses.field(default_factory=dict, init=False, repr=False)

    @property
    def raw(self) -> dict:
        return self._raw
```

## Decisão e Próximos Passos

A **Opção 1** é a preferida por manter a elegância da API pública e garantir retrocompatibilidade.

### Tarefas:
1. [ ] Criar uma classe base ou mixin para os modelos.
2. [ ] Atualizar o método `from_dict` de todos os modelos para injetar o `data` original no campo `_raw`.
3. [ ] Atualizar a documentação para demonstrar o uso do atributo `.raw`.
