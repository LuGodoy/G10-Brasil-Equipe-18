# Guia de rotulagem

> **Rascunho para validação.** As definições abaixo são uma proposta inicial e precisam ser revisadas e aprovadas pela Ketlyn e pela equipe antes de servirem de base para prompts e avaliação. Cada ajuste deve ser refletido nos exemplos.

Objetivo: rotular as interações de forma consistente, para que o LLM e as pessoas que avaliam cheguem ao mesmo resultado.

## Como rotular

1. Leia a mensagem inteira.
2. Escolha um valor para cada campo. Em caso de dúvida entre dois, use o desempate descrito na seção.
3. Rotule pelo **conteúdo da mensagem**, não pelo que você supõe sobre a pessoa.

## Tipo de insight (`tipo_insight`)

| Valor | Definição | Exemplo |
|-------|-----------|---------|
| `conquista` | A pessoa relata um resultado concreto alcançado (vaga, aprovação, projeto concluído). | "Fui aprovada em um estágio em dados." |
| `historia` | Relato de experiência, percurso ou impressão, sem um resultado marcante. | "A live de ontem foi excelente, a demonstração ajudou muito." |
| `duvida` | Pergunta ou pedido de ajuda. | "Alguém tem um passo a passo?" |
| `insight` | Dica, aprendizado ou prática que outras pessoas podem aplicar. | "Guardo as chaves em variáveis de ambiente." |
| `outro` | Apoio, cumprimento ou comentário sem conteúdo aproveitável. | "Parabéns!" |

**Desempates**

- Mais de um tipo na mensagem: escolher o predominante.
- Conquista ou história: vale `conquista` se houver resultado verificável no texto.
- Dúvida com resposta incluída na mesma mensagem: vale o que ocupa a maior parte do texto.

## Relevância (`relevancia`)

| Valor | Critério |
|-------|----------|
| `alta` | Conteúdo específico e aproveitável para marketing: conquista concreta, dúvida recorrente ou dica acionável. |
| `media` | Tem conteúdo útil, mas genérico, pontual ou dependente de contexto. |
| `baixa` | Sem conteúdo aproveitável: apoio, cumprimento, ruído. |

## Sentimento (`sentimento`)

Baseado no **tom** da mensagem, não no assunto.

| Valor | Quando usar |
|-------|-------------|
| `positivo` | Satisfação, entusiasmo, elogio, comemoração. |
| `neutro` | Informação ou pergunta sem carga emocional clara. |
| `negativo` | Frustração, dificuldade, crítica, insatisfação. |

Uma dúvida pode ser neutra. Um relato de dificuldade é negativo.

## Tópicos (`topicos`)

Lista fechada: `carreira`, `estudos`, `tecnologia`, `ferramentas`, `comunidade`, `eventos`, `outro`. Use o mínimo necessário, em geral um ou dois. Use `outro` só quando nenhum dos demais se aplica. A lista deve ser confirmada pela equipe.

## Casos difíceis (completar durante a rotulagem)

Registre aqui mensagens ambíguas e a decisão tomada, para manter a consistência ao longo do tempo.

| Mensagem (anonimizada) | Decisão | Motivo |
|------------------------|---------|--------|
| | | |

## Rotulagem para avaliação

- O conjunto de referência deve ser rotulado por pelo menos duas pessoas, de forma independente.
- Discordâncias são discutidas e resolvidas, e a regra resultante é registrada na tabela acima.
- Os rótulos de `exemplos/cenarios_demo.json` não foram validados por pessoas e **não** devem ser usados como gabarito.