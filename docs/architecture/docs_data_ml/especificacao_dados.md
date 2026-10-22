# Especificação Técnica do Modelo de Dados — CommunityLab

**Projeto:** CommunityLab (Detector Inteligente de Histórias de Sucesso e Testemunhos)  
**Hackathon:** ONE G10 — Oracle Next Education & Alura (Equipe 18)  
**Responsável Técnico:** Ketlyn Barbosa (*Machine Learning Engineer*)  
**Status:** Implementado, Validado e Integrado (`v1.0` / Schemas JSON Draft 2020-12 / Pydantic v2)  
**Cobertura de Testes:** ✅ 27/27 testes automatizados aprovados  

---

## 1. Visão Geral e Princípios Arquiteturais

Este documento define a **especificação técnica e contratual do modelo de dados** do CommunityLab, servindo como fonte única da verdade para todos os módulos do sistema:
- **Ingestão (`src.ingestion`):** Decodificação multi-encoding resiliente, parser CSV/JSON e pseudonimização determinística.
- **Pré-processamento (`src.preprocessing`):** Normalização de texto, desduplicação, descarte de ruídos e anonimização de dados pessoais (LGPD).
- **Análise por IA (`src.analysis`):** Enriquecimento semântico, extração estruturada de JSON de LLMs e agregação estatística.
- **Detecção e Extração (`src.detection` e `src.extraction`):** Identificação de candidatos a histórias de sucesso e extração de evidências literais.
- **Orquestração e Avaliação (`src.orchestration`):** Divisão em lotes e cálculo de acurácia contra conjuntos de referência rotulados.
- **Armazenamento e Contratos (`src.storage` e `src.modelos`):** Validação formal via JSON Schemas Draft 2020-12 e tipagem estrita com Pydantic v2.

### 1.1. Princípios de Dados
1. **Rastreabilidade Ponta a Ponta:** Todo ativo de marketing gerado ou história detectada armarra obrigatoriamente as citações literais e os identificadores numéricos das interações de origem (`interacoes_origem: [1, ...]`), eliminando alucinações e viabilizando auditoria.
2. **Privacidade e LGPD por Design:**
   - Pseudonimização determinística de autores via hash SHA-256 com sal criptográfico externo (`membro_######`).
   - Mascaramento rigoroso de PII (Personally Identifiable Information) no corpo do texto (`[EMAIL]`, `[TELEFONE]`, `[CPF]`, `[NOME]`), preservando termos técnicos e emojis essenciais para análise de sentimentos.
3. **Resiliência de Ingestão:** Suporte a arquivos com ou sem BOM, codificações alternativas (`utf-8-sig`, `cp1252`, `latin-1`), detecção automática de delimitadores CSV (`,` ou `;`) e suporte a envelopes JSON ou listas diretas.
4. **Fechamento Estrito de Contrato:** Todos os esquemas JSON operam com `"additionalProperties": false`, prevenindo poluição de campos não documentados ou vazamentos acidentais.

---

## 2. Esquemas de Entrada de Dados (Ingestão)

O sistema consome dados brutos provenientes de plataformas de comunidade (Discord, Slack, Fóruns Alura, eventos presenciais ou simulados) nos formatos **JSON** e **CSV**.

### 2.1. Envelope de Lote JSON (`schemas/lote_schema.json` & `src.modelos.LoteInteracoes`)

O formato padrão para envio em lote suporta metadados operacionais da coleta:

```json
{
  "versao_schema": "1.1",
  "id_lote": "lote_2026_semana_04",
  "origem_comunidade": "Discord_Grupo_ONE_G10",
  "periodo_referencia": "Semana_04",
  "criado_em": "2026-10-15T14:30:00Z",
  "interacoes": [
    {
      "versao_schema": "1.0",
      "id": 1,
      "autor_id": "membro_000101",
      "data": "2026-10-15T14:30:00Z",
      "origem": "discord",
      "texto": "Conquistei minha primeira vaga na área de IA após os cursos da Alura! Muito feliz! 🎉",
      "status_revisao": "pendente"
    },
    {
      "versao_schema": "1.0",
      "id": 2,
      "autor_id": "membro_000202",
      "data": "2026-10-15T15:00:00Z",
      "origem": "discord",
      "texto": "Desenvolvi um agente autônomo em Python para otimizar processos de logística.",
      "status_revisao": "pendente"
    }
  ]
}
```

