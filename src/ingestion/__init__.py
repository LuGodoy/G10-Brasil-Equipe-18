"""Módulo de ingestão de dados (CSV, JSON e DataFrames)."""
from .leitura import ler_arquivo_bytes
from .ingestion import (
    pseudonimizar_autor,
    processar_json,
    processar_csv,
    processar_dataframe,
    interacoes_para_dataframe,
)

__all__ = [
    "ler_arquivo_bytes",
    "pseudonimizar_autor",
    "processar_json",
    "processar_csv",
    "processar_dataframe",
    "interacoes_para_dataframe",
]
