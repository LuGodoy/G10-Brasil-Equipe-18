"""Tela Estúdio de Conteúdo - Placeholder para ETAPA 3."""
import streamlit as st

from styles import cabecalho, caixa, topbar


def render():
    topbar()
    cabecalho(
        "Etapa 3 de 4 · Revisar",
        "Estúdio de Conteúdo",
        "Visualize evidências originais e edite os rascunhos gerados pela IA.",
    )
    
    caixa("gray", "<b>Em desenvolvimento</b><br>"
          "O Estúdio de Conteúdo será implementado na ETAPA 3. "
          "Aqui você poderá ver lado a lado as evidências originais e os ativos gerados pela IA.")
    
    st.info("💡 **Próximas funcionalidades:**\n\n"
            "- Visualização de mensagem original com trechos destacados\n"
            "- Fatos extraídos com rastreabilidade\n"
            "- Edição de conteúdo gerado (testemunhos e cases)\n"
            "- Regeneração de rascunhos\n"
            "- Fontes do conteúdo\n"
            "- Envio para curadoria")
