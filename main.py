import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide")

# --- CSS: ESTILO TOTAL WHITE ---
st.markdown("""
    <style>
        .block-container { padding-top: 0rem; padding-bottom: 0rem; }
        [data-testid="stHeader"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        .main { background-color: #000000; }

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
            width: 150px;
            height: 150px;
            fill: #FFFFFF;
            margin-bottom: 30px;
        }

        /* PALAVRAS - AGORA VAI APARECER */
        .palavra-display {
            color: #FFFFFF;
            font-size: 28px;
            font-family: 'Courier New', Courier, monospace;
            letter-spacing: 12px;
            text-transform: uppercase;
            font-weight: 100;
            text-align: center;
        }
        
        .bioglow-box-white {
            border: 1px solid #FFFFFF;
            color: #FFFFFF;
            padding: 15px 50px;
            font-size: 45px;
            font-weight: 100;
            margin-top: 40px;
            letter-spacing: 20px;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# Vetor da Folha
svg_folha = """
<svg class="folha-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/>
</svg>
"""

# --- LÓGICA DA INTRO CORRIGIDA ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        # Usamos apenas um bloco de HTML puro para não bugar
        placeholder.write(f"""
            <div class="intro-screen">
                {svg_folha}
                <div class="palavra-display">{p}</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.5)
    
    # TELA FINAL
    placeholder.write(f"""
        <div class="intro-screen">
            <div style="color: #666; font-size: 10px; letter-spacing: 15px; margin-bottom: 20px;">LEGO EXPLORERS</div>
            {svg_folha}
            <div class="bioglow-box-white">BIOGLOW</div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.8)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- MENU E SITE (COLADO NO TOPO) ---
st.markdown("""
    <div style="display: flex; justify-content: center; background-color: #000; padding: 25px; border-bottom: 1px solid #222;">
        <a style="color:white; text-decoration:none; margin:0 25px; font-size:12px; letter-spacing:3px; opacity:0.6;" href="/adote_uma_arvore" target="_self">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin:0 25px; font-size:12px; letter-spacing:3px; opacity:0.6;" href="/Ilumina_JP" target="_self">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin:0 25px; font-size:12px; letter-spacing:3px; opacity:0.6;" href="/acompanhar_denuncias" target="_self">STATUS</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:white; text-align:center; font-weight:100; letter-spacing:15px; margin-top:100px;'>BIOGLOW</h1>", unsafe_allow_html=True)
