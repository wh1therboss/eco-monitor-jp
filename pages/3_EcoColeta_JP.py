import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# --- SEGURANÇA (OBRIGATÓRIO) ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

# --- CABEÇALHO LEGO EXPLORERS ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("hamtaro.webp", width=100)
with col_titulo:
    st.title("LEGO Explorers")
    st.subheader("♻️ EcoColeta JP")

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"

# --- LÓGICA DE DADOS ---
praias_jp = {"Bessa": [-7.085, -34.830], "Manaíra": [-7.092, -34.831], "Tambaú": [-7.114, -34.820], 
             "Cabo Branco": [-7.135, -34.818], "Penha": [-7.165, -34.795], "Seixas": [-7.155, -34.790]}

if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB): 
        st.session_state.db_relatos = pd.read_csv(DATA_DB)
    else: 
        st.session_state.db_relatos = pd.DataFrame(columns=['Bairro','Rua','Numero','Referencia','Tipo','Autor','Data','lat','lon'])

# --- FORMULÁRIO DETALHADO ---
with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📍 Registrar Descarte Irregular")
    bairro_sel = st.selectbox("Bairro/Praia:", list(praias_jp.keys()))
    rua = st.text_input("Nome da Rua:")
    
    col_n, col_r = st.columns([1, 2])
    with col_n: num = st.text_input("Número:")
    with col_r: ref = st.text_input("Ponto de Referência:")
    
    tipo_lixo = st.radio("Tipo de Resíduo:", ["Plástico", "Orgânico", "Entulho", "Rede de Pesca"], horizontal=True)
    fazer_anonimo = st.checkbox("Fazer denúncia de forma anónima")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua and ref:
            autor = "Anónimo" if fazer_anonimo else usuario_logado
            novo = {
                'Bairro': bairro_sel, 'Rua': rua, 'Numero': num if num else "S/N", 
                'Referencia': ref, 'Tipo': tipo_lixo, 'Autor': autor, 
                'Data': datetime.now().strftime("%d/%m/%Y"), 
                'lat': praias_jp[bairro_sel][0], 'lon': praias_jp[bairro_sel][1]
            }
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            st.success(f"Denúncia registada com sucesso! (Autor: {autor})")
            st.rerun()
        else:
            st.warning("Por favor, preencha a Rua e a Referência.")

# --- MAPA DE OCORRÊNCIAS ---
st.write("---")
st.subheader("📍 Localização dos Registos")
m = folium.Map(location=[-7.120, -34.820], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    # Vermelho para anónimo, Azul para identificado
    cor_ponto = 'red' if r['Autor'] == 'Anónimo' else 'blue'
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"Tipo: {r['Tipo']} | Ref: {r['Referencia']}", 
        icon=folium.Icon(color=cor_ponto, icon='trash')
    ).add_to(m)

folium_static(m, width=900)

# Tabela de Histórico
st.dataframe(st.session_state.db_relatos[['Data', 'Bairro', 'Rua', 'Tipo', 'Autor']], use_container_width=True)
