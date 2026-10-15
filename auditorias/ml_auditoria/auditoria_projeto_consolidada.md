# 📋 Relatório de Auditoria Completa — CommunityLab

**Data da Auditoria:** 15 de Outubro de 2026  
**Status Geral:** ✅ **APROVADO SEM RESSALVAS CRÍTICAS**  
**Suíte de Testes:** 27/27 testes passando (`pytest -v`)  
**Linter:** 0 erros / 0 avisos (`ruff check`)  
**Validação de Schemas:** 3/3 cenários íntegros (`validar.py`)  

---

## 1. Resumo Executivo

O projeto **CommunityLab** passou por uma auditoria completa de arquitetura, integridade de código, conformidade de contratos JSON Schema, segurança/LGPD e alinhamento com o [README.md](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/README.md).

Após o remanejamento completo do pacote antigo para [`src/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src) e a resolução de todos os problemas de importação e tipagem estática, o repositório encontra-se em estado **robusto, desacoplado e pronto para a fase de construção da interface (Streamlit) e orquestração OCI**.

| Dimensão Auditada | Status | Observação |
|---|:---:|---|
| **Arquitetura & Estrutura** | ✅ Excelente | Alinhada 100% à árvore planejada do README |
| **Qualidade do Código** | ✅ Excelente | Funções puras, tipagem estrita e zero efeitos colaterais |
| **Cobertura de Testes** | ✅ Excelente | 27 testes cobrindo todos os módulos e edge cases |
| **Conformidade de Schemas** | ✅ Excelente | Draft 2020-12 estrito com `additionalProperties: false` |
| **Segurança & Privacidade** | ✅ Excelente | Pseudonimização com sal, anonimização de PII e `.env.example` |
| **Stack de Tecnologias** | ✅ Excelente | Python 3.11+, Pandas, Pydantic v2, spaCy e jsonschema |

---

## 2. Estrutura do Repositório e Arquitetura

A árvore de diretórios reflete com exatidão o escopo proposto na especificação técnica:

```
CommunityLab/
├── .env.example                  # Variáveis de ambiente sem segredos expostos
├── .gitignore                    # Bloqueio de .env, venv, pycache, eggs e logs
├── pyproject.toml                # Metadados, dependências e configurações de ferramentas
├── README.md                     # Documento mestre do projeto e especificações do MVP
├── validar.py                    # Script de validação dos cenários contra os schemas
├── data/
│   └── samples/
│       ├── cenarios_demo.json    # 3 cenários ricos simulados
│       └── formato_hackathon.json
├── docs/
│   ├── architecture/
│   │   └── README.md             # Visão conceitual e arquitetura do pipeline
│   ├── agents.md                 # Diretrizes para desenvolvimento dos módulos
│   ├── avaliacao.md              # Template para registro de métricas de acurácia
│   ├── contrato_saida.md         # Especificação detalhada de I/O de cada módulo
│   └── guia_rotulagem.md         # Critérios e desempates para rotulagem humana
├── schemas/
│   ├── ativo_gerado_schema.json  # Schema formal de posts e newsletters
│   ├── historia_detectada.json   # Schema formal de histórias e evidências
│   ├── interacao_schema.json     # Schema formal de mensagens brutas e analisadas
│   └── lote_schema.json          # Schema do envelope de lotes
├── src/                          # Pacote principal modularizado
│   ├── __init__.py               # Ponto de entrada unificado com reexportação
│   ├── config.py                 # Constantes com fallback para variáveis de ambiente
│   ├── modelos.py                # Modelos Pydantic v2 (Interacao, Ativo, etc.)
│   ├── ingestion/                # Leitura resiliente, CSV, JSON, DataFrames e sal
│   ├── preprocessing/            # Limpeza, deduplicação e anonimização LGPD
│   ├── analysis/                 # LLM injetado, retry, fallbacks e agregação estatística
│   ├── detection/                # Filtragem de candidatos a histórias e conquistas
│   ├── extraction/               # Citações literais e evidências rastreáveis
│   ├── generation/               # Modelos e validação de ativos gerados
│   ├── orchestration/            # Divisão em lotes e avaliação de acurácia
│   └── storage/                  # Contratos JSON Schema e persistência OCI
├── tests/
│   └── test_communitylab.py      # Suíte de 27 testes unitários automatizados
├── app/                          # Reservado para a interface web Streamlit
└── workflows/                    # Reservado para automações e orquestrações de pipelines
```

---

## 3. Avaliação Módulo a Módulo (`src/`)

### 📥 3.1. Ingestão ([`src/ingestion/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/ingestion))
- **[`leitura.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/ingestion/leitura.py):**
  - Implementa a cascata de decodificação recomendada: `utf-8-sig` → `cp1252` → `latin-1` → `utf-8 (com replace)`.
  - Normaliza caracteres em Unicode NFC e unifica quebras de linha (`\r\n` → `\n`).
  - Nunca lança exceções não tratadas para a camada superior.
- **[`ingestion.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/ingestion/ingestion.py):**
  - Suporta JSON (lista simples ou envelope com chave `interacoes`) e CSV (autodetecção de delimitadores `,` e `;`).
  - **Detecção de colisão de pseudonimização no lote:** mantém mapa em memória e alerta caso dois autores distintos resultem no mesmo `membro_######`.
  - **Suporte a Pandas DataFrames:** `processar_dataframe` e `interacoes_para_dataframe` viabilizam análise e manipulação tabular conforme a stack do README.

