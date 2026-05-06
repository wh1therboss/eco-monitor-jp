import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide")

# --- CSS GLOBAL PARA O FUNDO PRETO ---
st.markdown("""
    <style>
        .main { background-color: #000000 !important; }
        [data-testid="stHeader"] { visibility: hidden; }
        .block-container { padding: 0; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DA ANIMAÇÃO (HTML PURO) ---
def render_intro(texto, final=False):
    svg_folha = '<svg width="150" height="150" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    if not final:
        html_code = f"""
        <div style="background:black; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; font-family:sans-serif;">
            {svg_folha}
            <div style="color:white; font-size:30px; letter-spacing:10px; text-transform:uppercase; margin-top:40px; font-weight:100;">{texto}</div>
        </div>
        """
    else:
        html_code = f"""
        <div style="background:black; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; font-family:sans-serif;">
            <div style="color:gray; font-size:12px; letter-spacing:15px; margin-bottom:30px;">LEGO EXPLORERS</div>
            {svg_folha}
            <div style="border:1px solid white; color:white; padding:15px 60px; font-size:45px; margin-top:40px; letter-spacing:20px;">BIOGLOW</div>
        </div>
        """
    return components.html(html_code, height=800)

# --- LÓGICA DE EXECUÇÃO ---
if 'abertura_concluida' not in st.session_state:
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    placeholder = st.empty()
    
    for p in palavras:
        with placeholder:
            render_intro(p)
        time.sleep(0.6)
    
    with placeholder:
        render_intro("", final=True)
    time.sleep(2.0)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- CONTEÚDO DO SITE (SÓ APARECE DEPOIS) ---
st.markdown("""
    <div style="display: flex; justify-content: center; background-color: #000; padding: 25px; border-bottom: 1px solid #222; margin-bottom:50px;">
        <a style="color:white; text-decoration:none; margin:0 25px; font-size:12px; letter-spacing:3px; opacity:0.6;" href="/adote_uma_arvore" target="_self">ADOTAR</a>
        <a style="color:white; text-decoration:none; margin:0 25px; font-size:12px; letter-spacing:3px; opacity:0.6;" href="/Ilumina_JP" target="_self">ILUMINA JP</a>
        <a style="color:white; text-decoration:none; margin:0 25px; font-size:12px; letter-spacing:3px; opacity:0.6;" href="/acompanhar_denuncias" target="_self">STATUS</a>
    </div>
    <h1 style='color:white; text-align:center; font-weight:100; letter-spacing:15px; margin-top:50px;'>BIOGLOW</h1>
""", unsafe_allow_html=True)
