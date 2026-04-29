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
    st.error("🚨 Acesso negado! Por favor, faça login na página principal (main).")
    st.stop()

# ==========================================
# 2. INICIALIZAÇÃO E BANCO DE DADOS
# ==========================================
usuario = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"

def carregar_denuncias():
    if os.path.exists(DATA_DB):
        df = pd.read_csv(DATA_DB)
        return df
    return pd.DataFrame(columns=['Bairro', 'Endereco', 'Tipo', 'Autor', 'Data', 'lat', 'lon'])

if 'db_relatos' not in st.session_state:
    st.session_state.db_relatos = carregar_denuncias()

# ==========================================
# 3. INTERFACE DO USUÁRIO
# ==========================================
st.title(f"👋 Olá, {usuario}!")
st.subheader("♻️ Sistema EcoColeta JP")

with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📢 Registrar Lixo Irregular")
    col1, col2 = st.columns(2)
    with col1:
        bairro = st.selectbox("Bairro:", ["Bessa", "Manaíra", "Tambaú", "Cabo Branco", "Mangabeira"])
        rua = st.text_input("Endereço/Referência:")
    with col2:
        tipo = st.radio("Tipo de Lixo:", ["Doméstico", "Entulho", "Móveis/Eletrônicos"])
        enviar = st.form_submit_button("REGISTRAR NO MAPA")

    if enviar and rua:
        # Coordenadas aproximadas para o mapa
        coords = {"Bessa": [-7.085, -34.830], "Manaíra": [-7.092, -34.831], 
                  "Tambaú": [-7.114, -34.820], "Cabo Branco": [-7.135, -34.818], 
                  "Mangabeira": [-7.165, -34.845]}
        
        nova_denuncia = {
            'Bairro': bairro, 'Endereco': rua, 'Tipo': tipo,
            'Autor': usuario, 'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'lat': coords[bairro][0], 'lon': coords[bairro][1]
        }
        
        # Atualiza o DataFrame e o arquivo CSV
        st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([nova_denuncia])], ignore_index=True)
        st.session_state.db_relatos.to_csv(DATA_DB, index=False)
        st.success("Denúncia registrada com sucesso!")
        st.rerun()

# ==========================================
# 4. MAPA DE OCORRÊNCIAS
# ==========================================
st.write("---")
st.subheader("📍 Mapa de Descartes Irregulares")

# Centraliza o mapa em João Pessoa
m = folium.Map(location=[-7.115, -34.85], zoom_start=12)

# Adiciona marcadores para cada denúncia
for _, r in st.session_state.db_relatos.iterrows():
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"<b>Tipo:</b> {r['Tipo']}<br><b>Local:</b> {r['Endereco']}<br><b>Por:</b> {r['Autor']}",
        icon=folium.Icon(color='red', icon='trash')
    ).add_to(m)

folium_static(m, width=700)
