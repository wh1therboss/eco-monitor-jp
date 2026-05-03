import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# CSS para padronizar as fotos e métricas
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
    
    .stImage > img {
        border-radius: 15px;
        height: 180px;
        object-fit: cover;
        border: 2px solid #e2e8f0;
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

# --- LINKS REVISADOS (APENAS NATUREZA) ---
especies = {
    "Ipê-Amarelo": {"img": "https://images.unsplash.com/photo-1622322062602-0e98031a0e98?w=400", "desc": "Flores amarelas intensas."},
    "Pau-Brasil": {"img": "https://images.unsplash.com/photo-1596716790906-8d1844b2f87c?w=400", "desc": "Nativa da Mata Atlântica."},
    "Baobá": {"img": "https://images.unsplash.com/photo-1527489377706-5bf97e608852?w=400", "desc": "Tronco largo e ancestral."},
    "Cajueiro": {"img": "https://images.unsplash.com/photo-1591181520189-adcb0735c65d?w=400", "desc": "Copa ampla e frutos típicos."},
    "Mangue": {"img": "https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=400", "desc": "Raízes aéreas essenciais."},
    "Oiti": {"img": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400", "desc": "Folhas verdes e sombra densa."},
    "Aroeira": {"img": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=400", "desc": "Resistente e nativa."},
    "Pau-Ferro": {"img": "https://images.unsplash.com/photo-1533038590840-1cde6e668a91?w=400", "desc": "Tronco liso marmorizado."},
    "Pau-d'arco": {"img": "https://images.unsplash.com/photo-1520121401995-928cd50d4e27?w=400", "desc": "Floração rosa exuberante."},
    "Pitombeira": {"img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400", "desc": "Frutos em cachos da região."}
}

st.title("🌳 Adote uma Árvore Nativa")
st.markdown("### LEGO Explorers: João Pessoa mais Verde")

tab1, tab2 = st.tabs(["🌱 Catálogo de Mudas", "🏡 Meu Jardim"])

with tab1:
    st.subheader("Escolha sua árvore")
    cols = st.columns(5)
    for i, (nome, info) in enumerate(especies.items()):
        with cols[i % 5]:
            st.image(info['img'], use_container_width=True)
            st.markdown(f"**{nome}**")
            if st.button(f"Adotar", key=f"btn_{nome}"):
                st.session_state.especie_selecionada = nome
    
    if 'especie_selecionada' in st.session_state:
        st.divider()
        with st.form("form_adocao"):
            st.success(f"Espécie: **{st.session_state.especie_selecionada}**")
            n_dono = st.text_input("Tutor (Seu Nome):")
            n_arvore = st.text_input("Nome que dará à árvore:")
            if st.form_submit_button("Confirmar Adoção"):
                if n_dono and n_arvore:
                    df = carregar_dados()
                    nova = {"Dono": n_dono, "Nome_Arvore": n_arvore, "Especie": st.session_state.especie_selecionada,
                            "XP": 0, "Nivel": "Semente 🌰", "Saude": 100, "Ultimo_Cuidado": datetime.now().strftime("%d/%m/%Y %H:%M")}
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success("Platada! Agora cuide dela no jardim.")
                    time.sleep(1)
                    st.rerun()

with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("O jardim está vazio. Escolha uma muda!")
    else:
        sel = st.selectbox("Escolha sua árvore:", df['Nome_Arvore'].tolist())
        d = df[df['Nome_Arvore'] == sel].iloc[0]
        
        xp = d['XP']
        if xp < 50: niv, icon = "Semente", "🌰"
        elif xp < 150: niv, icon = "Muda", "🌱"
        elif xp < 350: niv, icon = "Jovem", "🌿"
        else: niv, icon = "Adulta", "🌳"
        
        c_icon, c_txt = st.columns([1, 2])
        with c_icon:
            st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{icon}</h1>", unsafe_allow_html=True)
        with c_txt:
            st.metric("Fase", niv)
            st.write(f"**Tutor:** {d['Dono']} | **Espécie:** {d['Especie']}")
            st.write(f"**XP:** {xp}")
            st.progress(min((xp % 100)/100, 1.0) if xp < 400 else 1.0)

        st.divider()
        st.markdown("### Painel de Cuidado")
        ca1, ca2, ca3 = st.columns(3)
        if ca1.button("💧 Regar"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 10
            salvar_dados(df); st.toast("💧 Água é vida!"); time.sleep(0.5); st.rerun()
        if ca2.button("💩 Adubar"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 25
            salvar_dados(df); st.toast("💩 Nutrientes adicionados!"); time.sleep(0.5); st.rerun()
        if ca3.button("☀️ Sol"):
            df.loc[df['Nome_Arvore'] == sel, 'XP'] += 5
            salvar_dados(df); st.toast("☀️ Energia pura!"); time.sleep(0.5); st.rerun()

st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Resetar Tudo"):
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()
