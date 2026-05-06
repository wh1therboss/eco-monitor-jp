import streamlit as st
import streamlit.components.v1 as components
import time

# 1. Configuração de página
st.set_page_config(page_title="BIOGLOW", layout="wide")

# 2. CSS que mata as bordas mas DEIXA O CONTEÚDO APARECER
st.markdown("""
    <style>
        /* Remove as bordas cinzas chatas */
        [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
        [data-testid="stAppViewBlockContainer"] {
            padding: 0 !important;
            max-width: 100% !important;
        }
        /* Esconde header e sidebar */
        header, [data-testid="stSidebar"] { visibility: hidden; display: none; }
        
        /* Garante que o fundo seja preto em tudo */
        .stApp { background-color: black; }
    </style>
""", unsafe_allow_html=True)

# 3. Função de Intro (Centralização por Flexbox sem quebrar o layout)
def render_intro(texto):
    svg = '<svg width="180" height="180" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    html = f"""
    <div style="
        background-color: black;
        height: 85vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: sans-serif;
    ">
        {svg}
        <div style="color: white; font-size: 30px; letter-spacing: 15px; text-transform: uppercase; margin-top: 40px; font-weight: 100;">
            {texto}
        </div>
    </div>
    """
    components.html(html, height=800)

# 4. Lógica da Animação
if 'intro' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade", "BIOGLOW"]
    
    for p in palavras:
        with placeholder:
            render_intro(p)
        time.sleep(0.6)
    
    placeholder.empty()
    st.session_state['intro'] = True

# 5. Site Principal (Menu + Título)
st.markdown("""
    <div style="display: flex; justify-content: center; padding: 40px 0; border-bottom: 1px solid #222;">
        <a style="color:white; text-decoration:none; margin: 0 25px; font-size: 11px; letter-spacing: 4px; opacity: 0.6;" href="#">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin: 0 25px; font-size: 11px; letter-spacing: 4px; opacity: 0.6;" href="#">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin: 0 25px; font-size: 11px; letter-spacing: 4px; opacity: 0.6;" href="#">STATUS</a>
    </div>
    <div style="height: 60vh; display: flex; align-items: center; justify-content: center;">
        <h1 style='color: white; font-weight: 100; letter-spacing: 25px; font-size: 60px;'>BIOGLOW</h1>
    </div>
""", unsafe_allow_html=True)
