# CommunityLab · Front-end (Streamlit)

Interface do CommunityLab, feita em Streamlit. Por enquanto ela funciona sozinha, com **dados fictícios**, para o time poder ver e validar o fluxo antes de o back ficar pronto.

> Todos os nomes, mensagens e depoimentos do front são inventados. Nada aqui representa pessoas reais.

## Identidade Visual

O CommunityLab usa um estilo híbrido **SaaS corporativo + IA**, com visual limpo, profissional e acessível.

### Paleta de cores

| Cor | Código | Uso |
|---|---|---|
| **Azul-marinho** | `#101B32` | Sidebar e navegação |
| **Violeta** | `#7C3AED` | Cor primária, ações de IA e destaques |
| **Ciano** | `#22D3EE` | Detalhes tecnológicos (SOMENTE sobre fundo escuro) |
| **Branco-neutro** | `#F8FAFC` | Fundo da área de trabalho |
| **Verde** | `#10B981` (fundos) / `#047857` (textos) | Sucesso e aprovação |
| **Texto principal** | `#0F172A` | Títulos e conteúdo principal |
| **Texto secundário** | `#64748B` | Labels, legendas e informações auxiliares |
| **Borda suave** | `#E2E8F0` | Bordas de cards e divisores |

### Regras de contraste

- Todos os pares texto/fundo seguem **WCAG AA** (4.5:1 para texto normal, 3:1 para texto grande)
- Verde `#047857` é usado para **texto sobre fundo claro** (legibilidade garantida)
- Ciano `#22D3EE` aparece **apenas sobre azul-marinho** (nunca sobre fundo claro)
- Sidebar escura: texto claro `#F8FAFC` sobre azul-marinho `#101B32`

### Tipografia

- **Fonte:** Inter (pesos 400, 500, 600, 700)
- **Tom:** Natural, direto, sem jargão técnico excessivo
- **Slogan:** "Histórias reais. Impacto inteligente."

### Componentes

- **Cards:** Fundo branco com borda `#E2E8F0`, cantos arredondados (10px)
- **Botões:** Estados normal, hover e ativo com transições suaves
- **Chips:** Cores semânticas (verde = sucesso, amarelo = pendente, vermelho = erro, roxo = IA)
- **Sidebar:** Azul-marinho com destaque violeta no item ativo

## O que o front faz

O fluxo tem 6 módulos, organizados no menu lateral:

| Módulo | O que acontece |
|---|---|
| **Dashboard** | Visão geral com KPIs (interações, histórias, ativos gerados) e ações rápidas para navegar |
| **Importação** | Upload de CSV/JSON ou JSON colado, com prévia das interações e filtro por canal. Botão "Importar interações" dá início ao processamento |
| **Histórias** | Lista as histórias detectadas com categoria, relevância e trecho original. Filtros por categoria e relevância mínima. Botão "Ver no Estúdio" para cada história |
| **Estúdio de Conteúdo** | Visualização lado a lado de evidências e rascunhos. Coluna esquerda: mensagem original com destaques, fatos extraídos. Coluna direita: conteúdo editável (Testemunho estruturado ou Case de sucesso), contador de caracteres, seção "Fontes deste conteúdo" com rastreabilidade, botões Regenerar, Copiar e Enviar para curadoria |
| **Curadoria** | Revisa os rascunhos com três controles independentes: (1) Validação factual (Pendente, Validada, Evidências insuficientes, Contradição não resolvida), (2) Curadoria editorial (Rascunho, Ajustes solicitados, Aprovado, Rejeitado), (3) Autorização de publicação (Não registrada, Registrada). A autorização NÃO bloqueia a aprovação editorial. Regra RG-02: com "Contradição não resolvida", o botão Aprovar fica desabilitado. Regra RG-03: "Liberado para publicação" aparece apenas quando Validada + Aprovado + Registrada. O sistema nunca publica automaticamente |
| **Histórico** | Lista os pacotes salvos no bucket OCI, com visualização do JSON e download |

