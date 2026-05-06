import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide")

# --- CSS: ESTILO INOVATEC TOTAL WHITE ---
st.markdown("""
    <style>
        .block-container { padding-top: 0rem; padding-bottom: 0rem; }
        [data-testid="stHeader"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        .main { background-color: #000000; }

        /* Menu Superior Colado */
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #000000;
            padding: 30px 0;
            border-bottom: 1px solid #111;
            width: 100%;
        }
        .nav-link {
            color: #FFFFFF !important;
            text-decoration: none;
            font-weight: 300;
            margin: 0 30px;
            font-size: 11px;
            letter-spacing: 4px;
            text-transform: uppercase;
            opacity: 0.5;
        }

        /* Intro Screen */
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

        /* SVG DA FOLHA - BRANCO PURO */
        .folha-svg {
            width: 120px;
            height: 120px;
            fill: #FFFFFF; /* AQUI ESTA A COR BRANCA REAL */
            animation: flash-fast 0.4s ease-out forwards;
        }

        @keyframes flash-fast {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .palavra-anim {
            color: #FFFFFF;
            font-size: 16px;
            margin-top: 40px;
            font-family: 'Inter', sans-serif;
            letter-spacing: 10px;
            text-transform: uppercase;
            font-weight: 100;
        }
        
        .bioglow-box-white {
            border: 1px solid #FFFFFF;
            color: #FFFFFF;
            padding: 15px 50px;
            font-size: 40px;
            font-weight: 100;
            margin-top: 40px;
            letter-spacing: 18px;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# --- SVG DA FOLHA (Substitui o emoji verde) ---
svg_folha = """
<svg class="folha-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/>
</svg>
"""

# --- LÓGICA DA INTRO (ULTRA RÁPIDA) ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder.container():
            st.markdown(f"""
                <div class="intro-screen">
                    {svg_folha}
                    <div class="palavra-anim">{p}</div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.4)
    
    with placeholder.container():
        st.markdown(f"""
            <div class="intro-screen">
                <div style="color: #444; font-size: 10px; letter-spacing: 12px; margin-bottom: 30px;">LEGO EXPLORERS</div>
                {svg_folha}
                <div class="bioglow-box-white">BIOGLOW</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- MENU SUPERIOR ---
st.markdown("""
    <div class="nav-container">
        <a class="nav-link" href="/adote_uma_arvore" target="_self">Adotar</a>
        <a class="nav-link" href="/Ilumina_JP" target="_self">Ilumina JP</a>
        <a class="nav-link" href="/acompanhar_denuncias" target="_self">Status</a>
        <a class="nav-link" href="/admin_central" target="_self">Admin</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:white; text-align:center; font-weight:100; letter-spacing:15px; margin-top:100px;'>BIOGLOW</h1>", unsafe_allow_html=True)
