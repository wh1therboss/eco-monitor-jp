import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Admin", layout="wide")

# CSS PARA MÉTRICAS VISÍVEIS
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #e2e8f0 !important;
    }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; }
    .main { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_CSV = 'denuncias.csv'

# --- LOGIN ---
if 'admin_logado' not in st.session_state:
    st.title("🔐 Admin")
    if st.text_input("Senha:", type="password") == "09122307":
        if st.button("Entrar"):
            st.session_state.admin_logado = True
            st.rerun()
    st.stop()

st.title("📊 Gestão LEGO Explorers")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("Total", len(df))
    m2.metric("Pendentes", len(df[df['Status'].str.contains("Pendente", na=False)]))
    m3.metric("Resolvidos", len(df[df['Status'].str.contains("Resolvido", na=False)]))

    aba_mapa, aba_gestao = st.tabs(["🗺️ Mapa", "⚙️ Atualizar Status"])

    with aba_mapa:
        m_admin = folium.Map(location=[-7.1153, -34.8611], zoom_start=13)
        for _, r in df.iterrows():
            cor = "red" if "Pendente" in r['Status'] else "orange" if "Manutenção" in r['Status'] else "green"
            folium.Marker([r['Lat'], r['Lon']], popup=f"{r['Protocolo']}", icon=folium.Icon(color=cor)).add_to(m_admin)
        st_folium(m_admin, width="100%", height=500)

    with aba_gestao:
        st.subheader("🛠️ Gerenciar Ocorrência")
        prots_disponiveis = df['Protocolo'].unique()
        escolha = st.selectbox("Selecione o Protocolo:", prots_disponiveis)
        
        detalhes = df[df['Protocolo'] == escolha].iloc[0]
        
        st.markdown("### 📝 Relato do Usuário")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"**📍 Endereço:**\n{detalhes['Endereco']}")
            st.info(f"**🔍 Ponto de Referência:**\n{detalhes['Referencia']}")
        with col_info2:
            st.warning(f"**⚠️ Descrição:**\n{detalhes['Descricao']}")
            st.write(f"**👤 Autor:** {detalhes['Autor']}")

        st.write("---")
        novo_st = st.radio("Status:", ["Pendente 🟡", "Em Manutenção 🛠️", "Resolvido ✅"], horizontal=True)
        if st.button("Salvar Alteração"):
            df.loc[df['Protocolo'] == escolha, 'Status'] = novo_st
            df.to_csv(CAMINHO_CSV, index=False)
            st.success("Atualizado!")
            st.rerun()
    
    # --- BARRA LATERAL COM OS BOTÕES ---
    st.sidebar.image("hamtaro.webp", width=100)
    
    # NOVO BOTÃO: LIMPAR RESOLVIDOS
    if st.sidebar.button("🧹 LIMPAR RESOLVIDOS"):
        df_restante = df[~df['Status'].str.contains("Resolvido", na=False)]
        df_restante.to_csv(CAMINHO_CSV, index=False)
        st.sidebar.success("Resolvidos apagados!")
        st.rerun()

    if st.sidebar.button("🗑️ APAGAR TUDO"):
        os.remove(CAMINHO_CSV)
        st.rerun()
        
    if st.sidebar.button("🚪 Sair"):
        del st.session_state.admin_logado
        st.rerun()
else:
    st.info("Sem dados.")
