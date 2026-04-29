import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 1. Trava de Segurança
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

# 2. Configuração
usuario = st.session_state.get('usuario_atual', 'Explorador')
st.title("💧 AquaGuard JP")
st.subheader(f"Analista: {usuario}")

# 3. Dados e Mapa
dados = {
    'Ponto': ['Rio Sanhauá', 'Rio Jaguaribe', 'Reservatório Marés'],
    'Nível': [82, 45, 91],
    'lat': [-7.110, -7.140, -7.115],
    'lon': [-34.885, -34.850, -34.870]
}
df = pd.DataFrame(dados)

m = folium.Map(location=[-7.120, -34.900], zoom_start=12)
for _, r in df.iterrows():
    folium.Marker([r['lat'], r['lon']], popup=r['Ponto']).add_to(m)

folium_static(m, width=700)
st.dataframe(df[['Ponto', 'Nível']], use_container_width=True)
