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
from datetime import datetime, timezone

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
        motivo = ""
        if hasattr(oci_storage, "motivo_indisponivel"):
            motivo = oci_storage.motivo_indisponivel()
        ULTIMO_ERRO_OCI = motivo or "OCI indisponivel: credencial nao configurada"
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
def erro_armazenamento():
    """Motivo da ultima falha de armazenamento (vazio quando nao houve)."""
    return ULTIMO_ERRO_OCI


def bucket_atual():
    """Nome do bucket em uso. Vazio quando nao ha acesso a OCI."""
    armazenamento = _storage()
    if armazenamento is None:
        return ""
    try:
        return armazenamento.nome_bucket()
    except Exception:
        return ""


def listar_pacotes():
    """Lista os pacotes realmente salvos no bucket.

    Sem credencial nao existe persistencia: a lista volta vazia, em vez de
    mostrar objetos ficticios como se estivessem gravados.
    """
    global ULTIMO_ERRO_OCI
    armazenamento = _storage()
    if armazenamento is None:
        ULTIMO_ERRO_OCI = ULTIMO_ERRO_OCI or "OCI indisponivel: credencial nao configurada"
        return []
    ULTIMO_ERRO_OCI = ""
    try:
        itens = armazenamento.listar_pacotes()
    except Exception as erro:
        # Falha operacional fica visivel: lista vazia + motivo registrado.
        _registrar_erro_oci(erro)
        return []
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


def salvar_no_oci(pacotes, lote_id, historias=None):
    """Grava os pacotes do lote no bucket.

    O caminho e montado pelo backend a partir do lote e do nome do arquivo,
    entao repetir a gravacao sobrescreve em vez de duplicar (idempotente).
    Sem credencial, nada e gravado: o item volta como falha de simulacao.
    Sem conteudo, nada e gravado: o item volta como falha, para nao salvar
    um arquivo apenas com metadados.
    """
    if historias is None:
        return [
            {
                **dict(pacote),
                "status": "falhou",
                "persistencia": "nenhuma",
                "motivo": "Sem conteudo para gravar: a analise nao foi informada",
                "data": None,
                "tamanho": None,
            }
            for pacote in pacotes
        ]

    if not isinstance(historias, (list, tuple)):
        return [
            {
                **dict(pacote),
                "status": "falhou",
                "persistencia": "nenhuma",
                "motivo": "Conteudo em formato invalido: esperada uma lista de historias",
                "data": None,
                "tamanho": None,
            }
            for pacote in pacotes
        ]

    # lista vazia e resultado valido: o lote foi processado e nao havia
    # historias elegiveis. Nao e falha tecnica.
    historias = list(historias)

    conteudo = {
        "versao_schema": "1.0",
        "lote": lote_id,
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "origem_analise": ORIGEM_ANALISE,
        "historias": historias,
        "evidencias": [
            {"id_interacao": c.get("id_interacao"), "texto": c.get("texto")}
            for h in historias
            for c in (h.get("citacoes") or [])
        ],
    }

    armazenamento = _storage()
    if armazenamento is None:
        return [
            {
                **dict(pacote),
                "status": "falhou",
                "persistencia": "simulada",
                "motivo": ULTIMO_ERRO_OCI or "OCI indisponivel: credencial nao configurada",
                "data": None,
                "tamanho": None,
            }
            for pacote in pacotes
        ]

    atualizados = []
    for pacote in pacotes:
        caminho = armazenamento.caminho_do_lote(lote_id, pacote.get("caminho"))
        try:
            if "evidencia" in caminho:
                dados = {
                    "versao_schema": "1.0",
                    "lote": lote_id,
                    "gerado_em": conteudo["gerado_em"],
                    "evidencias": conteudo["evidencias"],
                }
            else:
                dados = conteudo
            resultado = armazenamento.salvar_objeto(caminho, dados)
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
                "motivo": ULTIMO_ERRO_OCI or "OCI indisponivel: credencial nao configurada",
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
    """Le o JSON de um objeto do bucket.

    Devolve None quando o objeto nao existe ou a leitura falha -- nunca um
    conteudo ficticio com aparencia de sucesso.
    """
    armazenamento = _storage()
    if armazenamento is None:
        global ULTIMO_ERRO_OCI
        ULTIMO_ERRO_OCI = ULTIMO_ERRO_OCI or "OCI indisponivel: credencial nao configurada"
        return None
    try:
        return armazenamento.ler_objeto(str(caminho))
    except Exception as erro:
        _registrar_erro_oci(erro)
        return None
