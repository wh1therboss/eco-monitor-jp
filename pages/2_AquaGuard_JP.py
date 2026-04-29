import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

# ==========================================
# 1. TRAVA DE SEGURANÇA (OBRIGATÓRIO)
# ==========================================
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso negado! Por favor, faça login na página principal.")
    st.stop()

# ==========================================
# 2. CONFIGURAÇÃO E DADOS SIMULADOS
# ==========================================
usuario = st.session_state.get('usuario_atual', 'Explorador')

# Dados de monitoramento das águas de JP (Simulação para a FLL)
dados_agua = {
    'Ponto de Coleta': ['Rio Sanhauá', 'Rio Jaguaribe', 'Bacia do Baixo Paraíba', 'Reservatório Marés'],
    'Nível (%)': [82, 45, 60, 91],
    'Qualidade': ['Boa', 'Alerta', 'Regular', 'Excelente'],
    'lat': [-7.110, -7.140, -7.080, -7.115],
    'lon': [-34.885, -34.850, -34.950, -34.870]
}
df_agua = pd.DataFrame(dados_agua)

# ==========================================
# 3. INTERFACE PRINCIPAL
# ==========================================
st.title("💧 AquaGuard JP")
st.subheader(f"Monitoramento Hídrico | Analista: {usuario}")

# Cartões de Resumo
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Nível Médio Rios", "62%", "-3%")
with col2:
    st.metric("Qualidade Geral", "Regular", "Sanhauá Estável")
with col3:
    st.metric("Volume Marés", "91%", "+1.2%")

st.write("---")

# ==========================================
# 4. MAPA HÍDRICO DE JOÃO PESSOA
# ==========================================
st.subheader("📍 Mapa de Pontos de Monitoramento")
# Centralizado na área dos rios e reservatórios de JP
m_agua = folium.Map(location=[-7.120, -34.900], zoom_start=12)

for _, r in df_agua.iterrows():
    # Cor do ícone baseada na qualidade
    cor = 'green' if r['Qualidade'] == 'Excelente' or r['Qualidade'] == 'Boa' else 'orange' if r['Qualidade'] == 'Regular' else 'red'
    
    folium.Marker(
        [r['lat'], r['lon']],
        popup=f"<b>{r['Ponto de Coleta']}</b><br>Nível: {r['Nível (%)']}%<br>Qualidade: {r['Qualidade']}",
        icon=folium.Icon(color=cor, icon='tint')
    ).add_to(m_agua)

folium_static(m_agua, width=1000)

# ==========================================
# 5. TABELA DE ANÁLISE DETALHADA
# ==========================================
st.write("---")
st.subheader("📊 Relatório de Qualidade da Água")

# Estilizando a tabela para destacar alertas
def destacar_alerta(val):
    color = 'red' if val == 'Alerta' else 'black'
    return f'color: {color}'

st.dataframe(df_agua[['Ponto de Coleta', 'Nível (%)', '
