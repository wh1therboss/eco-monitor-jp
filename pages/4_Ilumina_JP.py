import streamlit as st
import pandas as pd
import os
import uuid
import time
from datetime import datetime

# ... (seu código inicial de colunas e mapa) ...

# 1. Inicializa a variável de protocolo na memória se não existir
if 'protocolo_gerado' not in st.session_state:
    st.session_state.protocolo_gerado = None

with col1:
    st.subheader("📝 Detalhes da Ocorrência")
    
    # Se já existir um protocolo gerado, mostra ele em destaque antes do formulário
    if st.session_state.protocolo_gerado:
        st.success("✅ DENÚNCIA ENVIADA COM SUCESSO!")
        st.markdown(f"""
            <div style="background-color: #f0fff4; padding: 20px; border: 2px solid #2f855a; border-radius: 10px; text-align: center;">
                <p style="margin: 0; color: #2f855a; font-weight: bold;">COPIE SEU PROTOCOLO:</p>
                <h2 style="margin: 10px 0;">{st.session_state.protocolo_gerado}</h2>
                <p style="font-size: 0.8rem; color: #666;">Use este código na página de acompanhamento.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Fazer Nova Denúncia"):
            st.session_state.protocolo_gerado = None
            st.rerun()
            
    else:
        # Só mostra o formulário se não houver um protocolo recém-gerado
        with st.form("form_luz", clear_on_submit=True):
            rua_input = st.text_input("Rua/Avenida:", value=st.session_state.get('luz_endereco', ""))
            
            problema_selecionado = st.selectbox("Selecione o Defeito:", [
                "🚫 Lâmpada Apagada (Noite toda)",
                "🔄 Lâmpada Acesa Durante o Dia",
                "⚠️ Lâmpada Piscando/Oscilando",
                "💥 Poste Quebrado ou Danificado",
                "🔌 Fiação Exposta ou Curto-Circuito",
                "🌳 Árvore Galhando nos Fios",
                "🧱 Braço do Poste Desprendido"
            ])
            
            if st.form_submit_button("🚀 ENVIAR ALERTA"):
                if rua_input:
                    # Gera o protocolo e guarda no session_state para não sumir
                    novo_p = f"LUM-{str(uuid.uuid4()).upper()[:5]}"
                    st.session_state.protocolo_gerado = novo_p
                    
                    # Salva no CSV (Lógica de salvamento)
                    nova_denuncia = {
                        'Protocolo': novo_p,
                        'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                        'Endereço': rua_input,
                        'Problema': problema_selecionado,
                        'Status': '🟡 Pendente'
                    }
                    
                    # Aqui você carrega o seu DF e faz o append
                    if os.path.exists("alertas_iluminacao.csv"):
                        df = pd.read_csv("alertas_iluminacao.csv")
                    else:
                        df = pd.DataFrame(columns=['Protocolo', 'Data', 'Endereço', 'Problema', 'Status'])
                        
                    df = pd.concat([df, pd.DataFrame([nova_denuncia])], ignore_index=True)
                    df.to_csv("alertas_iluminacao.csv", index=False)
                    
                    st.rerun() # Recarrega para mostrar o box verde do protocolo
                else:
                    st.error("Por favor, informe o endereço.")
