import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURAÇÃO E IDENTIDADE (SIDEBAR) ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 🔑 Painel Master Admin")
    st.error("ACESSO RESTRITO: LEGO HQ")

# --- 2. TRAVA DE SEGURANÇA (SÓ VOCÊ ENTRA) ---
# Define aqui o nome que você usa para logar
USER_ADMIN = "friday" 

# Verifica se está logado
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso Negado. Por favor, faça login na página principal.")
    st.stop()

# Busca o usuário de forma segura para evitar o erro de AttributeError
usuario_logado = st.session_state.get('usuario_atual', 'Desconhecido')

if usuario_logado != USER_ADMIN:
    st.warning(f"⚠️ Olá {usuario_logado}, você não tem permissão para acessar esta área.")
    st.stop()

# --- 3. INÍCIO DO PAINEL ---
st.title("🖥️ Central de Comando LEGO Explorers")
st.markdown(f"Bem-vindo, Diretor **{usuario_logado}**.")

DATA_COLETA = "denuncias_ecocoleta.csv"
DATA_LUZ = "alertas_iluminacao.csv"

# Função para carregar dados e garantir a coluna 'Status'
def carregar_dados(caminho, colunas_padrao):
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        # Se a coluna Status não existir no arquivo antigo, ela é criada
        if 'Status' not in df.columns:
            df['Status'] = "Pendente"
        # Garante que as outras colunas básicas existam
        for col in colunas_padrao:
            if col not in df.columns: df[col] = "N/A"
        return df
    return pd.DataFrame(columns=colunas_padrao + ['Status'])

cols_coleta = ['Data', 'Rua', 'Tipo', 'Autor']
cols_luz = ['Data', 'Bairro', 'Rua', 'Problema', 'Autor']

df_lixo = carregar_dados(DATA_COLETA, cols_coleta)
df_luz = carregar_dados(DATA_LUZ, cols_luz)

# --- 4. GESTÃO DE STATUS ---
tab1, tab2, tab3 = st.tabs(["♻️ Gestão EcoColeta", "💡 Gestão IluminaJP", "📊 Controle Total"])

with tab1:
    st.subheader("Gerenciar Status: Lixo")
    if not df_lixo.empty:
        # Interface para mudar status
        idx_lixo = st.selectbox("Selecione o Registro (ID):", df_lixo.index, key="sel_lixo")
        novo_st_lixo = st.selectbox("Novo Status:", ["Pendente", "Equipe Enviada", "Resolvido", "Falso Alerta"], key="st_lixo")
        
        if st.button("Atualizar Lixo"):
            df_lixo.at[idx_lixo, 'Status'] = novo_st_lixo
            df_lixo.to_csv(DATA_COLETA, index=False)
            st.success("Status atualizado!")
            st.rerun()
        
        st.dataframe(df_lixo, use_container_width=True)
    else:
        st.info("Sem dados de coleta.")

with tab2:
    st.subheader("Gerenciar Status: Iluminação")
    if not df_luz.empty:
        idx_luz = st.selectbox("Selecione o Registro (ID):", df_luz.index, key="sel_luz")
        novo_st_luz = st.selectbox("Novo Status:", ["Aguardando Reparo", "Manutenção em Curso", "Concluído"], key="st_luz")
        
        if st.button("Atualizar Luz"):
            df_luz.at[idx_luz, 'Status'] = novo_st_luz
            df_luz.to_csv(DATA_LUZ, index=False)
            st.success("Status atualizado!")
            st.rerun()
            
        st.dataframe(df_luz, use_container_width=True)
    else:
        st.info("Sem dados de iluminação.")

with tab3:
    st.subheader("Configurações do Sistema")
    if st.button("🚨 LIMPAR TODOS OS REGISTROS (CUIDADO)"):
        if os.path.exists(DATA_COLETA): os.remove(DATA_COLETA)
        if os.path.exists(DATA_LUZ): os.remove(DATA_LUZ)
        st.warning("Bancos de dados deletados.")
        st.rerun()