**Fluxo de trabalho:**
1. **Importar** → carregar interações da comunidade
2. **Processar** → análise automática (transição entre Importação e Histórias)
3. **Revisar** → explorar histórias e editar rascunhos no Estúdio
4. **Decidir** → validar, aprovar ou rejeitar na Curadoria
5. **Consultar** → verificar pacotes salvos no Histórico

**Regras de Curadoria (conforme CQF):**
- **Três controles independentes:** Validação factual, Curadoria editorial e Autorização de publicação funcionam de forma separada
- **RG-01:** A interface nunca preenche lacunas com informação inventada. "Regenerar" apenas alterna entre variações fictícias baseadas nas evidências
- **RG-02:** Com "Contradição não resolvida", o botão Aprovar fica desabilitado até que a contradição seja resolvida ou a validação seja alterada
- **RG-03:** O indicador "Liberado para publicação" aparece apenas quando os três controles estão completos: Validação = Validada, Curadoria = Aprovado, Autorização = Registrada
- **Autorização não bloqueia aprovação:** É possível aprovar editorialmente um ativo mesmo sem autorização registrada (útil para análise interna)
- **Nada é publicado automaticamente:** Mesmo com "Liberado para publicação", o sistema não publica. A decisão final é do time

**Princípio do produto:** a IA sugere, o time decide. Nada é publicado automaticamente, e cada ativo gerado aponta para a mensagem original.

## Como rodar

Pré-requisito: Python 3.10 ou superior.

```bash
pip install -r requirements-front.txt
streamlit run app/main.py
```

No Windows, se `streamlit` não for reconhecido:

```bash
python -m streamlit run app/main.py
```

O app abre em `http://localhost:8501`.

## Modo demonstração

Na barra lateral, em **Modo demonstração**, dá para:

- simular erro ao salvar no OCI (mostra a tela de falha e o botão "Tentar novamente");
- alternar a tela de Histórico entre os estados normal, vazio, carregando e erro de conexão;
- reiniciar a demonstração.

Para acelerar ou desacelerar a simulação do Processamento, use a variável `COMMUNITYLAB_DELAY` (segundos por etapa).

## Estrutura de pastas

```
app/
  main.py                    entrada do app, menu lateral e roteamento
  state.py                   estado da sessão
  styles.py                  CSS e helpers de HTML
  telas/                     uma tela por arquivo
    dashboard.py             (nova) visão geral do sistema
    importacao.py            (era ingestao.py) upload de interações
    processamento.py
    historias.py
    estudio.py               (nova) placeholder para ETAPA 3
    curadoria.py
    historico.py             (era oci.py) consulta de pacotes salvos
  services/
    data_service.py          ÚNICO ponto de contato com os dados
  mocks/
    mock_data.py             dados fictícios
.streamlit/
  config.toml                tema (cores)
requirements-front.txt
```

## Como o back se conecta (importante)

As telas **não** importam o back diretamente. Elas só chamam funções do arquivo `app/services/data_service.py`. Hoje essas funções devolvem dados fictícios. Quando o back estiver pronto, basta trocar o corpo delas por chamadas reais, e as telas continuam iguais.

Procure por `TODO(back)` no arquivo para achar os pontos de integração:

| Função | O que o back precisa fazer |
|---|---|
| `analisar(interacoes)` | Receber as interações e devolver as histórias detectadas com os ativos gerados |
| `regenerar(historia, ativo_id, vez)` | Gerar um novo rascunho para um ativo |
| `listar_pacotes()` | Listar os objetos do bucket no OCI Object Storage |
| `salvar_no_oci(pacotes, lote_id)` | Gravar o pacote no OCI. **Precisa ser idempotente**: tentar de novo não pode duplicar resultados |
| `reenviar_pacote(pacote)` | Tentar gravar de novo um pacote que falhou |
| `conteudo_pacote(caminho)` | Ler o JSON de um objeto do bucket |

### Formato provisório dos dados

O formato abaixo é o que o front usa **hoje**. Ele é só um ponto de partida e **pode mudar**: quem define o contrato oficial é o back, e o time deve decidir em conjunto.

Interação (entrada):

```json
{ "autor": "Marina Costa", "canal": "#conquistas", "tipo": "mensagem", "texto": "..." }
```

