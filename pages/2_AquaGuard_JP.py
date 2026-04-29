import streamlit as st

# --- TRAVA DE SEGURANÇA ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso negado! Por favor, faz login na página principal (main).")
    st.stop()

# Agora que sabemos que está logado, podemos usar a variável
usuario = st.session_state.usuario_atual

st.title("💧 Sistema AquaGuard JP")
st.subheader(f"Colaborador: {usuario}")

st.info("Painel de monitorização de recursos hídricos em João Pessoa.")

# Exemplo de funcionalidade (podes manter o teu código original abaixo disto)
st.metric(label="Nível do Reservatório", value="85%", delta="2%")
