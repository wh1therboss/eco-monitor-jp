import streamlit as st
import streamlit.components.v1 as components
import time

# Configuração total
st.set_page_config(page_title="BIOGLOW", layout="wide")

# --- CSS PARA LIMPAR O STREAMLIT ---
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], 
        .main .block-container, .stApp {
            padding: 0 !important; margin: 0 !important;
            background-color: #000000 !important;
        }
        header { visibility: hidden; }
        [data-testid="stSidebar"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE RENDERIZAÇÃO (CENTRALIZAÇÃO REAL) ---
def render_centro_perfeito(texto, final=False):
    # SVG Branco puro
    svg = '<svg width="180" height="180" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    # HTML com centralização via Flexbox no Body
    html_content = f"""
    <body style="margin:0; padding:0; background-color:black; overflow:hidden;">
        <div style="
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            width: 100vw;
            font-family: sans-serif;
        ">
            {svg}
            <div style="
                color: white; 
                font-size: 35px; 
                letter-spacing: 15px; 
                text-transform: uppercase; 
                margin-top: 40px; 
                font-weight: 100;
                text-align: center;
            ">
                {texto if not final else 'BIOGLOW'}
            </div>
        </div>
    </body>
    """
    # height=100% no iframe garante que ele use o viewport do Streamlit
    return components.html(html_content, height=800)

# --- LÓGICA DA ANIMAÇÃO ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder:
            render_centro_perfeito(p)
        time.sleep(0.5)
    
    with placeholder:
        render_centro_perfeito("", final=True)
    time.sleep(1.8)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- MENU E CONTEÚDO (COLADO NO TOPO) ---
st.markdown("""
    <div style="display: flex; justify-content: center; background-color: #000; padding: 25px; border-bottom: 1px solid #111;">
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="/adote_uma_arvore" target="_self">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="/Ilumina_JP" target="_self">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="/acompanhar_denuncias" target="_self">STATUS</a>
    </div>
    <div style="display: flex; height: 60vh; align-items: center; justify-content: center;">
        <h1 style='color:white; font-weight:100; letter-spacing:25px;'>BIOGLOW</h1>
    </div>
""", unsafe_allow_html=True)
