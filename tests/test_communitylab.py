import json
import pytest
from pathlib import Path
from src import (
    ler_arquivo_bytes,
    pseudonimizar_autor,
    processar_json,
    processar_csv,
    normalizar_texto,
    limpar_e_filtrar_interacoes,
    anonimizar_texto,
    dividir_em_lotes,
    extrair_json_de_texto,
    classificar_interacao,
    gerar_agregacoes,
    avaliar_qualidade,
    carregar_schema,
    validar_interacao,
    validar_ativo,
)

def test_leitura_bytes():
    # Testa utf-8 com acentuação e quebras de linha
    texto_raw = "Linha 1\r\nLinha 2: Acentuação é válida!"
    res, enc, avisos = ler_arquivo_bytes(texto_raw.encode("utf-8"))
    assert "Acentuação é válida!" in res
    assert "\r" not in res
    assert enc == "utf-8-sig"
    assert len(avisos) == 0

def test_pseudonimizacao_autor():
    sal = "segredo123"
    p1 = pseudonimizar_autor("Carlos Silva", sal)
    p2 = pseudonimizar_autor("Carlos Silva", sal)
    p3 = pseudonimizar_autor("Ana Santos", sal)
    
    assert p1.startswith("membro_")
    assert p1 == p2
    assert p1 != p3
    # Se já estiver pseudonimizado, mantém
    assert pseudonimizar_autor("membro_123456", sal) == "membro_123456"

def test_processar_json():
    sal = "teste"
    conteudo = '[{"id": 1, "autor": "User A", "texto": "Mensagem relevante sobre o curso"}]'
    validas, rejeitadas, avisos = processar_json(conteudo, sal)
    assert len(validas) == 1
    assert len(rejeitadas) == 0
    assert validas[0]["id"] == 1
    assert validas[0]["texto"] == "Mensagem relevante sobre o curso"
    assert validas[0]["autor_id"].startswith("membro_")

def test_processar_csv():
    sal = "teste"
    csv_data = "id,autor,texto\n1,Maria,Aprendendo Python no curso!\n"
    validas, rejeitadas, avisos = processar_csv(csv_data, sal)
    assert len(validas) == 1
    assert len(rejeitadas) == 0
    assert validas[0]["id"] == 1
    assert validas[0]["texto"] == "Aprendendo Python no curso!"

def test_limpeza_e_duplicatas():
    # Testa normalização de espaços e caracteres
    assert normalizar_texto("  Texto   com   espaços   duplos \t\n") == "Texto com espaços duplos"

    interacoes = [
        {"id": 1, "autor_id": "membro_001", "texto": "Texto longo o suficiente para passar."},
        {"id": 2, "autor_id": "membro_001", "texto": "Texto longo o suficiente para passar."}, # duplicata
        {"id": 3, "autor_id": "membro_002", "texto": "Curto"}, # rejeitado por tamanho
    ]
    validas, rejeitadas = limpar_e_filtrar_interacoes(interacoes, tamanho_minimo=10)
    assert len(validas) == 1
    assert len(rejeitadas) == 2
    assert validas[0]["id"] == 1

def test_anonimizacao():
    texto = "Meu email é contato@exemplo.com e meu telefone é 11 98888-7777 com CPF 123.456.789-00."
    anonimizado, contagem = anonimizar_texto(texto)
    assert "[EMAIL]" in anonimizado
    assert "[TELEFONE]" in anonimizado
    assert "[CPF]" in anonimizado
    assert contagem["email"] == 1
    assert contagem["telefone"] == 1
    assert contagem["cpf"] == 1

def test_anonimizacao_ner_spacy():
    # Testa NER spaCy: mascara pessoa, preserva cidade e menção
    texto = "Conversei com Mariana Souza em São Paulo sobre o projeto no Discord com @membro_045."
    anonimizado, contagem = anonimizar_texto(texto)
    assert "[NOME]" in anonimizado
    assert "Mariana Souza" not in anonimizado
    assert "São Paulo" in anonimizado
    assert "@membro_045" in anonimizado
    assert contagem["nome"] >= 1

def test_anonimizacao_telefone_ddd_obrigatorio():
    # Telefone com DDD é mascarado
    t1, c1 = anonimizar_texto("Ligue para (11) 98888-7777 ou 21 3222-1234.")
    assert c1["telefone"] == 2
    assert "[TELEFONE]" in t1

    # Sequência de 8 dígitos sem DDD não é confundida com telefone
    t2, c2 = anonimizar_texto("O código do pedido é 12345678 e a data é 20261013.")
    assert c2["telefone"] == 0
    assert "12345678" in t2