> [!NOTE]
> O parser `src.ingestion.processar_json` aceita tanto o envelope acima (objeto com chave `interacoes`) quanto uma lista direta de interações `[...]`.

### 2.2. Estrutura Equivalente CSV

Para arquivos tabulares, a ingestão suporta delimitadores vírgula (`,`) e ponto e vírgula (`;`), com cabeçalhos padrão:

```csv
id,autor,data,origem,texto
1,Mariana Souza,2026-10-15T14:30:00Z,discord,"Conquistei minha primeira vaga na área de IA após os cursos da Alura! Muito feliz! 🎉"
2,Carlos Silva,2026-10-15T15:00:00Z,discord,"Desenvolvi um agente autônomo em Python para otimizar processos de logística."
```

*Nota de Ingestão:* O campo original `autor` é imediatamente convertido para `autor_id` pseudonimizado (`membro_######`) durante a leitura, não sendo persistido no objeto estruturado.

---

## 3. Definição de Campos, Tipos e Regras de Validação

### 3.1. Entidade Interação (`schemas/interacao_schema.json` & `src.modelos.Interacao`)

| Campo | Tipo JSON | Tipo Pydantic | Obrigatório? | Regras de Validação | Descrição |
| :--- | :--- | :--- | :---: | :--- | :--- |
| `versao_schema` | `string` | `str` | **Sim** | Constante `"1.0"` | Versão do contrato formal. |
| `id` | `integer` | `int` | **Sim** | Inteiro $\ge 1$ | Identificador numérico único dentro do lote. |
| `autor_id` | `string` | `str` | **Sim** | Regex `^membro_[0-9]{3,}$` | Código pseudonimizado. Nunca expõe o nome real. |
| `data` | `string` | `str` | **Sim** | Formato ISO 8601 UTC (`date-time`) | Data e hora da publicação da mensagem. |
| `origem` | `string` | `Literal` | **Sim** | Enum: `"simulado"`, `"discord"`, `"slack"`, `"forum"`, `"outro"` | Plataforma de onde a mensagem foi coletada. |
| `texto` | `string` | `str` | **Sim** | Mínimo 1, máximo 4.000 caracteres | Conteúdo textual limpo e anonimizado da mensagem. |
| `analise` | `object` | `Optional[AnaliseInteracao]` | Não | Estrutura conforme Seção 3.2 | Bloco enriquecido gerado pelo LLM. |
| `status_revisao` | `string` | `Literal` | Não | Enum: `"pendente"`, `"aprovado"`, `"rejeitado"` (padrão `"pendente"`) | Estado de curadoria da interação. |

---

### 3.2. Bloco Enriquecido de Análise (`analise` / `src.modelos.AnaliseInteracao`)

Preenchido pelos módulos de IA após inferência do LLM e validação:

```json
{
  "sentimento": "positivo",
  "relevancia": "alta",
  "topicos": ["carreira", "tecnologia"],
  "tipo_insight": "conquista",
  "justificativa": "Relato explícito de conquista de vaga de emprego após conclusão de trilha educacional.",
  "confianca": 0.95
}
```

| Campo | Tipo | Obrigatoriedade | Enum / Regras | Descrição |
| :--- | :--- | :---: | :--- | :--- |
| `sentimento` | `string` | **Obrigatório** | `"positivo"`, `"neutro"`, `"negativo"` | Tom emocional predominante da mensagem. |
| `relevancia` | `string` | **Obrigatório** | `"alta"`, `"media"`, `"baixa"` | Relevância para métricas de comunidade ou marketing. |
| `topicos` | `array[string]` | **Obrigatório** | Min. 1 item, sem duplicatas. Itens do enum: `"carreira"`, `"estudos"`, `"tecnologia"`, `"ferramentas"`, `"comunidade"`, `"eventos"`, `"outro"` | Assuntos abordados no texto. |
| `tipo_insight` | `string` | **Obrigatório** | `"historia"`, `"conquista"`, `"duvida"`, `"insight"`, `"outro"` | Categoria semântica da contribuição. |
| `justificativa` | `string` | Opcional | Máximo de 500 caracteres | Fundamentação gerada pela IA para a classificação. |
| `confianca` | `number` | Opcional | Float entre `0.0` e `1.0` | Nível de confiança da classificação atribuído pelo LLM. |

