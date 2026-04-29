import streamlit as st

# ==========================================
# 1. TRAVA DE SEGURANÇA (OBRIGATÓRIO NO TOPO)
# ==========================================
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso negado! Por favor, faça login na página principal (main).")
    st.stop()  # Para o código aqui se não houver login

# ==========================================
# 2. CONFIGURAÇÃO DA PÁGINA
# ==========================================
usuario = st.session_state.get('usuario_atual', 'Explorador')

st.title("💧 Sistema AquaGuard JP")
st.subheader(f"Colaborador: {usuario}")

st.markdown("""
---
### 🌊 Monitoramento Hídrico
Bem-vindo ao painel de controle da **LEGO Explorers**. 
Aqui monitoramos o nível das águas e o consumo em João Pessoa.
""")

# Exemplo de Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Nível do Rio", "78%", "+2%")
col2.metric("Qualidade", "Excelente", "98/100")
col3.metric("Consumo Médio", "120L", "-5%")

st.info("Dica: Use os relatórios mensais para análise de desperdício.")