def test_dividir_em_lotes():
    itens = [{"id": i} for i in range(12)]
    lotes = dividir_em_lotes(itens, tamanho_lote=5)
    assert len(lotes) == 3
    assert len(lotes[0]) == 5
    assert len(lotes[1]) == 5
    assert len(lotes[2]) == 2

    # Testa validação de tamanho de lote
    with pytest.raises(ValueError):
        dividir_em_lotes(itens, tamanho_lote=0)

def test_extrair_json_de_texto():
    # Bloco markdown com ```json
    markdown_resp = "Aqui está a análise:\n```json\n{\"sentimento\": \"positivo\"}\n```\nObrigado!"
    obj = extrair_json_de_texto(markdown_resp)
    assert obj == {"sentimento": "positivo"}

    # Texto puro com json
    puro = "Resultado: {\"chave\": 123}"
    obj2 = extrair_json_de_texto(puro)
    assert obj2 == {"chave": 123}

def test_agregacao():
    interacoes = [
        {
            "id": 1,
            "analise": {
                "sentimento": "positivo",
                "relevancia": "alta",
                "tipo_insight": "conquista",
                "topicos": ["carreira", "tecnologia"]
            }
        },
        {
            "id": 2,
            "analise": {
                "sentimento": "negativo",
                "relevancia": "baixa",
                "tipo_insight": "duvida",
                "topicos": ["carreira"]
            }
        }
    ]
    resumo = gerar_agregacoes(interacoes)
    assert resumo["total"] == 2
    assert resumo["por_sentimento"]["positivo"] == 1
    assert resumo["por_sentimento"]["negativo"] == 1
    assert resumo["por_relevancia"]["alta"] == 1
    assert resumo["ranking_topicos"][0]["topico"] == "carreira"
    assert resumo["ranking_topicos"][0]["total"] == 2

def test_validacao_schemas():
    base_dir = Path(__file__).parent.parent
    schema_interacao = carregar_schema(str(base_dir / "schemas/interacao_schema.json"))
    schema_ativo = carregar_schema(str(base_dir / "schemas/ativo_gerado_schema.json"))

    interacao_valida = {
        "versao_schema": "1.0",
        "id": 1,
        "autor_id": "membro_001",
        "data": "2026-10-15T10:00:00Z",
        "origem": "discord",
        "texto": "Mensagem válida de teste",
        "status_revisao": "pendente"
    }
    valido, erros = validar_interacao(interacao_valida, schema_interacao)
    assert valido, f"Erros: {erros}"

    ativo_valido = {
        "versao_schema": "1.0",
        "id_ativo": "ativo_001",
        "tipo": "post_linkedin",
        "texto": "Texto do post de divulgação",
        "interacoes_origem": [1],
        "status_revisao": "pendente",
        "criado_em": "2026-10-15T10:00:00Z"
    }
    valido_ativo, erros_ativo = validar_ativo(ativo_valido, schema_ativo)
    assert valido_ativo, f"Erros: {erros_ativo}"

def test_interacao_schema_versao_obrigatoria():
    base_dir = Path(__file__).parent.parent
    schema_interacao = carregar_schema(str(base_dir / "schemas/interacao_schema.json"))

    # Interação sem versao_schema deve falhar
    interacao_invalida = {
        "id": 1,
        "autor_id": "membro_001",
        "data": "2026-10-15T10:00:00Z",
        "origem": "discord",
        "texto": "Mensagem sem versão de schema",
    }
    valido, erros = validar_interacao(interacao_invalida, schema_interacao)
    assert not valido
    assert any("versao_schema" in e for e in erros)

def test_ingestion_fallback_data_dinamica():
    # Item sem data deve receber timestamp ISO atual gerado dinamicamente
    itens, _, _ = processar_json('[{"texto": "Sem data explícita"}]', sal="teste")
    assert len(itens) == 1
    data_gerada = itens[0]["data"]
    assert "T" in data_gerada
    assert data_gerada != "2026-10-13T00:00:00Z"

