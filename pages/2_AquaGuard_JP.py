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
# 2. BANCO DE DADOS DAS PRAIAS DE JP
# ==========================================
dados_praias = {
    'Praia': [
        'Bessa', 'Manaíra', 'Tambaú', 'Cabo Branco', 
        'Seixas', 'Penha', 'Jacarapé', 'Sol'
    ],
    'Status': ['Própria', 'Imprópria', 'Própria', 'Própria', 'Própria', 'Própria', 'Imprópria', 'Regular'],
    'Pureza (%)': [95, 30, 88, 92, 98, 85, 20, 55],
    'lat': [-7.085, -7.095, -7.116, -7.135, -7.155, -7.168, -7.185, -7.210],
    'lon': [-34.830, -34.832, -34.821, -34.819, -34.790, -34.796, -34.798, -34.800]
}
df_praias = pd.DataFrame(dados_praias)

# ==========================================
# 3. INTERFACE PRINCIPAL
# ==========================================
st.title("🌊 AquaGuard JP - Monitoramento")
st.subheader(f"Qualidade das Águas | Analista: {usuario}")

col1, col2, col3 = st.columns(3)
with col1: st.metric("Praias Analisadas", len(df_praias))
with col2: st.metric("Próprias", "6", "-1")
with col3: st.metric("Índice Geral", "72%", "+5%")

st.write("---")

# ==========================================
# 4. MAPA DE BALNEABILIDADE
# ==========================================
st.subheader("📍 Mapa das Praias de João Pessoa")
# Centralizado na costa de JP
m = folium.Map(location=[-7.140, -34.815], zoom_start=12)

for _, r in df_praias.iterrows():
    cor = 'green' if r['Status'] == 'Própria' else 'red' if r['Status'] == 'Imprópria' else 'orange'
    folium.Marker(
        [r['lat'], r['lon']],
        popup=f"{r['Praia']}: {r['Status']} ({r['Pureza (%)']}%)",
        icon=folium.Icon(color=cor, icon='tint')
    ).add_to(m)

folium_static(m, width=900)

# ==========================================
# 5. GRÁFICO E TABELA (CORREÇÃO DO ERRO)
# ==========================================
st.write("---")
col_g, col_t = st.columns([1, 1])

with col_g:
    st.subheader("📈 Nível de Pureza")
    st.bar_chart(df_praias.set_index('Praia')['Pureza (%)'])

with col_t:
    st.subheader("📋 Relatório Sudema")
    
    # CORREÇÃO AQUI: Usando map em vez de applymap para evitar o erro da imagem
    def colorir_status(val):
        color = 'green' if val == 'Própria' else 'red' if val == 'Imprópria' else 'orange'
        return f'color: {color}; font-weight: bold'

    # Exibe a tabela formatada
    st.dataframe(
        df_praias[['Praia', 'Status', 'Pureza (%)']].style.map(colorir_status, subset=['Status']),
        use_container_width=True
    )

st.info("💡 Dados atualizados conforme o último relatório de balneabilidade.")
