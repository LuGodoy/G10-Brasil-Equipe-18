"""Módulo de geração de ativos de conteúdo (testemunhos, cases e posts LinkedIn)."""
from ..modelos import AtivoGerado
from ..storage.contrato import validar_ativo

__all__ = ["AtivoGerado", "validar_ativo"]