> [!WARNING]
> Se `confianca < 0.6` (`LIMIAR_CONFIANCA`), a interação é sinalizada para **revisão prioritária** por curadores humanos.

---

## 4. Contrato de Histórias Detectadas e Evidências

### 4.1. Entidade História Detectada (`schemas/historia_detectada.json` & `src.modelos.HistoriaDetectada`)

Para garantir a auditabilidade, nenhuma história de sucesso é gerada sem apontamento explícito para as mensagens de origem e suas citações literais:

```json
{
  "versao_schema": "1.1",
  "id_historia": "historia_001",
  "tipo": "conquista_profissional",
  "resumo": "Membro conquistou vaga de Desenvolvedora Júnior na área de IA após formação.",
  "interacoes_origem": [1],
  "fatos": [
    "Concluiu a trilha de cursos da Alura",
    "Conquistou primeira vaga profissional como Dev Júnior"
  ],
  "resultados": [
    "Ingresso no mercado de tecnologia"
  ],
  "citacoes": [
    {
      "id_interacao": 1,
      "texto": "Conquistei minha primeira vaga na área de IA após os cursos da Alura!"
    }
  ],
  "autorizacao_divulgacao": "pendente",
  "confianca": 0.95,
  "status_revisao": "pendente"
}
```

| Campo | Tipo | Validação | Descrição |
| :--- | :--- | :--- | :--- |
| `versao_schema` | `string` | Constante `"1.1"` | Versão do schema de histórias. |
| `id_historia` | `string` | Regex `^historia_[0-9]{3,}$` | Identificador estruturado da história. |
| `tipo` | `string` | `"conquista_profissional"`, `"superacao"`, `"projeto_destaque"` | Categoria principal da história. |
| `resumo` | `string` | 1 a 1.000 caracteres | Resumo factual do case. |
| `interacoes_origem` | `array[integer]` | Mínimo 1 item | Lista de IDs numéricos das mensagens fundamentadoras. |
| `fatos` | `array[string]` | Mínimo 1 item | Acontecimentos comprováveis extraídos da mensagem. |
| `resultados` | `array[string]` | Lista de strings | Impactos alcançados (ex: vaga, promoção, projeto). |
| `citacoes` | `array[object]` | Mínimo 1 citação | Trechos literais extraídos da interação com seu `id_interacao`. |
| `autorizacao_divulgacao` | `string` | `"pendente"`, `"autorizada"`, `"negada"`, `"nao_aplicavel"` | Consentimento do autor para veiculação pública. |
| `confianca` | `number` | Float entre `0.0` e `1.0` | Grau de certeza da IA na consistência da história. |
| `status_revisao` | `string` | `"pendente"`, `"aprovado"`, `"rejeitado"` | Decisão do revisor humano. |

---

## 5. Contrato de Ativos Gerados de Marketing

### 5.1. Entidade Ativo Gerado (`schemas/ativo_gerado_schema.json` & `src.modelos.AtivoGerado`)

Ativos gerados pela Fase 4 (posts para redes sociais, resumos de newsletter) são estruturados sob contrato estrito:

```json
{
  "versao_schema": "1.0",
  "id_ativo": "ativo_001",
  "tipo": "post_linkedin",
  "titulo": "De aluna a desenvolvedora: o impacto da comunidade ONE",
  "texto": "Celebrando conquistas reais! Mais uma aluna ingressando no mercado de tecnologia...",
  "interacoes_origem": [1],
  "status_revisao": "pendente",
  "revisor": null,
  "observacao_revisor": null,
  "modelo_llm": "meta.llama-3.3-70b-instruct",
  "criado_em": "2026-10-15T16:00:00Z",
  "oci_object_path": "ativos/2026-10-15/ativo_001.json"
}
```

