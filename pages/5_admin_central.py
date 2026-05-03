import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Admin | Monitoramento JP", layout="wide")

CAMINHO_DENUNCIAS = 'denuncias.csv'
CAMINHO_ARVORES = 'arvores_adotadas.csv'

# Login Simples
if 'admin_logado' not in st.session_state:
    st.title("🔐 Acesso Restrito")
    pwd = st.text_input("Senha Admin:", type="password")
    if st.button("Entrar"):
        if pwd == "09122307": # Sua senha
            st.session_state.admin_logado = True
            st.rerun()
        else: st.error("Senha incorreta!")
    st.stop()

st.title("📊 Central de Comando LEGO Explorers")

aba_lixo, aba_arvore = st.tabs(["🗑️ Resíduos Urbanos", "🌳 Monitoramento Verde"])

# GESTÃO DE LIXO
with aba_lixo:
    if os.path.exists(CAMINHO_DENUNCIAS):
        df_lixo = pd.read_csv(CAMINHO_DENUNCIAS)
        st.dataframe(df_lixo, use_container_width=True)
    else: st.info("Sem denúncias de lixo.")

# MONITORAMENTO VERDE (FOTOS E XP)
with aba_arvore:
    if os.path.exists(CAMINHO_ARVORES):
        df_tree = pd.read_csv(CAMINHO_ARVORES)
        
        m1, m2 = st.columns(2)
        m1.metric("Árvores Ativas", len(df_tree))
        m2.metric("XP Total da Cidade", df_tree['XP'].sum())
        
        st.write("---")
        for i, row in df_tree.iterrows():
            with st.expander(f"🌳 {row['Nome_Arvore']} - Tutor: {row['Dono']}"):
                col_info, col_img = st.columns([2, 1])
                with col_info:
                    st.write(f"**Espécie:** {row['Especie']}")
                    st.write(f"**Local:** {row['Local']}")
                    st.write(f"**Saúde:** {row['Status_Saude']}")
                    st.write(f"**XP Acumulado:** {row['XP']}")
                    st.write(f"**Motivo:** {row['Motivo']}")
                with col_img:
                    f_path = str(row['Ultima_Foto'])
                    if f_path != "Sem registro" and os.path.exists(f_path):
                        st.image(f_path, caption="Foto enviada pelo tutor", width=250)
                    else:
                        st.warning("Sem foto registrada.")
    else:
        st.info("Nenhuma árvore foi adotada ainda.")

st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🚪 Sair"):
    del st.session_state.admin_logado
    st.rerun()
