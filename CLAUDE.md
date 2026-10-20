Você vai EVOLUIR o front-end Streamlit do CommunityLab que já existe neste repositório. Não recomece do zero. Trabalhe POR ETAPAS, fazendo commits profissionais e atualizando o README a cada etapa.

CONTEXTO
- Produto: CommunityLab, Detector Inteligente de Histórias de Sucesso e Testemunhos (Hackathon ONE G10, Oracle Next Education + Alura). Transforma conversas de comunidades digitais em testemunhos estruturados e cases de sucesso, com rastreabilidade e supervisão humana.
- Princípio: a IA sugere, o time decide. Nada é publicado automaticamente. Todo ativo gerado aponta para a mensagem original. Uma pontuação alta não comprova veracidade nem autoriza publicação.
- O front roda só com dados fictícios. Estrutura atual: app/main.py, app/telas/, app/services/data_service.py (único ponto de acesso a dados, com TODO(back)), app/mocks/mock_data.py, app/state.py, app/styles.py, .streamlit/config.toml, README do front.

REGRAS TÉCNICAS
- Streamlit >= 1.37. Evite parâmetros depreciados (ex.: use_container_width).
- As telas só falam com data_service.py. Não importe mocks dentro das telas. Mudanças no formato dos dados devem ser ADITIVAS (campos novos opcionais) e documentadas no README.
- Todo texto da interface em português do Brasil, natural e sem jargão.
- Não adicione dependências nem frameworks novos.
- Todos os dados continuam fictícios e identificados como tal.
- Mantenha o app funcionando ao fim de cada etapa. Nunca deixe o fluxo quebrado entre commits.

REGRAS DE GIT (siga à risca)
- Antes de tudo, rode `git status`, `git branch` e `git config user.name` / `git config user.email` e me mostre. Se o nome/e-mail não parecerem corretos, PARE e me avise (este computador é compartilhado).
- Nunca trabalhe na main. Crie uma branch por bloco de etapas (nomes abaixo).
- Nunca rode `git push`, `git push --force` nem `git reset --hard`. Você só faz commits locais. Eu envio ao GitHub.
- Commits pequenos, atômicos e frequentes: uma mudança lógica por commit, sem misturar visual, lógica e documentação no mesmo commit.
- Padrão Conventional Commits, em português: `tipo(escopo): descrição`.
  - Tipos: feat, fix, refactor, style, docs, chore, test.
  - Escopo: front (ou o nome da tela, ex.: front-curadoria).
  - Descrição no imperativo, minúscula, até 72 caracteres, sem ponto final.
  - Corpo (opcional, separado por linha em branco): explique O QUE mudou e POR QUÊ, em linhas de até 72 caracteres.
  - Exemplo: `feat(front-curadoria): separa aprovação editorial e autorização de uso`
- Antes de cada commit: rode o app, percorra o fluxo afetado e confira `git status` e `git diff --staged` para garantir que só os arquivos esperados entraram (sem __pycache__, .venv, .env).
- Se não existir, crie um .gitignore com: __pycache__/, *.pyc, .venv/, .env (commit próprio: `chore(front): adiciona .gitignore`).

COMO TRABALHAR POR ETAPAS
- PASSO 0 (antes de codar): leia o código atual, proponha um plano curto (arquivos que serão criados ou alterados, ordem, mensagens de commit previstas) e ESPERE minha confirmação.
- Ao fim de CADA etapa: (1) rode e teste; (2) atualize o README do front somente nas seções afetadas; (3) faça os commits (um de código por mudança lógica e um `docs(front): ...` para o README); (4) me mostre `git log --oneline` das últimas entradas, um resumo do que mudou, o que ficou de fora e o comando `git push` que devo rodar; (5) PARE e espere eu dizer "ok" para seguir.

ETAPAS

Branch: feat/front-visual-e-navegacao

