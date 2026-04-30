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
    st.markdown("### ♻️ Gestão de Resíduos")
    st.info("Preencha os dados e use o mapa abaixo para o ajuste fino da localização.")
    st.write("---")
    st.caption("version: 0.1")

# --- 2. SEGURANÇA E BANCO DE DADOS ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

geolocator = Nominatim(user_agent="lego_explorer_jp_v2")
DATA_DB = "denuncias_ecocoleta.csv"

if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        st.session_state.db_relatos = pd.read_csv(DATA_DB)
    else:
        # Criando o DataFrame com a coluna Endereço_Completo
        st.session_state.db_relatos = pd.DataFrame(columns=['Data', 'Endereço_Completo', 'Tipo', 'Autor', 'lat', 'lon', 'Status'])

# Inicialização de coordenadas
if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat = -7.1153 
    st.session_state.clique_lon = -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")

# --- 3. FORMULÁRIO DE OCORRÊNCIA ---
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Detalhes da Ocorrência")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        rua_input = st.text_input("Rua/Avenida:", value=st.session_state.endereco_clique)
    with col_num:
        numero_input = st.text_input("Nº:")

    # Opções Detalhadas de Resíduos
    tipo = st.selectbox("Tipo de Resíduo Específico:", [
        "📦 Descarte Irregular de Plásticos, PET e Embalagens",
        "📄 Papéis, Papelão e Resíduos de Escritório",
        "🍾 Vidros e Cristais (Garrafas ou Estilhaços)",
        "🥫 Metais, Latas e Alumínio Reciclável",
        "🍎 Resíduos Orgânicos e Restos de Alimentos",
        "🏗️ Entulho de Obras, Tijolos e Restos de Construção",
        "🛋️ Móveis e Grandes Objetos (Sofás, Colchões, Armários)",
        "🎣 Redes de Pesca, Cordas e Materiais Marítimos",
        "💻 Lixo Eletrônico (Baterias, Celulares, Periféricos)",
        "🚗 Pneus, Câmaras de Ar e Borrachas",
        "🌿 Resíduos Verdes (Podas de Árvores e Galhos)",
        "🧴 Substâncias Químicas, Tintas ou Óleo de Cozinha"
    ])
    
    ref = st.text_input("Ponto de Referência:")
    anonimo = st.checkbox("Fazer denúncia de forma anônima")

    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua_input:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            
            # Unindo Rua e Número para o banco de dados
            endereco_final = f"{rua_input}, {numero_input}" if numero_input else rua_input
            
            nova_denuncia = {
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Endereço_Completo': endereco_final,
                'Tipo': tipo,
                'Autor': autor,
                'lat': st.session_state.clique_lat,
                'lon': st.session_state.clique_lon,
                'Status': 'Pendente'
            }
            
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([nova_denuncia])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            
            st.success(f"✅ Denúncia enviada! Local: {endereco_final}")
            st.session_state.endereco_clique = ""
            st.rerun()
        else:
            st.warning("⚠️ Preencha o nome da rua ou selecione no mapa abaixo.")

# --- 4. MAPA INTERATIVO (EMBAIXO) ---
st.write("---")
st.subheader("📍 Ajuste a Localização no Mapa")
st.info("Clique na rua exata para capturar o endereço automaticamente.")

m_selecao = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=15)
folium.Marker(
    [st.session_state.clique_lat, st.session_state.clique_lon], 
    icon=folium.Icon(color='red', icon='trash')
).add_to(m_selecao)

# Captura do clique
output = st_folium(m_selecao, width=700, height=350, key="mapa_embaixo")

if output['last_clicked']:
    lat_clique = output['last_clicked']['lat']
    lon_clique = output['last_clicked']['lng']
    
    if lat_clique != st.session_state.clique_lat:
        st.session_state.clique_lat = lat_clique
        st.session_state.clique_lon = lon_clique
        try:
            location = geolocator.reverse(f"{lat_clique}, {lon_clique}")
            if location:
                # Pega apenas o nome da rua para o campo de texto
                st.session_state.endereco_clique = location.address.split(',')[0]
        except:
            st.session_state.endereco_clique = "Localização capturada"
        st.rerun()

# --- 5. TABELA DE HISTÓRICO ---
st.write("---")
st.subheader("📋 Registro de Ocorrências")
if not st.session_state.db_relatos.empty:
    # Inverte para mostrar as mais recentes no topo
    st.dataframe(st.session_state.db_relatos.iloc[::-1][['Data', 'Endereço_Completo', 'Tipo', 'Status']], use_container_width=True)
