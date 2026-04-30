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
    st.info("Aqui você gerencia todos os serviços de João Pessoa.")

# --- 2. TRAVA DE ACESSO (SÓ VOCÊ ENTRA) ---
# Altere 'admin' para o seu nome de usuário se preferir
USER_ADMIN = "friday" 

if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso Negado. Faça login na página principal.")
    st.stop()

if st.session_state.get('usuario_atual') != USER_ADMIN:
    st.warning(f"⚠️ Olá {st.session_state.usuario_atual}, você não tem permissão de Administrador para acessar esta página.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJwamNqZ3R3eGd6bmZ4eG54eG54eG54eG54eG54eG54eG54eGZpbmNlJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/10mg29O78Y9uPS/giphy.gif")
    st.stop()

st.title("🖥️ Central de Comando LEGO Explorers")

# --- 3. CARREGAMENTO DOS BANCOS DE DADOS ---
DATA_COLETA = "denuncias_ecocoleta.csv"
DATA_LUZ = "alertas_iluminacao.csv"

def carregar_dados(caminho, colunas_padrao):
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        for col in colunas_padrao:
            if col not in df.columns: df[col] = "Pendente" # Status padrão se não existir
        return df
    return pd.DataFrame(columns=colunas_padrao)

cols_coleta = ['Data', 'Rua', 'Tipo', 'Autor', 'Status']
cols_luz = ['Data', 'Bairro', 'Rua', 'Problema', 'Autor', 'Status']

df_lixo = carregar_dados(DATA_COLETA, cols_coleta)
df_luz = carregar_dados(DATA_LUZ, cols_luz)

# --- 4. GESTÃO DE DENÚNCIAS (MUDAR STATUS) ---
tab1, tab2, tab3 = st.tabs(["♻️ Gestão EcoColeta", "💡 Gestão IluminaJP", "📊 Estatísticas"])

with tab1:
    st.subheader("Gerenciar Denúncias de Lixo")
    if not df_lixo.empty:
        # Selecionar denúncia para editar
        indice = st.selectbox("Selecione o ID da denúncia para mudar o status:", df_lixo.index)
        novo_status = st.selectbox("Mudar status para:", 
                                 ["Pendente", "Em Processo", "Equipe a Caminho", "Resolvido", "Falsa Denúncia"], 
                                 key="status_lixo")
        
        if st.button("Atualizar Status EcoColeta"):
            df_lixo.at[indice, 'Status'] = novo_status
            df_lixo.to_csv(DATA_COLETA, index=False)
            st.success(f"Status da denúncia {indice} atualizado para {novo_status}!")
            st.rerun()
        
        st.write("---")
        st.dataframe(df_lixo, use_container_width=True)
    else:
        st.info("Nenhuma denúncia no banco de dados.")

with tab2:
    st.subheader("Gerenciar Alertas de Iluminação")
    if not df_luz.empty:
        indice_luz = st.selectbox("Selecione o ID do alerta de luz:", df_luz.index)
        status_luz = st.selectbox("Mudar status para:", 
                                ["Pendente", "Manutenção Agendada", "Lâmpada Trocada", "Aguardando Peça"], 
                                key="status_luz")
        
        if st.button("Atualizar Status IluminaJP"):
            df_luz.at[indice_luz, 'Status'] = status_luz
            df_luz.to_csv(DATA_LUZ, index=False)
            st.success(f"Alerta {indice_luz} atualizado!")
            st.rerun()
            
        st.write("---")
        st.dataframe(df_luz, use_container_width=True)
    else:
        st.info("Nenhum alerta de iluminação.")

with tab3:
    st.subheader("Resumo da Operação")
    c1, c2 = st.columns(2)
    c1.metric("Total EcoColeta", len(df_lixo))
    c2.metric("Total IluminaJP", len(df_luz))
    
    st.write("---")
    if st.button("🚨 RESETAR TODOS OS DADOS (LIMPAR CSVs)"):
        if os.path.exists(DATA_COLETA): os.remove(DATA_COLETA)
        if os.path.exists(DATA_LUZ): os.remove(DATA_LUZ)
        st.warning("Bancos de dados apagados!")
        st.rerun()
