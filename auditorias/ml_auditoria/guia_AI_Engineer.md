# 🚀 Guia de Integração e Handoff Técnico — Engenharia de IA

**De:** Ketlyn Barbosa (*Machine Learning Engineer*)  
**Para:** Jaqueline de Lira (*AI Engineer*)  
**Projeto:** CommunityLab (Hackathon ONE G10 — Oracle Next Education & Alura | Equipe 18)  
**Status da Pipeline de ML/Dados:** ✅ **100% Implementada, Auditada e Testada (27/27 testes aprovados)**  
**Branch de Trabalho:** `feature/pipeline-ml-completo`  

---

## 📌 1. Visão Geral das Entregas & Handoff

Olá, Jaque! Este documento consolida todo o ecossistema de dados, ingestão, pré-processamento, contratos de validação e pontos de injeção de LLM desenvolvidos para suportar os seus módulos de Inteligência Artificial (**Fase 3: Inteligência Artificial** e **Fase 4: Geração de Conteúdo**).

Todos os módulos sob minha responsabilidade foram entregues como **funções puras**, sem efeitos colaterais, sem dependência de APIs externas de LLM ou de nuvem (OCI), com **tipagem estrita (Pydantic v2)** e cobertura integral de testes (`pytest`).

### 📦 O que está 100% pronto para você:
1. **Ingestão Resiliente Multi-Encoding & Multi-Formato:** Leitura segura de CSV (vírgula ou ponto-e-vírgula) e JSON (listas puras ou envelopes de lote), com normalização Unicode NFC.
2. **Pseudonimização e Anonimização LGPD:**
   - Pseudonimização determinística de autores via hash SHA-256 com sal externo (`membro_######`), garantindo contagem de recorrência sem expor identidades.
   - Mascaramento rigoroso de PII em texto: e-mails (`[EMAIL]`), telefones brasileiros com DDD (`[TELEFONE]`), CPFs válidos (`[CPF]`) e nomes próprios (`[NOME]`).
   - Preservação de termos técnicos essenciais (*Python, Oracle, Alura, Docker, Streamlit, etc.*), menções (`@membro_###`) e pontuações/emojis cruciais para a análise de sentimentos.
3. **Módulo de Classificação e Parsing de LLM (`src.analysis.classificacao`):**
   - Função `classificar_interacao` pronta para receber a sua função de chamada ao LLM (`Callable[[str], str]`).
   - Parser resiliente que extrai JSONs válidos mesmo quando envelopados em blocos markdown (` ```json ... ``` `) ou cercados de texto explicativo.
   - Gestão de retentativas automáticas (`MAX_TENTATIVAS_LLM`) e sinalização de baixa confiança (`LIMIAR_CONFIANCA`).
4. **Modelos Pydantic v2 e Contratos JSON Schema (Draft 2020-12):** Validação estrita de entradas, análises, detecção de histórias e ativos gerados.
5. **Utilitários de Agregação, Divisão em Lotes e Avaliação:** Funções para ranking estável de tópicos, métricas estatísticas e cálculo de acurácia contra conjuntos de referência.

---

## 🛠️ 2. Contratos de Dados (I/O)

Toda a comunicação entre o pipeline de dados e os seus modelos de IA segue estritamente os JSON Schemas localizados no diretório [`schemas/`](schemas/).

### 2.1. O que o LLM recebe (Interação Pronta para Análise)
Cada mensagem de comunidade limpa e anonimizada segue a estrutura de [`schemas/interacao_schema.json`](schemas/interacao_schema.json):

```json
{
  "versao_schema": "1.0",
  "id": 1,
  "autor_id": "membro_000101",
  "origem": "discord",
  "data": "2026-10-13T14:30:00Z",
  "texto": "Consegui minha primeira vaga como Desenvolvedora Júnior após concluir a formação da Alura! Muito feliz! 🎉 [EMAIL]",
  "status_revisao": "pendente"
}
```

> **Atenção aos campos:**
> - `texto`: Contém o texto normalizado e anonimizado (não use `texto_original`).
> - `autor_id`: Sempre no padrão `^membro_[0-9]{3,}$`.
> - `origem`: Valores aceitos: `"discord"`, `"slack"`, `"forum"`, `"simulado"`, `"outro"`.

---

### 2.2. O que o seu LLM deve retornar no Bloco de Análise (`analise`)
O prompt de classificação do LLM deve instruir o modelo a responder com o objeto de análise estruturado. O schema exige as seguintes chaves e enumerações estritas:

```json
{
  "sentimento": "positivo",
  "relevancia": "alta",
  "topicos": ["carreira", "tecnologia"],
  "tipo_insight": "conquista",
  "justificativa": "Relato claro de conquista de vaga no mercado de trabalho após conclusão de curso.",
  "confianca": 0.95
}
```

