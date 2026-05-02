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
    st.caption("Sua identidade está protegida se desejar.")

# --- LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_jp_v7")

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
    st.session_state.end = ""

st.title("♻️ EcoColeta JP")

# --- FORMULÁRIO ---
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Registrar Descarte Irregular")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        end_input = st.text_input("Localização (clique no mapa):", value=st.session_state.end)
    with col_num:
        numero = st.text_input("Nº:")
        
    tipo_lixo = st.selectbox("O que foi descartado?", [
        "📦 Plástico / Embalagens", "📄 Papel / Papelão", "🍾 Vidro",
        "🥫 Metal / Latas", "🍎 Orgânico", "🏗️ Entulho", "🛋️ Móveis",
        "💻 Eletrônico", "🌿 Poda / Galhos", "🩺 Hospitalar", "🛞 Pneus", "🧪 Químico"
    ])
    
    # NOVA OPÇÃO: ANONIMATO
    anonimo = st.checkbox("🕵️ Desejo fazer uma denúncia anônima")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if end_input:
            # Define o autor baseado no checkbox
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Cidadão')
            
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": f"{end_input}, {numero}" if numero else end_input,
                "Tipo": tipo_lixo,
                "Autor": autor,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Denúncia registrada! Obrigado por ajudar João Pessoa.")
            st.balloons()
            st.session_state.end = "" 
        else:
            st.warning("⚠️ Clique no mapa para indicar o local.")

# --- MAPA ---
st.write("---")
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=16)
folium.Marker([st.session_state.lat, st.session_state.lon], icon=folium.Icon(color='red', icon='trash')).add_to(m)

mapa_retorno = st_folium(m, width=700, height=400, key="mapa_v7")

if mapa_retorno['last_clicked']:
    nova_lat = mapa_retorno['last_clicked']['lat']
    nova_lon = mapa_retorno['last_clicked']['lng']
    if nova_lat != st.session_state.lat:
        st.session_state.lat, st.session_state.lon = nova_lat, nova_lon
        try:
            loc = geolocator.reverse(f"{nova_lat}, {nova_lon}")
            st.session_state.end = loc.address.split(',')[0]
        except: st.session_state.end = "Local marcado"
        st.rerun()
