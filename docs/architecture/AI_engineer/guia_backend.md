# 🛠️ Guia de Integração e Arquitetura para o Backend

**Projeto:** CommunityLab — Detector Inteligente de Histórias de Sucesso e Testemunhos  
**Hackathon:** ONE G10 — Oracle Next Education & Alura (Equipe 18)  
**Destinatários:** Desenvolvedores Backend & Engenharia de Integração  
**Autor:** Ketlyn Barbosa (*Machine Learning Engineer*)  
**Status dos Módulos Core:** ✅ 100% Implementados, Tipados (Pydantic v2) e Testados (27/27 testes no Pytest)  
**Localização:** `docs/architecture/AI_engineer/guia_backend.md`  

---

## 📌 1. Visão Geral e Papel do Backend no CommunityLab

O ecossistema do CommunityLab foi concebido com uma clara separação de responsabilidades. O pacote `src/` funciona como um **core de regras de negócio e processamento puro** (sem efeitos colaterais de I/O de rede ou dependências rígidas de nuvem).

### Responsabilidades Centrais do Backend:
1. **Recepção e Upload de Dados:** Receber arquivos (`.csv`, `.json`) via API ou interface de upload (Streamlit) e encaminhar os bytes para os módulos de ingestão.
2. **Injeção do Provedor de IA (LLM Client):** Instanciar o cliente de inferência (Oracle Cloud Infrastructure GenAI, Cohere Command R+, Meta Llama 3) e fornecê-lo via injeção de dependência para a função de classificação.
3. **Persistência em Nuvem (OCI Object Storage):** Gerenciar o upload, versionamento e download dos ativos aprovados no bucket configurado (`communitylab-ativos`).
4. **Alimentação da Camada Visual (Streamlit/API):** Fornecer estruturas agregadas, interações prontas e status de revisão para os componentes visuais.
5. **Rastreabilidade e Curadoria:** Garantir que nenhuma alteração humana em status (`pendente` $\to$ `aprovado`/`rejeitado`) quebre a integridade referencial com os IDs de interação originais.

---

## 🧩 2. O que já está 100% Pronto no Core (`src/`)

O time de backend **não precisa reimplementar** algoritmos de limpeza, parsers ou validações. Todos os utilitários estão disponíveis diretamente via importação do pacote `src`:

```
┌────────────────────────────────────────────────────────────────────────┐
│                         src/ (Módulos Core)                            │
├─────────────────────┬──────────────────────────────────────────────────┤
│ Módulo              │ O que entrega pronto para o Backend             │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.ingestion       │ Decodificação com fallback (UTF-8, CP1252,       │
│                     │ Latin-1), parsers CSV/JSON, DataFrames Pandas e  │
│                     │ pseudonimização determinística (SHA-256 + sal). │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.preprocessing   │ Limpeza de espaços, filtro de ruídos (< 10 chars)│
│                     │ deduplicação no lote e mascaramento LGPD de PII. │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.analysis        │ Parser tolerante a markdown (```json), inferência│
│                     │ com retentativas e agregações estatísticas.      │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.detection       │ Filtragem de candidatos a histórias e cases.     │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.orchestration   │ Divisão operacional em lotes (batching) e       │
│                     │ cálculo de acurácia contra ground truth.         │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.storage         │ Validadores formais JSON Schema Draft 2020-12.   │
├─────────────────────┼──────────────────────────────────────────────────┤
│ src.modelos         │ Modelos de dados estruturados em Pydantic v2.    │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

## 🔌 3. Padrão de Injeção de LLM (`src.analysis.classificacao`)

Para manter o core isolado de custos ou instabilidades de rede durante testes locais, a classificação de mensagens utiliza o padrão **Injeção de Dependência**.

A função `classificar_interacao` recebe qualquer função Python que obedeça à assinatura:
$$\text{funcao\_chamar\_llm: } \text{Callable[[str], str]}$$

### Como o Backend Conecta o Cliente OCI GenAI:

```python
import oci
from typing import Callable
from src.analysis import classificar_interacao
from src.storage import carregar_schema
from src.config import MAX_TENTATIVAS_LLM, LIMIAR_CONFIANCA

# 1. Configuração do cliente OCI no Backend
def criar_cliente_oci_genai() -> Callable[[str], str]:
    config = oci.config.from_file("~/.oci/config", "DEFAULT")
    genai_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config)
    compartment_id = "ocid1.compartment.oc1..exemplo"

    def chamar_llm(prompt: str) -> str:
        # Monta a chamada para o modelo (Llama ou Cohere)
        detalhes_chat = oci.generative_ai_inference.models.ChatDetails(
            compartment_id=compartment_id,
            serving_mode=oci.generative_ai_inference.models.OnDemandServingMode(
                model_id="cohere.command-r-plus"
            ),
            chat_request=oci.generative_ai_inference.models.CohereChatRequest(
                message=prompt,
                temperature=0.2,
                max_tokens=800
            )
        )
        resposta = genai_client.chat(detalhes_chat)
        return resposta.data.chat_response.text

    return chamar_llm
```

