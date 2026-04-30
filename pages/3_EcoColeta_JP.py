import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os
from geopy.geocoders import Nominatim # <--- Necessário adicionar no requirements.txt

# --- 1. CONFIGURAÇÃO E IDENTIDADE (SIDEBAR) ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ♻️ Gestão de Resíduos")
    st.warning("ALERTA: PONTOS DE DESCARTE")
    st.metric("Reciclagem Mensal", "45%", "+2%")
    st.info("Ajude a manter as praias de JP limpas.")

# --- 2. SEGURANÇA ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"
colunas_sistema = ['Data', 'Bairro', 'Rua', 'Numero', 'Referencia', 'Tipo', 'Autor', 'lat', 'lon', 'Status']

# Inicializa o geolocalizador
geolocator = Nominatim(user_agent="lego_explorers_jp")

# Previne erro de coluna faltando
if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        df_lido = pd.read_csv(DATA_DB)
        for col in colunas_sistema:
            if col not in df_lido.columns: df_lido[col] = "N/A"
        st.session_state.db_relatos = df_lido
    else:
        st.session_state.db_relatos = pd.DataFrame(columns=colunas_sistema)

st.title("♻️ EcoColeta JP")

# --- 3. FORMULÁRIO COM GEOLOCALIZAÇÃO ---
with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📢 Registrar Descarte de Lixo")
    
    rua_input = st.text_input("Nome da Rua e Bairro:")
    col_n, col_r = st.columns([1, 2])
    with col_n: num = st.text_input("Nº:")
    with col_r: ref = st.text_input("Ponto de Referência:")
    
    tipo = st.selectbox("Tipo de Resíduo:", [
        "Plásticos (Garrafas/Embalagens)", "Papel/Papelão", "Vidro", 
        "Metal/Latas", "Resíduos Orgânicos", "Entulho de Construção", 
        "Móveis Abandonados", "Redes de Pesca", "Eletrônicos", "Pneus"
    ])
    
    anonimo = st.checkbox("Denúncia Anônima")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua_input and ref:
            # TENTA BUSCAR A COORDENADA REAL
            try:
                endereco_completo = f"{rua_input}, João Pessoa, Paraíba, Brasil"
                location = geolocator.geocode(endereco_completo)
                
                if location:
                    v_lat, v_lon = location.latitude, location.longitude
                else:
                    # Se não achar a rua, usa um ponto central de JP para não dar erro
                    v_lat, v_lon = -7.115, -34.863
                    st.warning("Rua não encontrada com precisão. Usando ponto central do bairro.")
                
                autor = "Anônimo" if anonimo else usuario_logado
                novo = {
                    'Data': datetime.now().strftime("%d/%m/%Y"), 
                    'Bairro': "João Pessoa", 'Rua': rua_input, 
                    'Numero': num if num else "S/N", 'Referencia': ref, 
                    'Tipo': tipo, 'Autor': autor, 
                    'lat': v_lat, 'lon': v_lon, 'Status': 'Pendente'
                }
                
                st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo])], ignore_index=True)
                st.session_state.db_relatos.to_csv(DATA_DB, index=False)
                st.success("✅ Denúncia registrada no mapa!")
                st.rerun()
                
            except Exception as e:
                st.error("Erro ao localizar endereço. Verifique sua conexão.")
        else:
            st.warning("⚠️ Preencha a Rua e a Referência.")

# --- 4. MAPA E TABELA ---
st.write("---")
st.subheader("📍 Mapa de Ocorrências Real")

# Centraliza o mapa na última denúncia feita ou no centro de JP
map_center = [st.session_state.db_relatos['lat'].iloc[-1], st.session_state.db_relatos['lon'].iloc[-1]] if not st.session_state.db_relatos.empty else [-7.115, -34.863]

m = folium.Map(location=map_center, zoom_start=13)

for _, r in st.session_state.db_relatos.iterrows():
    if r['lat'] != "N/A":
        cor_ponto = 'red' if r['Status'] == 'Pendente' else 'green'
        folium.Marker(
            [float(r['lat']), float(r['lon'])], 
            popup=f"<b>{r['Tipo']}</b><br>Status: {r['Status']}", 
            icon=folium.Icon(color=cor_ponto, icon='info-sign')
        ).add_to(m)

folium_static(m, width=700)

st.subheader("📊 Histórico de Registros")
st.dataframe(st.session_state.db_relatos[['Data', 'Rua', 'Tipo', 'Status', 'Autor']], use_container_width=True)
