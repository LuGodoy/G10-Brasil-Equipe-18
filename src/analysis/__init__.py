"""Módulo de análise de sentimentos, relevância e tópicos."""
from .classificacao import extrair_json_de_texto, classificar_interacao
from .agregacao import gerar_agregacoes

__all__ = [
    "extrair_json_de_texto",
    "classificar_interacao",
    "gerar_agregacoes",
]