| Campo | Tipo | Validação | Descrição |
| :--- | :--- | :--- | :--- |
| `versao_schema` | `string` | Constante `"1.0"` | Versão do schema de ativos. |
| `id_ativo` | `string` | Regex `^ativo_[0-9]{3,}$` | Identificador do ativo gerado. |
| `tipo` | `string` | `"post_linkedin"`, `"resumo_newsletter"` | Canal/formato de destino do conteúdo. |
| `titulo` | `string` | Opcional (máx. 200 caracteres) | Título de chamada ou assunto. |
| `texto` | `string` | Mínimo 1 caractere | Texto final elaborado pelo LLM. |
| `interacoes_origem` | `array[integer]` | Mínimo 1 item | IDs numéricos das mensagens utilizadas como fonte. |
| `status_revisao` | `string` | `"pendente"`, `"aprovado"`, `"rejeitado"` | Fluxo de aprovação humana. |
| `modelo_llm` | `string` | Opcional | Modelo utilizado (ex: `meta.llama-3.3-70b-instruct`). |
| `oci_object_path` | `string` | Opcional (regex `^ativos/[0-9]{4}-[0-9]{2}-[0-9]{2}/[A-Za-z0-9_.-]+\.json$`) | Caminho de persistência no Oracle Cloud Infrastructure Object Storage. |

---

## 6. Governança, Segurança e Privacidade (LGPD)

1. **Pseudonimização Determinística de Autores:**
   - Realizada em `src.ingestion.pseudonimizar_autor` utilizando SHA-256 alimentado com sal criptográfico externo (`SAL_PSEUDONIMIZACAO`).
   - Garante que o mesmo participante receba sempre o mesmo identificador determinístico (`membro_######`), permitindo identificar recorrência sem armazenar dados pessoais.
   - Detecção automática de colisões de pseudonimização dentro do lote com geração de avisos operacionais.
2. **Mascaramento Rigoroso de PII em Texto (`src.preprocessing.anonimizar_texto`):**
   - E-mails: regex universal substituindo por `[EMAIL]`.
   - Telefones: validação com DDD brasileiro obrigatório substituindo por `[TELEFONE]`.
   - CPFs: validação de formato e verificação matemática de dígitos verificadores substituindo por `[CPF]`.
   - Nomes Próprios: reconhecimento de entidades nomeadas via spaCy (`pt_core_news_sm`) com fallback heurístico para cidades e termos contextualizados substituindo por `[NOME]`.
   - Preservação estrita da lista de termos técnicos (`EXCECOES_TECNICAS`: *Python, Oracle, Alura, Docker, Kubernetes, Linux, AWS, Streamlit, etc.*), menções de comunidade (`@membro_###`) e pontuações/emojis vitais para a análise de sentimentos.
3. **Curadoria Humana Obrigatória (Human-in-the-Loop):**
   - Nenhuma história ou ativo de marketing gerado pode ser publicado automaticamente. O estado inicial obrigatório é `status_revisao: "pendente"`, exigindo aprovação expressa do gestor de comunidade via interface Streamlit.

---

## 7. Exemplo Prático de Utilização em Python

Demonstração do fluxo operacional completo utilizando as funções puras implementadas no projeto:

```python
from pathlib import Path
from src import (
    ler_arquivo_bytes,
    processar_json,
    limpar_e_filtrar_interacoes,
    anonimizar_texto,
    classificar_interacao,
    carregar_schema,
    gerar_agregacoes,
    filtrar_candidatos_historia,
    SAL_PADRAO,
    TAMANHO_MINIMO_TEXTO,
    LIMIAR_CONFIANCA,
    MAX_TENTATIVAS_LLM,
)

# 1. Ingestão segura com detecção automática de encoding
caminho = Path("data/samples/cenarios_demo.json")
conteudo, encoding, avisos_enc = ler_arquivo_bytes(caminho.read_bytes())

# 2. Processamento do formato e pseudonimização determinística de autores
interacoes_brutas, rejeitadas_ingestao, avisos_ing = processar_json(
    conteudo_texto=conteudo,
    sal=SAL_PADRAO
)

# 3. Limpeza de ruídos e remoção de duplicatas no lote
interacoes_limpas, rejeitadas_limpeza = limpar_e_filtrar_interacoes(
    interacoes=interacoes_brutas,
    tamanho_minimo=TAMANHO_MINIMO_TEXTO
)

# 4. Anonimização LGPD do corpo textual
interacoes_prontas = []
for item in interacoes_limpas:
    item_anonimo = item.copy()
    texto_anonimo, contagem_pii = anonimizar_texto(item["texto"])
    item_anonimo["texto"] = texto_anonimo
    interacoes_prontas.append(item_anonimo)

print(f"Total de interações prontas para IA: {len(interacoes_prontas)}")

# 5. Classificação semântica com injeção de LLM
schema_interacao = carregar_schema("schemas/interacao_schema.json")
prompt_template = "Classifique a seguinte mensagem: {{texto}}"

def cliente_llm_exemplo(prompt: str) -> str:
    return '{"sentimento": "positivo", "relevancia": "alta", "topicos": ["carreira"], "tipo_insight": "conquista", "justificativa": "Relato de vaga", "confianca": 0.95}'

interacoes_analisadas = []
for interacao in interacoes_prontas:
    analisada, status, avisos = classificar_interacao(
        interacao=interacao,
        schema_interacao=schema_interacao,
        funcao_chamar_llm=cliente_llm_exemplo,
        prompt_template=prompt_template,
        max_tentativas=MAX_TENTATIVAS_LLM,
        limiar_confianca=LIMIAR_CONFIANCA
    )
    interacoes_analisadas.append(analisada)

# 6. Agregações estatísticas e detecção de histórias
metricas = gerar_agregacoes(interacoes_analisadas)
candidatos_historias = filtrar_candidatos_historia(interacoes_analisadas)

print(f"Top Tópicos: {metricas['ranking_topicos'][:3]}")
print(f"Candidatos a História de Sucesso: {len(candidatos_historias)}")
```

---

## 8. Parâmetros Globais e Limiares de Negócio (`src/config.py`)

As variáveis e limiares operacionais são configuráveis via variáveis de ambiente (`.env`):

| Constante | Valor Padrão | Variável de Ambiente | Descrição |
|---|:---:|:---:|---|
| `TAMANHO_MINIMO_TEXTO` | `10` | `TAMANHO_MINIMO_TEXTO` | Comprimento mínimo de texto para não ser descartado como ruído. |
| `TAMANHO_MAXIMO_TEXTO` | `4000` | `TAMANHO_MAXIMO_TEXTO` | Limite máximo de caracteres por mensagem aceito pelo schema. |
| `LIMIAR_CONFIANCA` | `0.6` | `LIMIAR_CONFIANCA` | Abaixo deste valor, a classificação é enviada para revisão prioritária. |
| `MAX_TENTATIVAS_LLM` | `2` | `MAX_TENTATIVAS_LLM` | Quantidade de novas tentativas se o LLM devolver resposta inválida. |
| `TAMANHO_LOTE` | `50` | `TAMANHO_LOTE` | Quantidade padrão de interações processadas por lote. |
| `SAL_PADRAO` | `"communitylab_default_salt"` | `SAL_PSEUDONIMIZACAO` | Sal criptográfico para a pseudonimização SHA-256 de `autor_id`. |
| `VERSAO_SCHEMA_INTERACAO` | `"1.0"` | — | Versão atual do contrato de interação. |
| `VERSAO_SCHEMA_ATIVO` | `"1.0"` | — | Versão atual do contrato de ativos gerados. |
| `VERSAO_SCHEMA_LOTE` | `"1.1"` | — | Versão atual do contrato de envelope de lote. |
| `VERSAO_SCHEMA_HISTORIA` | `"1.1"` | — | Versão atual do contrato de história detectada. |

---

## 9. Validação e Conformidade

A aderência a esta especificação é validada automaticamente por meio de:
1. **Suíte Pytest:** `pytest -v` (27 testes validando schemas, modelos Pydantic, limites e regras de anonimização).
2. **Script de Validação de Schemas:** `python validar.py data/samples/cenarios_demo.json`.
