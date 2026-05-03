import streamlit as st
import time
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os
import uuid
from geopy.geocoders import Nominatim

st.set_page_config(page_title="IluminaJP | LEGO Explorers", layout="wide", page_icon="💡")

# --- BANCO DE DADOS ---
DATA_LUZ = "alertas_iluminacao.csv"

def inicializar_csv():
    colunas = ['Protocolo', 'Data', 'Endereço', 'Problema', 'Autor', 'Status', 'lat', 'lon']
    if not os.path.exists(DATA_LUZ):
        pd.DataFrame(columns=colunas).to_csv(DATA_LUZ, index=False)

inicializar_csv()

# Inicializa localização padrão (João Pessoa)
if 'luz_lat' not in st.session_state:
    st.session_state.luz_lat = -7.1153
    st.session_state.luz_lon = -34.8611
    st.session_state.luz_endereco = ""

st.title("💡 IluminaJP - Gestão de Iluminação")
st.markdown("Relate problemas na rede elétrica para que a equipe do LEGO Explorers possa encaminhar à prefeitura.")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 Detalhes da Ocorrência")
    with st.form("form_luz", clear_on_submit=True):
        # O endereço pode ser preenchido manualmente ou pelo clique no mapa
        rua_input = st.text_input("Rua/Avenida:", value=st.session_state.luz_endereco, help="Clique no mapa para preencher automaticamente")
        ref_input = st.text_input("Ponto de Referência (Opcional):")
        
        # --- AS OPÇÕES DE PROBLEMA DE VOLTA ---
        problema_selecionado = st.selectbox("Selecione o Defeito:", [
            "🚫 Lâmpada Apagada (Noite toda)",
            "🔄 Lâmpada Acesa Durante o Dia",
            "⚠️ Lâmpada Piscando/Oscilando",
            "💥 Poste Quebrado ou Danificado",
            "🔌 Fiação Exposta ou Curto-Circuito",
            "🌳 Árvore Galhando nos Fios",
            "🧱 Braço do Poste Desprendido",
            "🛠️ Outro Problema"
        ])
        
        anonimo = st.checkbox("Relato Anônimo")

        if st.form_submit_button("🚀 ENVIAR ALERTA"):
            if rua_input:
                # Geração de Protocolo
                protocolo = f"LUM-{str(uuid.uuid4()).upper()[:5]}"
                autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
                
                nova_denuncia = {
                    'Protocolo': protocolo,
                    'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'Endereço': f"{rua_input} ({ref_input})" if ref_input else rua_input,
                    'Problema': problema_selecionado,
                    'Autor': autor,
                    'Status': '🟡 Pendente',
                    'lat': st.session_state.luz_lat,
                    'lon': st.session_state.luz_lon
                }
                
                df = pd.read_csv(DATA_LUZ)
                df = pd.concat([df, pd.DataFrame([nova_denuncia])], ignore_index=True)
                df.to_csv(DATA_LUZ, index=False)
                
                st.success(f"✅ Alerta enviado com sucesso!")
                st.code(f"SEU PROTOCOLO: {protocolo}", language="text")
                st.session_state.luz_endereco = "" # Limpa para o próximo
                time.sleep(2)
                st.rerun()
            else:
                st.error("⚠️ Por favor, informe o local ou clique no mapa.")

with col2:
    st.subheader("📍 Localização do Poste")
    st.info("Clique no mapa para capturar as coordenadas exatas.")
    
    m = folium.Map(location=[st.session_state.luz_lat, st.session_state.luz_lon], zoom_start=15)
    folium.Marker(
        [st.session_state.luz_lat, st.session_state.luz_lon], 
        icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
    ).add_to(m)
    
    mapa_interativo = st_folium(m, height=400, width="100%", key="mapa_luz")

    # Se clicar no mapa, atualiza o endereço via Geopy
    if mapa_interativo['last_clicked']:
        lt = mapa_interativo['last_clicked']['lat']
        ln = mapa_interativo['last_clicked']['lng']
        
        if lt != st.session_state.luz_lat:
            st.session_state.luz_lat = lt
            st.session_state.luz_lon = ln
            
            # Tentativa de pegar o nome da rua automaticamente
            try:
                geolocator = Nominatim(user_agent="lego_explorer")
                location = geolocator.reverse(f"{lt}, {ln}")
                if location:
                    st.session_state.luz_endereco = location.address.split(',')[0]
            except:
                st.session_state.luz_endereco = "Coordenadas capturadas"
            st.rerun()

# --- BARRA LATERAL ---
st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Limpar Banco de Dados"):
    if os.path.exists(DATA_LUZ):
        os.remove(DATA_LUZ)
        st.rerun()
