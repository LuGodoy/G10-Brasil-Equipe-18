"""Módulo de detecção de histórias de sucesso, conquistas e relatos de superação."""
from typing import List, Dict, Any
from ..modelos import HistoriaDetectada

def filtrar_candidatos_historia(interacoes_analisadas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filtra interações que possuem alto potencial de história ou conquista."""
    candidatos = []
    for item in interacoes_analisadas:
        analise = item.get("analise", {})
        if not analise:
            continue
        tipo = analise.get("tipo_insight")
        relevancia = analise.get("relevancia")
        if tipo in ("conquista", "historia") and relevancia in ("alta", "media"):
            candidatos.append(item)
    return candidatos

__all__ = ["HistoriaDetectada", "filtrar_candidatos_historia"]
