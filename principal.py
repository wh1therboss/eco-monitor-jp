import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide", page_icon="🍃")

# Estilo para esconder o menu lateral e criar o menu superior
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;} /* Esconde a lateral */
    
    /* Animação de Abertura */
    .intro-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: black; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 9999;
    }
    .folha { font-size: 80px; animation: crescer 2s ease-out; }
    .palavras { color: white; font-size: 24px; margin-top: 20px; font-family: sans-serif; }
    @keyframes crescer { from {transform: scale(0);} to {transform: scale(1);} }

    /* Barra Superior */
    .nav-bar {
        display: flex; justify-content: center; background-color: #111;
        padding: 10px; border-radius: 50px; margin-bottom: 30px; gap: 20px;
    }
    .nav-item { color: white; text-decoration: none; font-weight: bold; padding: 5px 15px; }
    .nav-item:hover { background-color: #2f855a; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

# Lógica da Animação
if 'visto' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    for p in palavras:
        with placeholder.container():
            st.markdown(f'<div class="intro-bg"><div class="folha">🍃</div><div class="palavras">{p}</div></div>', unsafe_allow_html=True)
        time.sleep(1)
    
    with placeholder.container():
        st.markdown("""
        <div class="intro-bg">
            <div style="color: white; font-size: 18px;">LEGO EXPLORERS</div>
            <div class="folha">🍃</div>
            <div style="background-color: #2f855a; color: white; padding: 10px 30px; font-size: 40px; font-weight: bold; margin-top: 15px;">BIOGLOW</div>
        </div>
        """, unsafe_allow_html=True)
    time.sleep(2)
    placeholder.empty()
    st.session_state.visto = True

# Menu Superior
st.markdown("""
<div class="nav-bar">
    <a class="nav-item" href="/adote_uma_arvore" target="_self">🌳 ADOTAR</a>
    <a class="nav-item" href="/Ilumina_JP" target="_self">💡 ILUMINA JP</a>
    <a class="nav-item" href="/acompanhar_denuncias" target="_self">🕵️ STATUS</a>
    <a class="nav-item" href="/admin_central" target="_self">🔐 ADMIN</a>
</div>
""", unsafe_allow_html=True)

st.title("🌱 Bem-vindo ao Projeto BIOGLOW")
st.write("Sua plataforma de inovação e sustentabilidade em João Pessoa.")
