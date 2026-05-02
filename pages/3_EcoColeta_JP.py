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
geolocator = Nominatim(user_agent="eco_jp_final_v12")

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

# --- 2. ESTADO DA SESSÃO ---
if 'lat' not in st.session_state:
    st.session_state.lat = -7.1153
    st.session_state.lon = -34.8611
if 'endereco' not in st.session_state:
    st.session_state.endereco = ""

st.title("♻️ EcoColeta JP")

# --- 3. ÁREA DE BUSCA ---
st.subheader("Onde está o problema?")
col_busca, col_btn = st.columns([4, 1])

with col_busca:
    # Campo de texto que aceita digitação
    endereco_digitado = st.text_input("Digite a rua e número:", value=st.session_state.endereco)

with col_btn:
    st.write(" ") # Alinhamento
    buscar = st.button("🔍 Localizar")

if buscar and endereco_digitado:
    try:
        location = geolocator.geocode(f"{endereco_digitado}, João Pessoa, PB")
        if location:
            st.session_state.lat = location.latitude
            st.session_state.lon = location.longitude
            st.session_state.endereco = endereco_digitado
            st.rerun()
        else:
            st.error("Rua não encontrada.")
    except:
        st.error("Serviço de busca ocupado.")

# --- 4. MAPA INTERATIVO ---
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=18)
folium.Marker([st.session_state.lat, st.session_state.lon], 
              icon=folium.Icon(color='red', icon='trash', prefix='fa')).add_to(m)

# Key dinâmica para o mapa se mover quando as coordenadas mudarem
mapa_dados = st_folium(m, width=700, height=400, key=f"mapa_{st.session_state.lat}_{st.session_state.lon}")

# Se clicar no mapa, atualiza o texto e a posição
if mapa_dados['last_clicked']:
    st.session_state.lat = mapa_dados['last_clicked']['lat']
    st.session_state.lon = mapa_dados['last_clicked']['lng']
    try:
        rev_loc = geolocator.reverse(f"{st.session_state.lat}, {st.session_state.lon}")
        st.session_state.endereco = rev_loc.address.split(',')[0]
    except:
        st.session_state.endereco = "Local marcado no mapa"
    st.rerun()

# --- 5. FORMULÁRIO DE ENVIO ---
st.write("---")
with st.form("enviar_denuncia", clear_on_submit=True):
    st.markdown("### Detalhes da Ocorrência")
    
    tipo_lixo = st.selectbox("O que é?", [
        "📦 Plástico", "📄 Papel", "🍾 Vidro", "🥫 Metal", "🍎 Orgânico", 
        "🏗️ Entulho", "🛋️ Móveis", "💻 Eletrônico", "🌿 Poda", "🩺 Hospitalar", "🛞 Pneus"
    ])
    
    anonimo = st.checkbox("🕵️ Denúncia Anônima")
    
    if st.form_submit_button("🚀 GRAVAR NO CSV"):
        if st.session_state.endereco:
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": st.session_state.endereco,
                "Tipo": tipo_lixo,
                "Autor": "Anônimo" if anonimo else "Cidadão",
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Denúncia salva com sucesso!")
            st.balloons()
            st.session_state.endereco = "" 
        else:
            st.error("⚠️ Localização vazia!")

st.sidebar.image("hamtaro.webp", width=150)
st.sidebar.markdown("### LEGO EXPLORERS")
