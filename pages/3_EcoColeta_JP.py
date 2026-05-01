import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURAÇÃO DA SIDEBAR ---
with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("### ♻️ Gestão de Resíduos")
    st.info("Relate descarte irregular de lixo em João Pessoa.")
    st.write("---")
    st.caption("version: 0.2 (Cloud)")

# --- 2. SEGURANÇA E CONEXÃO CLOUD ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

# Conexão oficial com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados_google():
    try:
        # ttl=0 garante que ele leia os dados novos sempre que a página atualizar
        return conn.read(ttl=0)
    except Exception as e:
        # Se a planilha estiver vazia, cria o DataFrame com as colunas certas
        return pd.DataFrame(columns=['Data', 'Endereço_Completo', 'Tipo', 'Autor', 'lat', 'lon', 'Status'])

geolocator = Nominatim(user_agent="lego_explorer_jp_cloud_v2")

# Inicialização de coordenadas no mapa
if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat = -7.1153 
    st.session_state.clique_lon = -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")

# --- 3. FORMULÁRIO DE OCORRÊNCIA ---
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Detalhes da Ocorrência")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        rua_input = st.text_input("Rua/Avenida:", value=st.session_state.endereco_clique)
    with col_num:
        numero_input = st.text_input("Nº:")

    tipo = st.selectbox("Tipo de Resíduo:", [
        "📦 Plásticos e Embalagens",
        "📄 Papéis e Papelão",
        "🍾 Vidros (Garrafas e Cacos)",
        "🥫 Metais e Latas",
        "🍎 Resíduos Orgânicos",
        "🏗️ Entulho e Construção",
        "🛋️ Móveis e Grandes Objetos",
        "💻 Lixo Eletrônico",
        "🚗 Pneus",
        "🌿 Poda e Galhos",
        "🧴 Químicos ou Óleo"
    ])
    
    anonimo = st.checkbox("Fazer denúncia anônima")

    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua_input:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            endereco_final = f"{rua_input}, {numero_input}" if numero_input else rua_input
            
            # 1. Preparar a nova linha
            nova_denuncia = {
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Endereço_Completo': endereco_final,
                'Tipo': tipo,
                'Autor': autor,
                'lat': st.session_state.clique_lat,
                'lon': st.session_state.clique_lon,
                'Status': 'Pendente'
            }
            
            try:
                # 2. Ler dados atuais
                df_atual = carregar_dados_google()
                
                # 3. Concatenar com a nova denúncia
                df_final = pd.concat([df_atual, pd.DataFrame([nova_denuncia])], ignore_index=True)
                
                # 4. Atualizar a planilha no Google
                conn.update(data=df_final)
                
                st.success(f"✅ Denúncia salva na nuvem! Local: {endereco_final}")
                st.balloons()
                st.session_state.endereco_clique = ""
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao salvar na nuvem: {e}")
                st.info("Certifique-se de que a planilha está compartilhada como EDITOR.")
        else:
            st.warning("⚠️ Informe a rua ou use o mapa abaixo.")

# --- 4. MAPA INTERATIVO (EMBAIXO) ---
st.write("---")
st.subheader("📍 Ajuste a Localização no Mapa")

m_selecao = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=15)
folium.Marker(
    [st.session_state.clique_lat, st.session_state.clique_lon], 
    icon=folium.Icon(color='red', icon='trash')
).add_to(m_selecao)

output = st_folium(m_selecao, width=700, height=350, key="mapa_cloud_final")

if output['last_clicked']:
    lat_clique = output['last_clicked']['lat']
    lon_clique = output['last_clicked']['lng']
    if lat_clique != st.session_state.clique_lat:
        st.session_state.clique_lat = lat_clique
        st.session_state.clique_lon = lon_clique
        try:
            location = geolocator.reverse(f"{lat_clique}, {lon_clique}")
            if location:
                st.session_state.endereco_clique = location.address.split(',')[0]
        except:
            st.session_state.endereco_clique = "Localização capturada"
        st.rerun()

# --- 5. TABELA DE REGISTROS ---
st.write("---")
st.subheader("📋 Histórico Global (Google Sheets)")
df_historico = carregar_dados_google()
if not df_historico.empty:
    # Mostra as denúncias mais recentes primeiro
    st.dataframe(df_historico.iloc[::-1], use_container_width=True)
else:
    st.info("Aguardando a primeira denúncia na nuvem...")
