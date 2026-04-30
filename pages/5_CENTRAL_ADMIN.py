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
    st.info("Protocolo Friday ativado.")

# --- 2. TRAVA DE SEGURANÇA (SÓ A FRIDAY ENTRA) ---
# Atualizado conforme sua mudança
USER_ADMIN = "Friday" 

# Verifica se está logado de forma segura
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Sistema Bloqueado. Identifique-se na página principal.")
    st.stop()

# Pega o usuário logado (evita o erro de AttributeError que vimos antes)
usuario_logado = st.session_state.get('usuario_atual', 'Desconhecido')

if usuario_logado != USER_ADMIN:
    st.warning(f"⚠️ Acesso negado para {usuario_logado}. Somente a 'Friday' possui nível de acesso 5.")
    st.stop()

# --- 3. INÍCIO DO PAINEL ADMIN ---
st.title("🖥️ Central de Comando LEGO Explorers")
st.success(f"Bem-vinda de volta, **{usuario_logado}**! Todos os sistemas operacionais.")

DATA_COLETA = "denuncias_ecocoleta.csv"
DATA_LUZ = "alertas_iluminacao.csv"

# Função para carregar dados com a coluna de Status
def carregar_dados(caminho, colunas_padrao):
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        if 'Status' not in df.columns:
            df['Status'] = "Pendente"
        return df
    return pd.DataFrame(columns=colunas_padrao + ['Status'])

df_lixo = carregar_dados(DATA_COLETA, ['Data', 'Rua', 'Tipo', 'Autor'])
df_luz = carregar_dados(DATA_LUZ, ['Data', 'Bairro', 'Rua', 'Problema', 'Autor'])

# --- 4. GESTÃO DE DENÚNCIAS E STATUS ---
tab1, tab2, tab3 = st.tabs(["♻️ EcoColeta", "💡 IluminaJP", "⚙️ Sistema"])

with tab1:
    st.subheader("Controle de Resíduos")
    if not df_lixo.empty:
        idx = st.selectbox("ID da Denúncia:", df_lixo.index, key="lixo_idx")
        novo_status = st.selectbox("Atualizar para:", ["Pendente", "Em Processo", "Resolvido"], key="lixo_st")
        if st.button("Confirmar Alteração Lixo"):
            df_lixo.at[idx, 'Status'] = novo_status
            df_lixo.to_csv(DATA_COLETA, index=False)
            st.rerun()
        st.dataframe(df_lixo, use_container_width=True)

with tab2:
    st.subheader("Controle de Iluminação")
    if not df_luz.empty:
        idx_l = st.selectbox("ID do Alerta:", df_luz.index, key="luz_idx")
        novo_status_l = st.selectbox("Atualizar para:", ["Aguardando", "Manutenção", "Concluído"], key="luz_st")
        if st.button("Confirmar Alteração Luz"):
            df_luz.at[idx_l, 'Status'] = novo_status_l
            df_luz.to_csv(DATA_LUZ, index=False)
            st.rerun()
        st.dataframe(df_luz, use_container_width=True)

with tab3:
    st.subheader("Status dos Servidores")
    st.write("Base de dados: Online")
    if st.button("🚨 Resetar Protocolos (Limpar tudo)"):
        if os.path.exists(DATA_COLETA): os.remove(DATA_COLETA)
        if os.path.exists(DATA_LUZ): os.remove(DATA_LUZ)
        st.rerun()
