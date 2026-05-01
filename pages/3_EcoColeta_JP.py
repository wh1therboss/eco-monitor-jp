import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")

# Caminho do ficheiro (ajusta se o csv estiver noutra pasta)
CAMINHO_CSV = 'denuncias.csv'

# Função para guardar no CSV
def salvar_no_csv(nova_linha):
    # Se o ficheiro já existir, adiciona sem o cabeçalho (mode='a')
    # Se não existir, cria com o cabeçalho
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("### LEGO EXPLORERS")
    st.write("---")
    if st.button("📊 Ver Dados Locais (DEBUG)"):
        if os.path.exists(CAMINHO_CSV):
            dados = pd.read_csv(CAMINHO_CSV)
            st.dataframe(dados)
        else:
            st.error("Ficheiro CSV ainda não criado.")

# --- 2. LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_csv_local")

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
    st.session_state.end = ""

st.title("♻️ EcoColeta JP (Modo CSV Local)")

# --- 3. FORMULÁRIO ---
with st.form("form_csv", clear_on_submit=True):
    st.markdown("### 📝 Relatar Ocorrência")
    end_input = st.text_input("Localização:", value=st.session_state.end)
    tipo_lixo = st.selectbox("Tipo:", ["Plástico", "Vidro", "Entulho", "Orgânico", "Outros"])
    
    if st.form_submit_button("🚀 GRAVAR NO CSV"):
        if end_input:
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": end_input,
                "Tipo": tipo_lixo,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            
            try:
                salvar_no_csv(nova_denuncia)
                st.success("✅ Gravado com sucesso no arquivo local!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao gravar: {e}")
        else:
            st.warning("⚠️ Selecione o local no mapa.")

# --- 4. MAPA ---
st.write("---")
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
