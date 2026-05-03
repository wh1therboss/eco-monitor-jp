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

# --- DEFINIÇÃO DAS ABAS (Isso corrige o NameError) ---
tab1, tab2 = st.tabs(["📜 Adotar e Assinar", "🏡 Meu Jardim"])

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
        st.subheader("📝 Termo de Compromisso e Tutoria")
        
        with st.form("form_contrato"):
            c1, c2 = st.columns(2)
            with c1:
                tutor = st.text_input("Nome Completo do Tutor:")
                arvore_nome = st.text_input("Nome de Batismo da Árvore:")
            with c2:
                local = st.text_input("Localização do Plantio (Bairro/Rua):")
                motivo = st.text_area("Justificativa da Adoção:")

            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 25px; border-radius: 5px; color: #1e293b; border-left: 10px solid #2f855a; font-family: serif; line-height: 1.6;">
                <h2 style="text-align: center; color: #2f855a; margin-top: 0;">ESTADO DA PARAÍBA</h2>
                <h3 style="text-align: center;">Termo de Responsabilidade Ambiental № {datetime.now().strftime('%y%m%d')}-JP</h3>
                <p>Eu, <b>{tutor if tutor else "________________"}</b>, assumo a tutoria da árvore <b>{arvore_nome if arvore_nome else "________________"}</b>, 
                da espécie <b>{st.session_state.esp_sel}</b>.</p>
                <p>Comprometo-me a fornecer água, proteção e registrar sua evolução diariamente via registro fotográfico no sistema <b>LEGO Explorers</b>.</p>
                <p style="text-align: center; border-top: 1px solid #ccc; padding-top: 10px;">Assinado em {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            aceite = st.checkbox("Aceito integralmente os termos de responsabilidade.")
            
            if st.form_submit_button("ASSINAR E REGISTRAR TUTORIA ✒️"):
                if tutor and arvore_nome and local and aceite:
                    df = carregar_dados()
                    nova = {"Dono": tutor, "Nome_Arvore": arvore_nome, "Especie": st.session_state.esp_sel,
                            "Local": local, "Motivo": motivo, "XP": 0, "Status_Saude": "Excelente", "Ultima_Foto": "Sem registro"}
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success("Tutoria registrada!")
                    del st.session_state.esp_sel
                    time.sleep(2); st.rerun()
                else: st.error("Preencha todos os campos!")

with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Nenhuma árvore adotada.")
    else:
        sel = st.selectbox("Escolha sua árvore:", df['Nome_Arvore'].tolist())
        idx = df[df['Nome_Arvore'] == sel].index[0]
        d = df.loc[idx]
        
        c_cam, c_stat = st.columns(2)
        with c_cam:
            st.subheader("📸 Diário de Fotos")
            if st.button("📷 Abrir Câmera para Registro"):
                st.session_state.cam_on = True
            
            if st.session_state.get('cam_on'):
                foto = st.camera_input("Capture o crescimento!")
                if foto:
                    path = f"fotos_arvores/{sel}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
                    with open(path, "wb") as f: f.write(foto.getbuffer())
                    df.loc[idx, 'Ultima_Foto'] = path
                    df.loc[idx, 'XP'] += 50
                    salvar_dados(df)
                    st.session_state.cam_on = False
                    st.success("Foto salva! +50 XP"); time.sleep(1); st.rerun()
                if st.button("❌ Fechar"):
                    st.session_state.cam_on = False; st.rerun()
        
        with c_stat:
            st.subheader("📊 Status")
            f_p = str(d['Ultima_Foto'])
            if f_p != "Sem registro" and os.path.exists(f_p):
                st.image(f_p, caption=f"Foto de {sel}", use_container_width=True)
            st.metric("XP Verde", d['XP'])

st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Resetar Tudo (Limpa Erros)"):
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()
