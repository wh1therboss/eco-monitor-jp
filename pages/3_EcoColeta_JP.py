import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# --- SIDEBAR PERSONALIZADA: ECOCOLETA ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ♻️ Gestão de Resíduos")
    st.warning("ALERTA: PONTOS DE DESCARTE")
    st.metric("Reciclagem Mensal", "45%", "+2%")
    st.info("Ajude a manter as praias de JP limpas. Denuncie descarte irregular.")

# --- SEGURANÇA E DADOS ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"
colunas_sistema = ['Data', 'Bairro', 'Rua', 'Numero', 'Referencia', 'Tipo', 'Autor', 'lat', 'lon']

# Previne erro de coluna faltando (KeyError)
if 'db_relatos' not in st.session_state:
    if os.path.exists(DATA_DB):
        df_lido = pd.read_csv(DATA_DB)
        for col in colunas_sistema:
            if col not in df_lido.columns: df_lido[col] = "N/A"
        st.session_state.db_relatos = df_lido
    else:
        st.session_state.db_relatos = pd.DataFrame(columns=colunas_sistema)

st.title("♻️ EcoColeta JP")

# --- FORMULÁRIO COM MAIS OPÇÕES DE LIXO ---
with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📢 Registrar Descarte de Lixo")
    
    rua = st.text_input("Rua/Avenida:")
    col_n, col_r = st.columns([1, 2])
    with col_n: 
        num = st.text_input("Nº:")
    with col_r: 
        ref = st.text_input("Ponto de Referência:")
    
    # Lista expandida de opções de lixo
    tipo = st.selectbox("Tipo de Resíduo Encontrado:", [
        "Plásticos (Garrafas/Embalagens)", 
        "Papel/Papelão", 
        "Vidro", 
        "Metal/Latas", 
        "Resíduos Orgânicos", 
        "Entulho de Construção", 
        "Móveis Abandonados", 
        "Redes de Pesca/Artes de Pesca", 
        "Eletrônicos (E-lixo)", 
        "Pneus"
    ])
    
    anonimo = st.checkbox("Fazer denúncia de forma anônima")
    
    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua and ref:
            autor = "Anônimo" if anonimo else usuario_logado
            novo = {
                'Data': datetime.now().strftime("%d/%m/%Y"), 
                'Bairro': "João Pessoa", 
                'Rua': rua, 
                'Numero': num if num else "S/N", 
                'Referencia': ref, 
                'Tipo': tipo, 
                'Autor': autor, 
                'lat': -7.120, 
                'lon': -34.845
            }
            st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo])], ignore_index=True)
            st.session_state.db_relatos.to_csv(DATA_DB, index=False)
            st.success(f"✅ Denúncia enviada! Registrado por: {autor}")
            st.rerun()
        else:
            st.warning("⚠️ Preencha os campos de localização (Rua e Referência).")

# --- MAPA E TABELA ---
st.write("---")
st.subheader("📍 Mapa de Ocorrências")
m = folium.Map(location=[-7.120, -34.820], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    cor_ponto = 'red' if r['Autor'] == 'Anônimo' else 'blue'
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"<b>{r['Tipo']}</b><br>Ref: {r['Referencia']}", 
        icon=folium.Icon(color=cor_ponto, icon='trash')
    ).add_to(m)

folium_static(m, width=700)

st.subheader("📊 Histórico de Registros")
st.dataframe(st.session_state.db_relatos[['Data', 'Rua', 'Tipo', 'Autor']], use_container_width=True)
