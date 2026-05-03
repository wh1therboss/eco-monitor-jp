import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os
import random
import string

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️", layout="wide")

# CSS para deixar a interface moderna
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .report-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_CSV = 'denuncias.csv'
geolocator = Nominatim(user_agent="eco_jp_v16_final", timeout=10)

def gerar_protocolo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    colunas = ["Protocolo", "Data", "Endereco", "Tipo", "Autor", "Status", "Lat", "Lon"]
    df_aux = df_aux.reindex(columns=colunas)
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

# --- ESTADO DA SESSÃO ---
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
if 'endereco' not in st.session_state:
    st.session_state.endereco = ""

# --- INTERFACE ---
st.title("♻️ EcoColeta João Pessoa")
st.markdown("---")

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.subheader("📍 Localização do Problema")
    
    # Campo de busca com botão ao lado
    c_busca, c_lupa = st.columns([3, 1])
    with c_busca:
        endereco_input = st.text_input("Digite rua e número:", value=st.session_state.endereco, placeholder="Ex: Av. Epitácio Pessoa, 100")
    with c_lupa:
        st.write(" ") # Alinhamento
        if st.button("🔍"):
            if endereco_input:
                try:
                    location = geolocator.geocode(f"{endereco_input}, João Pessoa, PB")
                    if location:
                        st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
                        st.session_state.endereco = endereco_input
                        st.success("Localizado!")
                        st.rerun() # FORÇA O MAPA A RECARREGAR NA POSIÇÃO NOVA
                    else:
                        st.error("Rua não encontrada.")
                except: st.error("Erro na busca.")

    st.info("💡 Você também pode clicar diretamente no mapa ao lado para marcar o local.")

    with st.form("form_denuncia"):
        st.subheader("📝 Detalhes da Denúncia")
        tipo_lixo = st.selectbox("O que você encontrou?", [
            "📦 Descarte Irregular de Lixo", "🏗️ Entulho de Obras", "🛋️ Móveis Abandonados", 
            "💻 Lixo Eletrônico", "🌿 Restos de Poda", "🩺 Lixo Hospitalar", "💡 Iluminação Apagada"
        ])
        
        detalhes = st.text_area("Ponto de Referência:", placeholder="Ex: Perto do mercadinho, em frente à árvore grande.")
        anonimo = st.checkbox("🕵️ Fazer denúncia anônima")
        
        submit = st.form_submit_button("🚀 ENVIAR DENÚNCIA")
        
        if submit:
            if st.session_state.endereco:
                prot = gerar_protocolo()
                salvar_no_csv({
                    "Protocolo": prot, "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Endereco": st.session_state.endereco, "Tipo": tipo_lixo,
                    "Autor": "Anônimo" if anonimo else "Cidadão", "Status": "Pendente 🟡",
                    "Lat": st.session_state.lat, "Lon": st.session_state.lon
                })
                st.success(f"✅ REGISTRADO! Protocolo: **{prot}**")
                st.balloons()
            else:
                st.error("⚠️ Marque o local no mapa primeiro!")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🗺️ Mapa de João Pessoa")
    
    # Criar o mapa folium
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=18, tiles='OpenStreetMap')
    folium.Marker(
        [st.session_state.lat, st.session_state.lon], 
        icon=folium.Icon(color='red', icon='trash', prefix='fa')
    ).add_to(m)

    # st_folium precisa de uma KEY única baseada na posição para forçar o refresh quando você digita
    mapa_interativo = st_folium(
        m, 
        width='100%', 
        height=550, 
        key=f"mapa_{st.session_state.lat}_{st.session_state.lon}" 
    )

    # Se o usuário clicar no mapa, atualiza as coordenadas e o endereço
    if mapa_interativo['last_clicked']:
        n_lat, n_lon = mapa_interativo['last_clicked']['lat'], mapa_interativo['last_clicked']['lng']
        if n_lat != st.session_state.lat:
            st.session_state.lat, st.session_state.lon = n_lat, n_lon
            try:
                rev = geolocator.reverse(f"{n_lat}, {n_lon}")
                st.session_state.endereco = rev.address.split(',')[0]
            except: st.session_state.endereco = "Local marcado no mapa"
            st.rerun()

# Sidebar com a logo (Hamtaro)
st.sidebar.image("hamtaro.webp", width=150)
st.sidebar.title("LEGO EXPLORERS")
st.sidebar.info("Projeto focado no monitoramento ambiental de João Pessoa.")
