import streamlit as st
import streamlit.components.v1 as components
import time

# Configura a página para não ter margens
st.set_page_config(page_title="BIOGLOW", layout="wide", initial_sidebar_state="collapsed")

# --- CSS RADICAL: MATA TUDO QUE NÃO É PRETO ---
st.markdown("""
    <style>
        /* Remove absolutamente todas as margens e barras do Streamlit */
        [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], 
        .main .block-container, .stApp, footer, header {
            padding: 0 !important; margin: 0 !important;
            background-color: #000000 !important;
            height: 100vh !important;
        }
        [data-testid="stSidebar"] { display: none; }
        
        /* Garante que o componente de animação ocupe a tela toda sem scroll */
        iframe { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- A ANIMAÇÃO QUE NÃO ERRA O CENTRO ---
def render_intro(texto):
    # SVG da Folha Branca
    svg = '<svg width="180" height="180" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    html_code = f"""
    <div style="
        background-color: black;
        margin: 0; padding: 0;
        width: 100vw; height: 100vh;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        overflow: hidden;
    ">
        {svg}
        <div style="
            color: white; font-family: 'Inter', sans-serif;
            font-size: 32px; letter-spacing: 15px;
            text-transform: uppercase; margin-top: 40px;
            font-weight: 100; text-align: center;
        ">
            {texto}
        </div>
    </div>
    """
    return components.html(html_code, height=2000) # O height alto aqui é só pro iframe não cortar

# --- LÓGICA DE TRANSIÇÃO ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    for p in ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade", "BIOGLOW"]:
        with placeholder:
            render_intro(p)
        time.sleep(0.6)
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- CONTEÚDO FINAL (SÓ APARECE DEPOIS) ---
st.markdown("""
    <div style="display: flex; justify-content: center; padding: 30px; border-bottom: 1px solid #111;">
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="#">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="#">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="#">STATUS</a>
    </div>
    <div style="display: flex; height: 70vh; align-items: center; justify-content: center;">
        <h1 style='color:white; font-weight:100; letter-spacing:25px;'>BIOGLOW</h1>
    </div>
""", unsafe_allow_html=True)
