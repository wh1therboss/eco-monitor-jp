import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# 1. TRAVA DE SEGURANÇA (Resolve o erro de session_state)
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Acesso negado! Por favor, faça login na página principal.")
    st.stop()

# 2. CONFIGURAÇÕES E BANCO DE DADOS
DATA_DB = "denuncias_ecocoleta.csv"

def carregar_denuncias():
    if os.path.exists(DATA_DB):
        df = pd.read_csv(DATA_DB)
        if 'Endereco' not in df.columns:
            df['Endereco'] = "Não informado"
        return df
    return pd.DataFrame(columns=['Bairro', 'Endereco', 'Tipo', 'Autor', 'Data', 'lat', 'lon'])

if 'db_relatos' not in st.session_state:
    st.session_state.db_relatos = carregar_denuncias()

# 3. INTERFACE
st.title("♻️ Sistema EcoColeta JP")
st.subheader(f"Colaborador: {st.session_state.usuario_atual}")

with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📢 Registrar Lixo Irregular")
    col1, col2 = st.columns(2)
    with col1:
        bairro = st.selectbox("Bairro:", ["Bessa", "Manaíra", "Tambaú", "Cabo Branco", "Mangabeira"])
        rua = st.text_input("Endereço/Referência:")
    with col2:
        tipo = st.radio("Tipo:", ["Doméstico", "Entulho", "Móveis"])
        enviar = st.form_submit_button("REGISTRAR")

    if enviar and rua:
        coords = {"Bessa": [-7.085, -34.830], "Manaíra": [-7.092, -34.831], "Tambaú": [-7.114, -34.820], 
                  "Cabo Branco": [-7.135, -34.818], "Mangabeira": [-7.165, -34.845]}
        
        nova = {
            'Bairro': bairro, 'Endereco': rua, 'Tipo': tipo,
            'Autor': st.session_state.usuario_atual, 'Data': datetime.now().strftime("%d/%m/%Y"),
            'lat': coords[bairro][0], 'lon': coords[bairro][1]
        }
        st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([nova])], ignore_index=True)
        st.session_state.db_relatos.to_csv(DATA_DB, index=False)
        st.success("Registrado no mapa!")
        st.rerun()

# 4. MAPA
st.write("---")
st.subheader("📍 Mapa de Ocorrências em Tempo Real")
m = folium.Map(location=[-7.115, -34.85], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"Local: {r['Endereco']}<br>Tipo: {r['Tipo']}",
        icon=folium.Icon(color='red', icon='trash')
    ).add_to(m)

folium_static(m, width=1000)
