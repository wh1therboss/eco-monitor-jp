import streamlit as st
import streamlit.components.v1 as components
import time

# Configuração para ocupar a tela toda
st.set_page_config(page_title="BIOGLOW", layout="wide")

# --- CSS DE RESET TOTAL ---
st.markdown("""
    <style>
        /* Mata qualquer borda, margem ou padding do Streamlit */
        [data-testid="stAppViewContainer"], 
        [data-testid="stAppViewBlockContainer"], 
        .main .block-container, 
        .stApp {
            padding: 0 !important;
            margin: 0 !important;
            background-color: #000000 !important;
            overflow: hidden;
        }

        /* Esconde header e sidebar de vez */
        header { visibility: hidden; }
        [data-testid="stSidebar"] { display: none; }

        /* Garante que o iframe do componente ocupe a tela toda */
        iframe {
            display: block;
            width: 100vw;
            height: 100vh;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- HTML/CSS DA INTRO (CENTRALIZAÇÃO ABSOLUTA) ---
def render_full_center(texto, final=False):
    svg_folha = '<svg width="180" height="180" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    # Este HTML ignora as regras do Streamlit e centraliza no viewport do navegador
    html_content = f"""
    <div style="
        background-color: black;
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0;
        padding: 0;
        position: fixed;
        top: 0;
        left: 0;
    ">
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            {svg_folha}
            <div style="
                color: white; 
                font-size: 35px; 
                letter-spacing: 15px; 
                text-transform: uppercase; 
                margin-top: 40px; 
                font-family: 'Inter', sans-serif;
                font-weight: 100;
                text-align: center;
            ">
                {texto if not final else 'BIOGLOW'}
            </div>
        </div>
    </div>
    """
    return components.html(html_content, height=2000) # Altura grande para garantir que o fixed funcione

# --- LÓGICA DA ANIMAÇÃO ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder:
            render_full_center(p)
        time.sleep(0.5)
    
    with placeholder:
        render_full_center("", final=True)
    time.sleep(1.5)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- SITE PÓS-INTRO ---
st.markdown("""
    <div style="display: flex; justify-content: center; background-color: #000; padding: 30px; border-bottom: 1px solid #111;">
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="#">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="#">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:12px; letter-spacing:4px; opacity:0.5;" href="#">STATUS</a>
    </div>
    <div style="display: flex; height: 70vh; align-items: center; justify-content: center; background-color: black;">
        <h1 style='color:white; font-weight:100; letter-spacing:25px; text-align:center;'>BIOGLOW</h1>
    </div>
""", unsafe_allow_html=True)
