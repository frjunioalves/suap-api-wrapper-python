
# Documentação de Integração API SUAP - Modelos e Endpoints

Esta documentação define os endpoints e os esquemas de dados para integração. Os modelos devem prever campos nulos, strings vazias ou dados incompletos vindos da API, garantindo a extração de **todas** as informações disponíveis.

## 1. Endpoints Mapeados

### 1.1. Disciplinas do Semestre
- **Endpoint:** `GET /api/edu/disciplinas/{semestre}`
- **Descrição:** Lista as disciplinas do aluno em um determinado semestre. Funciona melhor que a rota de diários pois inclui dados de carga horária e total de faltas.
- **Uso:** Extrair o `id_diario` desta resposta para alimentar a rota de aulas.

### 1.2. Aulas da Disciplina
- **Endpoint:** `GET /api/edu/diarios/{id_diario}/aulas`
- **Descrição:** Retorna a listagem de aulas de um diário/disciplina específico.
- **Parâmetros:** `id_diario` obtido na rota `disciplinas`.

### 1.3. Mensagens e Avisos
- **Endpoint:** `GET /api/edu/mensagens/entrada/{status}/`
- **Descrição:** Retorna as mensagens de aviso para o usuário. 

### 1.4. Meus Dados
- **Endpoint:** `GET /api/comum/meus-dados/`
- **Descrição:** Retorna os dados pessoais e acadêmicos detalhados do aluno logado.

---

## 2. Modelos de Dados (Pydantic / Python)

Para garantir que o parser não falhe com dados `null` (ex: `filiacao`, `linha_pesquisa`, `tipo_sanguineo`), os modelos devem ser construídos estritamente com suporte a opcionais (`Optional`).

```python
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Any

# ==========================================
# 1. Modelos para /api/comum/meus-dados/
# ==========================================

class VinculoSuap(BaseModel):
    id: int
    matricula: str
    nome: str
    email: Optional[str] = None
    turno: Optional[str] = None
    curso: str
    campus: str
    situacao: str
    cota_sistec: Optional[str] = ""
    cota_mec: Optional[str] = ""
    situacao_sistemica: str
    matricula_regular: bool
    linha_pesquisa: Optional[str] = None
    curriculo_lattes: Optional[str] = None

class MeusDadosSuap(BaseModel):
    id: int
    matricula: str
    nome_usual: str
    cpf: str
    rg: Optional[str] = None
    filiacao: List[Optional[str]] = Field(default_factory=list) # Trata a lista com [null, null]
    data_nascimento: Optional[str] = None
    naturalidade: Optional[str] = None
    tipo_sanguineo: Optional[str] = None # Pode vir "NoneNone" ou null
    email: Optional[str] = ""
    url_foto_75x100: Optional[str] = None
    url_foto_150x200: Optional[str] = None
    tipo_vinculo: str
    vinculo: VinculoSuap

# ==========================================
# 2. Modelos para /api/edu/diarios/{id_diario}/aulas
# ==========================================

class AulaSuap(BaseModel):
    id: int
    etapa: str
    conteudo: str
    data: str # Formato DD/MM/YYYY
    qtd_aulas: int
    faltas: int

# ==========================================
# 3. Modelos para /api/edu/disciplinas/{semestre}
# ==========================================
# Nota: Modelo base inferido, o Claude deve expandir os campos 
# caso encontre novos retornos na inspeção da resposta HTTP.

class DisciplinaSuap(BaseModel):
    id_diario: int
    disciplina: str
    carga_horaria: Optional[int] = None
    faltas: Optional[int] = 0
    # Adicionar demais campos de notas e status retornados pela API

# ==========================================
# 4. Modelos para /api/edu/mensagens/entrada/{status}/
# ==========================================
# Nota: Modelo base inferido.

class MensagemSuap(BaseModel):
    id: int
    assunto: str
    remetente: str
    data_envio: str
    lida: bool
    # Adicionar demais campos de corpo da mensagem conforme retorno
```

## 3. Diretrizes de Tratamento
1. **Falta de Dados:** Valores como `tipo_sanguineo: "NoneNone"`, `rg: "None - / -"` ou `naturalidade: "-"` devem ser tratados no backend e convertidos para `None` real se houver necessidade de exibição limpa no front-end.
2. **Listas com Nulos:** O campo `filiacao` costuma retornar arrays com elementos nulos `[null, null]`. O parser não deve quebrar ao fazer iterações nessa lista.
3. **Exploração:** Ao processar as rotas de `disciplinas` e `mensagens`, faça o log completo do JSON recebido pela primeira vez para adicionar aos modelos Pydantic quaisquer campos extras que a documentação atual não cobriu.
