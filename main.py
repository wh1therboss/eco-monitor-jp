import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide", page_icon="🍃")

# --- CSS: ESTILO TOTAL BLACK & WHITE ---
st.markdown("""
    <style>
        /* Remove espaços do topo e esconde elementos padrão */
        .block-container { padding-top: 0rem; padding-bottom: 0rem; }
        [data-testid="stHeader"] { display: none; }
        [data-testid="stSidebar"] { display: none; }
        
        /* Fundo do site 100% Preto */
        .main { background-color: #000000; }

        /* Menu Superior 'Colado' e sem bordas verdes */
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #000000;
            padding: 25px 0;
            border-bottom: 1px solid #1A1A1A;
            width: 100%;
            margin-bottom: 50px;
        }
        .nav-link {
            color: #FFFFFF !important;
            text-decoration: none;
            font-weight: 400;
            font-family: 'Inter', sans-serif;
            margin: 0 25px;
            font-size: 13px;
            letter-spacing: 3px;
            text-transform: uppercase;
            transition: 0.5s;
            opacity: 0.7;
        }
        .nav-link:hover { opacity: 1; letter-spacing: 4px; }

        /* Tela de Intro 100% Preta */
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
        
        /* Folha Inteira Branca (Estilo Ícone) */
        .folha-branca {
            font-size: 140px;
            color: #FFFFFF;
            animation: flash 0.6s ease-out forwards;
        }

        @keyframes flash {
            0% { transform: scale(0.8); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .palavra-anim {
            color: #FFFFFF;
            font-size: 20px;
            margin-top: 40px;
            font-family: 'Courier New', Courier, monospace;
            letter-spacing: 10px;
            text-transform: uppercase;
            opacity: 0.8;
        }
        
        /* BIOGLOW AGORA É BRANCO */
        .bioglow-text {
            color: #FFFFFF;
            border: 2px solid #FFFFFF;
            padding: 10px 40px;
            font-size: 50px;
            font-weight: 200;
            margin-top: 30px;
            letter-spacing: 15px;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DA INTRO (RÁPIDA E LIMPA) ---
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
            time.sleep(0.5) # Rápido para não cansar
    
    # TELA FINAL: LEGO EXPLORERS + FOLHA + BIOGLOW (TUDO BRANCO)
    with placeholder.container():
        st.markdown(f"""
            <div class="intro-screen">
                <div style="color: #FFFFFF; font-size: 12px; letter-spacing: 15px; margin-bottom: 30px; opacity: 0.5;">LEGO EXPLORERS</div>
                <div class="folha-branca">🍃</div>
                <div class="bioglow-text">BIOGLOW</div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- SITE PÓS-INTRO ---
st.markdown("""
    <div class="nav-container">
        <a class="nav-link" href="/adote_uma_arvore" target="_self">Adotar</a>
        <a class="nav-link" href="/Ilumina_JP" target="_self">Ilumina JP</a>
        <a class="nav-link" href="/acompanhar_denuncias" target="_self">Status</a>
        <a class="nav-link" href="/admin_central" target="_self">Admin</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:white; text-align:center; font-weight:100; letter-spacing:5px;'>BIOGLOW</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#555; text-align:center; letter-spacing:2px;'>Sustentabilidade & Tecnologia</p>", unsafe_allow_html=True)
