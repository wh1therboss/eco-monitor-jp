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
    st.info("Preencha os detalhes e use o mapa abaixo para confirmar a localização.")
    st.write("---")
    st.caption("version: 0.1")

# --- 2. SEGURANÇA E CONEXÃO CLOUD ---
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Login necessário na página principal.")
    st.stop()

# Conexão com a planilha do Google
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados_google():
    try:
        # ttl=0 força o Streamlit a ler a planilha sempre que houver mudança
        return conn.read(ttl=0)
    except:
        return pd.DataFrame(columns=['Data', 'Endereço_Completo', 'Tipo', 'Autor', 'lat', 'lon', 'Status'])

geolocator = Nominatim(user_agent="lego_explorer_jp_cloud")

# Inicialização de coordenadas
if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat = -7.1153 
    st.session_state.clique_lon = -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")

# --- 3. FORMULÁRIO DE OCORRÊNCIA (O MESMO QUE VOCÊ GOSTA) ---
with st.form("form_denuncia", clear_on_submit=True):
    st.markdown("### 📝 Detalhes da Ocorrência")
    
    col_rua, col_num = st.columns([3, 1])
    with col_rua:
        rua_input = st.text_input("Rua/Avenida:", value=st.session_state.endereco_clique)
    with col_num:
        numero_input = st.text_input("Nº:")

    tipo = st.selectbox("Tipo de Resíduo Detalhado:", [
        "📦 Descarte Irregular de Plásticos e Embalagens",
        "📄 Papéis, Papelão e Revistas",
        "🍾 Vidros (Garrafas e Cacos)",
        "🥫 Metais (Latas e Alumínio)",
        "🍎 Resíduos Orgânicos/Restos de Alimentos",
        "🏗️ Entulho de Obras e Restos de Construção",
        "🛋️ Móveis Abandonados (Sofás, Colchões)",
        "🎣 Redes de Pesca e Equipamentos Marítimos",
        "💻 Lixo Eletrônico (Baterias, Telas, Cabos)",
        "🚗 Pneus e Borrachas",
        "🌿 Restos de Poda e Galhos",
        "🧴 Produtos Químicos ou Óleo de Cozinha"
    ])
    
    ref = st.text_input("Ponto de Referência (Ex: Próximo ao mercado X):")
    anonimo = st.checkbox("Fazer denúncia anônima")

    if st.form_submit_button("🚀 ENVIAR DENÚNCIA"):
        if rua_input:
            autor = "Anônimo" if anonimo else st.session_state.get('usuario_atual', 'Explorador')
            endereco_final = f"{rua_input}, {numero_input}" if numero_input else rua_input
            
            # Criar a nova linha de dados
            nova_denuncia = pd.DataFrame([{
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Endereço_Completo': endereco_final,
                'Tipo': tipo,
                'Autor': autor,
                'lat': st.session_state.clique_lat,
                'lon': st.session_state.clique_lon,
                'Status': 'Pendente'
            }])
            
            # Puxa os dados atuais do Google, junta com a nova e atualiza a planilha
            df_atual = carregar_dados_google()
            df_final = pd.concat([df_atual, nova_denuncia], ignore_index=True)
            conn.update(data=df_final)
            
            st.success(f"✅ Denúncia salva na nuvem! Local: {endereco_final}")
            st.session_state.endereco_clique = ""
            st.rerun()
        else:
            st.warning("⚠️ Selecione o local no mapa ou digite o endereço.")

# --- 4. MAPA INTERATIVO (EMBAIXO) ---
st.write("---")
st.subheader("📍 Confirme a Localização no Mapa")
st.info("Clique no local exato para capturar o endereço automaticamente.")

m_selecao = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=15)
folium.Marker(
    [st.session_state.clique_lat, st.session_state.clique_lon], 
    icon=folium.Icon(color='red', icon='trash')
).add_to(m_selecao)

output = st_folium(m_selecao, width=700, height=350, key="mapa_google")

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

# --- 5. TABELA DE REGISTROS (VEM DIRETO DO GOOGLE) ---
st.write("---")
st.subheader("📋 Histórico Global (Nuvem)")
df_historico = carregar_dados_google()
if not df_historico.empty:
    st.dataframe(df_historico.iloc[::-1], use_container_width=True)
else:
    st.info("Nenhuma denúncia registada na nuvem.")
