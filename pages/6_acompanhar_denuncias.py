import streamlit as st
import pandas as pd
import os

st.title("🕵️ Acompanhar Status")
prot = st.text_input("Protocolo:").upper().strip()

if st.button("Consultar") and os.path.exists('alertas_iluminacao.csv'):
    df = pd.read_csv('alertas_iluminacao.csv')
    res = df[df['Protocolo'] == prot]
    
    if not res.empty:
        r = res.iloc[0]
        st.success(f"Status: {r['Status']}")
        # CORREÇÃO: Usa .get para não dar erro se o nome da coluna mudar
        local = r.get('Endereço', r.get('Endereço_Completo', 'Não informado'))
        st.write(f"📍 **Local:** {local}")
    else:
        st.error("Protocolo não encontrado.")
