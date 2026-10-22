"""Análise de interações com provedor de LLM (Gemini).

Substitui o mock de `data_service.analisar()` por uma chamada real.

Contrato de saída (mesmo formato que as telas já consomem):
{
  "id", "autor", "iniciais", "canal", "origem", "categoria",
  "sentimento", "relevancia", "mensagem_original", "destaques",
  "fatos", "ativos": [{"id", "nome", "tipo", "campos", "variacoes"?}]
}

A chave é lida de st.secrets["GEMINI_API_KEY"] ou da variável de ambiente
GEMINI_API_KEY. Nunca fica no código.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata

import requests

MODELO_PADRAO = "gemini-3.8-flash"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

PROMPT = """Você analisa mensagens de uma comunidade online para encontrar histórias com potencial de conteúdo.

Receberá uma lista de interações em JSON, cada uma com "autor", "canal", "tipo" e "texto".

Sua tarefa:
1. Selecionar até {maximo} interações que contenham uma história real, um problema concreto ou uma conquista verificável.
2. Para cada uma, descrever a categoria, o sentimento e o quanto ela serve como conteúdo (relevância de 0 a 100).
3. Gerar dois ativos: um post para LinkedIn e um card de conquista.

Responda SOMENTE com JSON válido, neste formato exato:
{{
  "historias": [
    {{
      "id": "hist-001",
      "indice_interacao": 1,
      "autor": "nome do autor da interação",
      "canal": "canal da interação",
      "categoria": "categoria curta, ex: Conquista profissional",
      "sentimento": "Positivo | Negativo | Neutro",
      "relevancia": 0,
      "mensagem_original": "texto original, sem alterar",
      "destaques": ["trechos literais da mensagem"],
      "fatos": ["fato objetivo extraído, no formato Tema: detalhe"],
      "ativos": [
        {{
          "id": "post_linkedin",
          "nome": "Post para LinkedIn",
          "tipo": "texto",
          "campos": {{"texto": "post de até 120 palavras, português do Brasil, sem emoji, sem hashtag"}}
        }},
        {{
          "id": "card_conquista",
          "nome": "Card de conquista",
          "tipo": "card",
          "campos": {{"titulo": "até 60 caracteres", "frase": "uma frase de até 90 caracteres"}}
        }}
      ]
    }}
  ]
}}

