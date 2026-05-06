import streamlit as st
import time

st.set_page_config(page_title="BIOGLOW | LEGO Explorers", layout="wide", page_icon="🌱")

# --- ESTILO CSS PARA A ANIMAÇÃO E MENU SUPERIOR ---
st.markdown("""
<style>
    /* Esconder o menu padrão do Streamlit para parecer um site real */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Fundo Preto da Abertura */
    .intro-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: black;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeOut 1s ease-in-out 7s forwards; /* Some depois de 7 segundos */
    }

    /* A Folha Crescendo */
    .folha {
        font-size: 100px;
        animation: crescer 3s ease-out forwards;
        color: white;
    }

    /* Palavras que trocam */
    .palavras {
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-size: 24px;
        margin-top: 20px;
        height: 30px;
    }

    @keyframes crescer {
        0% { transform: scale(0) translateY(50px); opacity: 0; }
        100% { transform: scale(1) translateY(0); opacity: 1; }
    }

    @keyframes fadeOut {
        to { opacity: 0; visibility: hidden; }
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DA ANIMAÇÃO DE ABERTURA ---
if 'intro_visto' not in st.session_state:
    placeholder = st.empty()
    palavras = ["Persistência", "Inovação", "Equipe", "Resiliência", "Amizade"]
    
    with placeholder.container():
        # HTML da Intro
        for p in palavras:
            st.markdown(f"""
            <div class="intro-bg">
                <div class="folha">🍃</div>
                <div class="palavras">{p}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1.2) # Tempo de cada palavra
        
        # Tela Final da Intro: BIOGLOW
        st.markdown(f"""
        <div class="intro-bg">
            <div style="color: white; font-size: 20px; margin-bottom: 10px;">LEGO EXPLORERS</div>
            <div class="folha">🍃</div>
            <div style="background-color: #2f855a; color: white; padding: 10px 40px; font-size: 50px; font-weight: bold; margin-top: 20px;">BIOGLOW</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    
    placeholder.empty()
    st.session_state.intro_visto = True

# --- MENU SUPERIOR (SUBSTITUINDO A SIDEBAR) ---
st.markdown("""
<div style="display: flex; justify-content: space-around; background-color: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 30px;">
    <a href="/adote_uma_arvore" target="_self" style="color: white; text-decoration: none; font-weight: bold;">🌳 ADOTAR</a>
    <a href="/Ilumina_JP" target="_self" style="color: white; text-decoration: none; font-weight: bold;">💡 ILUMINA JP</a>
    <a href="/acompanhar_denuncias" target="_self" style="color: white; text-decoration: none; font-weight: bold;">🕵️ STATUS</a>
    <a href="/admin_central" target="_self" style="color: white; text-decoration: none; font-weight: bold;">🔐 ADMIN</a>
</div>
""", unsafe_allow_html=True)

st.title("Bem-vindo ao BIOGLOW")
st.write("O futuro sustentável de João Pessoa começa aqui.")
