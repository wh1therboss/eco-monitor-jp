import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# CSS para métricas e botões
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #2f855a !important;
    }
    [data-testid="stMetricLabel"] { color: #2d3748 !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #2f855a !important; }
    .main { background-color: #f7fafc; }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_ARVORES = 'arvores_adotadas.csv'

# --- LISTA DE ESPÉCIES (USANDO EMOJIS) ---
especies = {
    "Ipê-Amarelo": "🌼",
    "Pau-Brasil": "🌳",
    "Baobá": "🪵",
    "Cajueiro": "🍎",
    "Mangue": "🦀",
    "Oiti": "🍃",
    "Aroeira": "🌿",
    "Pau-Ferro": "🏗️",
    "Pau-d'arco": "🌸",
    "Pitombeira": "🍒"
}

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        return pd.read_csv(CAMINHO_ARVORES)
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "XP", "Nivel"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

st.title("🌳 Adote uma Árvore Nativa")
st.markdown("### LEGO Explorers: João Pessoa mais Verde")

tab1, tab2 = st.tabs(["🌱 Escolher Muda", "🏡 Meu Jardim"])

with tab1:
    st.subheader("Selecione uma espécie nativa para adotar")
    cols = st.columns(5)
    
    for i, (nome, emoji) in enumerate(especies.items()):
        with cols[i % 5]:
            st.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
            if st.button(f"Adotar {nome}", key=f"btn_{nome}"):
                st.session_state.especie_selecionada = nome
                st.session_state.emoji_selecionado = emoji

    if 'especie_selecionada' in st.session_state:
        st.divider()
        with st.form("form_adocao"):
            st.success(f"Você escolheu: {st.session_state.emoji_selecionada} **{st.session_state.especie_selecionada}**")
            n_dono = st.text_input("Tutor (Seu Nome):")
            n_arvore = st.text_input("Nome da Árvore:")
            if st.form_submit_button("Confirmar Plantio"):
                if n_dono and n_arvore:
                    df = carregar_dados()
                    nova = {
                        "Dono": n_dono, 
                        "Nome_Arvore": n_arvore, 
                        "Especie": st.session_state.especie_selecionada,
                        "XP": 0, 
                        "Nivel": "Semente 🌰"
                    }
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success("Platada com sucesso! Cuide dela no Jardim.")
                    time.sleep(1)
                    st.rerun()

with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("O jardim está vazio. Escolha uma muda na primeira aba!")
    else:
        sel = st.selectbox("Selecione sua árvore para cuidar:", df['Nome_Arvore'].tolist())
        d = df[df['Nome_Arvore'] == sel].iloc[0]
        
        # Evolução por XP
        xp = d['XP']
        if xp < 50: niv, icon = "Semente", "🌰"
        elif xp < 150: niv, icon = "Muda", "🌱"
        elif xp < 350: niv, icon = "Jovem", "🌿"
        else: niv, icon = "Adulta", "🌳"
        
        c_icon, c_txt = st.columns([1, 2])
        with c_icon:
            st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{icon}</h1>", unsafe_allow_html=True)
        with c_txt:
            st.metric("Fase atual", niv)
            st.write(f"**Tutor:** {d['Dono']} | **Espécie:** {d['Especie']}")
            st.write(f"**Experiência (XP):** {xp}")
            st.progress(min((xp % 100)/100, 1.0) if xp < 400 else 1.0)

        st.divider()
        st.markdown("### 🛠️ Painel de Cuidados")
        ca1, ca2, ca3 = st.columns(3)
        
        if ca1.button("💧 Regar (+10 XP)"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 10
            salvar_dados(df); st.toast("Você regou a planta! 💧"); time.sleep(0.5); st.rerun()
            
        if ca2.button("💩 Adubar (+25 XP)"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 25
            salvar_dados(df); st.toast("Solo fortalecido! 💩"); time.sleep(0.5); st.rerun()

        if ca3.button("☀️ Sol (+5 XP)"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 5
            salvar_dados(df); st.toast("Energia solar! ☀️"); time.sleep(0.5); st.rerun()

# Barra lateral
st.sidebar.image("hamtaro.webp", width=100)
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Resetar Jardim"):
    if os.path.exists(CAMINHO_ARVORES):
        os.remove(CAMINHO_ARVORES)
        st.rerun()
