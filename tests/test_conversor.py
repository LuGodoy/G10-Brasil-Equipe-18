"""Testes do conversor de história (app -> contrato de HistoriaDetectada)."""
from pathlib import Path

from src.extraction.historia import converter_historia, converter_lote
from src.storage.contrato import carregar_schema

RAIZ = Path(__file__).resolve().parents[1]
SCHEMA = carregar_schema(str(RAIZ / "schemas" / "historia_detectada.json"))

TEXTO = (
    "Depois de 8 meses de estudo no programa ONE, recebi minha proposta "
    "e fui contratada como Desenvolvedora Junior."
)


def historia(**mudancas):
    base = {
        "id": "hist-001",
        "autor": "membro_000101",
        "canal": "#conquistas",
        "mensagem_original": TEXTO,
        "tipo": "conquista_profissional",
        "resumo": "Membro contratado como desenvolvedora junior apos 8 meses de estudo.",
        "interacoes_origem": [1],
        "fatos": ["Estudou 8 meses no programa ONE"],
        "resultados": ["Contratacao como Desenvolvedora Junior"],
        "citacoes": [{"texto": "fui contratada como Desenvolvedora Junior", "id_interacao": 1}],
        "confianca": 0.9,
    }
    base.update(mudancas)
    return base


def test_historia_valida_e_convertida_para_o_contrato():
    convertida, motivos, avisos = converter_historia(historia(), SCHEMA)

    assert motivos == []
    assert convertida["versao_schema"] == "1.1"
    assert convertida["id_historia"] == "historia_001"
    assert convertida["tipo"] == "conquista_profissional"
    assert convertida["citacoes"][0]["id_interacao"] == 1
    assert convertida["confianca"] == 0.9


def test_status_de_governanca_nascem_pendentes():
    convertida, _, _ = converter_historia(historia(), SCHEMA)

    assert convertida["autorizacao_divulgacao"] == "pendente"
    assert convertida["status_revisao"] == "pendente"


def test_id_do_app_vira_id_do_contrato():
    convertida, _, avisos = converter_historia(historia(id="hist-7"), SCHEMA)

    assert convertida["id_historia"] == "historia_007"
    assert any("id_historia" in aviso for aviso in avisos)


def test_id_ja_no_padrao_do_contrato_e_preservado():
    convertida, _, avisos = converter_historia(historia(id="historia_012"), SCHEMA)

    assert convertida["id_historia"] == "historia_012"
    assert avisos == []


def test_id_sem_numero_usa_a_posicao_no_lote():
    convertida, _, avisos = converter_historia(historia(id="sem-numero"), SCHEMA, sequencia=4)

    assert convertida["id_historia"] == "historia_004"
    assert any("posicao no lote" in aviso for aviso in avisos)


def test_sem_citacao_e_recusada_pelo_schema():
    convertida, motivos, _ = converter_historia(historia(citacoes=[]), SCHEMA)

    assert convertida is None
    assert any("citacoes" in motivo for motivo in motivos)


def test_tipo_fora_da_lista_e_recusado_pelo_schema():
    convertida, motivos, _ = converter_historia(historia(tipo="conquista"), SCHEMA)

    assert convertida is None
    assert any("conquista_profissional" in motivo for motivo in motivos)


def test_campo_da_tela_nao_vaza_para_o_contrato():
    convertida, _, _ = converter_historia(historia(), SCHEMA)

    for campo in ("autor", "canal", "mensagem_original", "ativos", "id"):
        assert campo not in convertida


def test_confianca_ausente_nao_entra_no_objeto():
    convertida, _, _ = converter_historia(historia(confianca=None), SCHEMA)

    assert "confianca" not in convertida


def test_confianca_invalida_nao_entra_no_objeto():
    convertida, _, _ = converter_historia(historia(confianca="alta"), SCHEMA)

    assert "confianca" not in convertida


def test_historia_em_formato_invalido_e_recusada():
    convertida, motivos, _ = converter_historia("texto solto", SCHEMA)

    assert convertida is None
    assert "formato invalido" in motivos[0]


def test_lote_separa_convertidas_de_recusadas():
    convertidas, recusadas, avisos = converter_lote(
        [historia(id="hist-001"), historia(id="hist-002", citacoes=[])],
        SCHEMA,
    )

    assert [h["id_historia"] for h in convertidas] == ["historia_001"]
    assert recusadas[0]["id"] == "hist-002"
    assert recusadas[0]["motivo"]
