import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Admin Central - EcoMonitor", layout="wide")
CAMINHO_CSV = 'denuncias.csv'

# --- LOGIN (Senha: 09122307) ---
if 'admin_logado' not in st.session_state:
    st.title("🔑 Painel Administrativo")
    senha = st.text_input("Senha mestra:", type="password")
    if st.button("Entrar"):
        if senha == "09122307":
            st.session_state.admin_logado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- CARREGAMENTO DE DADOS ---
st.title("📊 Gestão Central LEGO Explorers")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    if not df.empty:
        # Criando as Abas
        aba_lixo, aba_iluminacao = st.tabs(["♻️ Descarte de Lixo", "💡 Iluminação Pública"])

        # --- ABA 1: LIXO ---
        with aba_lixo:
            # Filtra apenas o que NÃO é iluminação (ajuste os nomes conforme sua lista)
            df_lixo = df[~df['Tipo'].str.contains("Iluminação|Poste|Luz", case=False, na=False)]
            
            st.metric("Focos de Lixo Encontrados", len(df_lixo))
            
            m_lixo = folium.Map(location=[-7.1153, -34.8611], zoom_start=13)
            for _, row in df_lixo.iterrows():
                folium.Marker(
                    [row['Lat'], row['Lon']],
                    popup=f"<b>Tipo:</b> {row['Tipo']}<br><b>Rua:</b> {row['Endereco']}",
                    icon=folium.Icon(color='green', icon='trash', prefix='fa')
                ).add_to(m_lixo)
            
            st_folium(m_lixo, width=1100, height=450, key="mapa_lixo")
            st.dataframe(df_lixo.iloc[::-1], use_container_width=True)

        # --- ABA 2: ILUMINAÇÃO ---
        with aba_iluminacao:
            # Filtra apenas o que contém palavras de iluminação
            df_luz = df[df['Tipo'].str.contains("Iluminação|Poste|Luz", case=False, na=False)]
            
            st.metric("Problemas de Iluminação", len(df_luz))
            
            if not df_luz.empty:
                m_luz = folium.Map(location=[-7.1153, -34.8611], zoom_start=13)
                for _, row in df_luz.iterrows():
                    folium.Marker(
                        [row['Lat'], row['Lon']],
                        popup=f"<b>Problema:</b> {row['Tipo']}<br><b>Rua:</b> {row['Endereco']}",
                        icon=folium.Icon(color='orange', icon='lightbulb', prefix='fa')
                    ).add_to(m_luz)
                
                st_folium(m_luz, width=1100, height=450, key="mapa_luz")
                st.dataframe(df_luz.iloc[::-1], use_container_width=True)
            else:
                st.info("Nenhuma denúncia de iluminação registrada.")

        # Botão Geral para Limpar
        st.write("---")
        if st.button("⚠️ APAGAR TODO O BANCO DE DADOS (CSV)"):
            os.remove(CAMINHO_CSV)
            st.success("Dados apagados com sucesso!")
            st.rerun()

    else:
        st.info("O banco de dados está vazio.")
else:
    st.error("Arquivo CSV não encontrado.")

if st.sidebar.button("Sair"):
    del st.session_state.admin_logado
    st.rerun()