ETAPA 1: Identidade visual (estilo híbrido SaaS corporativo + IA)
Tokens (centralize em app/styles.py e .streamlit/config.toml):
- Azul-marinho #101B32: menu lateral e navegação. Texto e ícones claros sobre ele.
- Violeta #7C3AED: cor primária, ações de IA e elementos de destaque (botão principal, selo "Gerado por IA").
- Ciano #22D3EE: SOMENTE detalhes tecnológicos (ícones, barras de progresso, brilhos) e sobre o azul-marinho. Nunca como cor de texto sobre fundo claro.
- Branco-neutro #F8FAFC: fundo da área de trabalho. Cards brancos com borda #E2E8F0.
- Verde #10B981: sucesso e aprovação em ícones e fundos de chip. Para TEXTO sobre fundo claro use verde escuro (ex.: #047857).
- Texto principal #0F172A, secundário #64748B.
Regras: Inter, cantos arredondados, bastante respiro. Degradê violeta para ciano só em pequenos destaques (selo de IA, barra de processamento). Sem neon, sem excesso de efeitos. Contraste legível (WCAG AA). Sidebar escura: teste os botões do menu nos três estados (normal, hover, ativo). Foco em desktop, sem prometer responsividade completa. Slogan "Histórias reais. Impacto inteligente." apenas no cabeçalho da sidebar, mantendo os avisos de dados fictícios.
Commits previstos: `style(front): define tokens de cor e tipografia da nova identidade`, `style(front): aplica sidebar azul-marinho e estados do menu`, `docs(front): documenta a identidade visual`.

ETAPA 2: Navegação e Dashboard
Menu lateral: Dashboard, Importação, Histórias, Estúdio de Conteúdo, Curadoria, Histórico.
- Dashboard (nova): resumo simples (interações, histórias detectadas, ativos gerados, aprovados, pendentes). Sem gráficos complexos.
- Importação: Ingestão + Processamento atuais. Botão principal "Importar interações", com o maior destaque visual da tela.
- Histórias: listagem atual.
- Histórico: a tela de Armazenamento OCI atual (consulta e recuperação dos registros persistidos).
- Estúdio de Conteúdo e Curadoria: na etapa 2 apenas as entradas no menu apontando para as telas atuais (o Estúdio ganha conteúdo na etapa 3).
Commits previstos: `feat(front): reorganiza a navegação com os seis módulos`, `feat(front-dashboard): adiciona resumo de interações, histórias e ativos`, `refactor(front-importacao): renomeia ação principal para Importar interações`, `docs(front): atualiza navegação no README`.

Branch: feat/front-estudio-e-curadoria

ETAPA 3: Estúdio de Conteúdo (tela principal do produto)
Tipos de ativo do MVP: Testemunho estruturado e Case de sucesso (Post para LinkedIn pode existir como complementar). Atualize os mocks de forma aditiva para esses tipos.
Duas colunas lado a lado:
- Esquerda, "Fatos e evidências originais": mensagem original com os trechos usados destacados, fatos extraídos (cada um com "Vem da mensagem original"), canal, autor, lote.
- Direita, "Conteúdo gerado pela IA": abas por tipo de ativo, texto editável, contador de caracteres, selo "Gerado por IA", Regenerar e Copiar. O conteúdo da IA deve ser visualmente distinguível do original (faixa lateral ou selo).
- Abaixo do conteúdo: "Fontes deste conteúdo", ligando cada afirmação ao fato ou citação de origem.
- Botão "Enviar para curadoria". Nada é publicado.
- Regra: o Estúdio serve para LER evidências e EDITAR. A decisão (aprovar, rejeitar, ajustes) fica só na Curadoria.
Commits previstos: `feat(front-mocks): adiciona testemunho estruturado e case de sucesso`, `feat(front-estudio): exibe evidências ao lado do conteúdo gerado`, `feat(front-estudio): adiciona fontes do conteúdo e envio para curadoria`, `docs(front): documenta o Estúdio de Conteúdo`.

