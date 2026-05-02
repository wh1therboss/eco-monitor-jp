import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")

CAMINHO_CSV = 'denuncias.csv'
geolocator = Nominatim(user_agent="eco_jp_final_v10")

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

# --- 2. ESTADO DA SESSÃO ---
if 'lat' not in st.session_state:
    st.session_state.lat = -7.1153
    st.session_state.lon = -34.8611
if 'endereco_digitado' not in st.session_state:
    st.session_state.endereco_digitado = ""

st.title("♻️ EcoColeta JP")

# --- 3. CAMPO DE DIGITAÇÃO (BUSCA) ---
st.subheader("Onde está o problema?")
texto_busca = st.text_input("Digite a rua e número (ou clique no mapa):", value=st.session_state.endereco_digitado)

# BOTÃO PARA ATUALIZAR O MAPA BASEADO NO QUE FOI DIGITADO
if st.button("🔍 Localizar no Mapa"):
    if texto_busca:
        try:
            # Transforma TEXTO em COORDENADA
            location = geolocator.geocode(f"{texto_busca}, João Pessoa, PB")
            if location:
                st.session_state.lat = location.latitude
                st.session_state.lon = location.longitude
                st.session_state.endereco_digitado = texto_busca
                st.success(f"Localizado: {location.address}")
                st.rerun()
            else:
                st.error("Não achei esse endereço. Tente ser mais específico (ex: Rua tal, bairro).")
        except:
            st.error("Erro na busca. Tente clicar no mapa.")

# --- 4. O MAPA ---
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=17)
folium.Marker([st.session_state.lat, st.session_state.lon], 
              icon=folium.Icon(color='red', icon='trash', prefix='fa')).add_to(m)

# Captura clique manual no mapa também
mapa_dados = st_folium(m, width=700, height=400, key="mapa_v10")

if mapa_dados['last_clicked']:
    n_lat = mapa_dados['last_clicked']['lat']
    n_lon = mapa_dados['last_clicked']['lng']
    if n_lat != st.session_state.lat:
        st.session_state.lat = n_lat
        st.session_state.lon = n_lon
        try:
            # Transforma COORDENADA em TEXTO
            location = geolocator.reverse(f"{n_lat}, {n_lon}")
            st.session_state.endereco_digitado = location.address.split(',')[0]
        except:
            st.session_state.endereco_digitado = "Local marcado"
        st.rerun()

# --- 5. FORMULÁRIO DE ENVIO ---
st.write("---")
with st.form("form_final"):
    tipo_lixo = st.selectbox("O que você encontrou?", [
        "📦 Plástico", "📄 Papel", "🍾 Vidro", "🥫 Metal", 
        "🍎 Orgânico", "🏗️ Entulho", "🛋️ Móveis", "💻 Eletrônico", 
        "🌿 Poda", "🩺 Hospitalar", "🛞 Pneus", "🧪 Químico"
    ])
    
    anonimo = st.checkbox("🕵️ Denúncia Anônima")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if st.session_state.endereco_digitado:
            autor = "Anônimo" if anonimo else "Cidadão"
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": st.session_state.endereco_digitado,
                "Tipo": tipo_lixo,
                "Autor": autor,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Denúncia salva no local correto!")
            st.balloons()
        else:
            st.error("⚠️ Digite um endereço ou clique no mapa primeiro!")

st.sidebar.image("hamtaro.webp", width=150)