### 🧹 3.2. Pré-processamento ([`src/preprocessing/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/preprocessing))
- **[`limpeza.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/preprocessing/limpeza.py):**
  - Remove caracteres de controle sem corromper quebras de linha essenciais.
  - Rejeita mensagens abaixo de `TAMANHO_MINIMO_TEXTO` (10 caracteres).
  - Deduplicação robusta baseada em tupla `(autor_id, texto_normalizado_sem_pontuacao)`.
- **[`anonimizacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/preprocessing/anonimizacao.py):**
  - Mascaramento por tipo: `[EMAIL]`, `[TELEFONE]`, `[CPF]` e `[NOME]`.
  - Telefone exige DDD brasileiro válido (evitando falsos positivos em sequências de 8 dígitos).
  - CPF valida dígitos verificadores para números sem formatação de 11 dígitos, protegendo IDs ou números de pedidos legítimos.
  - NER via spaCy (`pt_core_news_sm`) com fallback heurístico e lista de exceções técnicas expandida (Python, Oracle, Alura, Docker, Kubernetes, Linux, etc.).

### 🧠 3.3. Análise ([`src/analysis/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/analysis))
- **[`classificacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/analysis/classificacao.py):**
  - LLM desacoplado como função injetada `Callable[[str], str]`.
  - Extração resiliente de JSON (direta, markdown ` ```json ` ou varredura de chaves `{...}`).
  - Loop de retry com limite configurável (`MAX_TENTATIVAS_LLM`).
  - Se a resposta for inválida após as tentativas, retorna sem preencher valores padrão fantasiosos.
  - Baixa confiança (< 0.6) sinaliza o item para revisão prioritária humana.
- **[`agregacao.py`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/analysis/agregacao.py):**
  - Totalizadores por sentimento, relevância, tipo de insight e tópicos.
  - Ranking ordenado por contagem com **desempate alfabético estável**, prevenindo oscilações na interface visual.

### 🎯 3.4. Detecção, Extração e Geração
- **[`src/detection/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/detection):** Função `filtrar_candidatos_historia` isola mensagens com alta probabilidade de sucesso.
- **[`src/extraction/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/extraction):** Modelo `Citacao` garante rastreabilidade estrita entre o texto gerado e a interação original.
- **[`src/generation/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/generation):** Modelo `AtivoGerado` e validador formal para posts LinkedIn e resumos de newsletter.

### ⚙️ 3.5. Orquestração e Storage
- **[`src/orchestration/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/orchestration):**
  - `dividir_em_lotes` com validação de tamanho de lote > 0.
  - `avaliar_qualidade` computa acurácia por campo contra conjuntos de teste rotulados.
