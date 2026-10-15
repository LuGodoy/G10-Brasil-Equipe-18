"""Módulo de orquestração de pipelines e divisão em lotes."""
from .lotes import dividir_em_lotes
from .avaliacao import avaliar_qualidade

__all__ = ["dividir_em_lotes", "avaliar_qualidade"]
