"""Módulo de armazenamento e integração com OCI Object Storage."""
from .contrato import (
    carregar_schema,
    validar_objeto_contra_schema,
    validar_interacao,
    validar_ativo,
)

__all__ = [
    "carregar_schema",
    "validar_objeto_contra_schema",
    "validar_interacao",
    "validar_ativo",
]
