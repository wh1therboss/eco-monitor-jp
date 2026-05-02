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

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

# --- 2. ESTADO DA SESSÃO (COORDENADAS) ---
# Se não houver nada marcado, começa no centro de João Pessoa
if 'lat' not in st.session_state:
    st.session_state.lat = -7.1153
    st.session_state.lon = -34.8611
    st.session_state.end = ""

geolocator = Nominatim(user_agent="eco_jp_final_fix")

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("### LEGO EXPLORERS")
    st.write("---")
    st.caption("Clique no mapa para ajustar o local.")

st.title("♻️ EcoColeta JP")

# --- 3. FORMULÁRIO ---
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Detalhes do Descarte")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        # Mostra o endereço capturado pelo clique
        end_input = st.text_input("Endereço aproximado:", value=st.session_state.end)
    with col_num:
        numero = st.text_input("Nº:")
        
    tipo_lixo = st.selectbox("O que você encontrou?", [
        "📦 Plástico / Embalagens", "📄 Papel / Papelão", "🍾 Vidro",
        "🥫 Metal / Latas", "🍎 Orgânico", "🏗️ Entulho", "🛋️ Móveis / Sofás",
        "💻 Eletrônico", "🌿 Poda / Galhos", "🩺 Hospitalar", "🛞 Pneus", "🧪 Químico / Óleo"
    ])
    
    anonimo = st.checkbox("🕵️ Fazer denúncia anônima")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if st.session_state.end != "":
            autor = "Anônimo" if anonimo else "Cidadão"
            
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": f"{end_input}, {numero}" if numero else end_input,
                "Tipo": tipo_lixo,
                "Autor": autor,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Localizado e Registrado!")
            st.balloons()
            # Reseta o endereço após o envio
            st.session_state.end = ""
        else:
            st.warning("⚠️ ERRO: Você precisa clicar no mapa para marcar o local primeiro!")

# --- 4. MAPA (O CORAÇÃO DO PROBLEMA) ---
st.write("---")
st.subheader("📍 TOQUE NO MAPA NO LOCAL DO LIXO")

# Criamos o objeto do mapa
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=17)

# Adicionamos o marcador exatamente onde está a coordenada da sessão
folium.Marker(
    [st.session_state.lat, st.session_state.lon], 
    popup="Local selecionado",
    icon=folium.Icon(color='red', icon='trash')
).add_to(m)

# O st_folium agora tem um ID dinâmico baseado na coordenada para forçar o refresh
mapa_retorno = st_folium(
    m, 
    width=700, 
    height=450, 
    key=f"mapa_{st.session_state.lat}" # Isso aqui é o que resolve o erro do local!
)

# Lógica de captura do clique
if mapa_retorno['last_clicked']:
    clique_lat = mapa_retorno['last_clicked']['lat']
    clique_lon = mapa_retorno['last_clicked']['lng']
    
    # Se o clique for novo, atualiza a sessão e recarrega
    if clique_lat != st.session_state.lat:
        st.session_state.lat = clique_lat
        st.session_state.lon = clique_lon
        try:
            # Busca o nome da rua pelo GPS
            loc = geolocator.reverse(f"{clique_lat}, {clique_lon}")
            st.session_state.end = loc.address.split(',')[0]
        except:
            st.session_state.end = "Local marcado no mapa"
        st.rerun()
