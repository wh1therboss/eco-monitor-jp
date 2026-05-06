import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide")

# --- CSS PARA MATAR A MOLDURA DO SITE (O "QUADRADO" CINZA) ---
st.markdown("""
    <style>
        /* 1. Mata a borda externa de todos os containers principais */
        [data-testid="stAppViewContainer"], 
        [data-testid="stAppViewBlockContainer"],
        .main .block-container,
        .stApp {
            padding: 0px !important;
            margin: 0px !important;
            background-color: #000000 !important;
        }

        /* 2. Esconde o Header e a Sidebar (inclusive o botão de abrir >) */
        header { visibility: hidden; height: 0; }
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
        
        /* 3. Remove o espaço branco/cinza que fica no topo */
        div[data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {
            padding-top: 0px !important;
        }

        /* 4. Estilo do Menu Superior Colado */
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #000000;
            padding: 25px 0;
            border-bottom: 1px solid #111;
            width: 100vw;
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
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE INTRO (SANGRAMENTO TOTAL NA TELA) ---
def render_intro(texto, final=False):
    svg_folha = '<svg width="150" height="150" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    # Adicionei 'width:100vw' e 'margin:0' no HTML do component para ele não criar borda interna
    html_content = f"""
    <div style="background:black; width:100vw; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; margin:0; padding:0; overflow:hidden;">
        {svg_folha}
        <div style="color:white; font-size:30px; letter-spacing:15px; text-transform:uppercase; margin-top:50px; font-weight:100; font-family:sans-serif;">{texto if not final else 'BIOGLOW'}</div>
    </div>
    """
    return components.html(html_content, height=1000)

# --- LÓGICA DE EXIBIÇÃO ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    for p in ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]:
        with placeholder: render_intro(p)
        time.sleep(0.5)
    with placeholder: render_intro("", final=True)
    time.sleep(1.5)
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- SITE PÓS-INTRO ---
st.markdown("""
    <div class="nav-container">
        <a class="nav-link" href="/adote_uma_arvore" target="_self">ADOTAR</a>
        <a class="nav-link" href="/Ilumina_JP" target="_self">ILUMINA JP</a>
        <a class="nav-link" href="/acompanhar_denuncias" target="_self">STATUS</a>
    </div>
    <div style="text-align:center; margin-top:150px;">
        <h1 style='color:white; font-weight:100; letter-spacing:25px;'>BIOGLOW</h1>
    </div>
""", unsafe_allow_html=True)
