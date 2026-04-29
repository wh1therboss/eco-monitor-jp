import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# ==========================================
# 1. TRAVA DE SEGURANÇA (OBRIGATÓRIO NO TOPO)
# ==========================================
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso negado! Por favor, faça login na página principal.")
    st.stop()

# ==========================================
# 2. CONFIGURAÇÃO E BANCO DE DADOS
# ==========================================
usuario = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"

def carregar_denuncias():
    if os.path.exists(DATA_DB):
        return pd.read_csv(DATA_DB)
    return pd.DataFrame(columns=['Bairro', 'Endereco', 'Tipo', 'Autor', 'Data', 'lat', 'lon'])

# Inicializa o estado do banco de dados
if 'db_relatos' not in st.session_state:
    st.session_state.db_relatos = carregar_denuncias()

# ==========================================
# 3. INTERFACE E FORMULÁRIO
# ==========================================
st.title(f"👋 Olá, {usuario}!")
st.subheader("♻️ Sistema EcoColeta JP - LEGO Explorers")

with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📢 Registar Lixo em Praias/Vias")
    col1, col2 = st.columns(2)
    with col1:
        # Foco nas praias e bairros costeiros de JP
        bairro = st.selectbox("Localização:", ["Bessa", "Manaíra", "Tambaú", "Cabo Branco", "Penha", "Seixas"])
        rua = st.text_input("Ponto de Referência (Ex: Quiosque X):")
    with col2:
        tipo = st.radio("Tipo de Resíduo:", ["Plástico/Garrafas", "Redes de Pesca", "Lixo Orgânico", "Entulho"])
        enviar = st.form_submit_button("ADICIONAR AO MAPA E TABELA")

    if enviar and rua:
        # Coordenadas reais das praias de João Pessoa
        coords = {
            "Bessa": [-7.085, -34.830], 
            "Manaíra": [-7.092, -34.831], 
            "Tambaú": [-7.114, -34.820], 
            "Cabo Branco": [-7.135, -34.818],
            "Penha": [-7.165, -34.795],
            "Seixas": [-7.155, -34.790]
        }
        
        novo_registo = {
            'Bairro': bairro, 'Endereco': rua, 'Tipo': tipo,
            'Autor': usuario, 'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'lat': coords[bairro][0], 'lon': coords[bairro][1]
        }
        
        st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo_registo])], ignore_index=True)
        st.session_state.db_relatos.to_csv(DATA_DB, index=False)
        st.success("✅ Registo guardado com sucesso!")
        st.rerun()

# ==========================================
# 4. MAPA DAS PRAIAS (FOLIUM)
# ==========================================
st.write("---")
st.subheader("📍 Mapa de Monitorização em Tempo Real")
m = folium.Map(location=[-7.120, -34.830], zoom_start=13)

# Adiciona os marcadores no mapa
for _, r in st.session_state.db_relatos.iterrows():
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"<b>{r['Tipo']}</b><br>{r['Endereco']}<br>Por: {r['Autor']}",
        icon=folium.Icon(color='blue' if 'Plástico' in r['Tipo'] else 'red', icon='info-sign')
    ).add_to(m)

folium_static(m, width=1000)

# ==========================================
# 5. TABELA DE DADOS DE VOLTA
# ==========================================
st.write("---")
st.subheader("📊 Tabela de Registos Detalhada")
if not st.session_state.db_relatos.empty:
    # Mostra a tabela formatada
    st.dataframe(st.session_state.db_relatos[['Data', 'Bairro', 'Endereco', 'Tipo', 'Autor']], use_container_width=True)
    
    # Botão para limpar (opcional para testes)
    if st.button("Limpar Histórico"):
        if os.path.exists(DATA_DB): os.remove(DATA_DB)
        st.session_state.db_relatos = pd.DataFrame(columns=['Bairro', 'Endereco', 'Tipo', 'Autor', 'Data', 'lat', 'lon'])
        st.rerun()
else:
    st.write("Ainda não há registos no mapa.")
