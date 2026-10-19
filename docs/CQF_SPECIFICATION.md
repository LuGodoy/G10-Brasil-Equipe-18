# CommunityLab Quality Framework (CQF)

**Versão:** 1.0 — Proposta para validação da equipe  
**Projeto:** CommunityLab — Detector Inteligente de Histórias de Sucesso e Testemunhos  
**Hackathon:** ONE G10 — Oracle Next Education & Alura  
**Responsável pela concepção funcional:** Marcus — Project Manager  
**Status:** Especificação proposta, pendente de validação e implementação

## 1. Visão geral

O **CommunityLab Quality Framework (CQF)** é uma metodologia de avaliação de qualidade e governança editorial destinada a apoiar a curadoria humana de histórias de sucesso identificadas por Inteligência Artificial.

Seu objetivo é estabelecer critérios consistentes para avaliar o potencial editorial de uma história, considerando sua relevância, completude, clareza e qualidade das evidências.

O CQF complementa os mecanismos de validação técnica e rastreabilidade do CommunityLab, sem substituí-los.

**Princípio fundamental:** uma pontuação elevada não comprova a veracidade de uma história nem autoriza automaticamente sua publicação.

## 2. Objetivos específicos

- Padronizar a avaliação editorial de histórias identificadas.
- Apoiar a priorização dos conteúdos que merecem revisão.
- Reduzir decisões subjetivas e inconsistentes.
- Valorizar histórias com evidências verificáveis.
- Identificar conteúdos que precisam de complementação.
- Apoiar a qualidade de testemunhos estruturados e cases de sucesso.
- Garantir transparência sobre os critérios utilizados.
- Preservar a decisão humana sobre aprovação editorial.

## 3. Escopo de aplicação

O CQF será aplicado às histórias detectadas pelo pipeline do CommunityLab, especialmente nas categorias:

- Conquista profissional.
- Projeto de destaque.
- Superação.
- Outras conquistas identificadas e sustentadas por evidências.

A metodologia deverá funcionar independentemente do formato de ativo produzido.

Os dois formatos principais do MVP são:

1. **Testemunho estruturado.**
2. **Case de sucesso.**

Posts LinkedIn poderão utilizar os mesmos critérios como funcionalidade complementar, caso sejam implementados.

## 4. Matriz de avaliação CQF

Cada critério receberá uma nota de **0 a 5**, multiplicada por seu peso.

| Critério | Peso |
|---|---:|
| Relevância da conquista | 25% |
| Completude narrativa | 25% |
| Clareza e impacto | 20% |
| Qualidade das evidências | 30% |
| **Total** | **100%** |

### 4.1 Relevância da conquista — 25%

Avalia o significado da experiência relatada e sua pertinência ao propósito do CommunityLab.

**Referências de pontuação:**

- 0: nenhuma conquista identificável.
- 1: relevância muito limitada.
- 2: conquista pouco contextualizada.
- 3: conquista relevante e compreensível.
- 4: conquista significativa, com contexto claro.
- 5: conquista especialmente representativa e bem fundamentada.

### 4.2 Completude narrativa — 25%

Avalia a presença de informações suficientes para construir uma narrativa fiel.

Considerar:

- Contexto da experiência.
- Situação ou desafio.
- Ações ou trajetória relatadas.
- Resultado ou conquista.
- Relação entre os fatos.

**A ausência de informações não deverá ser compensada com conteúdo inventado.**

Uma história poderá receber nota menor por incompletude sem que isso represente falta de mérito da pessoa retratada.

### 4.3 Clareza e impacto — 20%

Avalia a compreensão da história e seu potencial comunicacional.

Considerar:

- Clareza dos acontecimentos.
- Coerência narrativa.
- Facilidade de compreensão.
- Capacidade de transmitir aprendizado ou inspiração.
- Adequação ao público pretendido.

A avaliação não deverá privilegiar artificialmente histórias dramáticas ou resultados financeiros elevados.

### 4.4 Qualidade das evidências — 30%

Avalia a sustentação factual da história.

