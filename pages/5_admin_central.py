import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Admin Central", layout="wide")
CAMINHO_CSV = 'denuncias.csv'

if 'admin_logado' not in st.session_state:
    st.title("🔑 Admin")
    if st.text_input("Senha:", type="password") == "09122307":
        if st.button("Entrar"):
            st.session_state.admin_logado = True
            st.rerun()
    st.stop()

st.title("📊 Painel de Controle")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    aba1, aba2, aba3 = st.tabs(["♻️ Lixo", "💡 Iluminação", "⚙️ Mudar Status"])
    
    df_luz = df[df['Tipo'].str.contains("Iluminação", na=False)]
    df_lixo = df[~df['Tipo'].str.contains("Iluminação", na=False)]

    with aba1:
        st.dataframe(df_lixo, use_container_width=True)
    with aba2:
        st.dataframe(df_luz, use_container_width=True)
    with aba3:
        idx = st.selectbox("ID da Denúncia:", df.index, format_func=lambda x: f"{df.iloc[x]['Protocolo']} - {df.iloc[x]['Endereco']}")
        novo_status = st.radio("Status:", ["Pendente 🟡", "Em Manutenção 🛠️", "Resolvido ✅"])
        if st.button("Atualizar"):
            df.at[idx, 'Status'] = novo_status
            df.to_csv(CAMINHO_CSV, index=False)
            st.rerun()
