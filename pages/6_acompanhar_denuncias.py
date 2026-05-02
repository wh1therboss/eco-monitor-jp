import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Acompanhar - EcoColeta", page_icon="🕵️")

st.title("🕵️ Acompanhe sua Denúncia")
st.markdown("Veja abaixo o status das solicitações em João Pessoa.")

CAMINHO_CSV = 'denuncias.csv'

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    if not df.empty:
        # Exibimos apenas informações públicas: Data, Rua, Tipo e Status
        # Escondemos Latitude, Longitude e o Autor (se não for anônimo)
        df_publico = df[['Data', 'Endereco', 'Tipo', 'Status']]
        
        # Filtro de busca para o usuário achar a rua dele
        busca = st.text_input("🔍 Buscar por nome da rua:")
        if busca:
            df_publico = df_publico[df_publico['Endereco'].str.contains(busca, case=False)]

        st.table(df_publico.iloc[::-1]) # Tabela simples e limpa
    else:
        st.info("Nenhuma denúncia registrada no sistema.")
else:
    st.info("O sistema está processando as primeiras coletas...")

st.sidebar.caption("LEGO Explorers - Transparência e Privacidade")
