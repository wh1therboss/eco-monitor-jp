import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Adote uma Árvore", layout="wide")

# Caminho do banco
DB_ARVORES = 'arvores_adotadas.csv'

# Função para carregar dados SEM ERRO de colunas
def carregar_dados():
    if os.path.exists(DB_ARVORES):
        df = pd.read_csv(DB_ARVORES)
        # Se faltar a coluna da foto (seu erro do print), ele cria agora:
        if 'Ultima_Foto' not in df.columns:
            df['Ultima_Foto'] = "Sem registro"
        return df
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "Status", "Ultima_Foto"])

# TABS - Definir ANTES de usar
tab1, tab2 = st.tabs(["📜 Adotar e Assinar", "🏡 Meu Jardim"])

with tab1:
    st.subheader("Escolha sua muda")
    # ... seu código de formulário aqui ...

with tab2:
    st.subheader("Minhas Árvores")
    df = carregar_dados()
    st.dataframe(df)
