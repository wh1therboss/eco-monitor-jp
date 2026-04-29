import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="EcoMonitor JP | Lego Explorers", layout="wide")

# Estilização CSS (Identidade Lego Explorers e ajuste de contraste)
st.markdown("""
    <style>
    .stMetric { background-color: #1E2129; padding: 15px; border-radius: 10px; border: 1px solid #3e4452; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #ADB5BD !important; }
    
    .lego-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
    .lego-letters { font-size: 55px; font-weight: 900; line-height: 1; margin: 0; }
    .l-blue { color: #0055BF; } .e-yellow { color: #F2CD37; } .g-green { color: #237841; } .o-red { color: #C91A09; }
    
    .explorers-sub {
        color: #000000 !important;
        font-size: 22px;
        font-weight: bold;
        letter-spacing: 6px;
        margin-top: 5px;
        display: block;
    }
    .lego-sidebar-box {
        background-color: #FFFFFF; color: #000000; padding: 8px;
        border-radius: 4px; text-align: center; font-weight: 900; border: 2px solid #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRA LATERAL
with st.sidebar:
    if os.path.exists("hamtaro.webp"):
        st.image("hamtaro.webp", width=140)
    st.markdown('<div class="lego-sidebar-box">LEGO EXPLORERS</div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader("🛰️ Telemetria Landsat 8")
    st.success("STATUS: ONLINE")
    ano_selecionado = st.slider("Histórico Térmico JP:", 2013, 2026, 2026)

# 3. BANCO DE DADOS EXPANDIDO (25 Bairros de João Pessoa)
dados_jp_completos = {
    'Local': [
        'Centro', 'Mangabeira', 'Manaíra', 'Bessa', 'Cabo Branco', 'Altiplano', 'Jaguaribe', 
        'Torre', 'Bancários', 'Valentina', 'Cristo Redentor', 'Geisel', 'José Américo', 
        'Gramame', 'Paratibe', 'Cruz das Armas', 'Oitizeiro', 'Alto do Mateus', 'Bairro das Indústrias',
        'Tambauzinho', 'Expedicionários', 'Miramar', 'Castelo Branco', 'Varadouro', 'Roger'
    ],
    'Arborizacao': [
        4.2, 11.5, 15.3, 22.1, 38.5, 31.2, 8.4, 18.2, 20.5, 14.8, 12.1, 13.5, 16.2, 
        19.5, 21.0, 7.8, 6.5, 9.2, 10.4, 23.1, 21.8, 25.4, 28.1, 5.2, 11.0
    ],
    'Temperatura': [
        35.4, 33.8, 32.1, 31.5, 29.8, 30.2, 34.6, 32.5, 31.8, 33.5, 33.9, 33.2, 32.8, 
        32.1, 31.9, 34.8, 35.1, 34.2, 33.7, 31.4, 31.6, 30.9, 30.5, 35.2, 33.6
    ],
    'lat': [
        -7.1194, -7.1652, -7.0921, -7.0855, -7.1251, -7.1265, -7.1248, -7.1220, -7.1510, 
        -7.1850, -7.1410, -7.1610, -7.1520, -7.2100, -7.1980, -7.1350, -7.1320, -7.1080, 
        -7.1750, -7.1180, -7.1210, -7.1240, -7.1350, -7.1120, -7.1050
    ],
    'lon': [
        -34.8778, -34.8451, -34.8315, -34.8302, -34.8234, -34.8251, -34.8702, -34.8550, -34.8350, 
        -34.8380, -34.8650, -34.8550, -34.8480, -34.8450, -34.8520, -34.8880, -34.8980, -34.9080, 
        -34.9150, -34.8480, -34.8420, -34.8380, -34.8410, -34.8850, -34.8780
    ]
}
df_bairros = pd.DataFrame(dados_jp_completos)

# Histórico de aquecimento médio (Curva 2013-2026)
hist_jp = {
    'Ano': [2013, 2015, 2017, 2019, 2021, 2023, 2024, 2025, 2026],
    'Temp': [28.2, 28.6, 29.1, 29.8, 30.5, 31.2, 31.8, 32.1, 32.4]
}
df_hist = pd.DataFrame(hist_jp)

# 4. CABEÇALHO
col_tit, col_logo, col_ham = st.columns([2, 2, 1])
with col_tit:
    st.title("🛰️ EcoMonitor JP")
    st.write(f"Análise de 25 Bairros • Satélite Landsat 8 • **{ano_selecionado}**")
with col_logo:
    st.markdown(f"""
        <div class="lego-container">
            <div class="lego-letters">
                <span class="l-blue">L</span><span class="e-yellow">E</span><span class="g-green">G</span><span class="o-red">O</span>
            </div>
            <div class="explorers-sub">EXPLORERS</div>
        </div>
    """, unsafe_allow_html=True)
with col_ham:
    if os.path.exists("hamtaro.webp"):
        st.image("hamtaro.webp", width=150)

st.write("---")

# 5. LINHA DO TEMPO
df_view = df_hist[df_hist['Ano'] <= ano_selecionado]
fig_lin = px.line(df_view, x="Ano", y="Temp", markers=True, title="Aquecimento Médio da Capital (°C)")
fig_lin.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="black")
st.plotly_chart(fig_lin, use_container_width=True)

# 6. MAPA E CORRELAÇÃO
c1, c2 = st.columns(2)

with c1:
    st.subheader("📍 Mapa Térmico Completo")
    m = folium.Map(location=[-7.14, -34.86], zoom_start=12, tiles="cartodbpositron")
    for _, r in df_bairros.iterrows():
        # Efeito do slider na temperatura
        t_atual = r['Temperatura'] - (2026 - ano_selecionado) * 0.3
        cor = 'red' if t_atual > 33.5 else 'orange' if t_atual > 31.5 else 'green'
        folium.CircleMarker(
            [r['lat'], r['lon']], 
            radius=t_atual-20, 
            color=cor, 
            fill=True, 
            popup=f"<b>{r['Local']}</b><br>Temp: {round(t_atual,1)}°C<br>Verde: {r['Arborizacao']}%"
        ).add_to(m)
    folium_static(m, width=500, height=500)

with c2:
    st.subheader("📊 Gráfico de Dispersão: Verde vs Calor")
    fig_b = px.scatter(df_bairros, x="Arborizacao", y="Temperatura", size="Arborizacao", color="Temperatura", 
                       text="Local", color_continuous_scale='RdYlGn_r', height=500)
    fig_b.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="black")
    st.plotly_chart(fig_b, use_container_width=True)

# 7. TABELA DE RANKING (Extra para os juízes)
st.subheader("📋 Ranking de Vulnerabilidade Térmica")
df_ranking = df_bairros[['Local', 'Arborizacao', 'Temperatura']].sort_values(by='Temperatura', ascending=False)
st.dataframe(df_ranking, use_container_width=True)
