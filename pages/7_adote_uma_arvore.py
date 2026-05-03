import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# Criar pasta para fotos se não existir
if not os.path.exists("fotos_arvores"):
    os.makedirs("fotos_arvores")

CAMINHO_ARVORES = 'arvores_adotadas.csv'

# Lista oficial de mudas (Emojis)
especies = {
    "Ipê-Amarelo": "🌼", "Pau-Brasil": "🌳", "Baobá": "🪵", 
    "Cajueiro": "🍎", "Mangue": "🦀", "Oiti": "🍃", 
    "Aroeira": "🌿", "Pau-Ferro": "🏗️", "Pau-d'arco": "🌸", "Pitombeira": "🍒"
}

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        df = pd.read_csv(CAMINHO_ARVORES)
        if "Ultima_Foto" not in df.columns:
            df["Ultima_Foto"] = "Sem registro"
        return df
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "Motivo", "XP", "Status_Saude", "Ultima_Foto"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

st.title("🌳 Sistema de Tutoria Ambiental")

tab1, tab2 = st.tabs(["📜 Adotar e Assinar", "🏡 Meu Jardim"])

# --- TABELA 1: ESCOLHA E CONTRATO ---
with tab1:
    st.subheader("1. Selecione sua Muda Nativa")
    cols = st.columns(5)
    
    for i, (nome, emoji) in enumerate(especies.items()):
        with cols[i % 5]:
            st.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
            if st.button(f"Selecionar {nome}", key=f"btn_{nome}"):
                st.session_state.esp_sel = nome
                st.session_state.emo_sel = emoji

    if 'esp_sel' in st.session_state:
        st.divider()
        st.subheader("2. Formalização do Contrato")
        
        with st.form("form_contrato"):
            c1, c2 = st.columns(2)
            with c1:
                tutor = st.text_input("Seu Nome Completo:")
                arvore_nome = st.text_input("Nome da Árvore:")
            with c2:
                local = st.text_input("Localização (Bairro/Rua):")
                motivo = st.text_area("Por que quer adotar?")

            st.markdown(f"""
            <div style="background-color: #f1f5f9; padding: 15px; border-radius: 10px; color: #000; border: 2px solid #2f855a;">
                <h4 style="text-align: center;">CONTRATO DE TUTORIA № {datetime.now().strftime('%H%M%S')}</h4>
                <p>Eu, <b>{tutor if tutor else "___"}</b>, assumo a responsabilidade pela muda de <b>{st.session_state.esp_sel}</b>.</p>
                <p>Comprometo-me a regar, monitorar e registrar sua evolução no sistema.</p>
            </div>
            """, unsafe_allow_html=True)
            
            aceite = st.checkbox("Aceito os termos de responsabilidade ambiental.")
            
            if st.form_submit_button("ASSINAR E ADOTAR"):
                if tutor and arvore_nome and local and aceite:
                    df = carregar_dados()
                    nova = {
                        "Dono": tutor, "Nome_Arvore": arvore_nome, "Especie": st.session_state.esp_sel,
                        "Local": local, "Motivo": motivo, "XP": 0, "Status_Saude": "Excelente", "Ultima_Foto": "Sem registro"
                    }
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success("Tudo pronto! Sua árvore te espera no Jardim.")
                    del st.session_state.esp_sel
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Preencha tudo e assine o contrato!")

# --- TABELA 2: MEU JARDIM E CÂMERA ---
with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Escolha uma muda na aba ao lado primeiro!")
    else:
        sel = st.selectbox("Escolha sua árvore:", df['Nome_Arvore'].tolist())
        idx = df[df['Nome_Arvore'] == sel].index[0]
        d = df.loc[idx]
        
        col_cam, col_status = st.columns(2)
        
        with col_cam:
            st.subheader("📸 Diário de Fotos")
            if "ativar_camera" not in st.session_state: st.session_state.ativar_camera = False

            if not st.session_state.ativar_camera:
                if st.button("📷 Abrir Câmera para Registro"):
                    st.session_state.ativar_camera = True
                    st.rerun()
            else:
                f_captura = st.camera_input("Capture o crescimento!")
                if f_captura:
                    path = f"fotos_arvores/{sel}_{datetime.now().strftime('%Y%m%d')}.png"
                    with open(path, "wb") as f: f.write(f_captura.getbuffer())
                    df.loc[idx, 'Ultima_Foto'] = path
                    df.loc[idx, 'XP'] += 50
                    salvar_dados(df)
                    st.session_state.ativar_camera = False
                    st.success("Foto salva! +50 XP")
                    time.sleep(1); st.rerun()
                if st.button("❌ Cancelar"):
                    st.session_state.ativar_camera = False
                    st.rerun()

        with col_status:
            st.subheader("📊 Status")
            f_path = str(d['Ultima_Foto'])
            if f_path != "Sem registro" and os.path.exists(f_path):
                st.image(f_path, caption=f"Foto de hoje: {sel}", use_container_width=True)
            else:
                st.warning("Nenhuma foto enviada hoje.")
            
            st.metric("XP Verde", d['XP'])
            st.write(f"🏥 Saude: {d['Status_Saude']} | 📍 Local: {d['Local']}")
            
            # Ações rápidas
            c_r, c_a = st.columns(2)
            if c_r.button("💧 Regar"):
                df.loc[idx, 'XP'] += 10; salvar_dados(df); st.rerun()
            if c_a.button("💩 Adubar"):
                df.loc[idx, 'XP'] += 20; salvar_dados(df); st.rerun()

st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Resetar Jardim (Limpa Erros)"):
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()
