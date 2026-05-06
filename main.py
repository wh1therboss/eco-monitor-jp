import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide", page_icon="🍃")

# --- CSS PARA ESCONDER A SIDEBAR E CRIAR O DESIGN PERSONALIZADO ---
st.markdown("""
    <style>
        /* Esconde o menu lateral original */
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
        
        /* Fundo Preto para o corpo do site durante a intro */
        .main { background-color: #000000; }

        /* Barra de Navegação Superior Estilo Inovatec */
        .nav-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #111111;
            padding: 15px;
            position: sticky;
            top: 0;
            z-index: 999;
            border-bottom: 2px solid #2f855a;
            gap: 25px;
        }
        .nav-link {
            color: white !important;
            text-decoration: none;
            font-weight: bold;
            font-family: 'sans-serif';
            transition: 0.3s;
        }
        .nav-link:hover { color: #2f855a !important; }

        /* Animação da Folha e Palavras */
        .intro-screen {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: black;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        
        .folha-anim {
            font-size: 100px;
            animation: crescer 3s ease-out forwards;
        }

        @keyframes crescer {
            0% { transform: scale(0) rotate(-45deg); opacity: 0; }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }

        .palavra-anim {
            color: white;
            font-size: 30px;
            margin-top: 20px;
            font-family: 'monospace';
            letter-spacing: 5px;
            text-transform: uppercase;
        }
        
        .bioglow-final {
            background-color: #2f855a;
            color: white;
            padding: 10px 40px;
            font-size: 60px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DA ANIMAÇÃO DE ABERTURA ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder.container():
            st.markdown(f"""
                <div class="intro-screen">
                    <div class="folha-anim">🍃</div>
                    <div class="palavra-anim">{p}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(1.2) # Velocidade da troca das palavras
    
    # Tela Final da Intro: BIOGLOW
    with placeholder.container():
        st.markdown(f"""
            <div class="intro-screen">
                <div style="color: white; font-size: 20px; margin-bottom: 10px; letter-spacing: 10px;">LEGO EXPLORERS</div>
                <div class="folha-anim">🍃</div>
                <div class="bioglow-final">BIOGLOW</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- MENU SUPERIOR (APARECE DEPOIS DA INTRO) ---
st.markdown(f"""
    <div class="nav-container">
        <a class="nav-link" href="/adote_uma_arvore" target="_self">🌳 ADOTAR</a>
        <a class="nav-link" href="/Ilumina_JP" target="_self">💡 ILUMINA JP</a>
        <a class="nav-link" href="/acompanhar_denuncias" target="_self">🕵️ STATUS</a>
        <a class="nav-link" href="/admin_central" target="_self">🔐 ADMIN</a>
    </div>
""", unsafe_allow_html=True)

# --- CONTEÚDO DA HOME ---
st.title("Bem-vindo ao BIOGLOW")
st.write("Inovação tecnológica para uma João Pessoa mais sustentável.")
