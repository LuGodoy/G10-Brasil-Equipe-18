"""Modelos de dados estruturados utilizando Pydantic v2.

Compatíveis com os JSON Schemas do CommunityLab, garantindo tipagem estrita,
validação de regras de negócio e fácil serialização/desserialização.
"""
from typing import List, Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator


class AnaliseInteracao(BaseModel):
    """Estrutura do bloco de análise gerado pelo LLM para uma interação."""
    sentimento: Literal["positivo", "neutro", "negativo"]
    relevancia: Literal["alta", "media", "baixa"]
    topicos: List[Literal[
        "carreira",
        "estudos",
        "tecnologia",
        "ferramentas",
        "comunidade",
        "eventos",
        "outro"
    ]] = Field(..., min_length=1)
    tipo_insight: Literal["historia", "conquista", "duvida", "insight", "outro"]
    justificativa: Optional[str] = Field(None, max_length=500)
    confianca: Optional[float] = Field(None, ge=0.0, le=1.0)


class Interacao(BaseModel):
    """Modelo estruturado para uma interação de comunidade."""
    versao_schema: str = Field(default="1.0", pattern="^1\\.0$")
    id: int = Field(..., ge=1)
    autor_id: str = Field(..., pattern=r"^membro_[0-9]{3,}$")
    data: str
    origem: Literal["simulado", "discord", "slack", "forum", "outro"] = "discord"
    texto: str = Field(..., min_length=1, max_length=4000)
    analise: Optional[AnaliseInteracao] = None
    status_revisao: Literal["pendente", "aprovado", "rejeitado"] = "pendente"

    @field_validator("data", mode="before")
    @classmethod
    def validar_data_iso(cls, valor: str) -> str:
        if not valor:
            return datetime.now(timezone.utc).isoformat()
        return str(valor)


class Citacao(BaseModel):
    """Citação literal extraída de uma interação."""
    texto: str = Field(..., min_length=1, max_length=500)
    id_interacao: int = Field(..., ge=1)


class HistoriaDetectada(BaseModel):
    """História de sucesso detectada com fatos, resultados e citações."""
    versao_schema: str = Field(default="1.1", pattern="^1\\.1$")
    id_historia: str = Field(..., pattern=r"^historia_[0-9]{3,}$")
    tipo: Literal["conquista_profissional", "superacao", "projeto_destaque"]
    resumo: str = Field(..., min_length=1, max_length=1000)
    interacoes_origem: List[int] = Field(..., min_length=1)
    fatos: List[str] = Field(..., min_length=1)
    resultados: List[str] = Field(default_factory=list)
    citacoes: List[Citacao] = Field(..., min_length=1)
    autorizacao_divulgacao: Literal["pendente", "autorizada", "negada", "nao_aplicavel"] = "pendente"
    confianca: Optional[float] = Field(None, ge=0.0, le=1.0)
    status_revisao: Literal["pendente", "aprovado", "rejeitado"] = "pendente"


class AtivoGerado(BaseModel):
    """Conteúdo de marketing gerado a partir de histórias/interações aprovadas."""
    versao_schema: str = Field(default="1.0", pattern="^1\\.0$")
    id_ativo: str = Field(..., pattern=r"^ativo_[0-9]{3,}$")
    tipo: Literal["post_linkedin", "resumo_newsletter"]
    titulo: Optional[str] = Field(None, max_length=200)
    texto: str = Field(..., min_length=1)
    interacoes_origem: List[int] = Field(..., min_length=1)
    status_revisao: Literal["pendente", "aprovado", "rejeitado"] = "pendente"
    revisor: Optional[str] = None
    observacao_revisor: Optional[str] = Field(None, max_length=500)
    modelo_llm: Optional[str] = None
    criado_em: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    oci_object_path: Optional[str] = Field(
        None, 
        pattern=r"^ativos/[0-9]{4}-[0-9]{2}-[0-9]{2}/[A-Za-z0-9_.-]+\.json$"
    )


class LoteInteracoes(BaseModel):
    """Envelope para processamento de lote de interações."""
    versao_schema: str = Field(default="1.1", pattern="^1\\.1$")
    id_lote: Optional[str] = Field(None, pattern=r"^[A-Za-z0-9_.-]+$")
    origem_comunidade: Optional[str] = Field(None, max_length=200)
    periodo_referencia: Optional[str] = Field(None, max_length=100)
    criado_em: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    interacoes: List[Interacao] = Field(..., min_length=1)