- **[`src/storage/`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/src/storage):**
  - Funções de carregamento e validação de esquemas utilizando `Draft202012Validator` e `FormatChecker`.

---

## 4. Segurança, Privacidade e LGPD

1. **Pseudonimização Determinística de Autores:**
   - Autores reais nunca são salvos ou enviados ao LLM.
   - São convertidos para `membro_######` via hash SHA-256 alimentado por um sal externo.
2. **Sem Credenciais no Versionamento:**
   - `.env` excluído no `.gitignore`.
   - `.env.example` fornecido como modelo sem credenciais reais.
3. **Dados de Demonstração Éticos:**
   - Todos os dados em `data/samples/cenarios_demo.json` são explicitamente declarados como 100% simulados.

---

## 5. Análise da Suíte de Testes (27 Testes)

Todos os testes rodam em modo isolado (sem requisições de rede e sem dependência de APIs externas de LLM):

| Categoria | Quantidade | Principais Casos Testados |
|---|:---:|---|
| **Leitura e Encoding** | 2 | UTF-8, UTF-8 com BOM, CP1252 com euro (`€`), Latin-1 (`0x81`), CRLF → LF |
| **Ingestão e Parsers** | 5 | JSON lista, JSON lote, CSV vírgula, CSV ponto e vírgula, DataFrames Pandas |
| **Pseudonimização e Colisão** | 2 | Determinismo com sal, manutenção de formato já pseudonimizado, detecção de colisão no lote via monkeypatch |
| **Limpeza e Normalização** | 1 | Normalização de espaços, rejeição de textos curtos, deduplicação por autor + texto |
| **Anonimização LGPD** | 4 | E-mails, telefones com DDD, CPFs válidos vs números aleatórios, NER spaCy e termos técnicos |
| **Divisão em Lotes** | 1 | Divisão uniforme, fatiamento de sobras e exceção para `tamanho_lote <= 0` |
| **Classificação LLM** | 4 | Sucesso limpo, JSON dentro de Markdown, recuperação via retry, tentativas esgotadas e baixa confiança |
| **Agregação e Estatísticas** | 1 | Totalização, tópicos múltiplos e ordenação com desempate alfabético |
| **Avaliação de Qualidade** | 1 | Acurácia por campo, tratamento de itens sem análise e filtro de revisão prioritária |
| **Modelos Pydantic v2** | 2 | Validação de tipos, regex, enums fechados e estreitamento de tipos |
| **Schemas JSON** | 3 | Validação contra Draft 2020-12, obrigatoriedade de `versao_schema` em interações e ativos |
| **Submódulos de `src`** | 1 | Verificação de integridade e exportações de todas as subpastas da arquitetura |

---

## 6. Próximos Passos Recomendados para a Equipe

1. **Camada de Interface (`app/`):**
   - Implementar a aplicação Streamlit em `app/` para upload de arquivos, exibição dos gráficos de agregação e tela de curadoria/aprovação humana dos ativos.
2. **Orquestração e OCI (`workflows/`):**
   - Construir o script orquestrador que conecta a ingestão, chamada ao modelo de linguagem e o upload dos ativos aprovados para o bucket no OCI Object Storage.
3. **Avaliação Empírica ([`docs/avaliacao.md`](file:///home/ketlyn/Desktop/Desktop/communitLab_Oficial/G10-Brasil-Equipe-18/docs/avaliacao.md)):**
   - Preencher a tabela de métricas com dados reais quando o modelo final (ex: OCI Generative AI ou Cohere Command R+) for conectado e testado com o conjunto de referência rotulado.
