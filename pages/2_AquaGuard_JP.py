import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# ==========================================
# 1. TRAVA DE SEGURANÇA
# ==========================================
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

usuario = st.session_state.get('usuario_atual', 'Explorador')

# ==========================================
# 2. BANCO DE DADOS DE BALNEABILIDADE (PRAIAS)
# ==========================================
# Dados baseados nos pontos de coleta da Sudema em JP
dados_praias = {
    'Praia': [
        'Bessa (Leste)', 'Manaíra (Av. Flávio Ribeiro)', 'Tambaú (Busto de Tamandaré)', 
        'Cabo Branco (Ed. Arpoador)', 'Seixas (Farol)', 'Penha (Capela)', 
        'Jacarapé (Em frente à rua)', 'Sol (Desembocadura)'
    ],
    'Status': ['Própria', 'Imprópria', 'Própria', 'Própria', 'Própria', 'Própria', 'Imprópria', 'Regular'],
    'Nível de Balneabilidade': [95, 30, 88, 92, 98, 85, 20, 55],
    'lat': [-7.085, -7.095, -7.116, -7.135, -7.155, -7.168, -7.185, -7.210],
    'lon': [-34.830, -34.832, -34.821, -34.819, -34.790, -34.796, -34.798, -34.800]
}
df_praias = pd.DataFrame(dados_praias)

# ==========================================
# 3. INTERFACE PRINCIPAL
# ==========================================
st.title("🌊 AquaGuard JP - Monitoramento de Praias")
st.subheader(f"Qualidade da Água Costeira | Analista: {usuario}")

# Métricas de resumo
col1, col2, col3 = st.columns(3)
proprias = len(df_praias[df_praias['Status'] == 'Própria'])
with col1:
    st.metric("Praias Monitoradas", len(df_praias))
with col2:
    st.metric("Próprias para Banho", proprias, f"{proprias-len(df_praias)}")
with col3:
    st.metric("Qualidade Média", "82%", "+2% (Última semana)")

st.write("---")

# ==========================================
# 4. MAPA DE QUALIDADE DAS PRAIAS
# ==========================================
st.subheader("📍 Mapa de Balneabilidade (Tempo Real)")
m_praias = folium.Map(location=[-7.140, -34.815], zoom_start=12)

for _, r in df_praias.iterrows():
    # Define a cor do ícone
    if r['Status'] == 'Própria':
        cor = 'blue'
        icone = 'thumbs-up'
    elif r['Status'] == 'Imprópria':
        cor = 'red'
        icone = 'warning'
    else:
        cor = 'orange'
        icone = 'info-sign'
    
    folium.Marker(
        [r['lat'], r['lon']],
        popup=f"<b>{r['Praia']}</b><br>Status: {r['Status']}<br>Índice: {r['Nível de Balneabilidade']}",
        icon=folium.Icon(color=cor, icon=icone, prefix='fa')
    ).add_to(m_praias)

folium_static(m_praias, width=900)

# ==========================================
# 5. TABELA E GRÁFICO DE ANÁLISE
# ==========================================
st.write("---")
col_t, col_g = st.columns([1.2, 1])

with col_t:
    st.subheader("📊 Relatório Detalhado")
    # Tabela com cores
    def color_status(val):
        color = 'green' if val == 'Própria' else 'red' if val == 'Imprópria' else 'orange'
        return f'background-color: {color}; color: white; font-weight: bold'

    st.dataframe(df_praias[['Praia', 'Status', 'Nível de Balneabilidade']].style.applymap(color_status, subset=['Status']), use_container_width=True)

with col_g:
    st.subheader("📈 Índice de Pureza")
    # Gráfico de barras com os níveis
    st.bar_chart(df_praias.set_index('Praia')['Nível de Balneabilidade'])

st.info("💡 **Dica LEGO Explorers:** Evite o banho de mar nas praias classificadas como 'Imprópria', especialmente após chuvas intensas.")
