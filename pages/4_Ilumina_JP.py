import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# --- 1. SEGURANÇA E IDENTIDADE ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal para acessar o sistema.")
    st.stop()

# Cabeçalho LEGO Explorers com Hamtaro
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("hamtaro.webp", width=100)
with col_titulo:
    st.title("LEGO Explorers")
    st.subheader("💡 Ilumina JP")

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB_LUZ = "alertas_iluminacao.csv"

# --- 2. BANCO DE DADOS ---
bairros_jp = {
    "Centro": [-7.115, -34.885],
    "Mangabeira": [-7.165, -34.845],
    "Valentina": [-7.195, -34.860],
    "Manaíra": [-7.105, -34.835],
    "Bessa": [-7.085, -34.835],
    "Cristo": [-7.145, -34.870]
}

# Garante que o banco de dados tenha as colunas certas para evitar KeyError
colunas_luz = ['Data', 'Bairro', 'Rua', 'Referencia', 'Problema', 'Autor', 'lat', 'lon']

if 'db_luz' not in st.session_state:
    if os.path.exists(DATA_DB_LUZ):
        df_lido = pd.read_csv(DATA_DB_LUZ)
        # Verifica se todas as colunas existem
        for col in colunas_luz:
            if col not in df_lido.columns:
                df_lido[col] = "N/A"
        st.session_state.db_luz = df_lido
    else:
        st.session_state.db_luz = pd.DataFrame(columns=colunas_luz)

# --- 3. FORMULÁRIO DE MANUTENÇÃO ---
with st.form("alerta_iluminacao", clear_on_submit=True):
    st.markdown("### 🔦 Reportar Falha de Iluminação")
    
    bairro_sel = st.selectbox("Bairro:", list(bairros_jp.keys()))
    rua = st.text_input("Rua/Avenida:")
    ref = st.text_input("Ponto de Referência (Ex: Próximo ao colégio X):")
    
    tipo_falha = st.radio("Tipo de Problema:", 
                         ["Poste Apagado", "Luz Piscando", "Fiação Exposta", "Área sem Poste"], 
                         horizontal=True)
    
    anonimo = st.checkbox("Relatar de forma anônima")
    
    if st.form_submit_button("🚀 ENVIAR SOLICITAÇÃO"):
        if rua and ref:
            autor_final = "Anônimo" if anonimo else usuario_logado
            novo_alerta = {
                'Data': datetime.now().strftime("%d/%m/%Y"),
                'Bairro': bairro_sel, 'Rua': rua, 'Referencia': ref,
                'Problema': tipo_falha, 'Autor': autor_final,
                'lat': bairros_jp[bairro_sel][0], 'lon': bairros_jp[bairro_sel][1]
            }
            # Salva e atualiza
            st.session_state.db_luz = pd.concat([st.session_state.db_luz, pd.DataFrame([novo_alerta])], ignore_index=True)
            st.session_state.db_luz.to_csv(DATA_DB_LUZ, index=False)
            st.success("✅ Alerta enviado para a equipe de manutenção!")
            st.rerun()
        else:
            st.warning("Preencha a Rua e a Referência para localizarmos o poste.")

# --- 4. MAPA DE SEGURANÇA ---
st.write("---")
st.subheader("📍 Mapa de Pontos Escuros")
m_luz = folium.Map(location=[-7.135, -34.850], zoom_start=13)

for _, r in st.session_state.db_luz.iterrows():
    # Marcador amarelo para luz
    folium.Marker(
        [r['lat'], r['lon']],
        popup=f"🚨 {r['Problema']}\nLocal: {r['Rua']}\nStatus: Pendente",
        icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
    ).add_to(m_luz)

folium_static(m_luz, width=900)

# Tabela de ordens de serviço
st.subheader("📊 Ordens de Serviço Abertas")
st.dataframe(st.session_state.db_luz[['Data', 'Bairro', 'Rua', 'Problema', 'Autor']], use_container_width=True)
