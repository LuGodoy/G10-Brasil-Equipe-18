"""Conversão da história do app para o contrato de História Detectada.

O app monta a história no formato que as telas consomem (autor, canal,
mensagem_original, ativos). O contrato do pipeline espera outro conjunto de
campos: `schemas/historia_detectada.json`.

Este módulo faz só a ponte entre os dois. Ele não decide o que é história, não
chama modelo, não grava e não julga citação: isso fica na detecção, na geração e
na RG-01, cada um no seu lugar.

Regras seguidas (docs/architecture/docs_data_ml/AGENTS.md):

- função pura: recebe dicionário, devolve dicionário;
- sem Streamlit, sem SDK da OCI, sem variável de ambiente, sem print;
- o schema não é alterado nem contornado: o objeto é validado contra ele, e o
  que não fecha volta como recusa com o motivo, nunca corrigido em silêncio;
- a validação reutiliza `src.storage.contrato`, que o guia do módulo libera para
  qualquer módulo usar.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..storage.contrato import validar_historia

VERSAO_HISTORIA = "1.1"
AUTORIZACAO_PADRAO = "pendente"
STATUS_REVISAO_PADRAO = "pendente"

PADRAO_ID = re.compile(r"^historia_[0-9]{3,}$")

Recusa = Tuple[Optional[Dict[str, Any]], List[str], List[str]]


def _texto(valor: Any) -> str:
    return " ".join(str(valor or "").split())


def _lista_texto(valor: Any) -> List[str]:
    if not isinstance(valor, (list, tuple)):
        return []
    return [str(item).strip() for item in valor if str(item).strip()]


def _lista_inteiro(valor: Any) -> List[int]:
    if not isinstance(valor, (list, tuple)):
        return []
    ids: List[int] = []
    for item in valor:
        try:
            numero = int(item)
        except (TypeError, ValueError):
            continue
        if numero >= 1 and numero not in ids:
            ids.append(numero)
    return ids


def _citacoes(valor: Any) -> List[Dict[str, Any]]:
    if not isinstance(valor, (list, tuple)):
        return []
    saida = []
    for item in valor:
        if not isinstance(item, dict):
            continue
        saida.append(
            {
                "texto": _texto(item.get("texto")),
                "id_interacao": item.get("id_interacao"),
            }
        )
    return saida


def id_historia(valor: Any, sequencia: int, avisos: List[str]) -> str:
    """Id no padrão `historia_###`.

    O id do app (`hist-7`) é reaproveitado quando tem número. Quando não tem,
    o id é gerado pela posição no lote — e o ajuste vai para os avisos.
    """
    bruto = str(valor or "").strip()
    if PADRAO_ID.match(bruto):
        return bruto

    numeros = re.findall(r"[0-9]+", bruto)
    if numeros:
        numero = int(numeros[-1])
        if numero >= 1:
            gerado = f"historia_{numero:03d}"
            avisos.append(f"id_historia gerado a partir de {bruto!r}: {gerado}.")
            return gerado

    gerado = f"historia_{max(int(sequencia), 1):03d}"
    avisos.append(
        f"id_historia sem numero em {bruto!r}: gerado {gerado} pela posicao no lote."
    )
    return gerado


def converter_historia(
    historia: Any,
    schema: Dict[str, Any],
    sequencia: int = 1,
) -> Recusa:
    """Converte a história do app para o contrato e valida contra o schema.

    Devolve `(historia_do_contrato, motivos, avisos)`:
    - `motivos` vazio = convertida e válida;
    - `motivos` preenchido = não entrou, e o primeiro item é `None`;
    - `avisos` registra o que foi derivado (id gerado, por exemplo).
    """
    avisos: List[str] = []

    if not isinstance(historia, dict):
        return None, ["Historia em formato invalido: esperado um objeto."], avisos

    dados: Dict[str, Any] = {
        "versao_schema": VERSAO_HISTORIA,
        "id_historia": id_historia(
            historia.get("id_historia") or historia.get("id"), sequencia, avisos
        ),
        "tipo": historia.get("tipo"),
        "resumo": _texto(historia.get("resumo")),
        "interacoes_origem": _lista_inteiro(historia.get("interacoes_origem")),
        "fatos": _lista_texto(historia.get("fatos")),
        "resultados": _lista_texto(historia.get("resultados")),
        "citacoes": _citacoes(historia.get("citacoes")),
        "autorizacao_divulgacao": (
            historia.get("autorizacao_divulgacao") or AUTORIZACAO_PADRAO
        ),
        "status_revisao": historia.get("status_revisao") or STATUS_REVISAO_PADRAO,
    }

    confianca = historia.get("confianca")
    if isinstance(confianca, (int, float)) and not isinstance(confianca, bool):
        dados["confianca"] = float(confianca)

    valido, erros = validar_historia(dados, schema)
    if not valido:
        return None, list(erros), avisos

    return dados, [], avisos


def converter_lote(
    historias: Sequence[Any],
    schema: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    """Converte a lista inteira.

    Devolve `(convertidas, recusadas, avisos)`. Recusada guarda o id de origem e
    o motivo, para nada sumir sem explicação.
    """
    convertidas: List[Dict[str, Any]] = []
    recusadas: List[Dict[str, Any]] = []
    avisos: List[str] = []

    for posicao, historia in enumerate(historias or [], start=1):
        convertida, motivos, avisos_item = converter_historia(historia, schema, posicao)
        avisos.extend(avisos_item)
        if convertida is None:
            origem = historia.get("id") if isinstance(historia, dict) else None
            recusadas.append({"id": origem, "motivo": "; ".join(motivos)})
            continue
        convertidas.append(convertida)

    return convertidas, recusadas, avisos
