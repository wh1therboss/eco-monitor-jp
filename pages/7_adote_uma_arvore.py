import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

st.markdown("""
    <style>
    .tree-card { background-color: #f0fff4; padding: 20px; border-radius: 15px; border: 2px solid #2f855a; text-align: center; }
    [data-testid="stMetricValue"] { color: #2f855a !important; }
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

# --- CATÁLOGO COMPLETO DE ESPÉCIES NATIVAS DE JOÃO PESSOA ---
especies = {
    "Ipê-Amarelo": {"img": "https://images.unsplash.com/photo-1622322062602-0e98031a0e98?w=400", "desc": "Árvore símbolo do Brasil, comum na Mata Atlântica paraibana."},
    "Pau-Brasil": {"img": "https://images.unsplash.com/photo-1613063412534-1925343567df?w=400", "desc": "Espécie histórica que deu nome ao país, nativa das nossas matas."},
    "Baobá": {"img": "https://images.unsplash.com/photo-1518992028580-6d57bd80f2dd?w=400", "desc": "Árvores majestosas, JP possui exemplares históricos famosos."},
    "Sucupira": {"img": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=400", "desc": "Resistente e medicinal, muito presente no ecossistema de Tabuleiro."},
    "Cajueiro": {"img": "https://images.unsplash.com/photo-1621460241093-0667e41b7167?w=400", "desc": "Nativo do litoral, essencial para a fauna e culinária local."},
    "Mangue-Vermelho": {"img": "https://images.unsplash.com/photo-1590604518086-7a4f32a853bc?w=400", "desc": "Berço da vida marinha, protege as margens dos nossos rios."},
    "Oiti": {"img": "https://images.unsplash.com/photo-1596716790906-8d1844b2f87c?w=400", "desc": "A 'sombra' clássica das ruas de João Pessoa."},
    "Aroeira-da-Praia": {"img": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400", "desc": "Nativa de restinga, ajuda na fixação das dunas no nosso litoral."},
    "Pau-Ferro": {"img": "https://images.unsplash.com/photo-1463936575829-25148e1db1b8?w=400", "desc": "Tronco liso e marmorizado, belíssima para arborização urbana."},
    "Pau-d'arco": {"img": "https://images.unsplash.com/photo-1520121401995-928cd50d4e27?w=400", "desc": "Outro nome dado aos Ipês, variando entre roxo, rosa e branco."}
}

st.title("🌳 Adote uma Árvore Nativa")
st.markdown("### LEGO Explorers: Recuperando o Bioma de João Pessoa")

tab1, tab2 = st.tabs(["🌱 Escolher Muda", "🏡 Meu Jardim"])

with tab1:
    st.subheader("Catálogo de Espécies da Nossa Região")
    
    # Grid de 5 colunas para caber todas as espécies de forma organizada
    cols = st.columns(5)
    for i, (nome, info) in enumerate(especies.items()):
        idx_col = i % 5
        with cols[idx_col]:
            st.image(info['img'], use_container_width=True)
            st.markdown(f"**{nome}**")
            if st.button(f"Adotar {nome}", key=f"btn_{nome}"):
                st.session_state.especie_selecionada = nome
    
    if 'especie_selecionada' in st.session_state:
        st.divider()
        with st.form("form_adocao"):
            st.success(f"Você escolheu o **{st.session_state.especie_selecionada}**")
            n_dono = st.text_input("Seu Nome:")
            n_arvore = st.text_input("Nome da sua Árvore:")
            if st.form_submit_button("Finalizar Adoção"):
                if n_dono and n_arvore:
                    df = carregar_dados()
                    nova = {
                        "Dono": n_dono, "Nome_Arvore": n_arvore, "Especie": st.session_state.especie_selecionada,
                        "XP": 0, "Nivel": "Semente 🌰", "Saude": 100, "Ultimo_Cuidado": datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success(f"{n_arvore} foi plantada virtualmente!")
                else: st.error("Preencha os nomes!")

with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("O jardim está vazio. Adote uma árvore na aba ao lado!")
    else:
        st.subheader("Acompanhe o Crescimento")
        selecionada = st.selectbox("Qual árvore você quer cuidar?", df['Nome_Arvore'].tolist())
        d = df[df['Nome_Arvore'] == selecionada].iloc[0]
        
        # Sistema de Nível
        xp = d['XP']
        if xp < 50: niv, icon = "Semente", "🌰"
        elif xp < 150: niv, icon = "Muda", "🌱"
        elif xp < 350: niv, icon = "Jovem", "🌿"
        else: niv, icon = "Adulta", "🌳"
        
        col_img, col_info = st.columns([1, 2])
        with col_img:
            st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{icon}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>Nível: {niv}</h3>", unsafe_allow_html=True)
        
        with col_info:
            st.markdown(f"## {d['Nome_Arvore']}")
            st.caption(f"Espécie: {d['Especie']} | Tutor: {d['Dono']}")
            st.write(f"**Experiência Atual:** {xp} XP")
            st.progress(min((xp % 100) / 100, 1.0) if xp < 400 else 1.0)
            
            st.write("---")
            st.markdown("### Ações de Cuidado")
            ca1, ca2, ca3 = st.columns(3)
            
            if ca1.button("💧 Regar (+10)"):
                df.loc[df['Nome_Arvore'] == selecionada, 'XP'] += 10
                salvar_dados(df); st.toast("Regado!"); time.sleep(0.5); st.rerun()
            
            if ca2.button("💩 Adubar (+25)"):
                df.loc[df['Nome_Arvore'] == selecionada, 'XP'] += 25
                salvar_dados(df); st.toast("Nutrido!"); time.sleep(0.5); st.rerun()

            if ca3.button("☀️ Sol (+5)"):
                df.loc[df['Nome_Arvore'] == selecionada, 'XP'] += 5
                salvar_dados(df); st.toast("Luz recebida!"); time.sleep(0.5); st.rerun()

st.sidebar.image("hamtaro.webp", width=100)
st.sidebar.markdown("### LEGO EXPLORERS")
if st.sidebar.button("🗑️ Resetar Jardim (Cuidado)"):
    if os.path.exists(CAMINHO_ARVORES):
        os.remove(CAMINHO_ARVORES)
        st.rerun()
