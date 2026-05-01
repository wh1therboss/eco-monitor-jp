import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import requests

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")

# --- 2. LINKS IMPORTANTES (AJUSTE AQUI) ---
# 1. Coloque o link do seu Apps Script (o que termina em /exec)
URL_PROJETO_GOOGLE = "COLE_AQUI_O_SEU_URL_DO_APPS_SCRIPT"

# 2. Coloque o link NORMAL da sua planilha (aquele que você abre para ver os dados)
LINK_DA_PLANILHA_VISUALIZAR = "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit"

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("### LEGO EXPLORERS")
    st.write("---")
    # BOTÃO PARA ABRIR A PLANILHA
    st.markdown(f"""
        <a href="{LINK_DA_PLANILHA_VISUALIZAR}" target="_blank">
            <button style="
                width: 100%;
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;">
                📊 ABRIR PLANILHA DE DADOS
            </button>
        </a>
    """, unsafe_allow_html=True)
    st.write("---")

# --- 3. LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_jp_v3")

if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat, st.session_state.clique_lon = -7.1153, -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")
st.markdown("Relate descartes irregulares e ajude a manter João Pessoa limpa!")

# --- 4. FORMULÁRIO ---
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
    
    anonimo = st.checkbox("Denúncia Anônima")

    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua_input:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            endereco_final = f"{rua_input}, {numero_input}" if numero_input else rua_input
            
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
                # Envia os dados para a planilha via Apps Script
                response = requests.post(URL_PROJETO_GOOGLE, json=dados)
                if response.status_code == 200:
                    st.success("✅ Denúncia registrada com sucesso!")
                    st.balloons()
                    st.session_state.endereco_clique = ""
                    st.rerun()
                else:
                    st.error("Erro ao salvar. Verifique o link do Apps Script.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
        else:
            st.warning("⚠️ Selecione o local no mapa.")

# --- 5. MAPA ---
st.write("---")
st.subheader("📍 Toque no mapa para marcar o local")
m = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=15)
folium.Marker([st.session_state.clique_lat, st.session_state.clique_lon], icon=folium.Icon(color='red')).add_to(m)

output = st_folium(m, width=700, height=350, key="mapa_click")

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
