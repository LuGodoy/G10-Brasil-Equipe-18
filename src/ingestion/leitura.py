"""Módulo de leitura de arquivos com tratamento de encoding e fallbacks.

Responsável por converter bytes em texto de forma segura, sem levantar exceções.
"""
import unicodedata
from typing import Tuple, List

def ler_arquivo_bytes(conteudo_bytes: bytes) -> Tuple[str, str, List[str]]:
    """Lê bytes de um arquivo aplicando fallbacks de encoding em ordem rigorosa:
    1. utf-8-sig (cobre arquivos com e sem BOM)
    2. cp1252
    3. latin-1
    4. utf-8 com errors="replace" (com aviso)

    Retorna uma tupla contendo: (texto_normalizado, encoding_usado, avisos)
    """
    avisos: List[str] = []
    encodings_para_tentar = [
        ("utf-8-sig", False),
        ("cp1252", False),
        ("latin-1", False),
        ("utf-8", True) # com replace
    ]

    texto = ""
    encoding_usado = ""

    for enc, usar_replace in encodings_para_tentar:
        try:
            if usar_replace:
                texto = conteudo_bytes.decode(enc, errors="replace")
                avisos.append(f"encoding '{enc}' falhou nos anteriores; usado com replace")
            else:
                texto = conteudo_bytes.decode(enc)
            
            encoding_usado = enc
            break
        except UnicodeDecodeError:
            continue

    # Normalização para Unicode NFC, remoção de caracteres de controle e unificação de quebras de linha
    texto = unicodedata.normalize("NFC", texto)
    
    # Unificar quebras de linha para \n
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    
    return texto, encoding_usado, avisos