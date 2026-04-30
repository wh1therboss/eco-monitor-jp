import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import os

# --- SIDEBAR PERSONALIZADA: ILUMINA ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### 💡 Redes de Iluminação")
    st.success("MANUTENÇÃO: ATIVA")
    st.metric("Lâmpadas LED", "88%", "+5%")
    st.info("Reporte postes apagados para melhorar a segurança do seu bairro.")

# --- SEGURANÇA ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

st.title("💡 Ilumina JP")

# Lógica Simplificada para Exemplo
st.markdown("### 🔦 Registrar Falha de Poste")
with st.form("luz_form"):
    rua_luz = st.text_input("Rua do Poste:")
    problema = st.selectbox("Problema:", ["Poste Apagado", "Luz Piscando", "Fiação Exposta"])
    if st.form_submit_button("Enviar Alerta"):
        st.success("Equipe de manutenção notificada!")

m_luz = folium.Map(location=[-7.135, -34.850], zoom_start=13)
folium_static(m_luz, width=700)
