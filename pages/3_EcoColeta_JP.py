import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
import os
import random
import string

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")
CAMINHO_CSV = 'denuncias.csv'

# Configuração do Geocodificador com timeout maior para evitar erros de busca
geolocator = Nominatim(user_agent="eco_jp_v15_final", timeout=10)

def gerar_protocolo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def salvar_no_csv(nova_linha):
    header = not os.path.exists(CAMINHO_CSV)
    df_aux = pd.DataFrame([nova_linha])
    # Garante a ordem das colunas
    colunas = ["Protocolo", "Data", "Endereco", "Tipo", "Autor", "Status", "Lat", "Lon"]
    df_aux = df_aux.reindex(columns=colunas)
    df_aux.to_csv(CAMINHO_CSV, mode='a', index=False, header=header, encoding='utf-8')

# --- 2. ESTADO DA SESSÃO ---
if 'lat' not in st.session_state:
    st.session_state.lat, st.session_state.lon = -7.1153, -34.8611
if 'endereco' not in st.session_state:
    st.session_state.endereco = ""

st.title("♻️ EcoColeta JP")

# --- 3. BUSCA POR TEXTO ---
st.subheader("Onde está o problema?")
col_txt, col_btn = st.columns([4, 1])

with col_txt:
    # Usamos o valor da session_state para não perder o que foi clicado
    endereco_input = st.text_input("Digite rua e número:", value=st.session_state.endereco, key="campo_rua")

with col_btn:
    st.write(" ") # Alinhamento
    if st.button("🔍 Localizar"):
        if endereco_input:
            try:
                location = geolocator.geocode(f"{endereco_input}, João Pessoa, PB")
                if location:
                    st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
                    st.session_state.endereco = endereco_input
                    st.rerun()
                else:
                    st.error("Endereço não encontrado.")
            except:
                st.error("Serviço de busca lento. Tente clicar no mapa.")

# --- 4. MAPA INTERATIVO ---
m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=18)
folium.Marker([st.session_state.lat, st.session_state.lon], 
              icon=folium.Icon(color='red', icon='trash', prefix='fa')).add_to(m)

# O mapa usa uma KEY baseada na coordenada para atualizar o pino visualmente
mapa_dados = st_folium(m, width=700, height=400, key=f"mapa_{st.session_state.lat}_{st.session_state.lon}")

# Se clicar no mapa, atualiza os dados
if mapa_dados['last_clicked']:
    nova_lat = mapa_dados['last_clicked']['lat']
    nova_lon = mapa_dados['last_clicked']['lng']
    if nova_lat != st.session_state.lat:
        st.session_state.lat, st.session_state.lon = nova_lat, nova_lon
        try:
            rev = geolocator.reverse(f"{nova_lat}, {nova_lon}")
            st.session_state.endereco = rev.address.split(',')[0]
        except:
            st.session_state.endereco = "Local marcado no mapa"
        st.rerun()

# --- 5. FORMULÁRIO DE ENVIO ---
st.write("---")
with st.form("form_envio", clear_on_submit=True):
    st.markdown("### Detalhes da Denúncia")
    
    # Campo apenas de leitura para confirmação
    st.info(f"📍 Local selecionado: {st.session_state.endereco}")
    
    tipo_lixo = st.selectbox("O que foi encontrado?", [
        "📦 Plástico/Papel", "🍾 Vidro/Metal", "🍎 Orgânico", 
        "🏗️ Entulho", "🛋️ Móveis", "💻 Eletrônico", "🌿 Poda", 
        "💡 Iluminação Pública", "🛞 Pneus", "🩺 Hospitalar"
    ])
    
    anonimo = st.checkbox("🕵️ Denúncia Anônima")
    
    enviar = st.form_submit_button("🚀 ENVIAR AGORA")
    
    if enviar:
        if st.session_state.endereco and st.session_state.endereco != "":
            protocolo = gerar_protocolo()
            
            dados = {
                "Protocolo": protocolo,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Endereco": st.session_state.endereco,
                "Tipo": tipo_lixo,
                "Autor": "Anônimo" if anonimo else "Cidadão",
                "Status": "Pendente 🟡",
                "Lat": st.session_state.lat,
                "Lon": st.session_state.lon
            }
            
            salvar_no_csv(dados)
            st.success(f"✅ REGISTRADO! Código: {protocolo}")
            st.warning("Anote seu código para acompanhar o status.")
            st.balloons()
            # Limpa o endereço para a próxima denúncia
            st.session_state.endereco = ""
        else:
            st.error("⚠️ Erro: Localização inválida. Clique no mapa ou busque a rua.")

st.sidebar.image("hamtaro.webp", width=150)
st.sidebar.markdown("### LEGO EXPLORERS")