def test_classificar_interacao_sucesso():
    base_dir = Path(__file__).parent.parent
    schema_interacao = carregar_schema(str(base_dir / "schemas/interacao_schema.json"))
    
    interacao = {
        "versao_schema": "1.0",
        "id": 1,
        "autor_id": "membro_001",
        "data": "2026-10-15T10:00:00Z",
        "origem": "discord",
        "texto": "Consegui meu primeiro emprego como dev!",
        "status_revisao": "pendente"
    }

    # Mock de LLM retornando JSON válido
    def llm_fake(prompt: str) -> str:
        return """
        Aqui está a resposta:
        ```json
        {
            "sentimento": "positivo",
            "relevancia": "alta",
            "topicos": ["carreira"],
            "tipo_insight": "conquista",
            "justificativa": "Relato de contratação",
            "confianca": 0.95
        }
        ```
        """

    res, status, avisos = classificar_interacao(
        interacao=interacao,
        schema_interacao=schema_interacao,
        funcao_chamar_llm=llm_fake,
        prompt_template="Analise: {{texto}}",
        max_tentativas=2,
        limiar_confianca=0.6
    )

    assert status == "sucesso"
    assert "analise" in res
    assert res["analise"]["sentimento"] == "positivo"
    assert res["analise"]["tipo_insight"] == "conquista"
    assert len(avisos) == 0

def test_classificar_interacao_retry_e_recuperacao():
    base_dir = Path(__file__).parent.parent
    schema_interacao = carregar_schema(str(base_dir / "schemas/interacao_schema.json"))
    
    interacao = {
        "versao_schema": "1.0",
        "id": 2,
        "autor_id": "membro_002",
        "data": "2026-10-15T10:00:00Z",
        "origem": "discord",
        "texto": "Qual a melhor linguagem?",
        "status_revisao": "pendente"
    }

    tentativas = 0
    def llm_com_falha_inicial(prompt: str) -> str:
        nonlocal tentativas
        tentativas += 1
        if tentativas == 1:
            return "Resposta quebrada que não contém JSON"
        return '{"sentimento": "neutro", "relevancia": "media", "topicos": ["tecnologia"], "tipo_insight": "duvida", "confianca": 0.8}'

    res, status, avisos = classificar_interacao(
        interacao=interacao,
        schema_interacao=schema_interacao,
        funcao_chamar_llm=llm_com_falha_inicial,
        prompt_template="Analise: {{texto}}",
        max_tentativas=2
    )

    assert status == "sucesso"
    assert tentativas == 2
    assert res["analise"]["sentimento"] == "neutro"
    assert any("Tentativa 1 falhou" in a for a in avisos)

def test_classificar_interacao_tentativas_esgotadas():
    base_dir = Path(__file__).parent.parent
    schema_interacao = carregar_schema(str(base_dir / "schemas/interacao_schema.json"))
    
    interacao = {
        "versao_schema": "1.0",
        "id": 3,
        "autor_id": "membro_003",
        "data": "2026-10-15T10:00:00Z",
        "origem": "discord",
        "texto": "Mensagem qualquer",
        "status_revisao": "pendente"
    }

    def llm_sempre_invalido(prompt: str) -> str:
        return "Não sei a resposta"

    res, status, avisos = classificar_interacao(
        interacao=interacao,
        schema_interacao=schema_interacao,
        funcao_chamar_llm=llm_sempre_invalido,
        prompt_template="{{texto}}",
        max_tentativas=2
    )

    assert status == "sem_analise"
    assert "analise" not in res
    assert any("Esgotadas as tentativas" in a for a in avisos)

def test_classificar_interacao_baixa_confianca():
    base_dir = Path(__file__).parent.parent
    schema_interacao = carregar_schema(str(base_dir / "schemas/interacao_schema.json"))
    
    interacao = {
        "versao_schema": "1.0",
        "id": 4,
        "autor_id": "membro_004",
        "data": "2026-10-15T10:00:00Z",
        "origem": "discord",
        "texto": "Dúvida confusa",
        "status_revisao": "pendente"
    }

    def llm_baixa_confianca(prompt: str) -> str:
        return '{"sentimento": "neutro", "relevancia": "baixa", "topicos": ["outro"], "tipo_insight": "duvida", "confianca": 0.4}'

    res, status, avisos = classificar_interacao(
        interacao=interacao,
        schema_interacao=schema_interacao,
        funcao_chamar_llm=llm_baixa_confianca,
        prompt_template="{{texto}}",
        limiar_confianca=0.6
    )

    assert status == "sucesso"
    assert res["status_revisao"] == "pendente"
    assert any("Baixa confiança" in a for a in avisos)

