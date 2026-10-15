# 🔍 Auditoria do Projeto CommunityLab

**Data:** 15/10/2026  
**Escopo:** Código-fonte, testes, schemas, documentação e organização do repositório

---

## 1. Visão Geral

| Item | Status |
|------|--------|
| Testes (`pytest -v`) | ✅ **14/14 passando** |
| Validação de schemas (`validar.py`) | ✅ **3/3 cenários OK** |
| Estrutura de pacote (`pyproject.toml`) | ✅ Funcional |
| Documentação (`docs/`) | ✅ Consistente |
| Dados de exemplo (`data/samples/`) | ✅ 3 cenários completos |

---

## 2. Arquitetura e Organização

### ✅ Pontos fortes

- **Pipeline bem modularizado** — cada etapa (leitura → ingestão → limpeza → anonimização → classificação → agregação → avaliação) vive em seu próprio arquivo com responsabilidade única.
- **Dependências em direção única** conforme documentado em [agents.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/agents.md#L35).
- **LLM injetado como função** — `classificar_interacao` recebe `funcao_chamar_llm: Callable`, sem acoplamento com provedor.
- **Schemas JSON como contrato formal** — 4 schemas bem definidos com Draft 2020-12.
- **Sem efeitos colaterais nos módulos** — funções puras, sem `print`, sem I/O direto, sem variáveis de ambiente.

### ⚠️ Pontos de atenção

| # | Problema | Severidade | Localização |
|---|----------|------------|-------------|
| A1 | **Diretório `app/` vazio** — não há interface Streamlit nem orquestração | 🟡 Médio | `app/` |
| A2 | **Diretório `workflows/` vazio** — sem scripts de orquestração | 🟡 Médio | `workflows/` |
| A3 | **Falta `config.py`** — as constantes (`TAMANHO_MINIMO_TEXTO`, `LIMIAR_CONFIANCA`, `MAX_TENTATIVAS_LLM`, `TAMANHO_LOTE`) são mencionadas no [agents.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/agents.md#L55-L63) como devendo existir em um arquivo centralizado, mas estão hardcoded como parâmetros | 🟡 Médio | Vários módulos |
| A4 | **Falta `.env.example`** — mencionado no README mas não existe | 🟢 Baixo | Raiz |
| A5 | **README desatualizado quanto à estrutura** — menciona diretório `src/` que não existe; a estrutura real é `communityLab/` | 🟡 Médio | [README.md L157-178](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/README.md#L157-L178) |
| A6 | **`agents.md` menciona `requirements.txt`** que não existe (projeto usa `pyproject.toml`) | 🟢 Baixo | [agents.md L12](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/agents.md#L12) |
| A7 | **`agents.md` menciona `src/communitylab/`** mas o diretório real é `communityLab/` | 🟢 Baixo | [agents.md L22](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/agents.md#L22) |

---

## 3. Qualidade do Código

### Módulo por módulo

#### [`leitura.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/leitura.py) — ✅ Sólido
- Fallback de encoding correto: `utf-8-sig → cp1252 → latin-1 → utf-8 com replace`
- Normalização NFC e unificação de quebras de linha

#### [`ingestion.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/ingestion.py) — ✅ Bom, com ressalvas

| # | Achado | Severidade |
|---|--------|------------|
| C1 | **`pseudonimizar_autor` não detecta colisões de hash dentro do lote** — o [contrato_saida.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/contrato_saida.md#L35) exige que colisões sejam registradas como aviso, mas a função opera isoladamente por autor sem visão do conjunto | 🟡 Médio |
| C2 | O campo `id` da interação JSON não é validado como inteiro ≥ 1 na ingestão — poderia entrar `"id": -3` ou `"id": "abc"` e só falhar no schema depois | 🟢 Baixo |

#### [`limpeza.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/limpeza.py) — ✅ Sólido
- Tratamento de duplicatas com chave `(autor_id, texto normalizado)` funciona bem
- Remoção de pontuação para comparação evita falsos negativos

#### [`anonimizacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/anonimizacao.py) — ✅ Bom, com ressalvas

| # | Achado | Severidade |
|---|--------|------------|
| C3 | **Regex de CPF pega qualquer sequência de 11 dígitos** (`\b\d{11}\b`), o que pode causar falsos positivos em códigos numéricos longos (pedidos, matrículas) | 🟡 Médio |
| C4 | **Lista de exceções técnicas é curta** — falta cobertura de termos comuns como "Linux", "Java", "Docker", "React", "Node", "Angular", "Django", "Flask", "Alura", "Figma" etc. | 🟢 Baixo |
| C5 | **O fallback sem spaCy é agressivo** — qualquer palavra capitalizada após a primeira posição vira `[NOME]`, o que pode mascarar nomes de cidades, organizações etc. | 🟢 Baixo |

#### [`classificacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/classificacao.py) — ✅ Sólido
- Extração robusta de JSON com 3 fallbacks (direto, markdown, busca por `{...}`)
- Validação contra schema + retry com limite de tentativas
- Baixa confiança apenas marca para revisão, não rejeita

#### [`agregacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/agregacao.py) — ✅ Sólido
- Desempate alfabético estável no ranking de tópicos ✔

#### [`avaliacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/avaliacao.py) — ✅ Funcional

| # | Achado | Severidade |
|---|--------|------------|
| C6 | **Comparação de tópicos é binária (match exato)** — duas listas `["carreira", "tecnologia"]` vs `["tecnologia", "carreira"]` são iguais (usa `set`), mas poderia também medir sobreposição parcial para métricas mais granulares | 🟢 Baixo |

#### [`contrato.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/contrato.py) — ✅ Sólido
- Usa `Draft202012Validator` + `FormatChecker`

#### [`lotes.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/lotes.py) — ✅ Sólido
- Simples e correto

---

## 4. Testes

### ✅ Cobertura existente (14 testes)

| Módulo | Testes | Observação |
|--------|--------|------------|
| Leitura | 1 | UTF-8, CRLF → LF |
| Pseudonimização | 1 | Determinismo, idempotência |
| Ingestão JSON | 1 | Lista simples |
| Ingestão CSV | 1 | CSV com `,` |
| Limpeza | 1 | Duplicatas + tamanho mínimo |
| Anonimização | 3 | Email, telefone, CPF, NER, DDD |
| Lotes | 1 | Divisão em 3 lotes |
| Classificação | 1 | Extração de JSON |
| Agregação | 1 | Contagens e ranking |
| Validação de schemas | 2 | Interação válida/inválida, ativo |
| Ingestão fallback | 1 | Data dinâmica |

### ⚠️ Lacunas nos testes

| # | Teste ausente | Prioridade |
|---|--------------|------------|
| T1 | **Leitura com encoding `cp1252` e `latin-1`** — só testa UTF-8 | 🟡 Alta |
| T2 | **Leitura com bytes inválidos** — deveria retornar texto com replace e aviso | 🟡 Alta |
| T3 | **Ingestão de JSON inválido** (ex.: string truncada) | 🟡 Alta |
| T4 | **Ingestão de JSON no formato lote** (objeto com chave `interacoes`) | 🟡 Alta |
| T5 | **Ingestão com campo `texto` vazio** (deve rejeitar) | 🟢 Média |
| T6 | **CSV com `;` como separador** | 🟡 Alta |
| T7 | **CSV com quebra de linha dentro de campo** | 🟢 Média |
| T8 | **`classificar_interacao` com LLM fake** — resposta válida, inválida com retry, tentativas esgotadas | 🔴 Alta |
| T9 | **`classificar_interacao` com baixa confiança** (< 0.6) | 🟡 Alta |
| T10 | **`avaliar_qualidade`** — nenhum teste existe para esse módulo | 🔴 Alta |
| T11 | **`validar_objeto_contra_schema` com campo extra** (rejeição por `additionalProperties: false`) | 🟢 Média |
| T12 | **`gerar_agregacoes` com interações sem análise** | 🟢 Média |
| T13 | **Anonimização: falsos positivos conhecidos** (ex.: "Oracle", "São Paulo" não devem virar `[NOME]`) | 🟡 Alta |
| T14 | **Colisão de pseudonimização** dentro do lote | 🟢 Média |

---

## 5. Schemas JSON

### ✅ Pontos fortes
- Todos usam Draft 2020-12 ✔
- `additionalProperties: false` em todos os schemas ✔
- Enumerações fechadas para campos controlados ✔
- `versao_schema` como campo obrigatório ✔

### ⚠️ Achados

| # | Achado | Severidade |
|---|--------|------------|
| S1 | **`ativo_gerado_schema.json` não tem `versao_schema` como `required`** — o campo existe mas é opcional, diferente de `interacao_schema.json` onde é obrigatório | 🟡 Médio |
| S2 | **`historia_detectada.json` e `lote_schema.json` não possuem módulo Python correspondente** para validação — não estão referenciados em `contrato.py` | 🟢 Baixo |

---

## 6. Documentação

### ✅ Pontos fortes
- README detalhado com visão, problema, solução, equipe e roadmap
- [contrato_saida.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/contrato_saida.md) excelente como especificação técnica
- [guia_rotulagem.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/guia_rotulagem.md) bem estruturado com critérios e desempates
- [avaliacao.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/avaliacao.md) como template para métricas (ainda não preenchido)

### ⚠️ Desalinhamentos

| # | Achado |
|---|--------|
| D1 | **README lista Pydantic como tecnologia** mas o projeto usa `jsonschema` |
| D2 | **README menciona diretório `src/`** que não existe |
| D3 | **`agents.md` menciona `requirements.txt`** — projeto usa `pyproject.toml` |
| D4 | **`agents.md` referencia `exemplos/cenarios_demo.json`** — caminho real é `data/samples/cenarios_demo.json` |
| D5 | **`avaliacao.md` está vazio** (template) — nenhuma avaliação foi executada ainda |

---

## 7. Segurança e Privacidade

### ✅ Bem implementado
- Pseudonimização com hash + sal (sal como parâmetro externo) ✔
- Anonimização de email, telefone, CPF e nomes ✔
- Preservação de menções já pseudonimizadas (`@membro_*`) ✔
- `.gitignore` adequado: exclui `.env`, `__pycache__`, `.venv` etc. ✔
- Dados de exemplo são todos simulados ✔

### ⚠️ Atenção

| # | Achado | Severidade |
|---|--------|------------|
| P1 | **`communitylab.egg-info/` está versionado?** — deveria estar no `.gitignore` | 🟢 Baixo |
| P2 | **Nenhum mecanismo de auditoria** para rastrear quais dados foram processados e quando | 🟢 Baixo |

---

## 8. Dependências

```toml
# pyproject.toml
dependencies = [
    "jsonschema>=4.0.0",
    "pandas>=2.0.0",      # ⚠️ importado em algum lugar?
    "spacy>=3.0.0",
]
```

| # | Achado | Severidade |
|---|--------|------------|
| DEP1 | **`pandas` está como dependência mas não é usado em nenhum módulo** — nenhum `import pandas` encontrado no código | 🟡 Médio |
| DEP2 | **`spacy` é carregado de forma lazy** (bom) mas o download do modelo `pt_core_news_sm` é feito automaticamente se não existir — pode causar efeito colateral inesperado na primeira execução | 🟢 Baixo |

---

## 9. Resumo de Prioridades

### 🔴 Alta prioridade (fazer agora)
1. **Adicionar testes para `classificar_interacao`** com LLM fake (T8)
2. **Adicionar testes para `avaliar_qualidade`** (T10)
3. **Implementar detecção de colisão de hash** na pseudonimização (C1)

### 🟡 Média prioridade (próximo sprint)
4. Criar [`config.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/communityLab/config.py) com constantes centralizadas (A3)
5. Corrigir regex de CPF para evitar falsos positivos em sequências de 11 dígitos (C3)
6. Ampliar testes de encoding (T1, T2), JSON inválido (T3), CSV `;` (T6)
7. Tornar `versao_schema` obrigatório em `ativo_gerado_schema.json` (S1)
8. Remover `pandas` das dependências ou usá-lo onde previsto (DEP1)
9. Atualizar README com a estrutura real do projeto (A5, D1, D2)

### 🟢 Baixa prioridade (backlog)
10. Ampliar lista de exceções técnicas na anonimização (C4)
11. Criar `.env.example` (A4)
12. Adicionar `*.egg-info/` ao `.gitignore` (P1)
13. Corrigir referências em `agents.md` (A6, A7, D3, D4)
14. Implementar validadores para `historia_detectada` e `lote_schema` (S2)

---

## 10. Conclusão

O projeto está **bem estruturado para a fase atual de desenvolvimento**. O pipeline de processamento de dados é sólido, com módulos puros e desacoplados, schemas formais e testes que passam. Os principais gaps são:

1. **Cobertura de testes incompleta** — especialmente para os módulos de classificação e avaliação
2. **Documentação desalinhada com a implementação real** — referências a caminhos e tecnologias que mudaram
3. **Dependência não utilizada** (`pandas`) poluindo as instalações
4. **Lacuna de funcionalidade** — `app/` e `workflows/` vazios indicam que a interface e orquestração ainda precisam ser construídas

O código existente segue bem as regras do [agents.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/agents.md): funções puras, sem efeitos colaterais, LLM injetado, privacidade respeitada. É uma base sólida para as próximas etapas do hackathon.
