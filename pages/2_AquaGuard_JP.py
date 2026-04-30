import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# --- SEGURANÇA (OBRIGATÓRIO) ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

# --- CABEÇALHO LEGO EXPLORERS ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("hamtaro.webp", width=100)
with col_titulo:
    st.title("LEGO Explorers")
    st.subheader("🌊 AquaGuard JP")

usuario = st.session_state.get('usuario_atual', 'Explorador')
st.markdown(f"**Analista responsável:** {usuario}")

# --- BANCO DE DADOS DAS PRAIAS ---
dados_praias = {
    'Praia': ['Bessa', 'Manaíra', 'Tambaú', 'Cabo Branco', 'Seixas', 'Penha', 'Jacarapé', 'Sol'],
    'Status': ['Própria', 'Imprópria', 'Própria', 'Própria', 'Própria', 'Própria', 'Imprópria', 'Regular'],
    'Pureza (%)': [95, 30, 88, 92, 98, 85, 20, 55],
    'lat': [-7.085, -7.095, -7.116, -7.135, -7.155, -7.168, -7.185, -7.210],
    'lon': [-34.830, -34.832, -34.821, -34.819, -34.790, -34.796, -34.798, -34.800]
}
df_praias = pd.DataFrame(dados_praias)

st.write("---")
st.subheader("📍 Mapa de Balneabilidade Costeira")
m = folium.Map(location=[-7.140, -34.815], zoom_start=12)

for _, r in df_praias.iterrows():
    # Cores baseadas no status
    cor = 'green' if r['Status'] == 'Própria' else 'red' if r['Status'] == 'Imprópria' else 'orange'
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"{r['Praia']}: {r['Status']}", 
        icon=folium.Icon(color=cor, icon='tint')
    ).add_to(m)

folium_static(m, width=900)

# --- GRÁFICO E TABELA COLORIDA ---
st.write("---")
col_g, col_t = st.columns(2)

with col_g:
    st.subheader("📈 Nível de Pureza")
    st.bar_chart(df_praias.set_index('Praia')['Pureza (%)'])

with col_t:
    st.subheader("📋 Relatório de Status")
    def colorir_status(val):
        color = 'green' if val == 'Própria' else 'red' if val == 'Imprópria' else 'orange'
        return f'color: {color}; font-weight: bold'
    
    # Uso do .map para evitar o erro de Attribute
    st.dataframe(df_praias[['Praia', 'Status', 'Pureza (%)']].style.map(colorir_status, subset=['Status']), use_container_width=True)
