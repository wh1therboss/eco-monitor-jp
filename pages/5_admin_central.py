import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Admin Central", layout="wide")
CAMINHO_CSV = 'denuncias.csv'

if 'admin_logado' not in st.session_state:
    st.title("🔑 Painel Administrativo")
    senha = st.text_input("Senha mestra:", type="password")
    if st.button("Entrar"):
        if senha == "09122307":
            st.session_state.admin_logado = True
            st.rerun()
    st.stop()

st.title("📊 Gestão de Ocorrências")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    # Garantir que a coluna Status existe
    if 'Status' not in df.columns:
        df['Status'] = 'Pendente 🟡'
        df.to_csv(CAMINHO_CSV, index=False)

    aba_lixo, aba_iluminacao, aba_gestao = st.tabs(["♻️ Lixo", "💡 Iluminação", "⚙️ Mudar Status"])

    # --- FILTROS PARA AS ABAS ---
    df_luz = df[df['Tipo'].str.contains("Iluminação|Poste|Luz", case=False, na=False)]
    df_lixo = df[~df['Tipo'].str.contains("Iluminação|Poste|Luz", case=False, na=False)]

    with aba_lixo:
        st.dataframe(df_lixo, use_container_width=True)
    
    with aba_iluminacao:
        st.dataframe(df_luz, use_container_width=True)

    with aba_gestao:
        st.subheader("Atualizar Situação da Denúncia")
        # Selecionar denúncia pelo índice ou endereço
        opcao = st.selectbox("Selecione a denúncia para atualizar:", df.index, format_func=lambda x: f"ID {x} - {df.iloc[x]['Endereco']} ({df.iloc[x]['Tipo']})")
        
        novo_status = st.radio("Novo Status:", ["Pendente 🟡", "Em Manutenção 🛠️", "Resolvido ✅"])
        
        if st.button("💾 Salvar Alteração de Status"):
            df.at[opcao, 'Status'] = novo_status
            df.to_csv(CAMINHO_CSV, index=False)
            st.success(f"Status da denúncia {opcao} atualizado para {novo_status}!")
            st.rerun()

else:
    st.info("Aguardando denúncias...")