def test_avaliar_qualidade():
    referencia = [
        {
            "id": 1,
            "analise": {
                "sentimento": "positivo",
                "relevancia": "alta",
                "tipo_insight": "conquista",
                "topicos": ["carreira", "tecnologia"]
            }
        },
        {
            "id": 2,
            "analise": {
                "sentimento": "neutro",
                "relevancia": "media",
                "tipo_insight": "duvida",
                "topicos": ["estudos"]
            }
        }
    ]

    # Pipeline com 100% acerto no id 1, e erro de sentimento no id 2
    pipeline = [
        {
            "id": 1,
            "status_revisao": "pendente",
            "analise": {
                "sentimento": "positivo",
                "relevancia": "alta",
                "tipo_insight": "conquista",
                "topicos": ["tecnologia", "carreira"],
                "confianca": 0.9
            }
        },
        {
            "id": 2,
            "status_revisao": "pendente",
            "analise": {
                "sentimento": "negativo", # erro de sentimento
                "relevancia": "media",
                "tipo_insight": "duvida",
                "topicos": ["estudos"],
                "confianca": 0.5 # < 0.6 -> revisão prioritária
            }
        },
        {
            "id": 3,
            "status_revisao": "pendente"
            # sem analise
        }
    ]

    metricas = avaliar_qualidade(pipeline, referencia)
    assert metricas["total_comparados"] == 2
    assert metricas["acuracia"]["sentimento"] == 0.5
    assert metricas["acuracia"]["relevancia"] == 1.0
    assert metricas["acuracia"]["tipo_insight"] == 1.0
    assert metricas["acuracia"]["topicos"] == 1.0
    assert metricas["sem_analise"] == 1
    assert 2 in metricas["revisao_prioritaria"]

def test_ingestao_deteccao_colisao(monkeypatch):
    # Caso 1: autores iguais geram o mesmo autor_id sem aviso de colisão
    conteudo_sem_colisao = json.dumps([
        {"id": 1, "autor": "Carlos Silva", "texto": "Primeira mensagem válida"},
        {"id": 2, "autor": "Carlos Silva", "texto": "Segunda mensagem do mesmo autor"}
    ])
    itens, _, avisos_sem_colisao = processar_json(conteudo_sem_colisao, sal="sal_teste")
    assert len(itens) == 2
    assert not any("Detectada colisão" in a for a in avisos_sem_colisao)

    # Caso 2: autores distintos forçados ao mesmo autor_id geram aviso de colisão
    conteudo_com_colisao = json.dumps([
        {"id": 1, "autor": "Carlos Silva", "texto": "Mensagem da primeira pessoa"},
        {"id": 2, "autor": "Ana Santos", "texto": "Mensagem da segunda pessoa"}
    ])
    monkeypatch.setattr("src.ingestion.ingestion.pseudonimizar_autor", lambda autor, sal: "membro_777777")
    monkeypatch.setattr("src.ingestion.pseudonimizar_autor", lambda autor, sal: "membro_777777")
    
    itens_col, _, avisos_colisao = processar_json(conteudo_com_colisao, sal="sal_teste")
    assert len(itens_col) == 2
    assert any("Detectada colisão de pseudonimização" in a for a in avisos_colisao)
    assert any("membro_777777" in a for a in avisos_colisao)

def test_leitura_cp1252_latin1_e_replace():
    # Testa cp1252 com caractere específico (símbolo de euro €, mapeado para byte 0x80)
    texto_cp1252 = "Preço em euros: 50 €".encode("cp1252")
    res_cp, enc_cp, avisos_cp = ler_arquivo_bytes(texto_cp1252)
    assert "Preço em euros: 50" in res_cp
    assert enc_cp == "cp1252"

    # Testa fallback para latin-1 com byte 0x81 (indefinido em cp1252 e inválido em utf-8)
    bytes_latin1 = b"In\x81valido"
    res_lat, enc_lat, avisos_lat = ler_arquivo_bytes(bytes_latin1)
    assert "In" in res_lat
    assert enc_lat == "latin-1"

def test_processar_csv_delimitador_ponto_e_virgula():
    sal = "teste"
    csv_data = "id;autor;texto\n10;Carlos;Mensagem separada por ponto e virgula\n"
    validas, rejeitadas, avisos = processar_csv(csv_data, sal)
    assert len(validas) == 1
    assert len(rejeitadas) == 0
    assert validas[0]["id"] == 10
    assert validas[0]["texto"] == "Mensagem separada por ponto e virgula"

