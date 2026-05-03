import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os
import uuid
import time
from geopy.geocoders import Nominatim

st.set_page_config(page_title="IluminaJP | LEGO Explorers", layout="wide", page_icon="💡")

# --- 1. INICIALIZAÇÃO DE DADOS E VARIÁVEIS ---
DATA_LUZ = "alertas_iluminacao.csv"

if 'luz_lat' not in st.session_state:
    st.session_state.luz_lat = -7.1153
    st.session_state.luz_lon = -34.8611
    st.session_state.luz_endereco = ""
if 'protocolo_gerado' not in st.session_state:
    st.session_state.protocolo_gerado = None

def carregar_dados():
    if os.path.exists(DATA_LUZ):
        return pd.read_csv(DATA_LUZ)
    return pd.DataFrame(columns=['Protocolo', 'Data', 'Endereço', 'Problema', 'Status'])

# --- 2. LAYOUT DA PÁGINA ---
st.title("💡 IluminaJP - Gestão de Iluminação")

# Criamos as colunas primeiro para evitar o NameError
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 Detalhes da Ocorrência")
    
    # SE JÁ TIVER UM PROTOCOLO, MOSTRA O BOX E TRAVA O FORMULÁRIO
    if st.session_state.protocolo_gerado:
        st.success("✅ REGISTRO REALIZADO!")
        st.markdown(f"""
            <div style="background-color: #f0fff4; padding: 20px; border: 2px solid #2f855a; border-radius: 10px; text-align: center;">
                <p style="margin: 0; color: #2f855a; font-weight: bold;">ANOTE SEU PROTOCOLO:</p>
                <h2 style="margin: 10px 0; letter-spacing: 2px;">{st.session_state.protocolo_gerado}</h2>
                <p style="font-size: 0.8rem; color: #666;">Copie este código para acompanhar o status depois.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🆕 Fazer Novo Relato"):
            st.session_state.protocolo_gerado = None
            st.rerun()
            
    else:
        # MOSTRA O FORMULÁRIO APENAS SE NÃO TIVER PROTOCOLO NA TELA
        with st.form("form_luz", clear_on_submit=True):
            rua_input = st.text_input("Localização (Rua/Ref):", value=st.session_state.luz_endereco)
            
            problema = st.selectbox("Tipo de Defeito:", [
                "🚫 Lâmpada Apagada (Noite)",
                "🔄 Lâmpada Acesa (Dia)",
                "⚠️ Lâmpada Piscando",
                "💥 Poste Quebrado",
                "🔌 Fiação Exposta",
                "🌳 Árvore nos Fios"
            ])
            
            if st.form_submit_button("🚀 ENVIAR ALERTA"):
                if rua_input:
                    # Gerar protocolo único
                    novo_p = f"LUM-{str(uuid.uuid4()).upper()[:5]}"
                    st.session_state.protocolo_gerado = novo_p
                    
                    # Salvar dados
                    novo_dado = {
                        'Protocolo': novo_p,
                        'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                        'Endereço': rua_input,
                        'Problema': problema,
                        'Status': '🟡 Pendente'
                    }
                    
                    df = carregar_dados()
                    df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
                    df.to_csv(DATA_LUZ, index=False)
                    
                    st.rerun() # Recarrega para mostrar o protocolo
                else:
                    st.error("⚠️ Marque o local no mapa ou digite o endereço.")

with col2:
    st.subheader("📍 Marcar no Mapa")
    m = folium.Map(location=[st.session_state.luz_lat, st.session_state.luz_lon], zoom_start=15)
    folium.Marker([st.session_state.luz_lat, st.session_state.luz_lon], icon=folium.Icon(color='orange', icon='bolt', prefix='fa')).add_to(m)
    
    mapa = st_folium(m, height=350, width="100%", key="mapa_luz")

    if mapa['last_clicked']:
        lat, lon = mapa['last_clicked']['lat'], mapa['last_clicked']['lng']
        if lat != st.session_state.luz_lat:
            st.session_state.luz_lat, st.session_state.luz_lon = lat, lon
            try:
                geolocator = Nominatim(user_agent="lego_explorers_jp")
                location = geolocator.reverse(f"{lat}, {lon}")
                if location:
                    st.session_state.luz_endereco = location.address.split(',')[0]
            except:
                st.session_state.luz_endereco = "Localização capturada"
            st.rerun()

# --- BARRA LATERAL ---
st.sidebar.image("hamtaro.webp", width=100)
if st.sidebar.button("🗑️ Resetar Banco (Limpa Erros)"):
    if os.path.exists(DATA_LUZ):
        os.remove(DATA_LUZ)
    st.rerun()
