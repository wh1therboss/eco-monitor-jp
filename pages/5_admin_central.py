import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Admin - EcoColeta", layout="wide")

CAMINHO_CSV = 'denuncias.csv'

# Login Simples
if 'admin_logado' not in st.session_state:
    st.title("🔑 Acesso Restrito - Admin")
    senha = st.text_input("Insira a senha mestra:", type="password")
    if st.button("Entrar"):
        if senha == "lego123":
            st.session_state.admin_logado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# Conteúdo Admin
st.title("📊 Administração Central - EcoColeta JP")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Ocorrências", len(df))
    with col2:
        if st.button("🗑️ Limpar Banco de Dados"):
            os.remove(CAMINHO_CSV)
            st.rerun()

    st.write("---")
    
    st.subheader("🗺️ Mapa Geral de Ocorrências")
    m_admin = folium.Map(location=[-7.1153, -34.8611], zoom_start=13)
    for i, row in df.iterrows():
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"Tipo: {row['Tipo']}\nEnd: {row['Endereco']}",
            icon=folium.Icon(color='blue')
        ).add_to(m_admin)
    
    st_folium(m_admin, width=1100, height=500)

    st.write("---")
    st.subheader("📋 Tabela Detalhada")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Ainda não existem denúncias registradas.")

if st.sidebar.button("Sair"):
    del st.session_state.admin_logado
    st.rerun()
