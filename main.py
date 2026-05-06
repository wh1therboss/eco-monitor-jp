import streamlit as st
import streamlit.components.v1 as components
import time

# Configuração da página (Ícone branco para combinar)
st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide")

# --- CSS DESTRUIDOR: MATA SIDEBAR, BORDAS E DEIXA TUDO PRETO ---
st.markdown("""
    <style>
        /* Mata a barra lateral e o botão de abrir (>) */
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
        
        /* Remove o topo padrão e paddings */
        header { visibility: hidden; }
        .block-container { padding: 0 !important; max-width: 100%; }
        
        /* Fundo Preto Absoluto */
        .main { background-color: #000000 !important; }

        /* Estilo do Menu Superior (Sem borda verde, apenas linha sutil) */
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #000000;
            padding: 30px 0;
            border-bottom: 1px solid #111;
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
            transition: 0.3s;
        }
        .nav-link:hover { opacity: 1; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE RENDERIZAÇÃO (HTML PURO PARA NÃO BUGAR) ---
def render_intro(texto, final=False):
    # SVG da Folha Branca (Igual ao seu print)
    svg_folha = '<svg width="150" height="150" viewBox="0 0 24 24" fill="white"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,11 17,8 17,8Z"/></svg>'
    
    if not final:
        # Palavras puras, sem borda
        content = f'<div style="color:white; font-size:30px; letter-spacing:12px; text-transform:uppercase; margin-top:50px; font-weight:200; font-family:sans-serif;">{texto}</div>'
    else:
        # BIOGLOW final, também sem borda
        content = '<div style="color:white; font-size:50px; letter-spacing:20px; text-transform:uppercase; margin-top:50px; font-weight:100; font-family:sans-serif;">BIOGLOW</div>'

    html_code = f"""
    <div style="background:black; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; overflow:hidden;">
        {svg_folha}
        {content}
    </div>
    """
    return components.html(html_code, height=1000)

# --- EXECUÇÃO DA INTRO ---
if 'abertura_concluida' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder:
            render_intro(p)
        time.sleep(0.5)
    
    with placeholder:
        render_intro("", final=True)
    time.sleep(1.5)
    
    placeholder.empty()
    st.session_state.abertura_concluida = True

# --- SITE PRINCIPAL (SÓ APARECE DEPOIS) ---
st.markdown("""
    <div class="nav-container">
        <a class="nav-link" href="/adote_uma_arvore" target="_self">ADOTAR</a>
        <a class="nav-link" href="/Ilumina_JP" target="_self">ILUMINA JP</a>
        <a class="nav-link" href="/acompanhar_denuncias" target="_self">STATUS</a>
    </div>
    <h1 style='color:white; text-align:center; font-weight:100; letter-spacing:20px; margin-top:150px;'>BIOGLOW</h1>
""", unsafe_allow_html=True)
