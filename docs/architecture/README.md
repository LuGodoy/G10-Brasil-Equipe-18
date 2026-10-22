# Arquitetura do CommunityLab

Detector Inteligente de Histórias de Sucesso e Testemunhos com IA.

---

## 1. Visão Geral do Pipeline

```
[Mensagens da Comunidade (CSV / JSON)]
                  │
                  ▼
   1. [Ingestão & Leitura com Fallback de Encoding]
                  │
                  ▼
   2. [Pré-processamento: Limpeza, Normalização & Anonimização (LGPD)]
                  │
                  ▼
   3. [Análise de Sentimentos, Tópicos & Relevância (LLM Injetado)]
                  │
                  ▼
   4. [Detecção de Histórias de Sucesso, Conquistas & Superação]
                  │
                  ▼
   5. [Extração de Fatos, Resultados e Citações Literais]
                  │
                  ▼
   6. [Geração de Ativos: Posts LinkedIn, Testemunhos & Newsletter]
                  │
                  ▼
   7. [Interface de Curadoria e Aprovação Humana (Streamlit)]
                  │
                  ▼
   8. [Persistência e Recuperação no OCI Object Storage]
```

---

## 2. Componentes e Estrutura de Código (`src/`)

- **`src/ingestion/`**: Leitura tolerante a falhas (UTF-8, CP1252, Latin-1), suporte a CSV, JSON e Pandas DataFrames, e pseudonimização determinística com sal dos autores.
- **`src/preprocessing/`**: Remoção de duplicatas, normalização de caracteres e mascaramento de dados sensíveis (emails, telefones com DDD brasileiro, CPFs e nomes via NER spaCy).
- **`src/analysis/`**: Classificação estruturada com LLM via prompt parametrizado, validação contra JSON Schema e fallback controlado.
- **`src/detection/`**: Filtragem e agrupamento de interações com alto potencial estratégico de conquistas e histórias de superação.
- **`src/extraction/`**: Isolamento de evidências verificáveis e citações literais para garantir rastreabilidade aos textos de origem.
- **`src/generation/`**: Criação de ativos de marketing em formatos pré-definidos (LinkedIn, Newsletter, Testemunhos).
- **`src/orchestration/`**: Divisão em lotes configuráveis e avaliação de qualidade/acurácia contra conjuntos de referência rotulados.
- **`src/storage/`**: Integração e validação de contratos para armazenamento em nuvem Oracle Cloud Infrastructure (OCI).
