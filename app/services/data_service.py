"""Camada de dados do front.

Hoje: devolve dados fictícios (mocks).
Depois: cada função aqui vira uma chamada ao back (Python/n8n/OCI).
As telas só falam com este arquivo, então a troca não mexe nelas.

IMPORTANTE para combinar com o back: o formato dos dicionários abaixo é
PROVISÓRIO. Quem define o contrato oficial é o back.
"""
import copy
import csv
import io
import json

from mocks import mock_data as m

CAMPOS_OBRIGATORIOS = ("autor", "canal", "texto")


# ---------- Ingestão ----------
def _normalizar(itens):
    if not isinstance(itens, list) or not itens:
        raise ValueError("O arquivo precisa conter uma lista com pelo menos uma interação.")
    saida = []
    for i, item in enumerate(itens, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Interação {i}: formato inválido.")
        faltando = [c for c in CAMPOS_OBRIGATORIOS if not str(item.get(c, "")).strip()]
        if faltando:
            raise ValueError(f"Interação {i}: faltam os campos {', '.join(faltando)}.")
        saida.append({
            "autor": str(item["autor"]).strip(),
            "canal": str(item["canal"]).strip(),
            "tipo": str(item.get("tipo") or "mensagem").strip(),
            "texto": str(item["texto"]).strip(),
        })
    return saida


def interacoes_de_json(texto):
    """Aceita uma lista de interações ou um objeto com a chave 'interacoes'."""
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON inválido: {erro.msg} (linha {erro.lineno}).")
    if isinstance(dados, dict) and "interacoes" in dados:
        dados = dados["interacoes"]
    return _normalizar(dados)


def parse_interacoes(nome_arquivo, conteudo):
    """Lê um arquivo CSV ou JSON enviado no upload."""
    nome = nome_arquivo.lower()
    try:
        texto = conteudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError("Não foi possível ler o arquivo. Salve-o em UTF-8.")
    if nome.endswith(".json"):
        return interacoes_de_json(texto)
    if nome.endswith(".csv"):
        return _normalizar(list(csv.DictReader(io.StringIO(texto))))
    raise ValueError("Formato não suportado. Envie um arquivo CSV ou JSON.")


# ---------- Análise ----------
ORIGEM_ANALISE = "mock"   # "gemini" quando a análise real responde
ULTIMO_ERRO = ""          # preenchido quando a análise real falha


ULTIMO_ERRO_OCI = ""


def _storage():
    """Importa o modulo de storage; None quando indisponivel."""
    global ULTIMO_ERRO_OCI
    try:
        from . import oci_storage  # import local: evita custo quando nao usado
    except ImportError:
        try:
            from services import oci_storage  # type: ignore
        except ImportError:
            return None
    if not oci_storage.disponivel():
        return None
    return oci_storage


def _registrar_erro_oci(erro):
    global ULTIMO_ERRO_OCI
    ULTIMO_ERRO_OCI = str(erro)
    print(f"[oci] falhou: {ULTIMO_ERRO_OCI}", flush=True)


def _data_br(iso: str) -> str:
    """Converte 2026-10-22T04:05:54+00:00 em 22/10/2026 04:05."""
    texto = (iso or "").replace("T", " ")
    if len(texto) < 16:
        return texto
    data, hora = texto[:10], texto[11:16]
    partes = data.split("-")
    if len(partes) != 3:
        return texto
    return f"{partes[2]}/{partes[1]}/{partes[0]} {hora}"


def analisar(interacoes):
    """Analisa as interações com o provedor de LLM.

    Se a chave não estiver configurada ou a chamada falhar, devolve o mock
    (o protótipo continua navegável) e registra o motivo em ULTIMO_ERRO.
    """
    global ORIGEM_ANALISE, ULTIMO_ERRO
    try:
        from . import llm  # import local: evita custo quando não usado
    except ImportError:  # pragma: no cover - execução como pacote vs. script
        from services import llm  # type: ignore

    try:
        historias = llm.analisar(interacoes)
        # Analise concluida com sucesso: lista vazia tambem e resultado valido
        # (nenhuma historia elegivel no lote). O fallback mock fica reservado
        # para falha tecnica: rede, chave ausente ou resposta invalida.
        ORIGEM_ANALISE = "gemini"
        ULTIMO_ERRO = ""
        print(f"[analise] gemini OK: {len(historias)} historias", flush=True)
        return historias
    except Exception as erro:  # rede, chave ausente, JSON inválido
        ULTIMO_ERRO = str(erro)
        print(f"[analise] FALHOU -> fallback mock: {ULTIMO_ERRO}", flush=True)

    ORIGEM_ANALISE = "mock"
    return copy.deepcopy(m.HISTORIAS)


def regenerar(historia, ativo_id, vez):
    """TODO(back): pedir um novo rascunho. Aqui alterna entre variações fictícias."""
    for ativo in historia["ativos"]:
        if ativo["id"] == ativo_id:
            opcoes = [ativo["campos"]] + ativo["variacoes"]
            return dict(opcoes[vez % len(opcoes)])
    return {}


# ---------- OCI ----------
def bucket_atual():
    """Nome do bucket em uso. Sem credencial, devolve o nome do mock."""
    armazenamento = _storage()
    if armazenamento is None:
        return m.BUCKET
    try:
        return armazenamento.nome_bucket()
    except Exception:
        return m.BUCKET


def listar_pacotes():
    """Lista os pacotes realmente salvos no bucket.

    Sem credencial nao existe persistencia: a lista volta vazia, em vez de
    mostrar objetos ficticios como se estivessem gravados.
    """
    armazenamento = _storage()
    if armazenamento is None:
        return []
    try:
        itens = armazenamento.listar_pacotes()
    except Exception as erro:
        _registrar_erro_oci(erro)
        return copy.deepcopy(m.PACOTES_OCI)
    return [
        {
            "caminho": item["caminho"],
            "lote": item["lote"],
            "data": _data_br(item.get("salvo_em")),
            "tamanho": item.get("tamanho"),
            "status": "salvo",
            "persistencia": "real",
        }
        for item in itens
    ]


def salvar_no_oci(pacotes, lote_id):
    """Grava os pacotes do lote no bucket.

    O caminho e montado pelo backend a partir do lote e do nome do arquivo,
    entao repetir a gravacao sobrescreve em vez de duplicar (idempotente).
    Sem credencial, nada e gravado: o item volta como falha de simulacao.
    """
    armazenamento = _storage()
    if armazenamento is None:
        return [
            {
                **dict(pacote),
                "status": "falhou",
                "persistencia": "simulada",
                "motivo": "OCI indisponivel: credencial nao configurada",
                "data": None,
                "tamanho": None,
            }
            for pacote in pacotes
        ]

    atualizados = []
    for pacote in pacotes:
        caminho = armazenamento.caminho_do_lote(lote_id, pacote.get("caminho"))
        try:
            resultado = armazenamento.salvar_objeto(caminho, pacote)
            novo = dict(pacote)
            novo.update(
                {
                    "caminho": caminho,
                    "lote": lote_id,
                    "data": _data_br(resultado.get("salvo_em")),
                    "tamanho": resultado.get("tamanho"),
                    "status": "salvo",
                    "persistencia": "real",
                    "motivo": None,
                }
            )
        except Exception as erro:
            _registrar_erro_oci(erro)
            novo = dict(pacote)
            novo.update(
                {
                    "caminho": caminho,
                    "lote": lote_id,
                    "status": "falhou",
                    "persistencia": "real",
                    "motivo": str(erro),
                    "data": None,
                    "tamanho": None,
                }
            )
        atualizados.append(novo)
    return atualizados


def reenviar_pacote(pacote):
    """Tenta gravar de novo um pacote que falhou."""
    armazenamento = _storage()
    if armazenamento is None:
        novo = dict(pacote)
        novo.update(
            {
                "status": "falhou",
                "persistencia": "simulada",
                "motivo": "OCI indisponivel: credencial nao configurada",
                "data": None,
                "tamanho": None,
            }
        )
        return novo

    lote = pacote.get("lote") or ""
    caminho = armazenamento.caminho_do_lote(lote, pacote.get("caminho"))
    try:
        resultado = armazenamento.salvar_objeto(caminho, pacote)
    except Exception as erro:
        _registrar_erro_oci(erro)
        novo = dict(pacote)
        novo.update({"status": "falhou", "persistencia": "real", "motivo": str(erro)})
        return novo
    novo = dict(pacote)
    novo.update(
        {
            "caminho": caminho,
            "status": "salvo",
            "persistencia": "real",
            "motivo": None,
            "data": _data_br(resultado.get("salvo_em")),
            "tamanho": resultado.get("tamanho"),
        }
    )
    return novo


def conteudo_pacote(caminho):
    """Le o JSON de um objeto do bucket. Sem credencial, devolve o mock."""
    armazenamento = _storage()
    if armazenamento is not None:
        try:
            conteudo = armazenamento.ler_objeto(str(caminho))
            if conteudo is not None:
                return conteudo
        except Exception as erro:
            _registrar_erro_oci(erro)

    if caminho.endswith("evidencias.json"):
        return {
            "lote": "DEMO-001",
            "evidencias": [
                {"autor": h["autor"], "canal": h["canal"],
                 "mensagem_original": h["mensagem_original"], "citacoes": h["destaques"], "fatos": h["fatos"]}
                for h in m.HISTORIAS
            ],
        }
    return {
        "status": "sucesso",
        "lote": "DEMO-001",
        "gravado_em": "2026-10-15T14:32:00-03:00",
        "historias": [
            {"autor": h["autor"], "categoria": h["categoria"], "relevancia": h["relevancia"],
             "citacao": h["destaques"][0],
             "ativos": {a["id"]: {"status": "rascunho_aguardando_revisao"} for a in h["ativos"]}}
            for h in m.HISTORIAS
        ],
    }