> [!TIP]
> **Resiliência embutida:** A função `classificar_interacao` já lida internamente com o parser de markdown (` ```json ... ``` `), valida o retorno contra o JSON Schema oficial e executa novas tentativas automáticas se a resposta vier malformada.

---

## 📦 4. Contratos de Dados & Modelos Pydantic v2

O backend deve utilizar as classes de `src.modelos` para tipagem estrita de payloads e validação de requisições.

### 4.1. Interação (`src.modelos.Interacao`)
```python
from src.modelos import Interacao, AnaliseInteracao

interacao = Interacao(
    versao_schema="1.0",
    id=1,
    autor_id="membro_000101",
    data="2026-10-15T14:30:00Z",
    origem="discord",
    texto="Consegui minha vaga como Dev após o curso da Alura! [EMAIL]",
    analise=AnaliseInteracao(
        sentimento="positivo",
        relevancia="alta",
        topicos=["carreira", "tecnologia"],
        tipo_insight="conquista",
        justificativa="Relato de conquista profissional",
        confianca=0.95
    ),
    status_revisao="pendente"
)

# Exportação para dicionário compatível com JSON Schema
dado_json = interacao.model_dump()
```

### 4.2. Ativo Gerado (`src.modelos.AtivoGerado`)
```python
from src.modelos import AtivoGerado

ativo = AtivoGerado(
    versao_schema="1.0",
    id_ativo="ativo_001",
    tipo="post_linkedin",
    titulo="De aluna a desenvolvedora!",
    texto="História de superação da nossa aluna...",
    interacoes_origem=[1],  # Rastreabilidade estrita ao ID da interação
    status_revisao="pendente",
    modelo_llm="cohere.command-r-plus",
    oci_object_path="ativos/2026-10-15/ativo_001.json"
)
```

---

## ☁️ 5. Integração com OCI Object Storage

A persistência de arquivos gerados e exportações deve seguir o padrão de caminhos validado pelo regex do schema:
$$\text{Padrão: } \texttt{\text{\textasciicircum}ativos/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/[A-Za-z0-9\_.-]+\textbackslash.json\$} $$

### Estrutura de Salvamento Recomendada:
```python
import json
from datetime import datetime, timezone
import oci
from src.modelos import AtivoGerado
from src.storage import validar_ativo, carregar_schema

def salvar_ativo_oci(ativo: AtivoGerado, config_oci: dict, namespace: str, bucket_name: str) -> str:
    # 1. Validação do schema antes de subir para a nuvem
    schema_ativo = carregar_schema("schemas/ativo_gerado_schema.json")
    valido, erros = validar_ativo(ativo.model_dump(), schema_ativo)
    if not valido:
        raise ValueError(f"Ativo inválido para persistência: {erros}")

    # 2. Definição da chave de armazenamento particionada por data
    hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    nome_objeto = f"ativos/{hoje}/{ativo.id_ativo}.json"
    ativo.oci_object_path = nome_objeto

    # 3. Upload seguro no bucket OCI
    object_storage_client = oci.object_storage.ObjectStorageClient(config_oci)
    object_storage_client.put_object(
        namespace_name=namespace,
        bucket_name=bucket_name,
        object_name=nome_objeto,
        put_object_body=ativo.model_dump_json(indent=2).encode("utf-8"),
        content_type="application/json"
    )
    return nome_objeto
```

---

## ⚙️ 6. Variáveis de Ambiente Operacionais (`.env`)

O backend deve carregar o arquivo `.env` no startup da aplicação (via `python-dotenv`). Todas as constantes do core (`src/config.py`) leem diretamente essas chaves:

