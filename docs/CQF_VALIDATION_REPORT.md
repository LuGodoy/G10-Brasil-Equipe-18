# CommunityLab Quality Framework (CQF)
## Relatório de Validação Metodológica — v1.0

**Projeto:** CommunityLab — Hackathon ONE G10  
**Equipe:** 18  
**Responsável funcional:** Marcus — Project Manager  
**Data:** 19/10/2026  
**Status:** Referências de teste validadas pelo responsável funcional; revisão da equipe pendente.

---

## 1. Objetivo

Registrar os resultados da primeira rodada de validação metodológica do CommunityLab Quality Framework (CQF v1.0), utilizando três cenários simulados de histórias de sucesso.

A validação busca verificar a aplicabilidade inicial dos critérios de avaliação, a coerência das classificações editoriais e a rastreabilidade das justificativas.

Esta etapa não constitui validação estatística, homologação técnica nem aprovação para publicação de conteúdo.

## 2. Metodologia

Foram utilizados quatro critérios, avaliados de 0 a 5:

| Critério | Peso |
|---|---:|
| Relevância da conquista | 25% |
| Completude narrativa | 25% |
| Clareza e impacto | 20% |
| Qualidade das evidências | 30% |

**Fórmula:**

`CQF Score = (R × 0,25 + C × 0,25 + I × 0,20 + E × 0,30) × 20`

**Faixas de classificação:**

- 80–100: Alta prioridade editorial
- 60–79: Prioridade média
- 0–59: Baixa prioridade ou necessidade de informações adicionais

Os pesos e limites são provisórios e deverão ser reavaliados conforme os resultados de testes adicionais.

## 3. Resultados consolidados

| Caso | Cenário | R | C | I | E | Score | Classificação |
|---|---|---:|---:|---:|---:|---:|---|
| CQF-001 | Conquista profissional | 5 | 4 | 5 | 4 | 89 | Alta |
| CQF-002 | Projeto de destaque | 4 | 4 | 4 | 3 | 74 | Média |
| CQF-003 | Superação | 5 | 5 | 5 | 4 | 94 | Alta |

**Legenda:** R = Relevância; C = Completude; I = Clareza e impacto; E = Evidências.

### CQF-001 — Conquista profissional

**Contexto:** relato simulado sobre a obtenção do primeiro emprego em tecnologia após um período de estudos e participação em projetos.

**Resultado:** 89/100 — Alta prioridade editorial.

**Justificativa:** conquista relevante, narrativa clara e evidências textuais rastreáveis. Há oportunidades de detalhamento e ausência de comprovação externa independente.

**Decisão:** pontuação de referência validada pelo responsável funcional.

### CQF-002 — Projeto de destaque

**Contexto:** relato simulado sobre a participação em um hackathon, com responsabilidades de organização, documentação e entrega de protótipo.

**Resultado:** 74/100 — Prioridade média.

**Justificativa:** projeto relevante e narrativa estruturada, mas com evidências limitadas à declaração textual, sem artefatos técnicos apresentados.

**Decisão:** pontuação de referência validada pelo responsável funcional.

### CQF-003 — Superação

**Contexto:** relato simulado sobre transição de carreira após desemprego, dificuldades durante os estudos e conquista de estágio em análise de dados.

**Resultado:** 94/100 — Alta prioridade editorial.

**Justificativa:** narrativa completa, transformação significativa e evidências textuais diretamente relacionadas à história. Não há comprovação externa independente.

**Decisão:** pontuação de referência validada pelo responsável funcional.

## 4. Controles de governança

O CQF Score estabelece uma prioridade editorial, mas não autoriza automaticamente a utilização pública de uma história.

Permanecem obrigatórios e independentes:

1. **Validação factual:** verificar a correspondência entre o conteúdo produzido e a interação original, incluindo citações literais, ausência de invenções e tratamento de contradições.
2. **Curadoria humana:** revisar, editar, aprovar ou rejeitar o ativo de marketing. Alterações editoriais devem preservar a fidelidade factual.
3. **Autorização para publicação:** verificar a existência de permissão apropriada antes de divulgar histórias ou depoimentos reais.

Os três cenários deste relatório são fictícios e devem ser identificados como exemplos simulados em qualquer demonstração.

## 5. Conclusões preliminares

A primeira rodada demonstrou a possibilidade de aplicar os quatro critérios de forma estruturada a três tipos diferentes de narrativa.

Os resultados apresentaram classificações distintas: dois casos de alta prioridade e um de prioridade média.

Essa diferença é compatível com as justificativas atribuídas, mas não comprova, por si só, a validade ou a capacidade de generalização da metodologia.

## 6. Limitações

- Amostra restrita a três casos simulados.
- Notas atribuídas em uma única rodada de avaliação funcional.
- Ausência de avaliadores independentes.
- Pesos e faixas de classificação ainda não calibrados empiricamente.
- Ausência de integração com a interface Streamlit ou com a persistência OCI.
- Ausência de validação em mensagens reais autorizadas.

## 7. Próximas atividades propostas

1. Submeter o relatório à revisão da Equipe 18.
2. Testar casos negativos: evidências insuficientes, informações contraditórias e ausência de autorização.
3. Definir um protocolo de avaliação para reduzir divergências entre avaliadores.
4. Verificar a viabilidade de apresentar o CQF na interface de curadoria do Streamlit.
5. Definir a persistência dos resultados e do histórico de avaliação na OCI, conforme a arquitetura aprovada.
6. Revisar os pesos e limites caso os testes indiquem necessidade.

## 8. Responsabilidades propostas

**Marcus — Project Manager:** responsável funcional pelo CQF, critérios, documentação e acompanhamento das validações.

**Jaqueline — AI Engineer:** apoio à validação factual e à verificação de conteúdos gerados.

**Tissiany — Full Stack Developer:** avaliação da integração com a interface de curadoria.

**Ketlyn — Machine Learning Engineer:** apoio à preparação de dados e cenários adicionais de teste.

**Luciene — Agent Engineer:** avaliação da integração ao fluxo de processamento e persistência OCI.

As responsabilidades técnicas deverão ser alinhadas com as respectivas integrantes.

---

**Resultado da etapa:** três referências metodológicas aprovadas pelo responsável funcional, prontas para revisão coletiva e expansão da bateria de testes.
