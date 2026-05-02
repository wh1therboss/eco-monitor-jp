import streamlit as st
import pandas as pd
import os

st.title("🕵️ Acompanhar Minha Denúncia")
prot_input = st.text_input("Digite seu Protocolo:").upper().strip()

if st.button("Consultar") and os.path.exists('denuncias.csv'):
    df = pd.read_csv('denuncias.csv')
    res = df[df['Protocolo'] == prot_input]
    if not res.empty:
        st.success(f"Status: {res.iloc[0]['Status']}")
        st.write(f"**Local:** {res.iloc[0]['Endereco']}")
        st.write(f"**Tipo:** {res.iloc[0]['Tipo']}")
    else: st.error("Protocolo não encontrado.")
