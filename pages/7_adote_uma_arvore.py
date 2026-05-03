import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# Criar pasta para as fotos se não existir
if not os.path.exists("fotos_arvores"):
    os.makedirs("fotos_arvores")

CAMINHO_ARVORES = 'arvores_adotadas.csv'

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        return pd.read_csv(CAMINHO_ARVORES)
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "Motivo", "XP", "Status_Saude", "Ultima_Foto"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

st.title("🌳 Sistema de Adoção e Tutoria")

tab1, tab2 = st.tabs(["📜 Formalizar Adoção", "🏡 Meu Jardim & Diário"])

# --- TAB 1: ADOÇÃO (Mantido) ---
with tab1:
    st.info("Escolha uma muda e assine o contrato para começar.")
    # ... (mesmo código anterior de escolha de espécie e contrato)
    # [Apenas garanta que ao salvar a nova árvore, adicione a coluna "Ultima_Foto": "Sem registro"]

# --- TAB 2: JARDIM COM REGISTRO FOTOGRÁFICO ---
with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Nenhuma árvore adotada.")
    else:
        selecionada = st.selectbox("Selecione sua árvore:", df['Nome_Arvore'].tolist())
        idx = df[df['Nome_Arvore'] == selecionada].index[0]
        d = df.loc[idx]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Diário de Crescimento")
            st.write("Registre a evolução da sua árvore hoje!")
            
            # INPUT DE CÂMERA
            foto_tirada = st.camera_input("Tirar foto da árvore")
            
            if foto_tirada:
                # Salva o arquivo com nome único (Nome_Data.png)
                nome_foto = f"fotos_arvores/{selecionada}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
                with open(nome_foto, "wb") as f:
                    f.write(foto_tirada.getbuffer())
                
                # Atualiza os dados
                df.loc[idx, 'Ultima_Foto'] = nome_foto
                df.loc[idx, 'XP'] += 50  # Foto dá muito XP!
                salvar_dados(df)
                st.success("Foto registrada no diário! +50 XP")
                st.rerun()

        with col2:
            st.subheader("📊 Status e Evolução")
            # Mostra a última foto se existir
            if str(d['Ultima_Foto']) != "nan" and os.path.exists(str(d['Ultima_Foto'])):
                st.image(d['Ultima_Foto'], caption="Último registro fotográfico", use_container_width=True)
            else:
                st.warning("Ainda não há fotos desta árvore.")
            
            st.metric("XP Total", d['XP'])
            st.write(f"📍 **Local:** {d['Local']}")
            
            # AÇÕES RÁPIDAS
            st.divider()
            c_a, c_b = st.columns(2)
            if c_a.button("💧 Reguei"):
                df.loc[idx, 'XP'] += 10
                salvar_dados(df); st.rerun()
            if c_b.button("💩 Adubei"):
                df.loc[idx, 'XP'] += 20
                salvar_dados(df); st.rerun()

st.sidebar.image("hamtaro.webp", width=100)
