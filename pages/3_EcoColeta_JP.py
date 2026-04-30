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

# Cabeçalho LEGO Explorers com Hamtaro
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("hamtaro.webp", width=100)
with col_titulo:
    st.title("LEGO Explorers")
    st.subheader("♻️ EcoColeta JP")

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"

# --- 2. BANCO DE DADOS (COM CORREÇÃO DE COLUNAS) ---
praias_coords = {
    "Bessa": [-7.085, -34.830], "Manaíra": [-7.092, -34.831], 
    "Tambaú": [-7.114, -34.820], "Cabo Branco": [-7.135, -34.818], 
    "Penha": [-7.165, -34.795], "Seixas": [-7.155, -34.790]
}

# Lista oficial de colunas que o sistema precisa
colunas_necessarias = ['Data', 'Bairro', 'Rua', 'Numero', 'Referencia', 'Tipo', 'Autor', 'lat', 'lon']

if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        df_lido = pd.read_csv(DATA_DB)
        # CORREÇÃO DO ERRO: Garante que todas as colunas novas existam
        for col in colunas_necessarias:
            if col not in df_lido.columns:
                df_lido[col] = "Não informado"
        st.session_state.db_relatos = df_lido
    else:
        st.session_state.db_relatos = pd.DataFrame(columns=colunas_necessarias)

# --- 3. FORMULÁRIO DETALHADO E ANÓNIMO ---
with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📍 Detalhes da Localização")
    bairro_sel = st.selectbox("Bairro/Praia:", list(praias_coords.keys()))
    rua = st.text_input("Rua/Avenida:")
    
    col_n, col_r = st.columns([1, 2])
    with col_n: num = st.text_input("Nº:")
    with col_r: ref = st.text_input("Ponto de Referência:")
    
    tipo_lixo = st.radio("Tipo de Resíduo:", ["Plástico", "Orgânico", "Entulho", "Rede de Pesca"], horizontal=True)
    fazer_anonimo = st.checkbox("Fazer denúncia de forma anónima 🕵️")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua and ref:
            autor_final = "Anónimo" if fazer_anonimo else usuario_logado
            novo_relato = {
                'Data': datetime.now().strftime("%d/%m/%Y"),
                'Bairro': bairro_sel, 'Rua': rua, 'Numero': num if num else "S/N",
                'Referencia': ref, 'Tipo': tipo_lixo, 'Autor': autor_final,
                'lat': praias_coords[bairro_sel][0], 'lon': praias_coords[bairro_sel][1]
            }
            # Adiciona ao banco e guarda no CSV
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo_relato])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            st.success(f"✅ Denúncia registada! (Autor: {autor_final})")
            st.rerun()
        else:
            st.warning("⚠️ Por favor, preencha a Rua e o Ponto de Referência.")

# --- 4. MAPA E TABELA (SEM ERROS) ---
st.write("---")
st.subheader("📍 Mapa de Ocorrências")
m = folium.Map(location=[-7.120, -34.820], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    cor_ponto = 'red' if r['Autor'] == 'Anónimo' else 'blue'
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"<b>{r['Tipo']}</b><br>Ref: {r['Referencia']}<br>Por: {r['Autor']}",
        icon=folium.Icon(color=cor_ponto, icon='trash')
    ).add_to(m)

folium_static(m, width=900)

# Tabela final - Exibe apenas o que existe com segurança
st.subheader("📊 Histórico de Denúncias")
st.dataframe(st.session_state.db_relatos[['Data', 'Bairro', 'Rua', 'Tipo', 'Autor']], use_container_width=True)
