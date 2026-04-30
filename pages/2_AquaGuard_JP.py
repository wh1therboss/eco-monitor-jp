import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# --- SIDEBAR PERSONALIZADA: AQUAGUARD ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 🌊 Monitoramento Hídrico")
    st.success("STATUS: SENSORES ATIVOS")
    st.write("Nível de Pureza Médio:")
    st.progress(72)
    st.info("Monitorando balneabilidade e resíduos químicos na costa de JP.")

# --- SEGURANÇA ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

st.title("🌊 AquaGuard JP")

# Banco de Dados das Praias
dados_praias = {
    'Praia': ['Bessa', 'Manaíra', 'Tambaú', 'Cabo Branco', 'Seixas', 'Penha', 'Jacarapé', 'Sol'],
    'Status': ['Própria', 'Imprópria', 'Própria', 'Própria', 'Própria', 'Própria', 'Imprópria', 'Regular'],
    'Pureza (%)': [95, 30, 88, 92, 98, 85, 20, 55],
    'lat': [-7.085, -7.095, -7.116, -7.135, -7.155, -7.168, -7.185, -7.210],
    'lon': [-34.830, -34.832, -34.821, -34.819, -34.790, -34.796, -34.798, -34.800]
}
df_praias = pd.DataFrame(dados_praias)

# Mapa de Balneabilidade
st.subheader("📍 Mapa de Qualidade da Água")
m = folium.Map(location=[-7.140, -34.815], zoom_start=12)
for _, r in df_praias.iterrows():
    cor = 'green' if r['Status'] == 'Própria' else 'red' if r['Status'] == 'Imprópria' else 'orange'
    folium.Marker([r['lat'], r['lon']], popup=r['Praia'], icon=folium.Icon(color=cor, icon='tint')).add_to(m)
folium_static(m, width=700)

# Tabela com correção de erro de estilo
st.write("---")
def style_status(val):
    color = 'green' if val == 'Própria' else 'red' if val == 'Imprópria' else 'orange'
    return f'color: {color}; font-weight: bold'

st.dataframe(df_praias[['Praia', 'Status', 'Pureza (%)']].style.map(style_status, subset=['Status']), use_container_width=True)
st.bar_chart(df_praias.set_index('Praia')['Pureza (%)'])