ETAPA 4: Curadoria com controles separados (conforme a especificação do CQF)
A Curadoria é a fila de decisão. Três controles INDEPENDENTES por ativo:
1) Validação factual: Pendente, Validada, Evidências insuficientes, Contradição não resolvida.
2) Curadoria: Rascunho, Ajustes solicitados, Aprovado, Rejeitado (rejeição com motivo opcional; ajustes com observação).
3) Autorização de publicação: Não registrada, Registrada.
Regras:
- A autorização NÃO bloqueia a aprovação editorial. Sem autorização ainda é possível analisar e aprovar internamente.
- O indicador "Liberado para publicação" só aparece quando: curadoria = Aprovado, autorização = Registrada e validação factual = Validada. Mesmo assim, o sistema NÃO publica nada.
- RG-02: com "Contradição não resolvida", o botão Aprovar fica desabilitado, com explicação.
- RG-01: a interface nunca preenche lacunas com informação inventada. "Regenerar" não pode introduzir fatos que não estejam nas evidências (no mock, apenas alterna variações fictícias).
- Se o usuário editar fatos ou citações, mostre um alerta e volte a validação factual para "Pendente".
- Mantenha "Desfazer decisão".
Commits previstos: `refactor(front-curadoria): separa validação factual, curadoria e autorização`, `feat(front-curadoria): adiciona decisão Solicitar ajustes`, `feat(front-curadoria): bloqueia aprovação com contradição não resolvida (RG-02)`, `feat(front-curadoria): exibe liberação para publicação (RG-03)`, `docs(front): documenta as regras de curadoria`.

ETAPAS DO CQF: SÓ EXECUTE QUANDO EU CONFIRMAR (a proposta ainda está em validação pela equipe)

Branch: feat/front-cqf

ETAPA 5: Painel CQF, fase 1 (por história, na Curadoria)
- 4 critérios com nota de 0 a 5: Relevância da conquista (25%), Completude narrativa (25%), Clareza e impacto (20%), Qualidade das evidências (30%).
- CQF Score = (R*0,25 + C*0,25 + I*0,20 + E*0,30) * 20, em escala 0 a 100, calculado automaticamente.
- Classificação: 80 a 100 Alta prioridade editorial; 60 a 79 Prioridade média; 0 a 59 Baixa prioridade ou necessidade de complementação (faixas provisórias, deixe-as em constantes fáceis de ajustar).
- A pontuação é INFORMATIVA: nunca aprova, rejeita nem libera nada automaticamente. Exiba o aviso: "Pontuação alta não comprova veracidade nem autoriza publicação."
- Nomes na tela: "Relevância (IA)" para o valor que vem da IA e "CQF Score" para a pontuação editorial, para evitar confusão entre dois números de 0 a 100.
- Dados (aditivos, em data_service e mocks), seguindo a seção 8 da especificação: id_avaliacao, id_historia, id_ativo (opcional), versao_framework, nota_relevancia, nota_completude, nota_clareza_impacto, nota_evidencias, cqf_score, classificacao_editorial, status_validacao_factual, status_curadoria, status_autorizacao_publicacao, responsavel_avaliacao, data_avaliacao, observacoes. Marque o formato como provisório (a persistência na OCI está sendo definida com a equipe).
- Os valores de referência do relatório (89, 74, 94) só devem ser usados como pré-preenchimento se eu confirmar que os mocks correspondem aos cenários do relatório.
Commits previstos: `feat(front-cqf): adiciona cálculo do CQF Score e classificação`, `feat(front-cqf): adiciona painel de avaliação na curadoria`, `feat(front-cqf): inclui campos de avaliação no data_service e nos mocks`, `docs(front): documenta o CQF e o formato provisório dos dados`.

ETAPA 6 (opcional, só se sobrar tempo): campo de observações, responsável pela avaliação e histórico simples das avaliações. Não implemente os indicadores da seção 10 da especificação.

ETAPA FINAL: revisão
- Passe pelo fluxo completo, confira o README inteiro (como rodar, estrutura de pastas, navegação, regras de curadoria, formato provisório dos dados, limitações) e liste pendências.
- Commit: `docs(front): revisa o README final`.