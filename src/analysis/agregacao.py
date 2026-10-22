"""Módulo de agregação de dados e métricas.

Responsável por calcular contagens, rankings por tópico e distribuições 
por sentimento, relevância e tipo de insight a partir das interações analisadas.
"""
from typing import Dict, Any, List

def gerar_agregacoes(interacoes_analisadas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gera um resumo estatístico consolidado das interações analisadas."""
    total = len(interacoes_analisadas)
    sem_analise = 0
    
    por_sentimento = {"positivo": 0, "neutro": 0, "negativo": 0}
    por_relevancia = {"alta": 0, "media": 0, "baixa": 0}
    por_tipo_insight = {}
    por_topico = {}

    for item in interacoes_analisadas:
        analise = item.get("analise")
        if not analise:
            sem_analise += 1
            continue

        # Sentimento
        sentimento = analise.get("sentimento")
        if sentimento in por_sentimento:
            por_sentimento[sentimento] += 1

        # Relevância
        relevancia = analise.get("relevancia")
        if relevancia in por_relevancia:
            por_relevancia[relevancia] += 1

        # Tipo de Insight
        tipo = analise.get("tipo_insight")
        if tipo:
            por_tipo_insight[tipo] = por_tipo_insight.get(tipo, 0) + 1

        # Tópicos (uma interação pode ter múltiplos tópicos)
        topicos = analise.get("topicos", [])
        for topico in topicos:
            if topico not in por_topico:
                por_topico[topico] = {"total": 0, "positivo": 0, "neutro": 0, "negativo": 0}
            
            por_topico[topico]["total"] += 1
            if sentimento in por_topico[topico]:
                por_topico[topico][sentimento] += 1

    # Construção do ranking de tópicos com desempate alfabético estável
    ranking_topicos = [
        {"topico": t, "total": dados["total"]} 
        for t, dados in por_topico.items()
    ]
    # Ordena primariamente pelo total (decrescente) e alfabeticamente pelo nome do tópico (crescente)
    ranking_topicos.sort(key=lambda x: (-x["total"], x["topico"]))

    return {
        "total": total,
        "sem_analise": sem_analise,
        "por_topico": por_topico,
        "ranking_topicos": ranking_topicos,
        "por_sentimento": por_sentimento,
        "por_relevancia": por_relevancia,
        "por_tipo_insight": por_tipo_insight
    }