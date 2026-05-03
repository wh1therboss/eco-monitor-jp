import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os
import uuid  # Para gerar o protocolo
from geopy.geocoders import Nominatim

# ... (Configurações iniciais e carregar_dados_luz permanecem as mesmas)

def carregar_dados_luz():
    if os.path.exists("alertas_iluminacao.csv"):
        return pd.read_csv("alertas_iluminacao.csv")
    return pd.DataFrame(columns=['Protocolo', 'Data', 'Endereço_Completo', 'Problema', 'Autor', 'lat', 'lon', 'Status'])

# --- FORMULÁRIO ---
with st.form("form_iluminacao", clear_on_submit=True):
    # ... (campos de rua, problema, etc)
    
    if st.form_submit_button("🚀 ENVIAR ALERTA"):
        if st.session_state.luz_endereco != "":
            # GERAÇÃO DO PROTOCOLO ÚNICO
            prefixo = "LUM" # Prefixo para diferenciar de Lixo
            num_random = str(uuid.uuid4()).upper()[:5]
            protocolo_final = f"{prefixo}-{num_random}"
            
            novo_alerta = {
                'Protocolo': protocolo_final,
                'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Endereço_Completo': st.session_state.luz_endereco,
                'Problema': problema,
                'Autor': st.session_state.get('usuario_atual', 'Explorador'),
                'lat': st.session_state.luz_lat,
                'lon': st.session_state.luz_lon,
                'Status': '🟡 Pendente'
            }
            
            df = carregar_dados_luz()
            df = pd.concat([df, pd.DataFrame([novo_alerta])], ignore_index=True)
            df.to_csv("alertas_iluminacao.csv", index=False)
            
            st.success(f"✅ Alerta Enviado! ANOTE SEU PROTOCOLO: **{protocolo_final}**")
            st.session_state.luz_endereco = ""
            st.rerun()
