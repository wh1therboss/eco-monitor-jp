import streamlit as st
import streamlit.components.v1 as components
import time

# 1. Configuração de página
st.set_page_config(page_title="BIOGLOW", layout="wide")

# 2. CSS Global (Remove as bordas e garante o fundo preto)
st.markdown("""
    <style>
        .main { background-color: #000000 !important; }
        [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
        header, [data-testid="stSidebar"] { visibility: hidden; display: none; }
        .block-container { padding: 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DA INTRO CENTRALIZADA ---
def mostrar_intro(texto):
    svg_folha = '<svg width="150" height="150" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    html_intro = f"""
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: black;">
        {svg_folha}
        <div style="color: white; font-size: 30px; letter-spacing: 12px; text-transform: uppercase; margin-top: 30px; font-family: sans-serif; font-weight: 200;">
            {texto}
        </div>
    </div>
    """
    components.html(html_intro, height=1000)

# 3. LÓGICA DE EXIBIÇÃO (O PULO DO GATO)
if 'intro_finalizada' not in st.session_state:
    # Enquanto a intro não acaba, só existe o placeholder na tela
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade", "BIOGLOW"]
    
    for p in palavras:
        with placeholder.container():
            mostrar_intro(p)
        time.sleep(0.7)
    
    placeholder.empty()
    st.session_state['intro_finalizada'] = True
    st.rerun() # Força o script a recarregar para mostrar o site real

# 4. SITE REAL (Só carrega se a intro já era)
if st.session_state.get('intro_finalizada'):
    # Menu Superior (Só aparece agora)
    st.markdown("""
        <div style="display: flex; justify-content: center; padding: 40px 0; border-bottom: 1px solid #111; background-color: black;">
            <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">ADOTAR</a>
            <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">ILUMINA JP</a>
            <a style="color:white; text-decoration:none; margin:0 30px; font-size:11px; letter-spacing:4px; opacity:0.5;" href="#">STATUS</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Título do Site
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white; text-align:center; font-weight:100; letter-spacing:25px; font-size:50px;'>BIOGLOW</h1>", unsafe_allow_html=True)
