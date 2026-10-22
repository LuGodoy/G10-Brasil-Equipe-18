"""Módulo de limpeza, normalização e tratamento de duplicatas.

Responsável por normalizar espaços, remover caracteres de controle, 
rejeitar textos vazios ou curtos e identificar duplicatas com base no autor e texto normalizado.
"""
import re
from typing import Dict, Any, List, Tuple

def normalizar_texto(texto: str) -> str:
    """Normaliza o texto removendo espaços duplicados e caracteres de controle,
    preservando emojis, pontuação e expressões relevantes para análise de sentimentos.
    """
    if not texto:
        return ""
    
    # Remove caracteres de controle mantendo quebras de linha e tabulações comuns se necessário
    texto_limpo = "".join(ch for ch in texto if ord(ch) >= 32 or ch in "\n\t")
    
    # Substitui múltiplos espaços por um único espaço
    texto_limpo = re.sub(r'[ \t]+', ' ', texto_limpo)
    
    return texto_limpo.strip()

def limpar_e_filtrar_interacoes(
    interacoes: List[Dict[str, Any]], 
    tamanho_minimo: int = 10
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Aplica regras de limpeza, valida o tamanho mínimo e remove duplicatas 
    dentro do lote, mantendo a primeira ocorrência.
    """
    interacoes_validas = []
    rejeitadas = []
    textos_vistos = set()

    for item in interacoes:
        texto_original = item.get("texto", "")
        texto_normalizado = normalizar_texto(texto_original)
        autor_id = item.get("autor_id", "desconhecido")

        # Verifica se o texto é vazio ou menor que o tamanho mínimo
        if not texto_normalizado or len(texto_normalizado) < tamanho_minimo:
            rejeitadas.append({
                "posicao": item.get("id"),
                "motivo": f"Texto muito curto (abaixo de {tamanho_minimo} caracteres) ou vazio",
                "original": item
            })
            continue

        # Cria uma chave de duplicidade baseada no autor e no texto normalizado (minúsculas e sem pontuação final)
        chave_texto = re.sub(r'[^\w\s]', '', texto_normalizado.lower()).strip()
        chave_duplicidade = (autor_id, chave_texto)

        if chave_duplicidade in textos_vistos:
            rejeitadas.append({
                "posicao": item.get("id"),
                "motivo": "Registro duplicado no lote",
                "original": item
            })
            continue

        textos_vistos.add(chave_duplicidade)

        # Atualiza o item com o texto normalizado mantendo o restante dos campos
        item_limpo = item.copy()
        item_limpo["texto"] = texto_normalizado
        interacoes_validas.append(item_limpo)

    return interacoes_validas, rejeitadas