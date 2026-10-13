# CommunityLab

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/Artificial_Intelligence-8A2BE2?style=for-the-badge)
![Oracle Cloud](https://img.shields.io/badge/Oracle_Cloud-F80000?style=for-the-badge&logo=oracle&logoColor=white)
![ONE G10](https://img.shields.io/badge/ONE-G10-00875A?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Planning-orange?style=for-the-badge)


### Transformando Conversas de Comunidades Digitais em Inteligência e Conteúdo de Marketing com IA

**Hackathon ONE G10 - Equpe 18 | Oracle Next Education + Alura**

**Status:** Planejamento e estruturação do MVP

---

## 💡 Sobre o projeto

O **CommunityLab** é uma solução baseada em Inteligência Artificial que transforma interações de comunidades digitais em insights estratégicos e ativos de marketing.

O projeto busca ajudar equipes de marketing, gestores de comunidades e criadores de conteúdo a identificar assuntos relevantes, compreender sentimentos e aproveitar o conhecimento gerado espontaneamente pelas comunidades.

Por meio de análise de linguagem natural, modelos de linguagem (LLMs) e automação de processos, o CommunityLab pretende transformar dados não estruturados em informações organizadas e conteúdos que possam ser revisados e utilizados em estratégias de comunicação.

O projeto está sendo desenvolvido durante o **Hackathon ONE G10 — Oracle Next Education & Alura**.

---

## 🎯 O problema

Comunidades digitais produzem diariamente grandes volumes de informações relevantes, incluindo dúvidas, opiniões, sugestões, experiências e tendências.

Entretanto, boa parte desse conteúdo permanece dispersa, dificultando sua análise e utilização estratégica.

Entre os principais desafios estão:

- Identificar os temas mais discutidos.
- Compreender os sentimentos expressos pelos participantes.
- Reconhecer dúvidas e necessidades recorrentes.
- Selecionar interações com potencial para gerar conteúdo.
- Transformar informações em materiais de marketing.
- Reduzir o esforço manual de análise e produção.

---

## 🚀 Nossa solução

O CommunityLab propõe um fluxo automatizado capaz de receber interações de comunidades, processar seu conteúdo utilizando IA e gerar materiais de marketing a partir dos insights identificados.

O funcionamento previsto compreende:

1. **Ingestão:** recebimento de mensagens e arquivos CSV ou JSON.
2. **Processamento:** organização e preparação dos dados.
3. **Análise com IA:** identificação de sentimentos, tópicos e interações relevantes.
4. **Seleção de oportunidades:** identificação de informações com potencial de aproveitamento.
5. **Geração de conteúdo:** produção automatizada de pelo menos dois formatos de ativos de marketing.
6. **Curadoria:** visualização, revisão e seleção dos resultados por meio de uma interface amigável.
7. **Armazenamento:** integração com Oracle Cloud Infrastructure (OCI) Object Storage.

---

## 📋 Objetivo do MVP

Desenvolver e demonstrar uma solução funcional capaz de transformar interações de comunidades digitais em inteligência acionável e conteúdos de marketing, utilizando Inteligência Artificial e automação.

### ⚙️ Funcionalidades previstas

- [ ] Ingestão de mensagens e arquivos CSV/JSON.
- [ ] Análise de sentimentos com IA.
- [ ] Extração de tópicos relevantes.
- [ ] Identificação de interações de interesse.
- [ ] Geração de pelo menos dois formatos de ativos de marketing.
- [ ] Orquestração automatizada do processamento.
- [ ] Interface para visualização e curadoria.
- [ ] Integração com OCI Object Storage (Always Free).
- [ ] Demonstração de pelo menos três interações relevantes, conforme os requisitos do Hackathon.

As funcionalidades acima representam o escopo planejado, não implementações já concluídas.

---

## 🏗️ Arquitetura conceitual

O fluxo inicial proposto é:

**Comunidade digital / CSV / JSON**

↓

**Ingestão e preparação dos dados**

↓

**Análise com Inteligência Artificial**

↓

**Identificação de tópicos, sentimentos e oportunidades**

↓

**Geração automatizada de conteúdos**

↓

**Interface de visualização e curadoria**

↓

**Armazenamento e disponibilização dos resultados**

A arquitetura técnica definitiva será documentada após a validação das tecnologias e das integrações.

---

## 🛠️ Tecnologias

### Tecnologias e recursos previstos

| Tecnologia | Aplicação prevista |
|---|---|
| Python | Processamento de dados e lógica de aplicação |
| LLMs | Análise de linguagem e geração de conteúdo |
| n8n ou equivalente | Orquestração de processos |
| OCI Object Storage | Armazenamento de dados e artefatos |
| GitHub | Versionamento e colaboração |
| Trello | Gestão de atividades e entregáveis |

**Observação:** A escolha definitiva de frameworks, modelos, serviços complementares e ferramentas de interface será realizada durante a definição da arquitetura.

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

```text
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
│   ├── agents/
│   ├── generation/
│   ├── orchestration/
│   └── storage/
├── app/
├── tests/
└── workflows/
```

Essa estrutura representa a organização planejada. Os diretórios serão criados e ajustados conforme a evolução da implementação.

---

## 🤝 Padrões de colaboração

### Branches

A branch principal será `main`.

Novas funcionalidades deverão ser desenvolvidas em branches específicas, seguindo o padrão:

- `feature/nome-da-funcionalidade`
- `fix/descricao-da-correcao`
- `docs/descricao-da-documentacao`
- `chore/descricao-da-tarefa`

### Commits

Adotaremos mensagens objetivas e descritivas, preferencialmente seguindo o padrão Conventional Commits.

Exemplos:

- `feat: implementa ingestao de arquivos csv`
- `fix: corrige tratamento de mensagens vazias`
- `docs: atualiza arquitetura do projeto`
- `test: adiciona testes de analise de sentimentos`

### Pull Requests

As alterações deverão ser integradas preferencialmente por Pull Requests.

Cada Pull Request deverá apresentar:

1. Descrição da alteração.
2. Referência ao card correspondente no Trello, quando aplicável.
3. Evidências de testes realizados.
4. Informações sobre impactos em outros módulos.
5. Revisão técnica antes da integração de alterações críticas.

---

## 🔐 Segurança e proteção de credenciais

O projeto seguirá práticas básicas de segurança:

- Não armazenar senhas, tokens ou chaves de API no repositório.
- Utilizar variáveis de ambiente para informações sensíveis.
- Manter arquivos `.env` fora do controle de versão.
- Disponibilizar um `.env.example` sem valores secretos.
- Evitar publicar dados pessoais ou informações sensíveis provenientes das comunidades.
- Revisar permissões de acesso aos serviços utilizados.

---

## 📊 Gestão do projeto

O planejamento e o acompanhamento das atividades serão realizados por meio do Trello.

Cada atividade poderá ser relacionada a branches, commits e Pull Requests do GitHub, permitindo rastrear sua evolução desde o planejamento até a entrega.

A organização do trabalho considerará:

- Prioridade das atividades.
- Responsável principal.
- Dependências técnicas.
- Critérios de aceitação.
- Status de execução.
- Evidências de conclusão.

---

## 🗺️ Roadmap inicial

- [ ] Validação do escopo do MVP.
- [ ] Estruturação do repositório GitHub.
- [ ] Definição da arquitetura técnica.
- [ ] Preparação dos dados de demonstração.
- [ ] Implementação da ingestão.
- [ ] Desenvolvimento dos módulos de análise com IA.
- [ ] Implementação da geração de conteúdo.
- [ ] Desenvolvimento da interface.
- [ ] Integração com OCI Object Storage.
- [ ] Integração dos módulos e automação do fluxo.
- [ ] Testes funcionais e de integração.
- [ ] Preparação da demonstração final.

---

## 📈 Resultados esperados

Ao final do desenvolvimento, o CommunityLab deverá demonstrar a capacidade de:

- Processar interações provenientes de comunidades digitais.
- Identificar sentimentos, tópicos e informações relevantes.
- Transformar insights em conteúdos de marketing.
- Disponibilizar os resultados para revisão e curadoria.
- Executar um fluxo integrado e demonstrável utilizando os recursos definidos para o Hackathon.

---

## 📄 Licença

A licença do projeto será definida pela equipe, considerando as regras do Hackathon e a estratégia de disponibilização do código-fonte.

---

**CommunityLab — Da conversa à inteligência. Da inteligência à ação.**

Projeto desenvolvido para o Hackathon ONE G10 — Oracle Next Education & Alura.
