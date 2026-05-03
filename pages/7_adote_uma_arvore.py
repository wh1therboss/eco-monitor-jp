import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# CSS para o visual "Verde/Natureza"
st.markdown("""
    <style>
    .tree-card { background-color: #f0fff4; padding: 20px; border-radius: 15px; border: 2px solid #2f855a; text-align: center; }
    .status-bar { background-color: #e2e8f0; border-radius: 10px; height: 20px; width: 100%; margin: 10px 0; }
    .status-fill { background-color: #48bb78; height: 100%; border-radius: 10px; transition: width 0.5s; }
    .main { background-color: #f7fafc; }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_ARVORES = 'arvores_adotadas.csv'

# --- BANCO DE DADOS DAS ÁRVORES ---
def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        return pd.read_csv(CAMINHO_ARVORES)
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "XP", "Nivel", "Saude", "Ultimo_Cuidado"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

# --- CATÁLOGO DE ESPÉCIES NATIVAS ---
especies = {
    "Ipê Amarelo": {"img": "https://images.unsplash.com/photo-1622322062602-0e98031a0e98?w=400", "desc": "Símbolo do Brasil, floresce no inverno/primavera."},
    "Pau-Brasil": {"img": "https://images.unsplash.com/photo-1613063412534-1925343567df?w=400", "desc": "Nativa da Mata Atlântica, espécie histórica e protegida."},
    "Baobá": {"img": "https://images.unsplash.com/photo-1518992028580-6d57bd80f2dd?w=400", "desc": "Árvore milenar presente em pontos históricos de JP."},
    "Mangue Vermelho": {"img": "https://images.unsplash.com/photo-1590604518086-7a4f32a853bc?w=400", "desc": "Essencial para o ecossistema dos estuários da Paraíba."}
}

st.title("🌳 Adote uma Árvore e Proteja nosso Bioma")
st.write("Escolha uma muda, dê um nome a ela e ajude-a a crescer cuidando diariamente!")

tab1, tab2 = st.tabs(["🌱 Adotar Nova Árvore", "🏡 Meu Jardim"])

# --- TABELA 1: ADOÇÃO ---
with tab1:
    st.subheader("Selecione sua muda nativa")
    cols = st.columns(4)
    
    escolha_especie = None
    for i, (nome, info) in enumerate(especies.items()):
        with cols[i]:
            st.image(info['img'], use_container_width=True)
            st.markdown(f"**{nome}**")
            st.caption(info['desc'])
            if st.button(f"Escolher {nome}", key=nome):
                st.session_state.especie_selecionada = nome

    if 'especie_selecionada' in st.session_state:
        st.divider()
        with st.form("form_adocao"):
            st.success(f"Espécie selecionada: **{st.session_state.especie_selecionada}**")
            nome_dono = st.text_input("Seu Nome:")
            nome_arvore = st.text_input("Dê um nome para sua árvore:")
            
            if st.form_submit_button("Confirmar Adoção! 🌱"):
                if nome_dono and nome_arvore:
                    df = carregar_dados()
                    nova_arvore = {
                        "Dono": nome_dono,
                        "Nome_Arvore": nome_arvore,
                        "Especie": st.session_state.especie_selecionada,
                        "XP": 0,
                        "Nivel": "Semente 🌰",
                        "Saude": 100,
                        "Ultimo_Cuidado": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    df = pd.concat([df, pd.DataFrame([nova_arvore])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success(f"Parabéns! {nome_arvore} agora faz parte do bioma de João Pessoa!")
                else:
                    st.error("Preencha todos os campos!")

# --- TABELA 2: CUIDADOS E PROGRESSO ---
with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Ainda não há árvores adotadas. Comece adotando uma!")
    else:
        st.subheader("Suas Árvores")
        lista_arvores = df['Nome_Arvore'].tolist()
        arvore_foco = st.selectbox("Selecione qual árvore cuidar:", lista_arvores)
        
        dados_arvore = df[df['Nome_Arvore'] == arvore_foco].iloc[0]
        
        # Lógica de Nível baseada em XP
        xp = dados_arvore['XP']
        if xp < 50: nivel = "Semente 🌰"
        elif xp < 150: nivel = "Muda 🌱"
        elif xp < 300: nivel = "Árvore Jovem 🌿"
        else: nivel = "Árvore Adulta 🌳"
        
        # Interface de Status
        c1, c2 = st.columns([1, 2])
        with c1:
            if "Semente" in nivel: st.title("🌰")
            elif "Muda" in nivel: st.title("🌱")
            elif "Jovem" in nivel: st.title("🌿")
            else: st.title("🌳")
            st.write(f"**Nível:** {nivel}")
        
        with c2:
            st.markdown(f"### {dados_arvore['Nome_Arvore']} ({dados_arvore['Especie']})")
            st.write(f"**Tutor:** {dados_arvore['Dono']}")
            
            # Barra de XP
            progresso_xp = min(xp % 100 / 100, 1.0)
            st.write(f"**Experiência (XP):** {xp}")
            st.progress(progresso_xp)
            
            # Botões de Ação
            st.write("**Ações de Cuidado:**")
            ca1, ca2, ca3 = st.columns(3)
            
            if ca1.button("💧 Regar (+10 XP)"):
                df.loc[df['Nome_Arvore'] == arvore_foco, 'XP'] += 10
                df.loc[df['Nome_Arvore'] == arvore_foco, 'Ultimo_Cuidado'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                salvar_dados(df)
                st.toast("Você regou sua árvore! ✨")
                time.sleep(1)
                st.rerun()

            if ca2.button("💩 Adubar (+25 XP)"):
                df.loc[df['Nome_Arvore'] == arvore_foco, 'XP'] += 25
                salvar_dados(df)
                st.toast("Solo fortalecido! 🌟")
                time.sleep(1)
                st.rerun()
                
            if ca3.button("☀️ Sol (+5 XP)"):
                df.loc[df['Nome_Arvore'] == arvore_foco, 'XP'] += 5
                salvar_dados(df)
                st.toast("Fotossíntese a todo vapor! ☀️")
                time.sleep(1)
                st.rerun()

st.sidebar.image("hamtaro.webp", width=120)
st.sidebar.title("LEGO Explorers")
st.sidebar.info("Protegendo o bioma de João Pessoa através da tecnologia.")
