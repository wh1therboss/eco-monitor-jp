import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os
import hashlib

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="EcoColeta JP | LEGO Explorers", layout="wide")

# --- FUNÇÕES DE SEGURANÇA E BANCO DE DADOS ---

USER_DB = "usuarios.csv"
DATA_DB = "denuncias_ecocoleta.csv"

def carregar_usuarios():
    if os.path.exists(USER_DB):
        return pd.read_csv(USER_DB)
    return pd.DataFrame(columns=['usuario', 'senha'])

def salvar_usuario(novo_user, nova_senha):
    df = carregar_usuarios()
    if novo_user in df['usuario'].values:
        return False
    novo_df = pd.concat([df, pd.DataFrame([{'usuario': novo_user, 'senha': nova_senha}])], ignore_index=True)
    novo_df.to_csv(USER_DB, index=False)
    return True

def carregar_denuncias():
    if os.path.exists(DATA_DB):
        df = pd.read_csv(DATA_DB)
        if 'Endereco' not in df.columns:
            df['Endereco'] = "Não informado"
        return df
    return pd.DataFrame(columns=['Bairro', 'Endereco', 'Tipo', 'Autor', 'Data', 'lat', 'lon'])

# --- ESTADO DA SESSÃO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario_atual = ""

# --- TELA INICIAL (LOGIN OU CADASTRO) ---
if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align: center; color: #0055BF;'>♻️ EcoColeta João Pessoa</h1>", unsafe_allow_html=True)
    
    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])
    
    with aba_login:
        st.subheader("Acesse sua conta")
        user_login = st.text_input("Usuário (E-mail):", key="l_user")
        pass_login = st.text_input("Senha:", type="password", key="l_pass")
        
        if st.button("ENTRAR"):
            df_users = carregar_usuarios()
            # Verifica se o usuário e senha batem com o que está no CSV
            user_valido = df_users[(df_users['usuario'] == user_login) & (df_users['senha'] == pass_login)]
            
            if not user_valido.empty:
                st.session_state.autenticado = True
                st.session_state.usuario_atual = user_login.split('@')[0].capitalize()
                st.success(f"Bem-vindo de volta, {st.session_state.usuario_atual}!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    with aba_cadastro:
        st.subheader("Crie um novo acesso")
        novo_user = st.text_input("Escolha um E-mail:", key="c_user")
        nova_pass = st.text_input("Escolha uma Senha:", type="password", key="c_pass")
        confirma_pass = st.text_input("Confirme a Senha:", type="password", key="c_conf")
        
        if st.button("CADASTRAR"):
            if novo_user and nova_pass:
                if nova_pass == confirma_pass:
                    if salvar_usuario(novo_user, nova_pass):
                        st.success("Conta criada com sucesso! Agora você pode 'Entrar'.")
                    else:
                        st.warning("Este usuário já existe.")
                else:
                    st.error("As senhas não coincidem.")
            else:
                st.error("Preencha todos os campos.")
    st.stop()

# --- ÁREA DO SISTEMA (PÓS-LOGIN) ---

# 4. INTERFACE PRINCIPAL
col_t, col_s = st.columns([4, 1])
with col_t:
    st.title(f"👋 Olá, {st.session_state.usuario_atual}!")
with col_s:
    if st.button("SAIR"):
        st.session_state.autenticado = False
        st.rerun()

# 5. FORMULÁRIO DE REGISTRO
if 'db_relatos' not in st.session_state:
    st.session_state.db_relatos = carregar_denuncias()

with st.form("registro_lixo", clear_on_submit=True):
    st.subheader("📢 Registrar Novo Foco de Lixo")
    c1, c2 = st.columns(2)
    with c1:
        bairro = st.selectbox("Bairro:", ["Bessa", "Manaíra", "Tambaú", "Cabo Branco", "Mangabeira"])
        rua = st.text_input("Endereço Exato:")
    with c2:
        tipo = st.radio("Tipo de Lixo:", ["Doméstico", "Entulho", "Móveis"])
    
    if st.form_submit_button("REGISTRAR"):
        if rua:
            coords = {"Bessa": [-7.085, -34.830], "Manaíra": [-7.092, -34.831], "Tambaú": [-7.114, -34.820], 
                      "Cabo Branco": [-7.135, -34.818], "Mangabeira": [-7.165, -34.845]}
            
            novo = {
                'Bairro': bairro, 'Endereco': rua, 'Tipo': tipo,
                'Autor': st.session_state.usuario_atual, 'Data': datetime.now().strftime("%d/%m/%Y"),
                'lat': coords[bairro][0], 'lon': coords[bairro][1]
            }
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            st.success("Registrado!")
            st.rerun()

# 6. MAPA
st.write("---")
st.subheader("📍 Mapa de Monitoramento")
m = folium.Map(location=[-7.115, -34.85], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    # Evita erro de coluna 'Endereco' ausente
    info = f"Local: {r.get('Endereco', 'N/A')}<br>Tipo: {r['Tipo']}"
    folium.Marker([r['lat'], r['lon']], popup=info).add_to(m)

folium_static(m, width=1000)
