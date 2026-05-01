import streamlit as st
import pandas as pd
import plotly.express as px

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

# --- 2. LEITURA DIRETA DA PLANILHA ---
# Substitua o link abaixo pelo link da sua planilha (o link normal de visualizar)
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1wE0G8tHrRWsroT2iEixV3AwmDbncx3UnGJBRyEa_9Qc"

def carregar_dados():
    try:
        # Lemos a planilha diretamente como um CSV público
        return pd.read_csv(LINK_PLANILHA)
    except Exception as e:
        st.error(f"Erro ao ler planilha: {e}")
        return pd.DataFrame()

df = carregar_dados()

st.title("📊 Administração Central - LEGO Explorers")

if df.empty:
    st.warning("⚠️ A planilha parece estar vazia ou o link está incorreto.")
    st.info("Dica: No Google Sheets, clique em Compartilhar e mude para 'Qualquer pessoa com o link'.")
else:
    # --- 3. MÉTRICAS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Denúncias", len(df))
    with col2:
        # Verifica se a coluna Status existe antes de filtrar
        if 'Status' in df.columns:
            pendentes = len(df[df['Status'] == 'Pendente'])
            st.metric("Pendentes", pendentes)
    with col3:
        st.metric("Cidade", "João Pessoa")

    st.write("---")

    # --- 4. GRÁFICOS ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        if 'Tipo' in df.columns:
            st.subheader("📦 Tipos de Resíduos")
            fig_pizza = px.pie(df, names='Tipo', hole=0.4)
            st.plotly_chart(fig_pizza, use_container_width=True)

    with col_dir:
        st.subheader("📋 Últimos Registos")
        st.dataframe(df.iloc[::-1], use_container_width=True)

    if st.button("🔄 Atualizar Dados"):
        st.rerun()
