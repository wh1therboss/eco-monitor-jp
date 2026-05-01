import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="EcoColeta JP", page_icon="♻️")

# --- 2. CONFIGURAÇÃO DO WHATSAPP ---
# IMPORTANTE: Coloque seu número com 55 + DDD + Número (tudo junto)
# Exemplo: "5583988887777"
MEU_WHATSAPP = "5583900000000" 

with st.sidebar:
    st.image("hamtaro.webp", width=150)
    st.markdown("<h2 style='text-align: center;'>LEGO EXPLORERS</h2>", unsafe_allow_html=True)
    st.write("---")
    st.info("📢 As denúncias são enviadas diretamente para o WhatsApp da nossa central.")

# --- 3. LÓGICA DE LOCALIZAÇÃO ---
geolocator = Nominatim(user_agent="lego_explorer_jp_v4")

if 'clique_lat' not in st.session_state:
    st.session_state.clique_lat, st.session_state.clique_lon = -7.1153, -34.8611
    st.session_state.endereco_clique = ""

st.title("♻️ EcoColeta JP")
st.markdown("Relate o descarte irregular de lixo em João Pessoa de forma rápida!")

# --- 4. FORMULÁRIO ---
with st.form("form_denuncia_zap"):
    st.markdown("### 📝 Detalhes da Ocorrência")
    
    # O endereço é preenchido automaticamente ao clicar no mapa
    endereco = st.text_input("Endereço do local:", value=st.session_state.endereco_clique)
    
    tipo_lixo = st.selectbox("O que você encontrou?", [
        "📦 Plásticos e Embalagens",
        "📄 Papel e Papelão",
        "🍾 Vidros",
        "🥫 Metais",
        "🍎 Resíduos Orgânicos",
        "🏗️ Entulho de Obras",
        "🛋️ Móveis e Objetos Grandes",
        "💻 Lixo Eletrônico",
        "🌿 Poda e Galhos"
    ])
    
    # Preparando o texto da mensagem
    # %0A é o código para pular linha no WhatsApp
    mensagem = (
        f"🚨 *NOVA DENÚNCIA AMBIENTAL* 🚨%0A%0A"
        f"📍 *Local:* {endereco}%0A"
        f"♻️ *Tipo de Lixo:* {tipo_lixo}%0A"
        f"🌎 *Link do Mapa:* https://www.google.com/maps?q={st.session_state.clique_lat},{st.session_state.clique_lon}"
    )
    
    link_final_whatsapp = f"https://wa.me/{MEU_WHATSAPP}?text={mensagem}"

    enviar = st.form_submit_button("📢 ENVIAR DENÚNCIA")
    
    if enviar:
        if endereco:
            st.markdown(f"""
                <div style="text-align: center; padding: 20px; border: 2px solid #2ecc71; border-radius: 10px;">
                    <p>Quase lá! Clique no botão abaixo para confirmar o envio:</p>
                    <a href="{link_final_whatsapp}" target="_blank">
                        <button style="
                            background-color: #25D366;
                            color: white;
                            padding: 15px 30px;
                            border: none;
                            border-radius: 5px;
                            font-size: 18px;
                            font-weight: bold;
                            cursor: pointer;">
                            ✅ CONFIRMAR NO WHATSAPP
                        </button>
                    </a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, clique no mapa abaixo para marcar a localização.")

# --- 5. MAPA INTERATIVO ---
st.write("---")
st.subheader("📍 Toque no mapa para marcar o local exato")
m = folium.Map(location=[st.session_state.clique_lat, st.session_state.clique_lon], zoom_start=15)
folium.Marker(
    [st.session_state.clique_lat, st.session_state.clique_lon], 
    icon=folium.Icon(color='red', icon='trash')
).add_to(m)

# Exibe o mapa e captura o clique
map_data = st_folium(m, width=700, height=350, key="mapa_zap")

if map_data['last_clicked']:
    lat_c = map_data['last_clicked']['lat']
    lon_c = map_data['last_clicked']['lng']
    
    # Se o clique for diferente do anterior, atualiza
    if lat_c != st.session_state.clique_lat:
        st.session_state.clique_lat = lat_c
        st.session_state.clique_lon = lon_c
        try:
            # Tenta descobrir o nome da rua
            location = geolocator.reverse(f"{lat_c}, {lon_c}")
            if location:
                st.session_state.endereco_clique = location.address.split(',')[0]
        except:
            st.session_state.endereco_clique = "Localização capturada"
        st.rerun()

st.caption("Ao enviar, o seu aplicativo de WhatsApp será aberto com a mensagem pronta.")