Regras obrigatórias:
- Use apenas informação presente nas interações. Não invente nome, número ou fato.
- "indice_interacao" é a posição da interação no lote recebido, começando em 1.
- "destaques" deve conter trechos copiados do texto original, sem reescrever.
- Se nenhuma interação tiver potencial, devolva {{"historias": []}}.
- Não escreva nada antes ou depois do JSON.
"""


class ErroAnalise(RuntimeError):
    """Falha controlada na análise por LLM."""


def _chave() -> str:
    chave = ""
    try:
        import streamlit as st  # import local: o teste roda fora do Streamlit

        chave = st.secrets.get("GEMINI_API_KEY", "")  # type: ignore[union-attr]
    except Exception:
        chave = ""
    chave = chave or os.environ.get("GEMINI_API_KEY", "")
    if not chave:
        raise ErroAnalise(
            "Chave do Gemini ausente. Defina GEMINI_API_KEY em .streamlit/secrets.toml "
            "ou como variável de ambiente."
        )
    return chave.strip()


def _modelo() -> str:
    try:
        import streamlit as st

        return st.secrets.get("GEMINI_MODEL", MODELO_PADRAO) or MODELO_PADRAO
    except Exception:
        return os.environ.get("GEMINI_MODEL", MODELO_PADRAO) or MODELO_PADRAO


def _iniciais(nome: str) -> str:
    partes = [p for p in re.split(r"\s+", (nome or "").strip()) if p]
    if not partes:
        return "?"
    if len(partes) == 1:
        return partes[0][:2].upper()
    return (partes[0][0] + partes[-1][0]).upper()



def _colapsar(texto: str) -> str:
    """Reduz sequencias de espaco/quebra de linha a um espaco simples."""
    return re.sub(r"\s+", " ", (texto or "").strip())


def _achatado_com_mapa(texto: str):
    """Normaliza para comparacao (sem acento, minusculo, espaco simples).

    Devolve tambem o indice de cada caractere no texto original, para o
    recorte final sair do original com acento e caixa preservados.
    """
    achatado = []
    mapa = []
    anterior_espaco = True
    for i, ch in enumerate(texto or ""):
        if ch.isspace():
            if anterior_espaco:
                continue
            achatado.append(" ")
            mapa.append(i)
            anterior_espaco = True
            continue
        base = unicodedata.normalize("NFKD", ch)
        sem_acento = "".join(c for c in base if not unicodedata.combining(c))
        for c in sem_acento.lower():
            achatado.append(c)
            mapa.append(i)
        anterior_espaco = False
    while achatado and achatado[-1] == " ":
        achatado.pop()
        mapa.pop()
    return "".join(achatado), mapa


def _localizar(original: str, trecho: str):
    """Devolve o trecho como ele aparece no texto original, ou None.

    A comparacao ignora espaco, acento e maiuscula/minuscula. O valor
    devolvido e sempre o recorte do original, entao a citacao continua
    literal -- o que muda e so a tolerancia ao procurar.
    """
    if not original or not trecho:
        return None
    alvo = _colapsar(trecho)
    if not alvo:
        return None
    alvo_achatado, _ = _achatado_com_mapa(alvo)
    if not alvo_achatado:
        return None

    normalizado, mapa = _achatado_com_mapa(original)
    for candidato in (alvo_achatado, alvo_achatado.strip(".,;:!?'\"()[]")):
        if not candidato:
            continue
        posicao = normalizado.find(candidato)
        if posicao == -1:
            continue
        inicio_trecho = mapa[posicao]
        fim_trecho = mapa[posicao + len(candidato) - 1] + 1
        return original[inicio_trecho:fim_trecho]
    return None

def _nivel_relevancia(valor: int) -> str:
    if valor >= 85:
        return "alta"
    if valor >= 60:
        return "media"
    return "baixa"


def _normalizar(historias: list, interacoes: list) -> list:
    """Garante o contrato esperado pelas telas, sem confiar cegamente no modelo."""
    indice = {}
    por_posicao = {}
    for posicao, item in enumerate(interacoes, start=1):
        # O id vem do lote quando existir; senao, usa a posicao para referencia.
        item = dict(item)
        id_lote = item.get("id")
        item["_id"] = id_lote if isinstance(id_lote, int) and id_lote >= 1 else posicao
        indice[(item.get("autor"), item.get("texto"))] = item
        por_posicao[posicao] = item

    saida = []
    for n, hist in enumerate(historias, start=1):
        if not isinstance(hist, dict):
            continue
        autor = str(hist.get("autor") or "").strip()
        original = str(hist.get("mensagem_original") or "").strip()
        base = indice.get((autor, original)) or {}
        try:
            posicao_informada = int(hist.get("indice_interacao") or 0)
        except (TypeError, ValueError):
            posicao_informada = 0
        if posicao_informada in por_posicao and (
            por_posicao[posicao_informada].get("autor") == autor
            or _colapsar(por_posicao[posicao_informada].get("texto", "")) == _colapsar(original)
        ):
            base = por_posicao[posicao_informada]
        canal = str(hist.get("canal") or base.get("canal") or "")
        texto_fonte = str(base.get("texto") or original)
        id_interacao = int(base.get("_id") or posicao_informada or 0)

        ativos = []
        for ativo in hist.get("ativos") or []:
            if not isinstance(ativo, dict) or not ativo.get("id"):
                continue
            campos = ativo.get("campos") or {}
            if not isinstance(campos, dict) or not any(str(v).strip() for v in campos.values()):
                continue
            ativos.append(
                {
                    "id": str(ativo["id"]),
                    "nome": str(ativo.get("nome") or ativo["id"]),
                    "tipo": str(ativo.get("tipo") or "texto"),
                    "campos": {str(k): str(v) for k, v in campos.items()},
                    **({"variacoes": ativo["variacoes"]} if ativo.get("variacoes") else {}),
                }
            )

        if not autor or not original or not ativos:
            continue

        try:
            relevancia = int(float(hist.get("relevancia", 0)))
        except (TypeError, ValueError):
            relevancia = 0

        # Citacoes: cada trecho apontado pelo modelo e conferido contra o texto
        # original. Se nao existir literalmente, e descartado (nao inventamos).
        citacoes = []
        vistos = set()
        for destaque in hist.get("destaques") or []:
            recorte = _localizar(texto_fonte, str(destaque))
            # O contrato do pipeline limita a citacao a 500 caracteres.
            if recorte and len(recorte) > 500:
                recorte = recorte[:500].rsplit(" ", 1)[0] or recorte[:500]
            if not recorte or recorte.lower() in vistos:
                continue
            vistos.add(recorte.lower())
            citacoes.append({"texto": recorte, "id_interacao": id_interacao})

        relevancia_final = max(0, min(100, relevancia))
        saida.append(
            {
                "id": str(hist.get("id") or f"hist-{n:03d}"),
                "autor": autor,
                "iniciais": _iniciais(autor),
                "canal": canal,
                "origem": str(hist.get("origem") or "Mensagem da comunidade"),
                "categoria": str(hist.get("categoria") or "História da comunidade"),
                "sentimento": str(hist.get("sentimento") or "Neutro"),
                "relevancia": relevancia_final,
                "relevancia_nivel": _nivel_relevancia(relevancia_final),
                "mensagem_original": original,
                "citacoes": citacoes,
                "interacoes_origem": [id_interacao] if id_interacao else [],
                "destaques": [c["texto"] for c in citacoes],
                "fatos": [str(f) for f in (hist.get("fatos") or []) if str(f).strip()],
                "ativos": ativos,
            }
        )
    return saida


def analisar(interacoes: list, maximo: int = 3, timeout: int = 60) -> list:
    """Envia as interações ao Gemini e devolve as histórias no contrato do front."""
    if not interacoes:
        raise ErroAnalise("Nenhuma interação para analisar.")

    payload = [
        {
            "autor": i.get("autor", ""),
            "canal": i.get("canal", ""),
            "tipo": i.get("tipo", "mensagem"),
            "texto": i.get("texto", ""),
        }
        for i in interacoes
    ]

    corpo = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT.format(maximo=maximo)},
                    {"text": json.dumps(payload, ensure_ascii=False)},
                ]
            }
        ],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.4},
    }

    resposta = requests.post(
        ENDPOINT.format(modelo=_modelo()),
        params={"key": _chave()},
        json=corpo,
        timeout=timeout,
    )

    if resposta.status_code != 200:
        raise ErroAnalise(f"Gemini respondeu {resposta.status_code}: {resposta.text[:300]}")

    try:
        dados = resposta.json()
        texto = dados["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, ValueError) as erro:
        raise ErroAnalise(f"Resposta inesperada do Gemini: {erro}") from erro

    try:
        conteudo = json.loads(texto)
    except json.JSONDecodeError as erro:
        raise ErroAnalise(f"O modelo não devolveu JSON válido: {erro}") from erro

    historias = conteudo.get("historias") if isinstance(conteudo, dict) else conteudo
    if not isinstance(historias, list):
        raise ErroAnalise("JSON do modelo sem a chave 'historias'.")

    return _normalizar(historias, interacoes)
