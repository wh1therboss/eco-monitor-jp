import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# CSS para o Contrato e Métricas
st.markdown("""
    <style>
    .contrato-box {
        background-color: #f8fafc;
        padding: 20px;
        border: 2px solid #2f855a;
        border-radius: 10px;
        color: #1e293b;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #2f855a !important;
    }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_ARVORES = 'arvores_adotadas.csv'

especies = {
    "Ipê-Amarelo": "🌼", "Pau-Brasil": "🌳", "Baobá": "🪵", 
    "Cajueiro": "🍎", "Mangue": "🦀", "Oiti": "🍃", 
    "Aroeira": "🌿", "Pau-Ferro": "🏗️", "Pau-d'arco": "🌸", "Pitombeira": "🍒"
}

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        return pd.read_csv(CAMINHO_ARVORES)
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "Motivo", "XP", "Status_Saude"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

st.title("🌳 Sistema de Adoção e Tutoria Ambiental")

tab1, tab2 = st.tabs(["📜 Formalizar Adoção", "🏡 Central de Monitoramento"])

with tab1:
    st.subheader("1. Escolha sua Espécie")
    cols = st.columns(5)
    for i, (nome, emoji) in enumerate(especies.items()):
        with cols[i % 5]:
            st.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
            if st.button(f"Selecionar {nome}", key=f"sel_{nome}"):
                st.session_state.esp_sel = nome
                st.session_state.emo_sel = emoji

    if 'esp_sel' in st.session_state:
        st.divider()
        st.subheader("2. Termo de Compromisso Ambiental")
        
        with st.form("form_contrato"):
            col_a, col_b = st.columns(2)
            with col_a:
                nome_tutor = st.text_input("Nome Completo do Tutor:")
                nome_tree = st.text_input("Nome de Batismo da Árvore:")
            with col_b:
                local_plantio = st.text_input("Local da Adoção (Ex: Bairro/Rua ou Meu Quintal):")
                motivo_adocao = st.text_area("Por que você deseja adotar esta árvore?")

            # O CONTRATO
            st.markdown(f"""
            <div class="contrato-box">
                <h3 style="text-align:center;">CONTRATO DE ADOÇÃO VEGETAL № {datetime.now().strftime('%Y%m%d%H%M')}</h3>
                <p>Eu, <b>{nome_tutor if nome_tutor else "________"}</b>, assumo a partir desta data a tutoria da árvore 
                <b>{nome_tree if nome_tree else "________"}</b>, da espécie <b>{st.session_state.esp_sel}</b>.</p>
                <p><b>CLÁUSULA 1:</b> O tutor compromete-se a fornecer água, nutrientes e proteção contra pragas.</p>
                <p><b>CLÁUSULA 2:</b> O monitoramento da saúde deve ser reportado periodicamente no sistema LEGO Explorers.</p>
                <p><b>CLÁUSULA 3:</b> Esta árvore passa a ser um patrimônio simbólico do bioma de João Pessoa.</p>
                <p style="text-align:right;">João Pessoa, {datetime.now().strftime('%d de %B de %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            aceite = st.checkbox("Eu li e concordo com os termos do contrato de tutoria.")
            
            if st.form_submit_button("ASSINAR E PLANTAR 🖋️"):
                if nome_tutor and nome_tree and local_plantio and aceite:
                    df = carregar_dados()
                    nova = {
                        "Dono": nome_tutor, "Nome_Arvore": nome_tree, 
                        "Especie": st.session_state.esp_sel, "Local": local_plantio,
                        "Motivo": motivo_adocao, "XP": 0, "Status_Saude": "Excelente"
                    }
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success("Contrato assinado! A árvore agora é sua responsabilidade.")
                    time.sleep(2)
                    del st.session_state.esp_sel
                    st.rerun()
                else:
                    st.error("Por favor, preencha todos os campos e aceite o contrato.")

with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Nenhuma árvore sob custódia no momento.")
    else:
        selecionada = st.selectbox("Selecione sua árvore para gerenciar:", df['Nome_Arvore'].tolist())
        idx = df[df['Nome_Arvore'] == selecionada].index[0]
        d = df.loc[idx]
        
        # Lógica de XP e Nível
        xp = d['XP']
        if xp < 50: niv, icon = "Semente", "🌰"
        elif xp < 150: niv, icon = "Muda", "🌱"
        elif xp < 350: niv, icon = "Jovem", "🌿"
        else: niv, icon = "Adulta", "🌳"
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{icon}</h1>", unsafe_allow_html=True)
            st.metric("Saúde do Bioma", d['Status_Saude'])
        with c2:
            st.subheader(f"Árvore: {d['Nome_Arvore']}")
            st.write(f"📍 **Local:** {d['Local']}")
            st.write(f"📖 **Motivação:** {d['Motivo']}")
            st.progress(min((xp % 100)/100, 1.0) if xp < 400 else 1.0)
            st.write(f"XP acumulado: {xp} (Fase: {niv})")

        st.divider()
        st.subheader("🕹️ Painel de Ações do Tutor")
        ca1, ca2, ca3 = st.columns(3)
        
        with ca1:
            if st.button("💧 Regar Planta"):
                df.loc[idx, 'XP'] += 15
                salvar_dados(df); st.toast("Hidratação concluída!"); time.sleep(0.5); st.rerun()
        
        with ca2:
            saude_report = st.selectbox("Monitorar Saúde:", ["Excelente", "Precisando de Nutrientes", "Ataque de Pragas", "Seca"])
            if st.button("Relatar Estado"):
                df.loc[idx, 'Status_Saude'] = saude_report
                df.loc[idx, 'XP'] += 20
                salvar_dados(df); st.success("Relatório de saúde enviado!"); time.sleep(0.5); st.rerun()
        
        with ca3:
            if st.button("💩 Adubar Solo"):
                df.loc[idx, 'XP'] += 30
                salvar_dados(df); st.toast("Nutrientes aplicados!"); time.sleep(0.5); st.rerun()

st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Revogar Todas as Tutorias"):
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()
