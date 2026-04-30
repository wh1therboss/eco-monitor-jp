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
    st.info("Clique no mapa para marcar o local exato do descarte.")
    st.write("---")
    st.caption("version: 0.1")

# --- 2. SEGURANÇA E BANCO DE DADOS ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

# Inicializa o buscador de endereços
geolocator = Nominatim(user_agent="lego_explorer_jp_v2")
DATA_DB = "denuncias_ecocoleta.csv"

if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        st.session_state.db_relatos = pd.read_csv(DATA_DB)
    else:
        st.session_state.db_relatos = pd.DataFrame(columns=['Data', 'Rua', 'Tipo', 'Autor', 'lat', 'lon', 'Status'])

# --- 3. LÓGICA DE CLIQUE NO MAPA ---
if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat = -7.1153  # Centro de JP
    st.session_state.clique_lon = -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")
st.subheader("📍 Selecione o Local no Mapa")

# Cria o mapa para o usuário clicar
m_selecao = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=13)
folium.Marker(
    [st.session_state.clique_lat, st.session_state.clique_lon], 
    tooltip="Ponto Marcado",
    icon=folium.Icon(color='red', icon='trash')
).add_to(m_selecao)

# Renderiza o mapa e captura o clique
output = st_folium(m_selecao, width=700, height=350, key="mapa_interativo")

# Se o usuário clicar, atualiza as coordenadas e o endereço
if output['last_clicked']:
    nova_lat = output['last_clicked']['lat']
    nova_lon = output['last_clicked']['lng']
    
    if nova_lat != st.session_state.clique_lat:
        st.session_state.clique_lat = nova_lat
        st.session_state.clique_lon = nova_lon
        
        try:
            # Busca o nome da rua baseado na coordenada do clique
            location = geolocator.reverse(f"{nova_lat}, {nova_lon}")
            if location:
                # Limpa o endereço para ficar mais curto (Pega só rua e número se houver)
                st.session_state.endereco_clique = location.address.split(',')[0] + ", " + location.address.split(',')[1]
            else:
                st.session_state.endereco_clique = "Local desconhecido"
        except:
            st.session_state.endereco_clique = "Coordenada registrada"
        
        st.rerun()

# --- 4. FORMULÁRIO DE DENÚNCIA ---
st.write("---")
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Detalhes da Ocorrência")
    
    # O campo de rua é preenchido automaticamente pelo clique no mapa
    rua_final = st.text_input("Endereço Confirmado:", value=st.session_state.endereco_clique)
    
    tipo = st.selectbox("Tipo de Resíduo:", [
        "Plásticos/Garrafas", "Papel/Papelão", "Vidro", "Metal", 
        "Orgânico", "Entulho", "Móveis", "Eletrônicos", "Pneus"
    ])
    
    ref = st.text_input("Ponto de Referência (Opcional):")
    anonimo = st.checkbox("Fazer denúncia anônima")

    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua_final:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            
            nova_denuncia = {
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Rua': rua_final,
                'Tipo': tipo,
                'Autor': autor,
                'lat': st.session_state.clique_lat,
                'lon': st.session_state.clique_lon,
                'Status': 'Pendente'
            }
            
            # Salva no banco de dados
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([nova_denuncia])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            
            st.success(f"✅ Denúncia enviada com sucesso! Local: {rua_final}")
            # Limpa o endereço para a próxima
            st.session_state.endereco_clique = ""
            st.rerun()
        else:
            st.warning("⚠️ Por favor, clique no mapa para marcar o local.")

# --- 5. TABELA DE REGISTROS ---
st.write("---")
st.subheader("📋 Últimas Denúncias")
if not st.session_state.db_relatos.empty:
    # Mostra os mais recentes primeiro
    df_reverso = st.session_state.db_relatos.iloc[::-1]
    st.dataframe(df_reverso[['Data', 'Rua', 'Tipo', 'Status']], use_container_width=True)
else:
    st.info("Nenhuma denúncia registrada ainda.")
