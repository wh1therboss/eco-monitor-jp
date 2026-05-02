import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")

CAMINHO_CSV = 'denuncias.csv'

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("### LEGO EXPLORERS")
    st.write("---")
    st.caption("Acesso restrito para cidadãos.")

# --- LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_csv_v5")

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
    st.session_state.end = ""

st.title("♻️ EcoColeta JP")
st.markdown("### 📝 Relatar Ocorrência")

# --- FORMULÁRIO ---
with st.form("form_csv", clear_on_submit=True):
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        end_input = st.text_input("Localização/Rua:", value=st.session_state.end)
    with col_num:
        numero = st.text_input("Nº:")
        
    tipo_lixo = st.selectbox("Tipo de Resíduo:", ["Plástico", "Vidro", "Entulho", "Orgânico", "Outros"])
    
    if st.form_submit_button("🚀 GRAVAR DENÚNCIA"):
        if end_input:
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": f"{end_input}, {numero}" if numero else end_input,
                "Tipo": tipo_lixo,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Denúncia enviada com sucesso!")
            st.balloons()
            st.session_state.end = ""
        else:
            st.warning("⚠️ Por favor, selecione o local no mapa abaixo.")

# --- MAPA ---
st.write("---")
st.subheader("📍 Marque o local no mapa")
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=15)
folium.Marker([st.session_state.lat, st.session_state.lon], icon=folium.Icon(color='red')).add_to(m)

mapa = st_folium(m, width=700, height=350)

if mapa['last_clicked']:
    lt, ln = mapa['last_clicked']['lat'], mapa['last_clicked']['lng']
    st.session_state.lat, st.session_state.lon = lt, ln
    try:
        loc = geolocator.reverse(f"{lt}, {ln}")
        st.session_state.end = loc.address.split(',')[0]
    except: 
        st.session_state.end = "Local marcado"
    st.rerun()
