import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Admin - EcoColeta", layout="wide")

CAMINHO_CSV = 'denuncias.csv'

# --- SISTEMA DE LOGIN ---
if 'admin_logado' not in st.session_state:
    st.title("🔑 Acesso Restrito - Admin")
    st.markdown("Insira a senha para visualizar os dados coletados.")
    
    senha = st.text_input("Senha mestra:", type="password")
    
    if st.button("Entrar"):
        if senha == "09122307":
            st.session_state.admin_logado = True
            st.rerun()
        else:
            st.error("Senha incorreta! Tente novamente.")
    st.stop()

# --- CONTEÚDO ADMIN (SÓ APARECE SE LOGADO) ---
st.title("📊 Administração Central - EcoColeta JP")

if os.path.exists(CAMINHO_CSV):
    try:
        df = pd.read_csv(CAMINHO_CSV)
        
        if df.empty:
            st.info("O arquivo CSV existe, mas ainda não há denúncias registradas.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Ocorrências", len(df))
            with col2:
                if st.button("🗑️ Limpar Tudo (Apagar CSV)"):
                    os.remove(CAMINHO_CSV)
                    st.success("Arquivo apagado. Recarregue a página.")
                    st.rerun()

            st.write("---")
            
            # MAPA ADMIN (VÊ TODOS OS PONTOS)
            st.subheader("🗺️ Mapa Geral de Focos de Lixo")
            m_admin = folium.Map(location=[-7.1153, -34.8611], zoom_start=13)
            
            for i, row in df.iterrows():
                folium.Marker(
                    [row['Lat'], row['Lon']],
                    popup=f"<b>Tipo:</b> {row['Tipo']}<br><b>End:</b> {row['Endereco']}<br><b>Data:</b> {row['Data']}",
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(m_admin)
            
            st_folium(m_admin, width=1100, height=500)

            st.write("---")
            st.subheader("📋 Lista de Denúncias")
            st.dataframe(df.iloc[::-1], use_container_width=True) # Mostra as mais recentes primeiro
            
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
else:
    st.warning("Ainda não existem denúncias registradas no sistema.")

# Botão para deslogar
if st.sidebar.button("Sair do Painel"):
    del st.session_state.admin_logado
    st.rerun()
