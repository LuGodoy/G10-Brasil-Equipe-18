"""Módulo de avaliação de qualidade e acurácia.

Responsável por comparar os resultados gerados pelo pipeline com um 
conjunto de referência rotulado, calculando métricas de desempenho.
"""
from typing import Dict, Any, List

def avaliar_qualidade(
    resultados_pipeline: List[Dict[str, Any]], 
    conjunto_referencia: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Calcula a acurácia por campo comparando o pipeline com o conjunto de referência."""
    ref_dict = {item.get("id"): item for item in conjunto_referencia}
    
    total_comparados = 0
    acertos = {
        "sentimento": 0,
        "relevancia": 0,
        "tipo_insight": 0,
        "topicos": 0
    }
    
    interacoes_sem_analise = 0
    revisao_prioritaria = []

    for item in resultados_pipeline:
        item_id = item.get("id")
        analise = item.get("analise")
        
        if not analise:
            interacoes_sem_analise += 1
            continue
            
        if item.get("status_revisao") == "pendente" and analise.get("confianca", 1.0) < 0.6:
            revisao_prioritaria.append(item_id)

        if item_id in ref_dict:
            total_comparados += 1
            ref_analise = ref_dict[item_id].get("analise", {})
            
            if analise.get("sentimento") == ref_analise.get("sentimento"):
                acertos["sentimento"] += 1
            if analise.get("relevancia") == ref_analise.get("relevancia"):
                acertos["relevancia"] += 1
            if analise.get("tipo_insight") == ref_analise.get("tipo_insight"):
                acertos["tipo_insight"] += 1
            
            # Para tópicos, avalia interseção exata ou sobreposição principal
            topicos_calc = set(analise.get("topicos", []))
            topicos_ref = set(ref_analise.get("topicos", []))
            if topicos_calc == topicos_ref:
                acertos["topicos"] += 1

    # Cálculo das acurácias percentuais
    metricas_acuracia = {}
    if total_comparados > 0:
        for campo, qtd in acertos.items():
            metricas_acuracia[campo] = round(qtd / total_comparados, 4)
    else:
        for campo in acertos:
            metricas_acuracia[campo] = 0.0

    return {
        "total_comparados": total_comparados,
        "acuracia": metricas_acuracia,
        "sem_analise": interacoes_sem_analise,
        "revisao_prioritaria": revisao_prioritaria
    }