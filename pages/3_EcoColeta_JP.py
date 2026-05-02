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
    st.caption("Colabore com a limpeza de João Pessoa!")

# --- LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_jp_v6")

# Inicia no centro de João Pessoa se não houver clique
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
        "📦 Plástico / Embalagens",
        "📄 Papel / Papelão",
        "🍾 Vidro",
        "🥫 Metal / Latas",
        "🍎 Restos de Alimentos (Orgânico)",
        "🏗️ Entulho de Construção",
        "🛋️ Móveis / Sofás / Colchões",
        "💻 Lixo Eletrônico",
        "🌿 Poda de Árvores / Galhos",
        "🩺 Lixo Hospitalar / Máscaras",
        "🛞 Pneus",
        "🧪 Produtos Químicos / Óleo"
    ])
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if end_input:
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": f"{end_input}, {numero}" if numero else end_input,
                "Tipo": tipo_lixo,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Registrado com sucesso!")
            st.balloons()
            st.session_state.end = "" 
        else:
            st.warning("⚠️ Clique no mapa para indicar o local exato.")

# --- MAPA INTERATIVO ---
st.write("---")
st.subheader("📍 Toque no mapa para marcar o local exato")

# Cria o mapa centralizado no ponto atual
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=16)

# Adiciona o marcador vermelho no local selecionado
folium.Marker(
    [st.session_state.lat, st.session_state.lon], 
    icon=folium.Icon(color='red', icon='trash')
).add_to(m)

# Captura o clique e atualiza
mapa_retorno = st_folium(m, width=700, height=400, key="mapa_coleta")

if mapa_retorno['last_clicked']:
    nova_lat = mapa_retorno['last_clicked']['lat']
    nova_lon = mapa_retorno['last_clicked']['lng']
    
    # Só atualiza se o clique for em um lugar novo
    if nova_lat != st.session_state.lat:
        st.session_state.lat = nova_lat
        st.session_state.lon = nova_lon
        try:
            loc = geolocator.reverse(f"{nova_lat}, {nova_lon}")
            st.session_state.end = loc.address.split(',')[0]
        except:
            st.session_state.end = "Local marcado"
        st.rerun()
