import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Adote uma Árvore | BIOGLOW", layout="wide")

# Inicialização do Banco
CAMINHO_ARVORES = 'arvores_adotadas.csv'

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        df = pd.read_csv(CAMINHO_ARVORES)
        if "Ultima_Foto" not in df.columns: df["Ultima_Foto"] = "Sem registro"
        return df
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "XP", "Status_Saude", "Ultima_Foto"])

# --- INTERFACE ---
st.title("🌳 Portal de Tutoria Ambiental")

tab1, tab2 = st.tabs(["📜 Termo de Tutoria", "🏡 Meu Jardim"])

with tab1:
    st.header("Escolha sua Muda")
    especies = {"Ipê-Amarelo": "🌼", "Pau-Brasil": "🌳", "Baobá": "🪵", "Cajueiro": "🍎"}
    
    col_m = st.columns(len(especies))
    for i, (nome, emoji) in enumerate(especies.items()):
        if col_m[i].button(f"{emoji} {nome}"):
            st.session_state.esp_sel = nome

    if 'esp_sel' in st.session_state:
        st.info(f"Você selecionou: {st.session_state.esp_sel}")
        with st.form("form_adocao"):
            tutor = st.text_input("Seu Nome:")
            nome_pet = st.text_input("Dê um nome para a árvore:")
            
            # O Termo que você pediu
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-left: 5px solid green; color: black;">
                <b>TERMO DE COMPROMISSO BIOGLOW</b><br>
                Eu, {tutor if tutor else '___'}, prometo cuidar da vida de {nome_pet if nome_pet else '___'}.
            </div>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("ASSINAR TERMO"):
                # Lógica de salvar (append no CSV)
                st.success("Tutoria realizada!")

with tab2:
    df = carregar_dados()
    if df.empty:
        st.warning("Adote uma árvore para vê-la aqui.")
    else:
        st.dataframe(df)

st.sidebar.image("hamtaro.webp", width=100)
