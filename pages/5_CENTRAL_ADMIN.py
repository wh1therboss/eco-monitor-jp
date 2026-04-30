import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURAÇÃO DA SIDEBAR (IDENTIDADE LEGO) ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 🔑 Terminal de Comando")
    if st.session_state.get('admin_logado', False):
        st.success("SISTEMA: ONLINE")
        if st.button("Encerrar Sessão"):
            st.session_state.admin_logado = False
            st.rerun()
    else:
        st.error("SISTEMA: BLOQUEADO")

# --- 2. TELA DE LOGIN INTERNA ---
def tela_login():
    st.title("🔐 Acesso Restrito - Friday Protocol")
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("hamtaro.webp", width=150)
        with col2:
            st.markdown("### Identifique-se para acessar o HQ")
            user_input = st.text_input("Usuário:")
            pass_input = st.text_input("Senha:", type="password")
            
            if st.button("Acessar Central"):
                # Verificação das credenciais que você definiu
                if user_input == "LEGO EXPLORERS HQ" and pass_input == "09122307":
                    st.session_state.admin_logado = True
                    st.success("Acesso concedido! Carregando sistemas...")
                    st.rerun()
                else:
                    st.error("Credenciais incorretas. Alerta de intruso enviado!")

# --- 3. LÓGICA DE EXIBIÇÃO ---
if not st.session_state.get('admin_logado', False):
    tela_login()
    st.stop() # Interrompe o código aqui se não estiver logado

# --- 4. CENTRAL ADMIN (SÓ APARECE SE LOGAR COM SUCESSO) ---
st.title("🖥️ Central de Comando LEGO Explorers")
st.subheader("Bem-vinda, Friday. Status: Total Control.")

DATA_COLETA = "denuncias_ecocoleta.csv"
DATA_LUZ = "alertas_iluminacao.csv"

# Função para carregar dados com suporte a STATUS
def carregar_dados(caminho, colunas_padrao):
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        if 'Status' not in df.columns:
            df['Status'] = "Pendente"
        for col in colunas_padrao:
            if col not in df.columns: df[col] = "N/A"
        return df
    return pd.DataFrame(columns=colunas_padrao + ['Status'])

df_lixo = carregar_dados(DATA_COLETA, ['Data', 'Rua', 'Tipo', 'Autor'])
df_luz = carregar_dados(DATA_LUZ, ['Data', 'Bairro', 'Rua', 'Problema', 'Autor'])

# --- 5. GESTÃO DE STATUS ---
tab1, tab2, tab3 = st.tabs(["♻️ Gestão de Lixo", "💡 Gestão de Luz", "⚙️ Configurações"])

with tab1:
    st.markdown("### 📋 Atualizar Pedidos de Coleta")
    if not df_lixo.empty:
        idx = st.selectbox("Selecione o ID da Denúncia:", df_lixo.index, key="admin_lixo_idx")
        novo_st = st.selectbox("Mudar Status para:", 
                             ["Pendente", "Em Processo", "Equipe a Caminho", "Resolvido", "Falso Alerta"], 
                             key="admin_lixo_st")
        
        if st.button("Atualizar Status EcoColeta"):
            df_lixo.at[idx, 'Status'] = novo_st
            df_lixo.to_csv(DATA_COLETA, index=False)
            st.success("Status atualizado no banco de dados!")
            st.rerun()
        
        st.write("---")
        st.dataframe(df_lixo, use_container_width=True)
    else:
        st.info("Nenhuma denúncia registrada.")

with tab2:
    st.markdown("### 🔌 Manutenção de Iluminação")
    if not df_luz.empty:
        idx_l = st.selectbox("Selecione o ID do Alerta:", df_luz.index, key="admin_luz_idx")
        novo_st_l = st.selectbox("Mudar Status para:", 
                               ["Pendente", "Manutenção Agendada", "Lâmpada Trocada", "Aguardando Peça"], 
                               key="admin_luz_st")
        
        if st.button("Atualizar Status IluminaJP"):
            df_luz.at[idx_l, 'Status'] = novo_st_l
            df_luz.to_csv(DATA_LUZ, index=False)
            st.success("Ordem de serviço atualizada!")
            st.rerun()
            
        st.write("---")
        st.dataframe(df_luz, use_container_width=True)
    else:
        st.info("Sem alertas de iluminação.")

with tab3:
    st.markdown("### 🛠️ Painel do Desenvolvedor")
    if st.button("🚨 APAGAR TODOS OS REGISTROS"):
        if os.path.exists(DATA_COLETA): os.remove(DATA_COLETA)
        if os.path.exists(DATA_LUZ): os.remove(DATA_LUZ)
        st.warning("Bancos de dados resetados com sucesso.")
        st.rerun()
