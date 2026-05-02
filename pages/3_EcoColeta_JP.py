import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os
import random
import string

st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")
CAMINHO_CSV = 'denuncias.csv'
geolocator = Nominatim(user_agent="eco_jp_final_v13")

def gerar_protocolo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
if 'endereco' not in st.session_state:
    st.session_state.endereco = ""

st.title("♻️ EcoColeta JP")

# --- BUSCA E MAPA ---
st.subheader("Onde está o problema?")
endereco_digitado = st.text_input("Digite a rua e número:", value=st.session_state.endereco)

if st.button("🔍 Localizar"):
    if endereco_digitado:
        try:
            location = geolocator.geocode(f"{endereco_digitado}, João Pessoa, PB")
            if location:
                st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
                st.session_state.endereco = endereco_digitado
                st.rerun()
        except: st.error("Erro na busca.")

m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=18)
folium.Marker([st.session_state.lat, st.session_state.lon], icon=folium.Icon(color='red', icon='trash', prefix='fa')).add_to(m)
mapa_dados = st_folium(m, width=700, height=400, key=f"mapa_{st.session_state.lat}")

if mapa_dados['last_clicked']:
    st.session_state.lat, st.session_state.lon = mapa_dados['last_clicked']['lat'], mapa_dados['last_clicked']['lng']
    try:
        rev = geolocator.reverse(f"{st.session_state.lat}, {st.session_state.lon}")
        st.session_state.endereco = rev.address.split(',')[0]
    except: st.session_state.endereco = "Local marcado"
    st.rerun()

# --- FORMULÁRIO ---
with st.form("envio"):
    tipo = st.selectbox("Tipo:", ["📦 Plástico", "📄 Papel", "🍾 Vidro", "🥫 Metal", "🍎 Orgânico", "🏗️ Entulho", "🛋️ Móveis", "💡 Iluminação Pública"])
    anonimo = st.checkbox("🕵️ Denúncia Anônima")
    if st.form_submit_button("🚀 ENVIAR"):
        if st.session_state.endereco:
            prot = gerar_protocolo()
            salvar_no_csv({
                "Protocolo": prot, "Data": datetime.now().strftime("%d/%m/%Y"),
                "Endereco": st.session_state.endereco, "Tipo": tipo,
                "Autor": "Anônimo" if anonimo else "Cidadão",
                "Status": "Pendente 🟡", "Lat": st.session_state.lat, "Lon": st.session_state.lon
            })
            st.success(f"✅ Enviado! PROTOCOLO: {prot}")
            st.info("Guarde seu protocolo para consultar depois.")
            st.balloons()
