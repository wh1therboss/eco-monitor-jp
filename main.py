import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="EcoMonitor JP | LEGO Explorers", layout="wide", initial_sidebar_state="collapsed")

# CSS para esconder a barra lateral antes do login
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS DE USUÁRIOS ---
USER_DB = "usuarios.csv"

def carregar_usuarios():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB)
    return pd.DataFrame(columns=['usuario', 'senha'])

def salvar_usuario(u, s):
    df = carregar_usuarios()
    if u in df['usuario'].values: return False
    pd.concat([df, pd.DataFrame([{'usuario': u, 'senha': s}])], ignore_index=True).to_csv(USER_DB, index=False)
    return True

# --- LÓGICA DE ACESSO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# --- TELA DE LOGIN (COM HAMTARO E LEGO EXPLORERS) ---
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Trazendo o Hamtaro de volta
        if os.path.exists("hamtaro.webp"):
            st.image("hamtaro.webp", width=150)
            
        st.markdown("<h1 style='text-align: center; color: #0055BF;'>♻️ EcoMonitor João Pessoa</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Equipe: LEGO Explorers 🚀</h3>", unsafe_allow_html=True)
        
        aba1, aba2 = st.tabs(["🔑 Entrar", "📝 Criar Conta"])
        
        with aba1:
            u = st.text_input("E-mail:")
            p = st.text_input("Senha:", type="password")
            if st.button("ENTRAR NO SISTEMA"):
                users = carregar_usuarios()
                if not users[(users['usuario'] == u) & (users['senha'] == p)].empty:
                    st.session_state.autenticado = True
                    st.session_state.user = u.split('@')[0].capitalize()
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
                    
        with aba2:
            st.subheader("Junte-se aos Explorers")
            nu = st.text_input("Novo E-mail:")
            np = st.text_input("Nova Senha:", type="password")
            if st.button("Finalizar Cadastro"):
                if nu and np and salvar_usuario(nu, np):
                    st.success("Conta criada! Agora use a aba 'Entrar'.")
                else:
                    st.error("Erro ao cadastrar ou usuário já existe.")
    st.stop()

# --- ÁREA LOGADA (AQUI OS SISTEMAS APARECEM) ---
st.sidebar.image("hamtaro.webp", width=100) # Hamtaro na barra lateral
st.sidebar.success(f"Conectado: {st.session_state.user}")
st.sidebar.markdown("---")
st.sidebar.write("🏆 **LEGO Explorers**")

if st.sidebar.button("Sair do Sistema"):
    st.session_state.autenticado = False
    st.rerun()

# Painel Principal
st.title(f"👋 Olá, {st.session_state.user}!")
st.markdown("### Bem-vindo ao Painel da LEGO Explorers")
st.write("Todos os sistemas de monitoramento de João Pessoa estão liberados na barra lateral.")

col_ham1, col_ham2 = st.columns(2)
with col_ham1:
    st.info("💡 **Dica:** Use o EcoColeta para registrar descartes de lixo.")
with col_ham2:
    if os.path.exists("hamtaro.webp"):
        st.image("hamtaro.webp", caption="Hamtaro Explorer", width=200)