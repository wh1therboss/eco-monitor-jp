import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Admin | LEGO Explorers", layout="wide")

# CSS para manter as métricas visíveis e bonitas
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #2f855a !important;
    }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; }
    .main { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_DENUNCIAS = 'denuncias.csv'
CAMINHO_ARVORES = 'arvores_adotadas.csv'

# --- LOGIN ---
if 'admin_logado' not in st.session_state:
    st.title("🔐 Acesso Administrativo")
    if st.text_input("Senha de Acesso:", type="password") == "09122307":
        if st.button("Acessar Painel"):
            st.session_state.admin_logado = True
            st.rerun()
    st.stop()

st.title("📊 Central de Comando LEGO Explorers")

# Criando as Abas de Gestão
aba1, aba2 = st.tabs(["🗑️ Gestão de Resíduos", "🌳 Monitoramento de Biomas"])

# --- ABA 1: DENÚNCIAS (O que já tínhamos) ---
with aba1:
    if os.path.exists(CAMINHO_DENUNCIAS):
        df_lixo = pd.read_csv(CAMINHO_DENUNCIAS)
        col1, col2, col3 = st.columns(3)
        col1.metric("Denúncias Totais", len(df_lixo))
        col2.metric("Pendentes", len(df_lixo[df_lixo['Status'].str.contains("Pendente", na=False)]))
        col3.metric("Resolvidos", len(df_lixo[df_lixo['Status'].str.contains("Resolvido", na=False)]))
        
        st.write("---")
        # Espaço para o mapa e atualização de status (mesmo código anterior)
        st.dataframe(df_lixo, use_container_width=True)
    else:
        st.info("Nenhuma denúncia de lixo registrada.")

# --- ABA 2: MONITORAMENTO DAS ÁRVORES (NOVIDADE) ---
with aba2:
    if os.path.exists(CAMINHO_ARVORES):
        df_tree = pd.read_csv(CAMINHO_ARVORES)
        
        # Métricas Verdes
        m1, m2, m3 = st.columns(3)
        m1.metric("Árvores Adotadas", len(df_tree))
        m2.metric("Total XP Verde", df_tree['XP'].sum())
        
        # Calcula saúde média (simbólico)
        saudaveis = len(df_tree[df_tree['Status_Saude'] == "Excelente"])
        m3.metric("Saúde do Bioma", f"{(saudaveis/len(df_tree)*100):.0f}% Saudáveis")

        st.subheader("🌲 Mapa de Reflorestamento e Tutoria")
        
        # Lista detalhada das árvores
        for index, row in df_tree.iterrows():
            with st.expander(f"🌳 {row['Nome_Arvore']} ({row['Especie']}) - Tutor: {row['Dono']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write(f"📍 **Local:** {row['Local']}")
                    st.write(f"📈 **XP Atual:** {row['XP']}")
                with c2:
                    st.write(f"❤️ **Estado de Saúde:** {row['Status_Saude']}")
                    st.write(f"📖 **Motivo:** {row['Motivo']}")
                with c3:
                    # Botão para o admin intervir se necessário
                    if st.button(f"Enviar Notificação para {row['Dono']}", key=f"notif_{index}"):
                        st.success(f"Notificação enviada para o tutor de {row['Nome_Arvore']}!")
        
        st.write("---")
        st.subheader("📋 Tabela Geral de Ativos Verdes")
        st.table(df_tree[["Dono", "Nome_Arvore", "Especie", "Local", "Status_Saude", "XP"]])

    else:
        st.info("Ainda não existem árvores adotadas no sistema.")

# --- BARRA LATERAL ---
st.sidebar.image("hamtaro.webp", width=100)
st.sidebar.markdown("### Administração Geral")

if st.sidebar.button("🧹 LIMPAR RESOLVIDOS (LIXO)"):
    if os.path.exists(CAMINHO_DENUNCIAS):
        df_lixo = pd.read_csv(CAMINHO_DENUNCIAS)
        df_lixo = df_lixo[~df_lixo['Status'].str.contains("Resolvido", na=False)]
        df_lixo.to_csv(CAMINHO_DENUNCIAS, index=False)
        st.rerun()

if st.sidebar.button("🔥 RESETAR TODOS OS DADOS"):
    if os.path.exists(CAMINHO_DENUNCIAS): os.remove(CAMINHO_DENUNCIAS)
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()

if st.sidebar.button("🚪 Sair do Admin"):
    del st.session_state.admin_logado
    st.rerun()
