import streamlit as st
import streamlit.components.v1 as components
import time

# 1. Configuração de página
st.set_page_config(page_title="BIOGLOW", layout="wide")

# 2. CSS NINJA: Mata o menu e força o fundo preto absoluto
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], .main, .stApp {
            background-color: #000000 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        header, footer, [data-testid="stSidebar"] { visibility: hidden; display: none; }
        
        /* Remove o scrollbar durante a intro */
        body { overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNÇÃO DA INTRO (CENTRO ABSOLUTO DO MONITOR)
def render_intro_total(texto):
    svg_folha = '<svg width="150" height="150" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    html_intro = f"""
    <div style="
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: black; z-index: 9999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    ">
        {svg_folha}
        <div style="
            color: white; font-family: sans-serif; font-weight: 100;
            font-size: 30px; letter-spacing: 15px; text-transform: uppercase;
            margin-top: 30px; text-align: center;
        ">
            {texto}
        </div>
    </div>
    """
    return components.html(html_intro, height=2000)

# 4. LÓGICA DA ANIMAÇÃO
if 'finalizado' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade", "BIOGLOW"]
    
    for p in palavras:
        with placeholder:
            render_intro_total(p)
        time.sleep(0.6)
    
    placeholder.empty()
    st.session_state['finalizado'] = True
    st.rerun()

# 5. SITE REAL (Só aparece depois)
st.markdown("""
    <div style="display: flex; justify-content: center; padding: 40px 0; border-bottom: 1px solid #111;">
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">STATUS</a>
    </div>
    <div style="height: 60vh; display: flex; align-items: center; justify-content: center;">
        <h1 style='color:white; font-weight:100; letter-spacing:25px; font-size:50px;'>BIOGLOW</h1>
    </div>
""", unsafe_allow_html=True)
