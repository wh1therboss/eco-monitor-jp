import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import requests  # Importante: Adicione 'requests' no seu requirements.txt

# --- 1. CONFIGURAÇÃO DA SIDEBAR ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.caption("v0.3 - Cloud Sync")

# --- 2. CONFIGURAÇÃO DO GOOGLE SCRIPT ---
# COLOQUE O SEU LINK QUE TERMINA EM /exec ENTRE AS ASPAS ABAIXO:
URL_PROJETO_GOOGLE = "https://script.google.com/macros/s/AKfycbwXi0mTvqcgeQYfjsaJFaV1A0lZWNZDxmciPXWonMPARuE8FlUaPf4gxA5rypxVLQ97/exec"

# --- 3. LOGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_jp_v3")

if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat, st.session_state.clique_lon = -7.1153, -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")

# --- 4. FORMULÁRIO DE DENÚNCIA ---
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Detalhes da Ocorrência")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        rua_input = st.text_input("Rua/Avenida:", value=st.session_state.endereco_clique)
    with col_num:
        numero_input = st.text_input("Nº:")

    tipo = st.selectbox("Tipo de Resíduo:", [
        "📦 Plásticos/Embalagens", "📄 Papel/Papelão", "🍾 Vidro", 
        "🥫 Metal", "🍎 Orgânico", "🏗️ Entulho", "🛋️ Móveis", "💻 Eletrônicos"
    ])
    
    anonimo = st.checkbox("Fazer denúncia anônima")

    if st.form_submit_button("🚀 ENVIAR PARA A PLANILHA"):
        if rua_input:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            endereco_final = f"{rua_input}, {numero_input}" if numero_input else rua_input
            
            # Dados formatados para o Apps Script
            dados = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereço_Completo": endereco_final,
                "Tipo": tipo,
                "Autor": autor,
                "lat": st.session_state.clique_lat,
                "lon": st.session_state.clique_lon,
                "Status": "Pendente"
            }
            
            try:
                # Envio via POST para o Google
                response = requests.post(URL_PROJETO_GOOGLE, json=dados)
                
                if response.status_code == 200:
                    st.success("✅ Denúncia salva com sucesso na planilha!")
                    st.balloons()
                    st.session_state.endereco_clique = ""
                    st.rerun()
                else:
                    st.error(f"Erro no servidor Google: {response.status_code}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
        else:
            st.warning("⚠️ Por favor, selecione um local no mapa ou digite o endereço.")

# --- 5. MAPA PARA SELEÇÃO ---
st.write("---")
st.subheader("📍 Selecione o Local no Mapa")
m = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=15)
folium.Marker([st.session_state.clique_lat, st.session_state.clique_lon], icon=folium.Icon(color='red')).add_to(m)

output = st_folium(m, width=700, height=350, key="mapa_sync")

if output['last_clicked']:
    lt, ln = output['last_clicked']['lat'], output['last_clicked']['lng']
    if lt != st.session_state.clique_lat:
        st.session_state.clique_lat, st.session_state.clique_lon = lt, ln
        try:
            loc = geolocator.reverse(f"{lt}, {ln}")
            if loc:
                st.session_state.endereco_clique = loc.address.split(',')[0]
        except: pass
        st.rerun()

st.info("💡 As denúncias enviadas são registradas em tempo real na planilha do projeto.")
