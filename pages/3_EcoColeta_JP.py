import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# --- 1. SEGURANÇA E IDENTIDADE ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

# Identidade LEGO Explorers com Hamtaro
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("hamtaro.webp", width=100)
with col_titulo:
    st.title("LEGO Explorers")
    st.subheader("♻️ EcoColeta JP")

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"

# --- 2. BANCO DE DADOS (CORREÇÃO DE COLUNAS) ---
praias_coords = {
    "Bessa": [-7.085, -34.830], "Manaíra": [-7.092, -34.831], 
    "Tambaú": [-7.114, -34.820], "Cabo Branco": [-7.135, -34.818], 
    "Penha": [-7.165, -34.795], "Seixas": [-7.155, -34.790]
}

# Lista completa das colunas que o sistema precisa ter
colunas_sistema = ['Data', 'Bairro', 'Rua', 'Numero', 'Referencia', 'Tipo', 'Autor', 'lat', 'lon']

if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        df_lido = pd.read_csv(DATA_DB)
        # RESOLUÇÃO DO ERRO: Adiciona colunas faltando se o CSV for antigo
        for col in colunas_sistema:
            if col not in df_lido.columns:
                df_lido[col] = "N/A"
        st.session_state.db_relatos = df_lido
    else:
        st.session_state.db_relatos = pd.DataFrame(columns=colunas_sistema)

# --- 3. FORMULÁRIO DETALHADO ---
with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📍 Registrar Ocorrência")
    bairro_sel = st.selectbox("Bairro/Praia:", list(praias_coords.keys()))
    rua = st.text_input("Rua/Avenida:")
    
    col_n, col_r = st.columns([1, 2])
    with col_n: num = st.text_input("Nº:")
    with col_r: ref = st.text_input("Ponto de Referência:")
    
    tipo_lixo = st.radio("Tipo de Resíduo:", ["Plástico", "Orgânico", "Entulho", "Redes"], horizontal=True)
    fazer_anonimo = st.checkbox("Denúncia Anônima 🕵️")
    
    if st.form_submit_button("🚀 ENVIAR"):
        if rua and ref:
            autor = "Anônimo" if fazer_anonimo else usuario_logado
            novo = {
                'Data': datetime.now().strftime("%d/%m/%Y"),
                'Bairro': bairro_sel, 'Rua': rua, 'Numero': num if num else "S/N",
                'Referencia': ref, 'Tipo': tipo_lixo, 'Autor': autor,
                'lat': praias_coords[bairro_sel][0], 'lon': praias_coords[bairro_sel][1]
            }
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            st.success("✅ Denúncia registrada!")
            st.rerun()
        else:
            st.warning("Preencha a Rua e a Referência!")

# --- 4. MAPA E TABELA (BLINDADOS) ---
st.write("---")
st.subheader("📍 Mapa de Resíduos")
m = folium.Map(location=[-7.120, -34.820], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    cor = 'red' if r['Autor'] == 'Anônimo' else 'blue'
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"{r['Tipo']} - Ref: {r['Referencia']}",
        icon=folium.Icon(color=cor, icon='trash')
    ).add_to(m)

folium_static(m, width=900)

st.subheader("📊 Histórico de Coleta")
# Exibe apenas as colunas que agora temos certeza que existem
st.dataframe(st.session_state.db_relatos[['Data', 'Bairro', 'Rua', 'Tipo', 'Autor']], use_container_width=True)
