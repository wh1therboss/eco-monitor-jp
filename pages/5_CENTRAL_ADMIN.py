import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Admin - EcoMonitor", layout="wide")

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("### 🛠️ PAINEL DE CONTROLE")
    st.write("---")

# Verificação de Login
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso restrito. Faça login na página principal.")
    st.stop()

# --- 2. CONEXÃO COM A NUVEM ---
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        # ttl=0 para garantir que o admin sempre veja o dado mais novo
        df = conn.read(ttl=0)
        return df
    except:
        return pd.DataFrame()

df = carregar_dados()

st.title("📊 Administração Central - LEGO Explorers")
st.markdown("Monitoramento em tempo real das ocorrências em João Pessoa.")

if df.empty:
    st.warning("⚠️ Nenhuma denúncia encontrada na planilha do Google.")
else:
    # --- 3. MÉTRICAS RÁPIDAS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Denúncias", len(df))
    with col2:
        pendentes = len(df[df['Status'] == 'Pendente'])
        st.metric("Pendentes", pendentes, delta_color="inverse")
    with col3:
        st.metric("Cidades Atendidas", "1 (João Pessoa)")

    st.write("---")

    # --- 4. GRÁFICOS E ANÁLISES ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("📦 Tipos de Resíduos Reportados")
        fig_pizza = px.pie(df, names='Tipo', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col_dir:
        st.subheader("📈 Evolução das Denúncias")
        # Pequeno ajuste para garantir que a data seja lida corretamente
        df['Data_Limpa'] = pd.to_datetime(df['Data'], errors='coerce').dt.date
        contagem_data = df.groupby('Data_Limpa').size().reset_index(name='Quantidade')
        fig_linha = px.line(contagem_data, x='Data_Limpa', y='Quantidade', markers=True)
        st.plotly_chart(fig_linha, use_container_width=True)

    # --- 5. TABELA DE GERENCIAMENTO ---
    st.write("---")
    st.subheader("📋 Lista de Ocorrências (Google Sheets)")
    
    # Filtro rápido
    filtro_tipo = st.multiselect("Filtrar por Tipo:", options=df['Tipo'].unique())
    
    df_exibir = df.copy()
    if filtro_tipo:
        df_exibir = df_exibir[df_exibir['Tipo'].isin(filtro_tipo)]
    
    st.dataframe(df_exibir.iloc[::-1], use_container_width=True)

    # Botão de Atualização Manual
    if st.button("🔄 Forçar Atualização dos Dados"):
        st.rerun()

st.info("💡 Dica: Para alterar o status de 'Pendente' para 'Resolvido', você pode editar diretamente na sua planilha do Google Sheets. As mudanças aparecerão aqui ao atualizar.")
