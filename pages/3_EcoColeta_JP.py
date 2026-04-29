import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import os

# ==========================================
# 1. TRAVA DE SEGURANÇA
# ==========================================
if 'autenticado' not in st.session_state or not st.session_state.autenticado:
    st.error("🚨 Por favor, faça login na página principal.")
    st.stop()

usuario_logado = st.session_state.get('usuario_atual', 'Explorador')
DATA_DB = "denuncias_ecocoleta.csv"

# ==========================================
# 2. BANCO DE DADOS E COORDENADAS
# ==========================================
praias_jp = {
    "Bessa": [-7.085, -34.830],
    "Manaíra": [-7.092, -34.831],
    "Tambaú": [-7.114, -34.820],
    "Cabo Branco": [-7.135, -34.818],
    "Penha": [-7.165, -34.795],
    "Seixas": [-7.155, -34.790],
    "Gramame": [-7.240, -34.805]
}

def carregar_denuncias():
    if os.path.exists(DATA_DB):
        return pd.read_csv(DATA_DB)
    return pd.DataFrame(columns=['Bairro', 'Rua', 'Numero', 'Referencia', 'Tipo', 'Autor', 'Data', 'lat', 'lon'])

if 'db_relatos' not in st.session_state:
    st.session_state.db_relatos = carregar_denuncias()

# ==========================================
# 3. INTERFACE E FORMULÁRIO DETALHADO
# ==========================================
st.title("♻️ EcoColeta JP")
st.subheader("📢 Central de Denúncias de Resíduos")

with st.form("nova_denuncia", clear_on_submit=True):
    st.markdown("### 📍 Detalhes da Localização")
    
    # Endereço dividido por linhas
    bairro_sel = st.selectbox("Bairro/Praia:", list(praias_jp.keys()))
    rua = st.text_input("Rua/Avenida:")
    col_end1, col_end2 = st.columns([1, 2])
    with col_end1:
        numero = st.text_input("Número (se houver):")
    with col_end2:
        ponto_ref = st.text_input("Ponto de Referência (Ex: Próximo ao quiosque X):")
    
    st.markdown("---")
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        tipo_lixo = st.radio("Tipo de Resíduo:", ["Plástico/Garrafas", "Orgânico", "Entulho/Móveis", "Redes de Pesca"])
    with col_info2:
        # Opção de anonimato
        fazer_anonimo = st.checkbox("Denúncia Anónima (Ocultar meu nome)")
        enviar = st.form_submit_button("🚀 ENVIAR DENÚNCIA")

    if enviar and rua and ponto_ref:
        # Define o autor baseado na escolha de anonimato
        autor_final = "Anónimo" if fazer_anonimo else usuario_logado
        
        novo_relato = {
            'Bairro': bairro_sel, 
            'Rua': rua, 
            'Numero': numero if numero else "S/N", 
            'Referencia': ponto_ref,
            'Tipo': tipo_lixo, 
            'Autor': autor_final, 
            'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'lat': praias_jp[bairro_sel][0], 
            'lon': praias_jp[bairro_sel][1]
        }
        
        # Salva no banco de dados
        st.session_state.db_relatos = pd.concat([st.session_state.db_relatos, pd.DataFrame([novo_relato])], ignore_index=True)
        st.session_state.db_relatos.to_csv(DATA_DB, index=False)
        st.success(f"✅ Obrigado! Denúncia registada como: {autor_final}")
        st.rerun()

# ==========================================
# 4. MAPA E GRÁFICO
# ==========================================
st.write("---")
st.subheader("📍 Mapa de Ocorrências")
m = folium.Map(location=[-7.120, -34.820], zoom_start=12)

for _, r in st.session_state.db_relatos.iterrows():
    folium.Marker(
        [r['lat'], r['lon']], 
        popup=f"<b>{r['Tipo']}</b><br>{r['Rua']}, {r['Numero']}<br>Ref: {r['Referencia']}<br>Por: {r['Autor']}",
        icon=folium.Icon(color='red' if r['Autor'] == 'Anónimo' else 'blue', icon='trash')
    ).add_to(m)

folium_static(m, width=900)

# ==========================================
# 5. TABELA DE REGISTOS
# ==========================================
st.write("---")
st.subheader("📊 Histórico de Limpeza")
if not st.session_state.db_relatos.empty:
    # Exibe a tabela com as novas colunas de endereço
    st.dataframe(
        st.session_state.db_relatos[['Data', 'Bairro', 'Rua', 'Numero', 'Tipo', 'Autor']], 
        use_container_width=True
    )
else:
    st.info("Nenhuma denúncia registada no momento.")