#### 📋 Enumerações Válidas (Conforme `schemas/interacao_schema.json` e `docs/guia_rotulagem.md`):
- **`sentimento`** *(obrigatório)*: `"positivo"` | `"neutro"` | `"negativo"`
- **`relevancia`** *(obrigatório)*: `"alta"` | `"media"` | `"baixa"`
- **`topicos`** *(obrigatório, array com pelo menos 1 item)*:
  `["carreira" | "estudos" | "tecnologia" | "ferramentas" | "comunidade" | "eventos" | "outro"]`
- **`tipo_insight`** *(obrigatório)*: `"historia"` | `"conquista"` | `"duvida"` | `"insight"` | `"outro"`
- **`justificativa`** *(opcional)*: String com até 500 caracteres fundamentando a classificação.
- **`confianca`** *(opcional, mas altamente recomendado)*: Float entre `0.0` e `1.0`. Se `< 0.6` (`LIMIAR_CONFIANCA`), a interação será marcada automaticamente para revisão prioritária.

---

### 2.3. Esquemas de Saída para as Próximas Etapas (Geração e Histórias)

À medida que você avançar na implementação dos módulos de **Detecção/Extração** e **Geração de Conteúdo**, utilize os seguintes modelos já disponíveis no projeto:

1. **Histórias Detectadas (`schemas/historia_detectada.json` & `src.modelos.HistoriaDetectada`):**
   ```python
   from src.modelos import HistoriaDetectada, Citacao

   historia = HistoriaDetectada(
       id_historia="historia_001",
       tipo="conquista_profissional",  # "conquista_profissional" | "superacao" | "projeto_destaque"
       resumo="Membro conquistou vaga de Desenvolvedora Júnior após formação.",
       interacoes_origem=[1],
       fatos=["Concluiu formação da Alura", "Contratada como Desenvolvedora Júnior"],
       resultados=["Ingresso no mercado de tecnologia"],
       citacoes=[Citacao(texto="Consegui minha primeira vaga como Desenvolvedora Júnior", id_interacao=1)],
       autorizacao_divulgacao="pendente",
       confianca=0.95
   )
   ```

2. **Ativos Gerados de Marketing (`schemas/ativo_gerado_schema.json` & `src.modelos.AtivoGerado`):**
   ```python
   from src.modelos import AtivoGerado

   ativo = AtivoGerado(
       id_ativo="ativo_001",
       tipo="post_linkedin",  # "post_linkedin" | "resumo_newsletter"
       titulo="De aluna a desenvolvedora: o poder da comunidade ONE",
       texto="História inspiradora da nossa comunidade...",
       interacoes_origem=[1],
       modelo_llm="meta.llama-3.3-70b-instruct"
   )
   ```

---

## 💻 3. Como Importar e Usar os Módulos (Exemplo Prático de Integração)

Você pode importar tudo diretamente do pacote principal `src` ou dos submódulos específicos.

### Exemplo Completo de Pipeline com Injeção de LLM:

```python
import json
from pathlib import Path
from src import (
    ler_arquivo_bytes,
    processar_json,
    limpar_e_filtrar_interacoes,
    anonimizar_texto,
    classificar_interacao,
    carregar_schema,
    gerar_agregacoes,
    filtrar_candidatos_historia
)

# 1. Carregar arquivo e realizar Ingestão Segura
caminho = Path("data/samples/cenarios_demo.json")
conteudo, encoding, avisos = ler_arquivo_bytes(caminho.read_bytes())

# Processar JSON (suporta lista ou envelope) aplicando pseudonimização com sal
interacoes_brutas, rejeitadas, avisos_json = processar_json(
    conteudo_texto=conteudo, 
    sal="sal_secreto_hackathon_equipe18"
)

# 2. Limpeza de ruídos e remoção de duplicatas no lote
interacoes_limpas, rejeitadas_limpeza = limpar_e_filtrar_interacoes(
    interacoes=interacoes_brutas, 
    tamanho_minimo=10
)

# 3. Anonimização LGPD do texto
interacoes_prontas = []
for item in interacoes_limpas:
    item_anonimo = item.copy()
    texto_anonimizado, contagem_pii = anonimizar_texto(item["texto"])
    item_anonimo["texto"] = texto_anonimizado
    interacoes_prontas.append(item_anonimo)

print(f"✅ Interações prontas para o LLM: {len(interacoes_prontas)}")

# 4. Injeção de LLM na Classificação (src.analysis.classificacao)
schema_interacao = carregar_schema("schemas/interacao_schema.json")

# Template de prompt definido por você (AI Engineer)
prompt_template = """
Analise a mensagem da comunidade abaixo e retorne um objeto JSON estrito com:
sentimento (positivo, neutro, negativo),
relevancia (alta, media, baixa),
topicos (lista com: carreira, estudos, tecnologia, ferramentas, comunidade, eventos, outro),
tipo_insight (historia, conquista, duvida, insight, outro),
justificativa (texto breve),
confianca (float de 0.0 a 1.0).

Mensagem:
{{texto}}
"""

# Função simulada ou integração real com seu cliente LLM (OCI GenAI, OpenAI, etc.)
def minha_funcao_llm(prompt: str) -> str:
    # Aqui entra sua chamada à API (ex: client.chat.completions.create ou oci.generative_ai_inference)
    return '''
    ```json
    {
      "sentimento": "positivo",
      "relevancia": "alta",
      "topicos": ["carreira"],
      "tipo_insight": "conquista",
      "justificativa": "Usuário celebra aprovação em processo seletivo.",
      "confianca": 0.95
    }
    ```
    '''

# Classificação com parsing automático de markdown, retentativas e validação de schema
interacoes_analisadas = []
for interacao in interacoes_prontas:
    interacao_com_analise, status, avisos_class = classificar_interacao(
        interacao=interacao,
        schema_interacao=schema_interacao,
        funcao_chamar_llm=minha_funcao_llm,
        prompt_template=prompt_template,
        max_tentativas=2,
        limiar_confianca=0.6
    )
    interacoes_analisadas.append(interacao_com_analise)

# 5. Agregação e Métricas Consolidadas para a Interface (Tissiany)
resumo_estatistico = gerar_agregacoes(interacoes_analisadas)
print("Ranking de Tópicos:", resumo_estatistico["ranking_topicos"])

# 6. Filtragem de Candidatos para Geração de Histórias/Cases
candidatos_historia = filtrar_candidatos_historia(interacoes_analisadas)
print(f"🎯 Histórias em potencial identificadas: {len(candidatos_historia)}")
```

---

## ⚙️ 4. Parâmetros Globais e Configurações (`src/config.py`)

Os limiares de negócio estão centralizados em `src/config.py` e suportam injeção via variáveis de ambiente (`.env`):

| Constante | Valor Padrão | Variável de Ambiente | Descrição |
|---|:---:|:---:|---|
| `TAMANHO_MINIMO_TEXTO` | `10` | `COMMUNITYLAB_TAMANHO_MINIMO_TEXTO` | Mínimo de caracteres para o texto ser processado. |
| `TAMANHO_MAXIMO_TEXTO` | `4000` | `COMMUNITYLAB_TAMANHO_MAXIMO_TEXTO` | Máximo de caracteres permitido pelo schema. |
| `LIMIAR_CONFIANCA` | `0.6` | `COMMUNITYLAB_LIMIAR_CONFIANCA` | Abaixo deste valor, o item é marcado para revisão prioritária. |
| `MAX_TENTATIVAS_LLM` | `2` | `COMMUNITYLAB_MAX_TENTATIVAS_LLM` | Quantidade de novas tentativas se o LLM devolver JSON inválido. |
| `TAMANHO_LOTE` | `50` | `COMMUNITYLAB_TAMANHO_LOTE` | Quantidade de itens por lote em processamentos massivos. |
| `SAL_PADRAO` | `"communitylab_dev_salt"` | `COMMUNITYLAB_SAL_PSEUDONIMIZACAO` | Sal criptográfico para o hash SHA-256 de `autor_id`. |

---

## 🧪 5. Validação e Execução de Testes

Antes de submeter PRs ou integrar novos prompts, execute as validações na raiz do projeto:

```bash
# 1. Executar a suíte de testes unitários (27 testes em ~1.5s)
pytest -v

# 2. Validar integridade dos cenários de demonstração contra os schemas oficiais
python validar.py data/samples/cenarios_demo.json

# 3. Testar a acurácia de novos prompts contra o conjunto de referência
# (Consulte docs/avaliacao.md e use src.orchestration.avaliacao.avaliar_qualidade)
```

---

## 🤝 6. Próximos Passos Pareados (Ketlyn & Jaqueline)

1. **Refinamento dos Prompts de Classificação:** Utilizar as definições de `docs/guia_rotulagem.md` como *system instructions* ou *few-shot examples* nos seus prompts.
2. **Implementação de Detecção e Extração (`src/detection` e `src/extraction`):** Usar `filtrar_candidatos_historia` como ponto de partida e criar as rotinas de extração de citações literais (`Citacao`) e fatos/resultados.
3. **Avaliação Formal de Acurácia:** Preencher o relatório em `docs/avaliacao.md` com métricas reais obtidas pelo modelo escolhido (ex: Llama 3 / Command R+ / GPT-4o-mini).

Qualquer dúvida ou necessidade de novos ajustes nos modelos e schemas, conte comigo! 🚀
