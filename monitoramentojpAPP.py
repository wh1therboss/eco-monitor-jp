import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(layout="wide", page_title="Lego Explorers | EcoMonitor JP")

# 2. CSS CUSTOMIZADO
st.markdown("""
    <style>
    /* Fundo principal escuro */
    .main { background-color: #0e1117; }
    
    /* Métricas com letras brancas e nítidas */
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 38px !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #deff9a !important; font-size: 20px !important; }
    .stMetric { 
        background-color: #1c2128; 
        border: 2px solid #30363d; 
        padding: 25px; 
        border-radius: 15px; 
    }
    
    /* Estilo da Nota Técnica */
    .nota-tecnica {
        background-color: #1c2128;
        border-left: 10px solid #deff9a;
        padding: 25px;
        border-radius: 10px;
        color: #f0f0f0;
        margin-top: 20px;
    }

    /* COR PRETA PARA O NOME LEGO EXPLORERS NA BARRA LATERAL */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown p { 
        color: #000000 !important; 
    }

    /* Títulos do dashboard principal continuam brancos */
    .main h1, .main h2, .main h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE TELEMETRIA
def info_satelite():
    data_lancamento = datetime(2013, 2, 11)
    return (datetime.now() - data_lancamento).days

# 4. BARRA LATERAL (LEGO EXPLORERS & HAMTARO)
with st.sidebar:
    # Carrega a foto do Hamtaro
    try:
        st.image("hamtaro.webp", width=180)
    except:
        st.error("Arquivo 'hamtaro.webp' não encontrado!")
    
    st.title("LEGO EXPLORERS")
    st.subheader("Equipe de Monitoramento")
    st.divider()
    
    st.header("🛰️ Telemetria Landsat 8")
    st.metric("Dias em Órbita", f"{info_satelite()}")
    st.success("STATUS: SATÉLITE ONLINE")
    
    st.divider()
    # Slider de 10 anos
    ano_selecionado = st.slider("Exploração Temporal:", 2016, 2026, 2026)
    st.info(f"Ciclo de Análise: {ano_selecionado}")

# 5. PROCESSAMENTO DOS DADOS
def get_data(ano):
    df_base = pd.read_csv('dados_historicos_jp.csv')
    fator = (ano - 2016) / 10
    df_ano = df_base[['Bairro', 'lat', 'lon']].copy()
    df_ano['Temperatura'] = df_base['Temp2016'] + (df_base['Temp2026'] - df_base['Temp2016']) * fator
    df_ano['Arborizacao'] = df_base['Verde2016'] + (df_base['Verde2026'] - df_base['Verde2016']) * fator
    return df_ano

df = get_data(ano_selecionado)

# 6. FUNÇÃO DE NOTA TÉCNICA
def gerar_nota(df, ano):
    media_t = df['Temperatura'].mean()
    bairro_max = df.loc[df['Temperatura'].idxmax(), 'Bairro']
    
    if ano == 2016:
        status = "ESTÁVEL"
        msg = "Equilíbrio térmico preservado pela densidade vegetal."
    elif media_t > 32:
        status = "CRÍTICO"
        msg = f"Alto risco em {bairro_max}. Necessário reflorestamento urgente."
    else:
        status = "ALERTA"
        msg = "Tendência de aquecimento por redução de áreas verdes."
        
    return f"""
    ### 📝 NOTA TÉCNICA LEGO EXPLORERS ({ano})
    **STATUS:** {status}  
    **PARECER:** Média de {media_t:.1f}°C. O monitoramento via satélite identifica {bairro_max} como zona de estresse térmico máximo. {msg}
    """

# 7. DASHBOARD PRINCIPAL
st.title("🛰️ EcoMonitor JP | João Pessoa")
st.markdown(f"**Sistema de Monitoramento Térmico | Ciclo {ano_selecionado}**")

# Métricas
m1, m2, m3 = st.columns(3)
m1.metric("Temperatura Média", f"{df['Temperatura'].mean():.1f} °C")
m2.metric("Ponto Crítico", df.loc[df['Temperatura'].idxmax(), 'Bairro'], f"{df['Temperatura'].max():.1f} °C")
m3.metric("Cobertura Verde", f"{df['Arborizacao'].mean():.1f}%")

st.divider()

# Mapa e Gráfico
col_map, col_plot = st.columns([1, 1.3])

with col_map:
    st.subheader("📍 Mapa Térmico de Superfície")
    m = folium.Map(location=[-7.14, -34.85], zoom_start=12, tiles="cartodbpositron")
    for _, row in df.iterrows():
        cor = "#d73027" if row['Temperatura'] > 32 else "#fc8d59" if row['Temperatura'] > 29 else "#1a9850"
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['Temperatura'] * 0.8,
            popup=f"{row['Bairro']}: {row['Temperatura']:.1f}°C",
            color=cor, fill=True, fill_opacity=0.7
        ).add_to(m)
    st_folium(m, width="100%", height=600)

with col_plot:
    st.subheader("📊 Correlação: Árvores vs Calor")
    fig = px.scatter(df, x="Arborizacao", y="Temperatura", text="Bairro",
                     color="Temperatura", size="Temperatura",
                     color_continuous_scale="RdYlGn_r",
                     range_x=[0, 60], range_y=[25, 37], height=600)
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Nota Técnica Final
st.markdown('<div class="nota-tecnica">', unsafe_allow_html=True)
st.markdown(gerar_nota(df, ano_selecionado))
st.markdown('</div>', unsafe_allow_html=True)