| Variável | Padrão | Utilidade no Backend |
|---|:---:|---|
| `SAL_PSEUDONIMIZACAO` | `"communitylab_default_salt"` | Chave secreta de hash para pseudonimizar autores. **Nunca expor no front.** |
| `TAMANHO_MINIMO_TEXTO` | `10` | Descarta ruídos na ingestão. |
| `TAMANHO_MAXIMO_TEXTO` | `4000` | Limite de payload aceito pelo schema. |
| `LIMIAR_CONFIANCA` | `0.6` | Marcação automática para revisão prioritária. |
| `MAX_TENTATIVAS_LLM` | `2` | Tentativas de recuperação de resposta JSON do LLM. |
| `TAMANHO_LOTE` | `50` | Fatiamento de mensagens em lotes operacionais. |
| `OCI_CONFIG_FILE` | `~/.oci/config` | Caminho do arquivo de autenticação OCI. |
| `OCI_BUCKET_NAME` | `communitylab-ativos` | Nome do bucket OCI de persistência. |

---

## 🚀 7. Exemplo de Serviço de Backend Completo (`PipelineService`)

Abaixo está o exemplo recomendado de classe de serviço para orquestrar o pipeline de ponta a ponta:

```python
from pathlib import Path
from typing import List, Dict, Any, Callable
from src import (
    ler_arquivo_bytes,
    processar_json,
    processar_csv,
    limpar_e_filtrar_interacoes,
    anonimizar_texto,
    classificar_interacao,
    filtrar_candidatos_historia,
    gerar_agregacoes,
    carregar_schema,
    dividir_em_lotes,
    SAL_PADRAO,
    TAMANHO_MINIMO_TEXTO,
    LIMIAR_CONFIANCA,
    MAX_TENTATIVAS_LLM,
    TAMANHO_LOTE,
)

class PipelineService:
    def __init__(self, funcao_llm: Callable[[str], str]):
        self.funcao_llm = funcao_llm
        self.schema_interacao = carregar_schema("schemas/interacao_schema.json")
        self.prompt_template = (
            "Analise a seguinte mensagem de comunidade e retorne JSON estrito: {{texto}}"
        )

    def processar_upload(self, arquivo_bytes: bytes, nome_arquivo: str) -> Dict[str, Any]:
        # 1. Leitura tolerante a falhas de encoding
        texto_decodificado, encoding, avisos_enc = ler_arquivo_bytes(arquivo_bytes)

        # 2. Ingestão por formato com pseudonimização determinística
        if nome_arquivo.endswith(".csv"):
            brutos, rejeitados, avisos = processar_csv(texto_decodificado, sal=SAL_PADRAO)
        else:
            brutos, rejeitados, avisos = processar_json(texto_decodificado, sal=SAL_PADRAO)

        # 3. Limpeza e desduplicação
        limpos, rejeitados_limpeza = limpar_e_filtrar_interacoes(
            brutos, tamanho_minimo=TAMANHO_MINIMO_TEXTO
        )
        todos_rejeitados = rejeitados + rejeitados_limpeza

        # 4. Anonimização LGPD
        prontos = []
        metricas_pii = {"email": 0, "telefone": 0, "cpf": 0, "nome": 0}
        for item in limpos:
            item_anonimo = item.copy()
            texto_anonimo, contagem = anonimizar_texto(item["texto"])
            item_anonimo["texto"] = texto_anonimo
            prontos.append(item_anonimo)
            for k in metricas_pii:
                metricas_pii[k] += contagem.get(k, 0)

        # 5. Execução em Lotes com o LLM
        interacoes_analisadas = []
        lotes = dividir_em_lotes(prontos, tamanho_lote=TAMANHO_LOTE)

        for lote in lotes:
            for interacao in lote:
                analisada, status, avisos_llm = classificar_interacao(
                    interacao=interacao,
                    schema_interacao=self.schema_interacao,
                    funcao_chamar_llm=self.funcao_llm,
                    prompt_template=self.prompt_template,
                    max_tentativas=MAX_TENTATIVAS_LLM,
                    limiar_confianca=LIMIAR_CONFIANCA,
                )
                interacoes_analisadas.append(analisada)

        # 6. Agregações e detecção para a interface
        metricas_dashboard = gerar_agregacoes(interacoes_analisadas)
        candidatos = filtrar_candidatos_historia(interacoes_analisadas)

        return {
            "total_processadas": len(interacoes_analisadas),
            "rejeitadas": todos_rejeitados,
            "metricas_pii": metricas_pii,
            "metricas_dashboard": metricas_dashboard,
            "candidatos_historias": candidatos,
            "interacoes": interacoes_analisadas,
        }
```

---

## 🧪 8. Comandos Úteis para o Backend

```bash
# Executar a suíte de testes de validação do core
pytest -v

# Validar cenários de dados contra os schemas oficiais
python validar.py data/samples/cenarios_demo.json

# Instalar dependências em modo editável
pip install -e .
```

---

Para suporte a alterações em contratos ou novas necessidades de dados, consulte a equipe de ML (Ketlyn Barbosa).
