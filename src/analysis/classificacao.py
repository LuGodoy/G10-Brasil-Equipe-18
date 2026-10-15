"""Módulo de classificação de interações utilizando LLM injetado.

Responsável por interagir com a função de LLM fornecida, extrair o JSON estruturado,
validar contra o schema de interações e gerenciar tentativas e fallbacks.
"""
import json
import re
from typing import Callable, Dict, Any, Tuple, List
from jsonschema import validate, ValidationError

def extrair_json_de_texto(resposta_bruta: str) -> Dict[str, Any]:
    """Extrai um objeto JSON válido da resposta do LLM, mesmo que esteja 
    cercado por blocos de código markdown ou texto explicativo.
    """
    if not resposta_bruta:
        raise ValueError("Resposta vazia do LLM")
        
    # Tenta carregar diretamente caso seja um JSON puro
    try:
        return json.loads(resposta_bruta)
    except json.JSONDecodeError:
        pass

    # Procura por blocos de código markdown ```json ... ``` ou ``` ... ```
    padrao_bloco = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(padrao_bloco, resposta_bruta, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Tenta encontrar a primeira chave '{' e a última '}' no texto
    inicio = resposta_bruta.find('{')
    fim = resposta_bruta.rfind('}')
    if inicio != -1 and fim != -1 and fim > inicio:
        candidato = resposta_bruta[inicio:fim+1]
        try:
            return json.loads(candidato)
        except json.JSONDecodeError:
            pass

    raise ValueError("Nenhum JSON válido encontrado na resposta do LLM")

def classificar_interacao(
    interacao: Dict[str, Any], 
    schema_interacao: Dict[str, Any],
    funcao_chamar_llm: Callable[[str], str],
    prompt_template: str,
    max_tentativas: int = 2,
    limiar_confianca: float = 0.6
) -> Tuple[Dict[str, Any], str, List[str]]:
    """Envia a interação para o LLM via função injetada, valida o resultado 
    contra o schema e gerencia novas tentativas em caso de falha.
    """
    avisos = []
    texto_interacao = interacao.get("texto", "")
    
    # Monta o prompt substituindo a variável de texto
    prompt = prompt_template.replace("{{texto}}", texto_interacao)
    
    tentativa = 0
    ultimo_erro = ""

    while tentativa < max_tentativas:
        tentativa += 1
        try:
            resposta_bruta = funcao_chamar_llm(prompt)
            dados_analise = extrair_json_de_texto(resposta_bruta)
            
            # Valida se o bloco de análise atende aos critérios do schema
            # Criamos um objeto temporário simulando a interação completa para validação
            interacao_teste = interacao.copy()
            interacao_teste["analise"] = dados_analise
            
            validate(instance=interacao_teste, schema=schema_interacao)
            
            # Validação bem-sucedida, verifica limiar de confiança para revisão prioritária
            confianca = dados_analise.get("confianca", 1.0)
            if confianca < limiar_confianca:
                avisos.append(f"Baixa confiança detectada ({confianca}); marcado para revisão prioritária.")
                interacao_teste["status_revisao"] = "pendente"
            
            return interacao_teste, "sucesso", avisos

        except (ValueError, ValidationError) as e:
            ultimo_erro = str(e)
            avisos.append(f"Tentativa {tentativa} falhou: {ultimo_erro}")
            continue

    # Se esgotou as tentativas sem sucesso, retorna a interação original sem análise (sem preencher com valores padrão)
    avisos.append(f"Esgotadas as tentativas ({max_tentativas}). Interação sem análise válida.")
    return interacao, "sem_analise", avisos