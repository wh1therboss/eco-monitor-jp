import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os
from geopy.geocoders import Nominatim

# --- 1. CONFIGURAÇÃO DA SIDEBAR ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 💡 IluminaJP")
    st.info("Relate postes apagados ou problemas na rede elétrica de João Pessoa.")
    st.write("---")
    st.caption("version: 0.1")

# --- 2. SEGURANÇA E BANCO DE DADOS ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

geolocator = Nominatim(user_agent="lego_explorer_ilumina_jp")
DATA_LUZ = "alertas_iluminacao.csv"
colunas_luz = ['Data', 'Endereço_Completo', 'Problema', 'Autor', 'lat', 'lon', 'Status']

# Função de carregamento sempre atualizado
def carregar_dados_luz():
    if os.path.exists(DATA_LUZ):
        df = pd.read_csv(DATA_LUZ)
        if 'Endereço_Completo' not in df.columns:
            return pd.DataFrame(columns=colunas_luz)
        return df
    return pd.DataFrame(columns=colunas_luz)

st.session_state.db_luz = carregar_dados_luz()

# Inicialização de coordenadas para o mapa
if 'luz_lat' not in st.session_state:
    st.session_state.luz_lat = -7.1153 
    st.session_state.luz_lon = -34.8611
    st.session_state.luz_endereco = ""

st.title("💡 IluminaJP - Gestão de Iluminação")

# --- 3. FORMULÁRIO DE ALERTA ---
with st.form("form_iluminacao", clear_on_submit=True):
    st.markdown("### 🔦 Relatar Problema de Iluminação")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        rua_luz = st.text_input("Rua/Avenida do Poste:", value=st.session_state.luz_endereco)
    with col_num:
        num_luz = st.text_input("Nº Prox:")

    problema = st.selectbox("Tipo de Defeito:", [
        "🚫 Poste com Lâmpada Apagada (Noite toda)",
        "🔄 Lâmpada Acesa Durante o Dia",
        "⚠️ Lâmpada Piscando/Oscilando",
        "💥 Poste Quebrado ou Danificado",
        "🔌 Fiação Exposta ou Curto-Circuito",
        "🌳 Árvore Galhando nos Fios",
        "🧱 Braço do Poste Desprendido"
    ])
    
    ref_luz = st.text_input("Referência (Ex: Em frente à praça):")
    anonimo = st.checkbox("Relato Anônimo")

    if st.form_submit_button("🚀 ENVIAR ALERTA"):
        if rua_luz:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            endereco_final = f"{rua_luz}, {num_luz}" if num_luz else rua_luz
            
            novo_alerta = {
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Endereço_Completo': endereco_final,
                'Problema': problema,
                'Autor': autor,
                'lat': st.session_state.luz_lat,
                'lon': st.session_state.luz_lon,
                'Status': 'Pendente'
            }
            
            df_novo = pd.concat([st.session_state.db_luz, pd.DataFrame([novo_alerta])], ignore_index=True)
            df_novo.to_csv(DATA_LUZ, index=False)
            
            st.success(f"✅ Alerta enviado! Protocolo gerado para: {endereco_final}")
            st.session_state.luz_endereco = ""
            st.rerun()
        else:
            st.warning("⚠️ Use o mapa abaixo para marcar a localização do poste.")

# --- 4. MAPA INTERATIVO (EMBAIXO) ---
st.write("---")
st.subheader("📍 Marque o Poste no Mapa")
st.info("Clique no local exato do poste para capturar o endereço automaticamente.")

m_luz = folium.Map(location=[st.session_state.luz_lat, st.session_state.luz_lon], zoom_start=15)
folium.Marker(
    [st.session_state.luz_lat, st.session_state.luz_lon], 
    icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
).add_to(m_luz)

output_luz = st_folium(m_luz, width=700, height=350, key="mapa_luz")

if output_luz['last_clicked']:
    lt, ln = output_luz['last_clicked']['lat'], output_luz['last_clicked']['lng']
    if lt != st.session_state.luz_lat:
        st.session_state.luz_lat, st.session_state.luz_lon = lt, ln
        try:
            location = geolocator.reverse(f"{lt}, {ln}")
            if location: st.session_state.luz_endereco = location.address.split(',')[0]
        except: st.session_state.luz_endereco = "Localização capturada"
        st.rerun()

# --- 5. HISTÓRICO DE ALERTAS ---
st.write("---")
st.subheader("📋 Status dos Reparos em JP")
if not st.session_state.db_luz.empty:
    st.dataframe(st.session_state.db_luz.iloc[::-1][['Data', 'Endereço_Completo', 'Problema', 'Status']], use_container_width=True)
else:
    st.info("Nenhum problema de iluminação relatado nesta área.")
