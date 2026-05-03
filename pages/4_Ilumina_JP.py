import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os
import uuid

st.set_page_config(page_title="IluminaJP | LEGO Explorers", layout="wide")

# --- INICIALIZAÇÃO DE DADOS ---
DATA_LUZ = "alertas_iluminacao.csv"

# Garante que o arquivo tenha as colunas certas desde o início
def inicializar_csv():
    colunas = ['Protocolo', 'Data', 'Endereço', 'Problema', 'Autor', 'Status']
    if not os.path.exists(DATA_LUZ):
        pd.DataFrame(columns=colunas).to_csv(DATA_LUZ, index=False)

inicializar_csv()

# Inicializa variáveis de mapa se não existirem
if 'luz_lat' not in st.session_state:
    st.session_state.luz_lat = -7.1153
    st.session_state.luz_lon = -34.8611

st.title("💡 IluminaJP - Relatar Problema")

# --- MAPA ---
st.subheader("1. Marque o poste no mapa")
m = folium.Map(location=[st.session_state.luz_lat, st.session_state.luz_lon], zoom_start=15)
folium.Marker([st.session_state.luz_lat, st.session_state.luz_lon], icon=folium.Icon(color='orange')).add_to(m)
mapa = st_folium(m, height=300, width=700)

if mapa['last_clicked']:
    st.session_state.luz_lat = mapa['last_clicked']['lat']
    st.session_state.luz_lon = mapa['last_clicked']['lng']

# --- FORMULÁRIO ---
st.subheader("2. Detalhes da Ocorrência")
with st.form("form_luz", clear_on_submit=True):
    rua = st.text_input("Rua/Referência:")
    defeito = st.selectbox("Problema:", ["Lâmpada Apagada", "Acesa de Dia", "Piscando", "Poste Caído"])
    
    if st.form_submit_button("🚀 ENVIAR ALERTA"):
        if rua:
            # GERA PROTOCOLO
            novo_p = f"LUM-{str(uuid.uuid4()).upper()[:5]}"
            
            nova_linha = {
                'Protocolo': novo_p,
                'Data': datetime.now().strftime("%d/%m/%Y"),
                'Endereço': rua,
                'Problema': defeito,
                'Autor': st.session_state.get('usuario_atual', 'Anônimo'),
                'Status': '🟡 Pendente'
            }
            
            df = pd.read_csv(DATA_LUZ)
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            df.to_csv(DATA_LUZ, index=False)
            
            st.success(f"✅ Enviado! ANOTE SEU PROTOCOLO: {novo_p}")
        else:
            st.error("Preencha o endereço!")
