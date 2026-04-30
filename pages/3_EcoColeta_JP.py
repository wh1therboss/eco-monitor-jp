import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# --- SIDEBAR PERSONALIZADA: ECOCOLETA ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ♻️ Gestão de Resíduos")
    st.warning("ALERTA: PONTOS DE DESCARTE")
    st.metric("Reciclagem Mensal", "45%", "+2%")
    st.info("Ajude a manter as praias de JP limpas. Denuncie descarte irregular.")

# --- SEGURANÇA E DADOS ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário.")
    st.stop()

DATA_DB = "denuncias_ecocoleta.csv"
colunas_sistema = ['Data', 'Bairro', 'Rua', 'Numero', 'Referencia', 'Tipo', 'Autor', 'lat', 'lon']

# Previne erro de coluna faltando
if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        df_lido = pd.read_csv(DATA_DB)
        for col in colunas_sistema:
            if col not in df_lido.columns: df_lido[col] = "N/A"
        st.session_state.db_relatos = df_lido
    else:
        st.session_state.db_relatos = pd.DataFrame(columns=colunas_sistema)

st.title("♻️ EcoColeta JP")

# Formulário Detalhado
with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📢 Registrar Descarte de Lixo")
    rua = st.text_input("Rua/Avenida:")
    col_n, col_r = st.columns([1, 2])
    with col_n: num = st.text_input("Nº:")
    with col_r: ref = st.text_input("Ponto de Referência:")
    tipo = st.radio("Tipo de Lixo:", ["Plástico", "Orgânico", "Entulho"], horizontal=True)
    anonimo = st.checkbox("Denúncia Anônima")
    
    if st.form_submit_button("🚀 ENVIAR"):
        autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
        novo = {'Data': datetime.now().strftime("%d/%m/%Y"), 'Bairro': "João Pessoa", 'Rua': rua, 
                'Numero': num, 'Referencia': ref, 'Tipo': tipo, 'Autor': autor, 'lat': -7.12, 'lon': -34.82}
        st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo])], ignore_index=True)
        st.session_state.db_relatos.to_csv(DATA_DB, index=False)
        st.success("Denúncia Registrada!")
        st.rerun()

# Mapa e Tabela Blindada contra KeyError
m = folium.Map(location=[-7.120, -34.820], zoom_start=12)
folium_static(m, width=700)
st.dataframe(st.session_state.db_relatos[['Data', 'Rua', 'Tipo', 'Autor']], use_container_width=True)