def test_processar_e_exportar_dataframe_pandas():
    import pandas as pd
    from src import processar_dataframe, interacoes_para_dataframe

    dados = pd.DataFrame([
        {"id": 1, "autor": "Beatriz", "texto": "Adorando o curso de dados!"},
        {"id": 2, "autor": "Beatriz", "texto": ""}, # deve ser rejeitada
        {"id": 3, "autor": "Lucas", "texto": "Excelente mentoria hoje."}
    ])

    validas, rejeitadas, avisos = processar_dataframe(dados, sal="segredo")
    assert len(validas) == 2
    assert len(rejeitadas) == 1
    assert validas[0]["autor_id"].startswith("membro_")

    # Testa conversão para DataFrame de volta
    df_result = interacoes_para_dataframe(validas)
    assert isinstance(df_result, pd.DataFrame)
    assert len(df_result) == 2
    assert "autor_id" in df_result.columns
    assert "texto" in df_result.columns

def test_modelos_pydantic_validacao():
    from src import (
        Interacao,
        AnaliseInteracao,
        Citacao,
        HistoriaDetectada,
        AtivoGerado,
        LoteInteracoes,
    )

    interacao = Interacao(
        id=1,
        autor_id="membro_123456",
        data="2026-10-15T10:00:00Z",
        texto="Texto da mensagem de teste",
        analise=AnaliseInteracao(
            sentimento="positivo",
            relevancia="alta",
            topicos=["carreira"],
            tipo_insight="conquista",
            confianca=0.9
        )
    )
    assert interacao.id == 1
    assert interacao.analise is not None
    assert interacao.analise.sentimento == "positivo"
    assert interacao.versao_schema == "1.0"

    citacao = Citacao(texto="Fui contratado!", id_interacao=1)
    historia = HistoriaDetectada(
        id_historia="historia_001",
        tipo="conquista_profissional",
        resumo="Contratação de novo dev",
        interacoes_origem=[1],
        fatos=["Foi contratado"],
        citacoes=[citacao]
    )
    assert historia.id_historia == "historia_001"
    assert historia.versao_schema == "1.1"

    ativo = AtivoGerado(
        id_ativo="ativo_001",
        tipo="post_linkedin",
        texto="Texto do post",
        interacoes_origem=[1]
    )
    assert ativo.versao_schema == "1.0"

    lote = LoteInteracoes(interacoes=[interacao])
    assert len(lote.interacoes) == 1

def test_cpf_valido_vs_sequencia_numerica():
    # Sequência de 11 dígitos que NÃO é CPF válido não é mascarada
    t1, c1 = anonimizar_texto("O código do pedido é 99988877766 e o outro é 12345678901.")
    assert c1["cpf"] == 0
    assert "99988877766" in t1

    # CPF formatado é mascarado
    t2, c2 = anonimizar_texto("Meu CPF é 123.456.789-00.")
    assert c2["cpf"] == 1
    assert "[CPF]" in t2

def test_ativo_gerado_schema_versao_obrigatoria():
    base_dir = Path(__file__).parent.parent
    schema_ativo = carregar_schema(str(base_dir / "schemas/ativo_gerado_schema.json"))

    ativo_sem_versao = {
        "id_ativo": "ativo_001",
        "tipo": "post_linkedin",
        "texto": "Post",
        "interacoes_origem": [1],
        "status_revisao": "pendente",
        "criado_em": "2026-10-15T10:00:00Z"
    }
    valido, erros = validar_ativo(ativo_sem_versao, schema_ativo)
    assert not valido
    assert any("versao_schema" in e for e in erros)

def test_modulos_src_pipeline():
    # Testa os submódulos de src criados conforme o README
    import src.ingestion
    import src.preprocessing
    import src.analysis
    import src.detection
    import src.extraction
    import src.generation
    import src.orchestration
    import src.storage

    assert hasattr(src.ingestion, "ler_arquivo_bytes")
    assert hasattr(src.preprocessing, "anonimizar_texto")
    assert hasattr(src.analysis, "classificar_interacao")
    assert hasattr(src.detection, "filtrar_candidatos_historia")
    assert hasattr(src.generation, "AtivoGerado")
    assert hasattr(src.orchestration, "dividir_em_lotes")
    assert hasattr(src.storage, "carregar_schema")



