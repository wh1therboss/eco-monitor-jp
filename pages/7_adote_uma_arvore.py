import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# CSS CORRIGIDO: Força cores escuras nos textos e fundos claros nos cards para visibilidade total
st.markdown("""
    <style>
    /* Estilo para os cards de métricas e status */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid #2f855a !important;
    }
    [data-testid="stMetricLabel"] { color: #2d3748 !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #2f855a !important; }
    
    .tree-card { 
        background-color: white; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
    .main { background-color: #f7fafc; }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_ARVORES = 'arvores_adotadas.csv'

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        return pd.read_csv(CAMINHO_ARVORES)
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "XP", "Nivel", "Saude", "Ultimo_Cuidado"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

# --- CATÁLOGO COM LINKS DE IMAGENS ATUALIZADOS ---
especies = {
    "Ipê-Amarelo": {"img": "https://img.freepik.com/fotos-gratis/ipe-amarelo-florescendo-no-parque_23-2148914041.jpg", "desc": "Árvore símbolo do Brasil."},
    "Pau-Brasil": {"img": "https://img.freepik.com/fotos-gratis/arvore-verde-crescendo-na-natureza_23-2148821422.jpg", "desc": "Espécie histórica nativa."},
    "Baobá": {"img": "https://img.freepik.com/fotos-gratis/arvores-de-baoba-majestosas-na-natureza_23-2150754160.jpg", "desc": "Árvore milenar e sagrada."},
    "Sucupira": {"img": "https://img.freepik.com/fotos-gratis/floresta-tropical-exotica-com-vegetacao-densa_23-2150764123.jpg", "desc": "Resistente e medicinal."},
    "Cajueiro": {"img": "https://img.freepik.com/fotos-gratis/deliciosos-cajus-na-arvore_23-2148963953.jpg", "desc": "Nativo do nosso litoral."},
    "Mangue": {"img": "https://img.freepik.com/fotos-gratis/belo-ecossistema-de-manguezais_23-2150711925.jpg", "desc": "Protetor dos rios."},
    "Oiti": {"img": "https://img.freepik.com/fotos-gratis/folhas-verdes-frescas-no-ramo-da-arvore_23-2148130386.jpg", "desc": "A sombra das ruas de JP."},
    "Aroeira": {"img": "https://img.freepik.com/fotos-gratis/detalhe-da-natureza-folhas-verdes_23-2148111956.jpg", "desc": "Nativa de restinga."},
    "Pau-Ferro": {"img": "https://img.freepik.com/fotos-gratis/tronco-de-arvore-com-textura-unica_23-2148954712.jpg", "desc": "Tronco marmorizado."},
    "Pau-d'arco": {"img": "https://img.freepik.com/fotos-gratis/belas-flores-cor-de-rosa-na-arvore_23-2148883652.jpg", "desc": "Beleza exuberante."}
}

st.title("🌳 Adote uma Árvore Nativa")
st.markdown("### LEGO Explorers: Recuperando o Bioma de João Pessoa")

tab1, tab2 = st.tabs(["🌱 Escolher Muda", "🏡 Meu Jardim"])

with tab1:
    st.subheader("Selecione uma espécie para começar")
    cols = st.columns(5)
    for i, (nome, info) in enumerate(especies.items()):
        with cols[i % 5]:
            st.markdown(f'<div class="tree-card">', unsafe_allow_html=True)
            st.image(info['img'], use_container_width=True)
            st.markdown(f"**{nome}**")
            if st.button(f"Adotar", key=f"btn_{nome}"):
                st.session_state.especie_selecionada = nome
            st.markdown('</div>', unsafe_allow_html=True)
    
    if 'especie_selecionada' in st.session_state:
        st.divider()
        with st.form("form_adocao"):
            st.success(f"Espécie: **{st.session_state.especie_selecionada}**")
            n_dono = st.text_input("Seu Nome:")
            n_arvore = st.text_input("Nome da Árvore:")
            if st.form_submit_button("Confirmar Adoção"):
                if n_dono and n_arvore:
                    df = carregar_dados()
                    nova = {"Dono": n_dono, "Nome_Arvore": n_arvore, "Especie": st.session_state.especie_selecionada,
                            "XP": 0, "Nivel": "Semente 🌰", "Saude": 100, "Ultimo_Cuidado": datetime.now().strftime("%d/%m/%Y %H:%M")}
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success("Plantada com sucesso!")
                    time.sleep(1)
                    st.rerun()

with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Adote uma árvore primeiro!")
    else:
        sel = st.selectbox("Escolha sua árvore:", df['Nome_Arvore'].tolist())
        d = df[df['Nome_Arvore'] == sel].iloc[0]
        
        xp = d['XP']
        if xp < 50: niv, icon = "Semente", "🌰"
        elif xp < 150: niv, icon = "Muda", "🌱"
        elif xp < 350: niv, icon = "Jovem", "🌿"
        else: niv, icon = "Adulta", "🌳"
        
        col_icon, col_txt = st.columns([1, 2])
        with col_icon:
            st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{icon}</h1>", unsafe_allow_html=True)
        with col_txt:
            st.metric("Nível", niv)
            st.write(f"**Tutor:** {d['Dono']} | **Espécie:** {d['Especie']}")
            st.write(f"**XP Total:** {xp}")
            st.progress(min((xp % 100)/100, 1.0) if xp < 400 else 1.0)

        st.divider()
        ca1, ca2, ca3 = st.columns(3)
        if ca1.button("💧 Regar (+10)"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 10
            salvar_dados(df); st.toast("💧 Regada!"); time.sleep(0.5); st.rerun()
        if ca2.button("💩 Adubar (+25)"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 25
            salvar_dados(df); st.toast("💩 Adubada!"); time.sleep(0.5); st.rerun()
        if ca3.button("☀️ Sol (+5)"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 5
            salvar_dados(df); st.toast("☀️ Sol recebido!"); time.sleep(0.5); st.rerun()

st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Resetar Jardim"):
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()
