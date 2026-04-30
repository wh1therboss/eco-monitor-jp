import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# --- 1. SEGURANÇA E IDENTIDADE (SIDEBAR) ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 💡 Redes de Iluminação")
    st.success("MANUTENÇÃO: ATIVA")
    st.metric("Eficiência LED", "88%", "+5%")
    st.info("Reporte falhas para garantir a segurança noturna em nossa capital.")

if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal para acessar o sistema.")
    st.stop()

# Cabeçalho da página
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("hamtaro.webp", width=100)
with col_titulo:
    st.title("LEGO Explorers")
    st.subheader("💡 Ilumina JP - Manutenção de Postes")

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB_LUZ = "alertas_iluminacao.csv"

# --- 2. BANCO DE DADOS (PREVENÇÃO DE ERROS) ---
bairros_jp = {
    "Centro": [-7.115, -34.885], "Mangabeira": [-7.165, -34.845],
    "Valentina": [-7.195, -34.860], "Manaíra": [-7.105, -34.835],
    "Bessa": [-7.085, -34.835], "Cristo": [-7.145, -34.870],
    "Cabo Branco": [-7.130, -34.820], "Bancários": [-7.150, -34.830]
}

colunas_luz = ['Data', 'Bairro', 'Rua', 'Referencia', 'Problema', 'Autor', 'lat', 'lon']

if 'db_luz' not in st.session_state:
    if os.path.exists(DATA_DB_LUZ):
        df_lido = pd.read_csv(DATA_DB_LUZ)
        # Garante que colunas novas não causem KeyError
        for col in colunas_luz:
            if col not in df_lido.columns: df_lido[col] = "N/A"
        st.session_state.db_luz = df_lido
    else:
        st.session_state.db_luz = pd.DataFrame(columns=colunas_luz)

# --- 3. FORMULÁRIO COM MAIS OPÇÕES ---
with st.form("alerta_iluminacao", clear_on_submit=True):
    st.markdown("### 🔦 Reportar Falha ou Sugestão")
    
    bairro_sel = st.selectbox("Bairro:", list(bairros_jp.keys()))
    rua = st.text_input("Rua/Avenida:")
    ref = st.text_input("Ponto de Referência (Ex: Em frente à farmácia):")
    
    # Lista expandida de problemas
    tipo_falha = st.selectbox("O que está acontecendo?", [
        "Lâmpada Apagada (Poste Escuro)", 
        "Lâmpada Acesa durante o Dia", 
        "Lâmpada Piscando (Efeito Estroboscópico)",
        "Poste Danificado/Caído",
        "Fiação Solta ou Exposta",
        "Curto-circuito/Faíscas",
        "Área que Necessita de Novo Poste",
        "Braço de Iluminação Quebrado",
        "Transformador com Barulho Estranho"
    ])
    
    anonimo = st.checkbox("Relatar de forma anônima 🕵️")
    
    if st.form_submit_button("🚀 ENVIAR SOLICITAÇÃO"):
        if rua and ref:
            autor_final = "Anônimo" if anonimo else usuario_logado
            novo_alerta = {
                'Data': datetime.now().strftime("%d/%m/%Y"),
                'Bairro': bairro_sel, 'Rua': rua, 'Referencia': ref,
                'Problema': tipo_falha, 'Autor': autor_final,
                'lat': bairros_jp[bairro_sel][0], 'lon': bairros_jp[bairro_sel][1]
            }
            st.session_state.db_luz = pd.concat([st.session_state.db_luz, pd.DataFrame([novo_alerta])], ignore_index=True)
            st.session_state.db_luz.to_csv(DATA_DB_LUZ, index=False)
            st.success("✅ Ordem de serviço aberta! Obrigado por colaborar.")
            st.rerun()
        else:
            st.warning("⚠️ Forneça o nome da rua e a referência para a equipe técnica.")

# --- 4. MAPA E HISTÓRICO ---
st.write("---")
st.subheader("📍 Pontos de Manutenção Pendente")
m_luz = folium.Map(location=[-7.135, -34.850], zoom_start=13)

for _, r in st.session_state.db_luz.iterrows():
    folium.Marker(
        [r['lat'], r['lon']],
        popup=f"🚨 {r['Problema']}\nLocal: {r['Rua']}",
        icon=folium.Icon(color='orange', icon='bolt', prefix='fa')
    ).add_to(m_luz)

folium_static(m_luz, width=700)

st.subheader("📋 Status das Solicitações")
st.dataframe(st.session_state.db_luz[['Data', 'Bairro', 'Rua', 'Problema', 'Autor']], use_container_width=True)