Considerar:

- Existência de fontes identificáveis.
- Correspondência entre fatos e mensagens originais.
- Preservação de citações literais.
- Ausência de contradições relevantes.
- Rastreabilidade dos dados utilizados.

Uma boa pontuação neste critério não substitui a validação factual obrigatória.

## 5. Cálculo do CQF Score

O resultado será calculado em uma escala de 0 a 100:

**CQF Score = (R × 0,25 + C × 0,25 + I × 0,20 + E × 0,30) × 20**

Onde:

- **R:** relevância da conquista.
- **C:** completude narrativa.
- **I:** clareza e impacto.
- **E:** qualidade das evidências.

Cada variável recebe uma nota de 0 a 5.

### Faixas propostas

| Pontuação | Classificação |
|---|---|
| 80 a 100 | Alta prioridade editorial |
| 60 a 79 | Prioridade média |
| 0 a 59 | Baixa prioridade ou necessidade de complementação |

Essas faixas são **parâmetros iniciais**, sujeitos à calibração após testes com histórias reais ou simuladas.

A classificação representa potencial editorial, não autorização de publicação.

## 6. Regras obrigatórias de governança

Independentemente da pontuação, o sistema deverá observar três controles separados.

### 6.1 Validação factual

Verificar se:

- Os fatos estão sustentados pelas fontes.
- As citações literais correspondem ao texto original.
- Não existem informações inventadas.
- As evidências são rastreáveis.
- Não há contradições relevantes não resolvidas.

Histórias com evidências insuficientes ou contraditórias deverão ser encaminhadas para revisão, complementação ou rejeição.

### 6.2 Curadoria editorial

A revisão humana deverá permitir:

- Examinar a história e suas evidências.
- Consultar o CQF Score e seus critérios.
- Editar os conteúdos gerados.
- Solicitar ajustes.
- Aprovar ou rejeitar os ativos.
- Registrar a decisão editorial.

A edição de fatos ou citações deverá exigir nova validação de fidelidade.

### 6.3 Autorização para publicação

A autorização deverá ser registrada separadamente da aprovação editorial.

**Uma história aprovada não estará automaticamente autorizada para publicação.**

A ausência de autorização deverá impedir a liberação para publicação, mesmo quando o CQF Score for elevado.

## 7. Fluxo funcional proposto

1. Receber uma história detectada pelo pipeline.
2. Consultar fatos e evidências associados.
3. Executar as verificações técnicas de fidelidade.
4. Disponibilizar os critérios de avaliação CQF.
5. Registrar as notas atribuídas pelo avaliador humano.
6. Calcular o CQF Score.
7. Apresentar a classificação de prioridade editorial.
8. Encaminhar os ativos para curadoria.
9. Registrar aprovação, rejeição ou solicitação de ajustes.
10. Manter a autorização para publicação como controle independente.
11. Persistir a avaliação e as decisões, conforme a integração com OCI.

**No MVP, recomenda-se avaliação humana assistida pelo sistema, sem aprovação automática baseada na pontuação.**

## 8. Estrutura de dados proposta

Cada avaliação CQF deverá conter:

- `id_avaliacao`
- `id_historia`
- `id_ativo`, quando aplicável
- `versao_framework`
- `nota_relevancia`
- `nota_completude`
- `nota_clareza_impacto`
- `nota_evidencias`
- `cqf_score`
- `classificacao_editorial`
- `status_validacao_factual`
- `status_curadoria`
- `status_autorizacao_publicacao`
- `responsavel_avaliacao`
- `data_avaliacao`
- `observacoes`

O modelo definitivo deverá ser alinhado aos contratos de dados e às estruturas já adotadas pelo projeto.

## 9. Integração com a interface

A interface Streamlit poderá apresentar um painel CQF na área de curadoria, contendo:

- Critérios de avaliação.
- Notas de 0 a 5.
- Pesos aplicados.
- CQF Score calculado.
- Classificação editorial.
- Evidências associadas.
- Alertas de validação factual.
- Campo de observações.
- Identificação do responsável pela avaliação.
- Estados de curadoria e autorização separados.

