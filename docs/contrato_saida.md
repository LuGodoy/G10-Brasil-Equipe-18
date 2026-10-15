# Contrato de entrada e saída dos módulos

Fonte da verdade dos objetos: `schemas/interacao.schema.json` e `schemas/ativo_gerado.schema.json`. Este documento descreve o que cada módulo devolve e como tratar os casos de erro.

## 1. Ingestão

Entrada: bytes ou texto de CSV ou JSON.

```python
{
    "interacoes": [...],     # objetos válidos conforme interacao.schema.json
    "rejeitadas": [          # nenhum registro some sem explicação
        {"posicao": 7, "motivo": "texto vazio", "original": {...}}
    ],
    "avisos": ["encoding detectado: cp1252"],
    "encoding": "cp1252",
    "total_lidas": 120
}
```

**JSON:** aceita lista de interações ou objeto de lote com a chave `interacoes`. JSON inválido vira rejeição com motivo.

**CSV:** colunas esperadas `id, autor_id, data, origem, texto`. Detectar o separador (`,` ou `;`), aceitar aspas e quebra de linha dentro do texto e ignorar colunas extras com aviso.

**Campos ausentes:** `id` pode ser gerado em sequência (com aviso). `data` inválida vira rejeição. `origem` ausente usa o valor configurado.

## 2. Autor: pseudonimização, não rejeição

O schema exige `autor_id` no formato `membro_###`. Arquivos exportados de plataformas costumam trazer nome ou apelido. Nesse caso a ingestão **converte** o valor, em vez de rejeitar o registro:

- Se o valor já segue `membro_` mais dígitos, mantém.
- Caso contrário, gera `membro_` mais 6 dígitos derivados de um hash com **sal** do valor original. O mesmo autor recebe sempre o mesmo código, o que preserva a contagem de participações por pessoa.
- O sal é recebido como parâmetro pela função (vem de configuração externa) e **nunca** fica no repositório. Sem o sal, não dá para refazer o mapeamento.
- O valor original **nunca** é guardado, logado nem enviado ao LLM.
- Colisões (dois autores com o mesmo código) são improváveis, mas devem ser detectadas dentro do lote e registradas como aviso.

Menções a nomes dentro do `texto` são tratadas pela anonimização (seção 4).

## 3. Limpeza

- Normalizar espaços.
- Rejeitar texto vazio ou abaixo de `TAMANHO_MINIMO_TEXTO`.
- Duplicatas: comparar o texto normalizado (minúsculas, sem pontuação final, sem espaços duplicados) junto com `autor_id`. Mantém a primeira e registra as demais em `rejeitadas` com o motivo "duplicada".
- Texto acima do limite do schema: rejeitar ou truncar com aviso, conforme decisão da equipe.

## 4. Anonimização do texto

| Tipo | Substituição |
|------|--------------|
| E-mail | `[EMAIL]` |
| Telefone (formatos brasileiros) | `[TELEFONE]` |
| CPF | `[CPF]` |
| Nomes próprios | `[NOME]` |

- Menções já pseudonimizadas (`@membro_031`) são mantidas.
- A detecção de nomes é **melhor esforço** e pode errar nos dois sentidos. Termos técnicos e de produtos (Python, Oracle, Streamlit, GitHub) precisam estar numa lista de exceções, e o teste de falsos positivos deve ser ampliado conforme os erros aparecerem.
- Devolver apenas a **contagem** do que foi mascarado por tipo, nunca o valor original.

## 5. Classificação

Saída: a interação com o bloco `analise` preenchido, conforme o schema.

```python
{
    "resultados": [...],     # interações com analise válida
    "sem_analise": [         # esgotadas as tentativas
        {"id": 12, "motivo": "resposta inválida após 2 tentativas"}
    ],
    "revisao_prioritaria": [7, 31],   # ids com confianca < LIMIAR_CONFIANCA
    "uso": {"chamadas": 48, "tentativas_extras": 3, "falhas": 1}
}
```

- Resposta do LLM: extrair o JSON mesmo com texto ao redor ou bloco de código markdown, validar contra o schema.
- Inválida: nova tentativa até `MAX_TENTATIVAS_LLM`. Depois disso, a interação vai para `sem_analise`. **Não** preencher valores padrão.
- Baixa confiança: mantém a análise e marca para revisão prioritária.

## 6. Agregação (F03)

```python
{
    "total": 15,
    "sem_analise": 0,
    "por_topico": {
        "carreira": {"total": 6, "positivo": 4, "neutro": 0, "negativo": 2}
    },
    "ranking_topicos": [{"topico": "carreira", "total": 6}],
    "por_sentimento": {"positivo": 9, "neutro": 1, "negativo": 5},
    "por_relevancia": {"alta": 8, "media": 4, "baixa": 3},
    "por_tipo_insight": {"conquista": 3, "duvida": 4}
}
```

- Considera só interações com `analise` válida e informa quantas ficaram de fora.
- Interação com vários tópicos conta em cada um.
- Ranking com desempate alfabético, para a interface não reordenar sozinha.

## 7. Pontos a combinar com a equipe

- Formato e local do arquivo ou da função que a Tissiany lê e que a Luciene envia ao OCI Object Storage.
- Quem escreve o prompt de classificação (Jaqueline), quem chama a API e quem valida a resposta (este módulo).
- Tamanho de lote e valores das constantes de configuração.