import streamlit as st
import streamlit.components.v1 as components
import time

# 1. Configuração inicial
st.set_page_config(page_title="BIOGLOW", layout="wide")

# 2. CSS para resetar o Streamlit e permitir centralização real
st.markdown("""
    <style>
        /* Remove o fundo cinza e as margens chatas */
        .main { background-color: #000000 !important; }
        [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
        
        /* Mata a barra lateral e o topo */
        header, [data-testid="stSidebar"] { display: none; }
        
        /* Remove o espaço branco no topo da página */
        .block-container { padding-top: 0rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DA INTRO ---
def mostrar_intro(texto):
    # SVG da Folha
    svg_folha = '<svg width="150" height="150" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    html_intro = f"""
    <div style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
        background-color: black;
        margin: 0;
    ">
        {svg_folha}
        <div style="
            color: white; 
            font-size: 30px; 
            letter-spacing: 12px; 
            text-transform: uppercase; 
            margin-top: 30px; 
            font-family: sans-serif;
            font-weight: 200;
        ">
            {texto}
        </div>
    </div>
    """
    st.components.v1.html(html_intro, height=600)

# 3. Lógica da Animação (Só roda uma vez)
if 'intro_visto' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade", "BIOGLOW"]
    
    for p in palavras:
        with placeholder.container():
            mostrar_intro(p)
        time.sleep(0.7)
    
    placeholder.empty() # Limpa a tela para o site aparecer
    st.session_state['intro_visto'] = True

# 4. O SITE (Só aparece depois da intro)
if st.session_state.get('intro_visto'):
    # Menu Superior
    st.markdown("""
        <div style="display: flex; justify-content: center; padding: 30px; border-bottom: 1px solid #111;">
            <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">ADOTAR</a>
            <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">ILUMINA JP</a>
            <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">STATUS</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Nome Centralizado
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white; text-align:center; font-weight:100; letter-spacing:25px;'>BIOGLOW</h1>", unsafe_allow_html=True)