A implementação deverá priorizar clareza, simplicidade e aderência ao prazo do Hackathon.

## 10. Indicadores de acompanhamento

Após a implementação, poderão ser acompanhados:

- Quantidade de histórias avaliadas.
- Distribuição dos CQF Scores.
- Histórias por prioridade editorial.
- Proporção de histórias com evidências suficientes.
- Quantidade de ativos aprovados ou rejeitados.
- Principais motivos de revisão.
- Tempo médio de curadoria, se houver registro adequado.

Os indicadores deverão utilizar dados efetivamente registrados pelo sistema.

## 11. Responsabilidades

**Marcus — Project Manager / Responsável funcional pelo CQF**

- Conceber a metodologia.
- Definir critérios e regras de negócio.
- Validar pesos e classificações.
- Elaborar critérios de aceitação.
- Coordenar a avaliação dos resultados.

**Jaqueline de Lira — AI Engineer**

- Avaliar compatibilidade com os mecanismos de validação factual.
- Apoiar a associação entre histórias, ativos e evidências.
- Contribuir para os testes de qualidade.

**Tissiany Delmiro — Full Stack Developer**

- Avaliar a incorporação da matriz à interface Streamlit.
- Implementar os controles de avaliação, conforme priorização.
- Integrar a experiência à curadoria.

**Ketlyn Barbosa — Machine Learning Engineer**

- Apoiar a definição de dados de teste.
- Verificar consistência das informações de entrada.
- Contribuir para a avaliação dos resultados.

**Luciene Godoy — Agent Engineer**

- Avaliar a integração dos registros ao pipeline.
- Apoiar a persistência e recuperação das avaliações na OCI.
- Preservar os identificadores de rastreabilidade.

## 12. Validação inicial

A metodologia deverá ser testada com os três cenários obrigatórios do CommunityLab:

1. Conquista profissional.
2. Projeto de destaque.
3. Superação.

Para cada cenário:

- Aplicar os quatro critérios.
- Calcular o CQF Score.
- Verificar a coerência da classificação.
- Conferir a qualidade das evidências.
- Registrar eventuais divergências entre avaliadores.
- Avaliar a necessidade de ajustes nos pesos ou nas faixas.

Também deverão ser testados casos com evidências insuficientes, informações contraditórias e ausência de autorização para publicação.

## 13. Critérios de aceitação

A especificação funcional do CQF será considerada validada quando:

- Os quatro critérios estiverem definidos.
- Os pesos totalizarem 100%.
- A fórmula estiver documentada e verificada.
- As faixas de classificação estiverem definidas como parâmetros iniciais.
- A distinção entre pontuação e validação factual estiver clara.
- As regras de curadoria humana estiverem documentadas.
- A autorização para publicação estiver separada da aprovação.
- Os três cenários tiverem sido avaliados.
- Os resultados forem discutidos com a equipe.
- A viabilidade de integração ao MVP for confirmada.

A implementação técnica deverá possuir critérios de aceitação próprios.

## 14. Limitações e evolução

A versão 1.0 é uma proposta metodológica, ainda não calibrada empiricamente.

Os pesos e limites poderão ser revisados após os testes.

Evoluções futuras poderão incluir:

- Apoio automatizado à sugestão de notas.
- Comparação entre avaliações de diferentes revisores.
- Histórico de versões das avaliações.
- Análise de consistência editorial.
- Indicadores de qualidade ao longo do tempo.

Essas evoluções não fazem parte obrigatória do MVP.

## 15. Resultado esperado

Estabelecer uma metodologia documentada, transparente e reproduzível para apoiar a avaliação editorial das histórias de sucesso identificadas pelo CommunityLab.

O **CommunityLab Quality Framework** deverá contribuir para que os conteúdos gerados sejam relevantes, fundamentados, rastreáveis e submetidos à decisão humana responsável.

**O CQF não substitui a validação técnica, a curadoria humana nem a autorização para publicação.**
