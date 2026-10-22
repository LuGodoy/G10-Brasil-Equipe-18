"""CommunityLab – Detector Inteligente de Histórias de Sucesso e Testemunhos com IA."""

from .ingestion import (
    ler_arquivo_bytes,
    pseudonimizar_autor,
    processar_json,
    processar_csv,
    processar_dataframe,
    interacoes_para_dataframe,
)
from .preprocessing import (
    normalizar_texto,
    limpar_e_filtrar_interacoes,
    anonimizar_texto,
)
from .analysis import (
    extrair_json_de_texto,
    classificar_interacao,
    gerar_agregacoes,
)
from .detection import (
    filtrar_candidatos_historia,
)
from .orchestration import (
    dividir_em_lotes,
    avaliar_qualidade,
    PESOS_CQF,
    calcular_cqf_score,
    validar_integridade_evidencias,
    avaliar_aprovacao_editorial,
    validar_liberacao_publicacao,
    consolidar_decisao_governança,
)
from .storage import (
    carregar_schema,
    validar_objeto_contra_schema,
    validar_interacao,
    validar_ativo,
    validar_historia,
    validar_avaliacao_cqf,
)
from .modelos import (
    Interacao,
    AnaliseInteracao,
    Citacao,
    HistoriaDetectada,
    AtivoGerado,
    AvaliacaoCQF,
    LoteInteracoes,
)
from .config import (
    TAMANHO_MINIMO_TEXTO,
    TAMANHO_MAXIMO_TEXTO,
    LIMIAR_CONFIANCA,
    MAX_TENTATIVAS_LLM,
    TAMANHO_LOTE,
    SAL_PADRAO,
)

__all__ = [
    "ler_arquivo_bytes",
    "pseudonimizar_autor",
    "processar_json",
    "processar_csv",
    "processar_dataframe",
    "interacoes_para_dataframe",
    "normalizar_texto",
    "limpar_e_filtrar_interacoes",
    "anonimizar_texto",
    "dividir_em_lotes",
    "extrair_json_de_texto",
    "classificar_interacao",
    "gerar_agregacoes",
    "filtrar_candidatos_historia",
    "avaliar_qualidade",
    "PESOS_CQF",
    "calcular_cqf_score",
    "validar_integridade_evidencias",
    "avaliar_aprovacao_editorial",
    "validar_liberacao_publicacao",
    "consolidar_decisao_governança",
    "carregar_schema",
    "validar_objeto_contra_schema",
    "validar_interacao",
    "validar_ativo",
    "validar_historia",
    "validar_avaliacao_cqf",
    "Interacao",
    "AnaliseInteracao",
    "Citacao",
    "HistoriaDetectada",
    "AtivoGerado",
    "AvaliacaoCQF",
    "LoteInteracoes",
    "TAMANHO_MINIMO_TEXTO",
    "TAMANHO_MAXIMO_TEXTO",
    "LIMIAR_CONFIANCA",
    "MAX_TENTATIVAS_LLM",
    "TAMANHO_LOTE",
    "SAL_PADRAO",
]
