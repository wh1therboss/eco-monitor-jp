import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide", page_icon="🍃")

# --- CSS DEFINITIVO: FUNDO PRETO, MENU NO TOPO E ANIMAÇÕES ---
st.markdown("""
    <style>
        /* Remove paddings padrão do Streamlit para o menu colar no topo */
        .block-container { padding-top: 0rem; padding-bottom: 0rem; }
        [data-testid="stHeader"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        
        /* Fundo do site */
        .main { background-color: #000000; }

        /* Menu Superior 'Colado' Estilo Inovatec */
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #000000;
            padding: 20px 0;
            border-bottom: 1px solid #222;
            width: 100%;
            margin-bottom: 40px;
        }
        .nav-link {
            color: white !important;
            text-decoration: none;
            font-weight: 500;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0 20px;
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: 0.3s;
        }
        .nav-link:hover { color: #2f855a !important; }

        /* Tela de Introdução */
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
        
        /* Folha Branca Minimalista */
        .folha-branca {
            font-size: 120px;
            color: white;
            filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
            animation: crescer 0.8s ease-out forwards;
        }

        @keyframes crescer {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .palavra-anim {
            color: white;
            font-size: 22px;
            margin-top: 30px;
            font-family: 'Arial', sans-serif;
            letter-spacing: 8px;
            text-transform: uppercase;
            font-weight: 300;
        }
        
        .bioglow-box {
            background-color: #2f855a;
            color: white;
            padding: 15px 50px;
            font-size: 45px;
            font-weight: bold;
            margin-top: 25px;
            letter-spacing: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DA INTRO (RÁPIDA) ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder.container():
            st.markdown(f"""
                <div class="intro-screen">
                    <div class="folha-branca">🍃</div>
                    <div class="palavra-anim">{p}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.6) # Velocidade rápida mas legível
    
    # BIOGLOW FINAL
    with placeholder.container():
        st.markdown(f"""
            <div class="intro-screen">
                <div style="color: rgba(255,255,255,0.6); font-size: 14px; letter-spacing: 12px; margin-bottom: 20px;">LEGO EXPLORERS</div>
                <div class="folha-branca">🍃</div>
                <div class="bioglow-box">BIOGLOW</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.8)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- CONTEÚDO PÓS-INTRO ---
# Menu "Colado" no topo
st.markdown("""
    <div class="nav-container">
        <a class="nav-link" href="/adote_uma_arvore" target="_self">Adotar</a>
        <a class="nav-link" href="/Ilumina_JP" target="_self">Ilumina JP</a>
        <a class="nav-link" href="/acompanhar_denuncias" target="_self">Status</a>
        <a class="nav-link" href="/admin_central" target="_self">Admin</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:white; text-align:center;'>Bem-vindo ao BIOGLOW</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#888; text-align:center;'>Inovação tecnológica para uma João Pessoa mais sustentável.</p>", unsafe_allow_html=True)
