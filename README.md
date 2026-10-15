# CommunityLab

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/Artificial_Intelligence-8A2BE2?style=for-the-badge)
![Oracle Cloud](https://img.shields.io/badge/Oracle_Cloud-F80000?style=for-the-badge&logo=oracle&logoColor=white)
![ONE G10](https://img.shields.io/badge/ONE-G10-00875A?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Planning-orange?style=for-the-badge)


**Detector Inteligente de Histórias de Sucesso e Testemunhos com IA**

**Hackathon ONE G10 — Equipe 18 | Oracle Next Education + Alura**

**Status:** Planejamento e redefinição do escopo funcional do MVP

---

## 💡 Sobre o projeto

**O CommunityLab** é uma solução baseada em Inteligência Artificial que identifica histórias de sucesso, relatos de superação, conquistas profissionais e projetos de destaque em interações de comunidades digitais.
A proposta é transformar experiências compartilhadas espontaneamente em testemunhos, cases de sucesso e sugestões de conteúdo para redes sociais, utilizando modelos de linguagem (LLMs), processamento de linguagem natural e automação.
O projeto busca apoiar equipes de marketing e gestores de comunidades na identificação de histórias relevantes, preservando as evidências originais e permitindo revisão humana antes de qualquer utilização pública.
Desenvolvido para o **Hackathon ONE G10 — Oracle Next Education & Alura**, com participação na simulação de projetos da No Country.

---

## 🎯 O problema

Comunidades de aprendizagem, tecnologia e desenvolvimento profissional produzem diariamente mensagens sobre conquistas, desafios superados, oportunidades profissionais e projetos realizados.
Entretanto, muitas dessas histórias permanecem dispersas em conversas e históricos de mensagens.
Entre os principais desafios estão:
- Identificar conquistas profissionais e histórias de superação.
- Reconhecer projetos e realizações de destaque.
- Localizar testemunhos espontâneos dos participantes.
- Extrair fatos, resultados e citações verificáveis.
- Transformar relatos em conteúdos estruturados.
- Reduzir o esforço manual de análise e produção de materiais de marketing.
O resultado é a perda de oportunidades de comunicação, reconhecimento e engajamento.

---

## 🚀 Nossa solução

O CommunityLab propõe um Detector Inteligente de Histórias de Sucesso e Testemunhos, capaz de analisar interações de comunidades digitais e identificar automaticamente relatos relevantes.
O fluxo previsto compreende:

1. **Ingestão:** recebimento de mensagens por arquivos CSV ou JSON.
2. **Preparação:** limpeza, normalização e estruturação dos dados.
3. **Análise com IA:** identificação de sentimentos, tópicos e relevância.
4. **Detecção:** reconhecimento de histórias de sucesso, conquistas profissionais, superação e projetos de destaque.
5. **Extração:** identificação de fatos, resultados, evidências e citações originais.
6. **Geração:** produção automatizada de testemunhos, cases de sucesso e sugestões de posts LinkedIn.
7. **Curadoria:** visualização, edição, aprovação ou rejeição dos conteúdos.
8. **Armazenamento:** persistência e recuperação dos ativos no OCI Object Storage.

Os conteúdos não serão publicados automaticamente. A divulgação de relatos identificáveis dependerá de autorização apropriada.

---

## 📋 Objetivo do MVP

Desenvolver e demonstrar uma solução funcional capaz de identificar histórias de sucesso em comunidades digitais e transformá-las em ativos de marketing, utilizando Inteligência Artificial, automação e curadoria humana.

### ⚙️ Funcionalidades previstas

- [ ] Ingestão de mensagens por CSV/JSON.
- [ ] Preparação e estruturação textual dos dados.
- [ ] Análise de sentimentos utilizando LLMs.
- [ ] Extração e classificação de tópicos relevantes.
- [ ] Identificação de interações com potencial estratégico.
- [ ] Detecção de histórias de sucesso, conquistas e relatos de superação.
- [ ] Extração de fatos, resultados, evidências e citações originais.
- [ ] Geração de testemunhos estruturados.
- [ ] Geração de cases de sucesso.
- [ ] Geração complementar de sugestões de posts LinkedIn.
- [ ] Orquestração automatizada do processamento em Python.
- [ ] Interface web para visualização e curadoria.
- [ ] Integração com OCI Object Storage — Always Free.
- [ ] Persistência e recuperação dos ativos gerados.
- [ ] Demonstração de pelo menos três casos de uso.

As funcionalidades representam o escopo planejado e não implementações já concluídas.
Limites do MVP, a primeira versão priorizará arquivos CSV/JSON, sem exigir integração direta com Discord, Slack ou outras plataformas.
Publicação automática, dashboards avançados e monitoramento em tempo real poderão ser desenvolvidos futuramente.

---

## 🏗️ Arquitetura conceitual

O fluxo proposto é:

**Mensagens de comunidades digitais — CSV / JSON**
                    ↓
       **Ingestão e preparação dos dados**
                    ↓
    **Análise de sentimentos e tópicos com LLM**
                    ↓
       **Detecção de histórias de sucesso**
                    ↓
   **Extração de fatos, resultados e citações**
                    ↓
    **Geração de testemunhos, cases e posts**
                    ↓
       **Interface de visualização e curadoria**
                    ↓
 Persistência e recuperação no OCI Object Storage
A orquestração será realizada por scripts Python, com tratamento de erros e fluxos condicionais.
A arquitetura técnica definitiva será validada durante o desenvolvimento.

---

## 🛠️ Tecnologias

### Stack proposta

| Tecnologia | Aplicação prevista |
|---|---|
| Python | Processamento de dados e lógica de aplicação |
| Pandas | Leitura e preparação dos dados |
| LLMs | Análise, extração e geração de conteúdo |
| Pydantic | Validação de dados estruturados |
| Streamlit | Interface web e curadoria |
| OCI Python SDK | Integração com Oracle Cloud 
| OCI Object Storage | Persistência e recuperação dos ativos |
| pytest | Testes automatizados |
| GitHub | Versionamento e colaboração |
| Trello | Gestão de atividades e entregáveis |


**Observação:** O provedor de LLM e as configurações definitivas serão definidos conforme os requisitos e recursos disponíveis.

---

## 👥 Equipe

| Integrante | Responsabilidade |
|---|---|
| Marcus | Project Manager |
| Ketlyn Barbosa | Machine Learning Engineer |
| Tissiany Delmiro | Full Stack Developer |
| Jaqueline de Lira | AI Engineer |
| Luciene Godoy | Agent Engineer |

O desenvolvimento será conduzido colaborativamente, com responsabilidades distribuídas conforme as especialidades técnicas e as necessidades do MVP.

---

## 📁 Organização do repositório

Estrutura inicial proposta:

```
CommunityLab/
├── README.md
├── .gitignore
├── .env.example
├── docs/
│   └── architecture/
├── data/
│   └── samples/
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── analysis/
│   ├── detection/
│   ├── extraction/
│   ├── generation/
│   ├── orchestration/
│   └── storage/
├── app/
├── tests/
└── workflows/
```
Essa estrutura é planejada. Os diretórios serão criados e ajustados durante a implementação.

---

## 🤝 Padrões de colaboração

### Branches

A branch principal será main.

Novas funcionalidades deverão ser desenvolvidas em branches específicas:

- feature/nome-da-funcionalidade
- fix/descricao-da-correcao
- docs/descricao-da-documentacao
- chore/descricao-da-tarefa

### Commits

Adotaremos mensagens objetivas, preferencialmente seguindo o padrão Conventional Commits.

Exemplos:

- feat: implementa ingestao de arquivos csv
- feat: adiciona detector de historias de sucesso
- feat: gera testemunhos estruturados
- fix: corrige extracao de citacoes
- docs: atualiza arquitetura do projeto
- test: adiciona testes de classificacao

### Pull Requests

As alterações deverão ser integradas preferencialmente por Pull Requests.

Cada Pull Request deverá apresentar:

1. Descrição da alteração.
2. Referência ao card correspondente no Trello.
3. Evidências de testes realizados.
4. Informações sobre impactos em outros módulos.
5. Revisão técnica antes da integração de alterações críticas.

---

## 🔐 Segurança, privacidade e proteção de credenciais

O projeto seguirá práticas de segurança e proteção de dados:

- Não armazenar senhas, tokens ou chaves de API no repositório.
- Utilizar variáveis de ambiente para informações sensíveis.
- Manter arquivos .env fora do versionamento.
- Disponibilizar .env.example sem valores secretos.
- Preservar a rastreabilidade entre citações e mensagens originais.
- Evitar gerar fatos, resultados ou declarações não comprovados.
- Utilizar dados simulados ou autorizados nas demonstrações.
- Exigir revisão humana antes da utilização pública dos conteúdos.
- Respeitar a privacidade e a autorização dos participantes.
- Revisar permissões de acesso aos serviços utilizados.

---

## 📊 Gestão do projeto

O planejamento e acompanhamento serão realizados no Trello, utilizando Kanban.
O projeto está estruturado em 25 cards distribuídos em sete fases:

1. Planejamento e Arquitetura.
2. Ingestão e Preparação.
3. Inteligência Artificial.
4. Geração de Conteúdo.
5. Automação e OCI.
6. Interface e Visualização.
7. Testes, Documentação e Apresentação.

Cada atividade será acompanhada por prioridade, responsável, dependências, critérios de aceitação e status de execução.
Branches, commits e Pull Requests poderão ser associados aos cards para garantir rastreabilidade.

---

## 🗺️ Roadmap inicial
- [ ] Validar o escopo revisado do detector.
- [ ] Configurar o repositório e os padrões de colaboração.
- [ ] Validar a arquitetura Python + LLM + Streamlit + OCI.
- [ ] Preparar os dados de demonstração.
- [ ] Implementar ingestão CSV/JSON.
- [ ] Desenvolver análise de sentimentos e tópicos.
- [ ] Implementar detecção de histórias de sucesso.
- [ ] Implementar extração de fatos, resultados e citações.
- [ ] Desenvolver geração de testemunhos.
- [ ] Desenvolver geração de cases de sucesso.
- [ ] Implementar orquestração automatizada.
- [ ] Desenvolver interface de curadoria.
- [ ] Integrar OCI Object Storage.
- [ ] Executar testes funcionais e de integração.
- [ ] Demonstrar três casos de uso.
- [ ] Finalizar documentação e apresentação.

---

## 🧪 Casos de demonstração

.Caso 1 — Conquista profissional
Identificação de um relato de obtenção de emprego após participação em uma comunidade de aprendizagem.
Resultado esperado: extração da conquista, identificação de evidências e geração de testemunho.

.Caso 2 — Projeto de destaque
Identificação de um projeto tecnológico relevante desenvolvido por participantes da comunidade.
Resultado esperado: extração de informações e geração de case de sucesso.

.Caso 3 — Superação e transformação profissional
Identificação de uma trajetória de desenvolvimento, superação de dificuldades ou transição de carreira.
Resultado esperado: geração de testemunho e sugestão de publicação para LinkedIn.

As demonstrações utilizarão dados simulados ou autorizados.

---

## 📈 Resultados esperados

Ao final do desenvolvimento, o CommunityLab deverá demonstrar a capacidade de:

- Processar interações provenientes de comunidades digitais.
- Identificar histórias de sucesso e testemunhos relevantes.
- Classificar sentimentos e tópicos.
- Extrair fatos, resultados e citações rastreáveis.
- Transformar histórias em ativos de marketing.
- Permitir revisão e curadoria humana.
- Armazenar e recuperar os conteúdos no OCI Object Storage.
- Executar um fluxo automatizado, integrado e demonstrável.

O objetivo é reduzir o esforço manual de curadoria e ampliar o aproveitamento das histórias produzidas pelas comunidades.

---

## 📄 Licença

A licença do projeto será definida pela equipe, considerando as regras do Hackathon e a estratégia de disponibilização do código-fonte.
CommunityLab — Histórias que inspiram. Inteligência que transforma.
Projeto desenvolvido para o Hackathon ONE G10 — Oracle Next Education & Alura.
Equipe 18 | Prazo final: 24 de novembro de 2026.