História detectada (saída):

```json
{
  "id": "hist-001",
  "autor": "Marina Costa",
  "canal": "#conquistas",
  "categoria": "Conquista profissional",
  "sentimento": "Positivo",
  "relevancia": 96,
  "relevancia_nivel": "alta",
  "mensagem_original": "...",
  "citacoes": [{ "texto": "trecho literal do original", "id_interacao": 1 }],
  "interacoes_origem": [1],
  "destaques": ["trecho da mensagem usado no rascunho"],
  "fatos": ["Conquista: primeira vaga como dev júnior"],
  "ativos": [
    { "id": "post_linkedin", "nome": "Post para LinkedIn", "tipo": "texto", "campos": { "texto": "..." } },
    { "id": "card_conquista", "nome": "Card de conquista", "tipo": "card", "campos": { "titulo": "...", "frase": "..." } }
  ]
}
```

Campos novos (aditivos, outubro/2026):

- `citacoes` — cada trecho de prova com o `id_interacao` de origem. O trecho é recortado do texto original, não copiado do modelo; se não existir literalmente no original, é descartado.
- `interacoes_origem` — lista de ids das interações que sustentam a história.
- `relevancia_nivel` — faixa derivada da numérica: `alta` (85+), `media` (60 a 84) e `baixa` (abaixo de 60).
- `destaques` passa a ser derivado das citações validadas, então o destaque em negrito na tela sempre corresponde a texto que existe na mensagem.

Pacote salvo no OCI (listagem):

```json
{ "caminho": "ativos/demo-001/pacote-distribuicao.json", "lote": "DEMO-001",
  "data": "15/10/2026 14:32", "tamanho": "2,4 KB", "status": "salvo" }
```

## Pontos para alinhar com o back

- **Tipos de ativo:** o front agora usa Testemunho estruturado (título + descrição + citação) e Case de sucesso (texto narrativo). Confirmar se o back vai gerar nesse formato.
- **Rastreabilidade:** o front espera um campo `fontes` em cada ativo, com a estrutura: `[{"afirmacao": "...", "fato": "...", "trecho": "..."}]`. Alinhar formato com o back.
- Se o campo `tipo` da interação vai ser preenchido e com quais valores.
- O que o pacote salvo no OCI deve conter. Hoje o JSON de exemplo só tem o status dos ativos. O ideal é guardar também o texto gerado, as citações com a mensagem de origem e se a autorização foi confirmada.
- Se o status de aprovação ou rejeição feito na Curadoria deve ser atualizado no bucket e como.
- **Fluxo:** o front agora tem Histórias → Estúdio → Curadoria. Confirmar se o back segue essa sequência.

## Limitações conhecidas do protótipo

- A análise sempre devolve as 3 histórias fictícias, mesmo que você envie outro arquivo (o arquivo é validado e aparece na prévia, mas não é analisado).
- Aprovar ou rejeitar só vale durante a sessão e não grava em lugar nenhum.
- "Copiar texto" mostra um bloco com ícone de copiar, porque o Streamlit não acessa a área de transferência.
- Testado no Streamlit 1.66. O `requirements-front.txt` pede `>=1.37`.
- Tipos de ativo disponíveis: Testemunho estruturado (título + descrição + citação) e Case de sucesso (texto narrativo completo).

## Como contribuir no front

1. Para mudar um texto ou visual de uma tela, edite o arquivo dela em `app/telas/`.
2. Para mudar os dados de exemplo, edite `app/mocks/mock_data.py`.
3. Para conectar o back, edite só `app/services/data_service.py`.
4. Não misture os mocks do front com a pasta de dados de demonstração do back.

## Como executar no Windows

1. Abra o Prompt de Comando ou PowerShell.
2. Navegue até a pasta do projeto:
   ```bash
   cd "c:\Users\communitylab-front\communitylab-front"
   ```
3. Ative o ambiente virtual (se existir):
   ```bash
   .\.venv\Scripts\Activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements-front.txt
   ```
5. Execute o aplicativo:
   ```bash
   streamlit run app/main.py
   ```
