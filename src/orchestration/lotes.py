"""Módulo de divisão em lotes e controle de processamento.

Responsável por segmentar grandes volumes de interações em lotes menores 
para otimizar chamadas e gerenciar o fluxo operacional.
"""
from typing import List, Dict, Any

def dividir_em_lotes(interacoes: List[Dict[str, Any]], tamanho_lote: int = 50) -> List[List[Dict[str, Any]]]:
    """Divide uma lista de interações em lotes menores com base no tamanho configurado."""
    if tamanho_lote <= 0:
        raise ValueError("O tamanho do lote deve ser maior que zero.")
    
    if not interacoes:
        return []

    return [interacoes[i:i + tamanho_lote] for i in range(0, len(interacoes), tamanho_lote)]