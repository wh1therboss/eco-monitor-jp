import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")

CAMINHO_CSV = 'denuncias.csv'

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("### LEGO EXPLORERS")
    st.write("---")
    st.caption("Acesso restrito para cidadãos.")

# --- LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_csv_v5")

if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
    st.session_state.end = ""

st.title("♻️ EcoColeta JP")
st.markdown("### 📝 Relatar Ocorrência")

# --- FORMULÁRIO COMPLETO ---
with st.form("form_csv", clear_on_submit=True):
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        end_input = st.text_input("Localização/Rua:", value=st.session_state.end)
    with col_num:
        numero = st.text_input("Nº:")
        
    tipo_lixo = st.selectbox("Tipo de Resíduo:", ["Plástico", "Vidro", "Entulho", "Orgânico", "Outros"])
    
    # Nota: Usuários normais não vêem a tabela nem os pontos no mapa dos outros
    if st.form_submit_button("🚀 GRAVAR DENÚNCIA"):
        if end_input:
            nova_denuncia = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": f"{end_input}, {numero}" if numero else end_input,
                "Tipo": tipo_lixo,
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            salvar_no_csv(nova_denuncia)
            st.success("✅ Denúncia enviada com sucesso! Obrigado pela colaboração.")
            st.balloons()
            st.session_state.end = "" # Limpa para o próximo
        else:
            st.warning("⚠️ Por favor, selecione o local no mapa abaixo.")

# --- MAPA APENAS PARA MARCAÇÃO ---
st.write("---")
st.subheader("📍 Marque o local no mapa")
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=15)
# Mostra apenas o marcador atual que a pessoa está a clicar
folium.Marker([st.session_state.lat, st.session_state.lon], icon=folium.Icon(color='red')).add_to(m)

mapa = st_folium(m, width=700, height=350)

if mapa['last_clicked']:
    lt, ln = mapa['last_clicked']['lat'], mapa['last_clicked']['lng']
    st.session_state.lat, st.session_state.lon = lt, ln
    try:
        loc = geolocator.reverse(f"{lt}, {ln}")
        st.session_state.end = loc.address.split(',')[0]
    except: 
        st.session_state.end = "Local marcado"
    st.rerun()

### 2. Ficheiro: `pages/4_ADMIN_CENTRAL.py`
*(Painel restrito com senha)*

```python
import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Painel Admin - EcoColeta", layout="wide")

CAMINHO_CSV = 'denuncias.csv'

# --- SISTEMA DE LOGIN SIMPLES ---
def login():
    st.title("🔑 Acesso Restrito - Admin")
    senha = st.text_input("Insira a senha mestra:", type="password")
    if senha == "lego123": # <--- TUA SENHA AQUI
        st.session_state.admin_logado = True
        st.rerun()
    elif senha != "":
        st.error("Senha incorreta!")

if 'admin_logado' not in st.session_state:
    login()
    st.stop()

# --- CONTEÚDO ADMIN ---
st.title("📊 Administração Central - EcoColeta JP")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Ocorrências", len(df))
    with col2:
        if st.button("🗑️ Limpar Banco de Dados (CUIDADO)"):
            os.remove(CAMINHO_CSV)
            st.rerun()

    st.write("---")
    
    # MAPA COM TODOS OS PONTOS (VISÃO ADMIN)
    st.subheader("🗺️ Mapa Geral de Ocorrências")
    m_admin = folium.Map(location=[-7.1153, -34.8611], zoom_start=13)
    for i, row in df.iterrows():
        folium.Marker(
            [row['Lat'], row['Lon']],
            popup=f"Tipo: {row['Tipo']}\nEnd: {row['Endereco']}",
            icon=folium.Icon(color='blue')
        ).add_to(m_admin)
    
    st_folium(m_admin, width=1100, height=500)

    st.write("---")
    st.subheader("📋 Tabela Detalhada")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Ainda não existem denúncias registradas no CSV.")

if st.sidebar.button("Sair"):
    del st.session_state.admin_logado
    st.rerun()

Aqui está a solução completa! O cidadão agora só vê o formulário e o mapa limpo para ele marcar. Já na **Central Admin**, tu colocas a senha (defini como `lego123` mas podes mudar) e vês tudo: o mapa com todos os pontos e a tabela completa.

Espero que os slides ajudem na apresentação do projeto! Se precisar de mais alguma coisa, avisa. 🐹🚀🏁
