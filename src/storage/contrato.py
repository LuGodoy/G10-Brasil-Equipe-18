"""Módulo de validação de contratos e esquemas JSON.

Responsável por fornecer funções utilitárias para validar interações,
lotes e ativos gerados contra os JSON Schemas oficiais do CommunityLab.
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from jsonschema import Draft202012Validator, FormatChecker

def carregar_schema(caminho_schema: str) -> Dict[str, Any]:
    """Carrega um arquivo JSON Schema a partir do caminho informado."""
    return json.loads(Path(caminho_schema).read_text(encoding="utf-8"))

def validar_objeto_contra_schema(objeto: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Valida um objeto arbitrário contra um JSON Schema específico.
    Retorna uma tupla (valido: bool, lista_de_erros: List[str]).
    """
    validador = Draft202012Validator(schema, format_checker=FormatChecker())
    erros = [f"{'/'.join(map(str, e.path)) or '(raiz)'}: {e.message}" for e in validador.iter_errors(objeto)]
    
    return len(erros) == 0, erros

def validar_interacao(interacao: Dict[str, Any], schema_interacao: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Valida especificamente uma interação contra o interacao.schema.json."""
    return validar_objeto_contra_schema(interacao, schema_interacao)

def validar_ativo(ativo: Dict[str, Any], schema_ativo: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Valida especificamente um ativo gerado contra o ativo_gerado.schema.json."""
    return validar_objeto_contra_schema(ativo, schema_ativo)