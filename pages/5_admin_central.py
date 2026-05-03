import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Admin Central", layout="wide")
CAMINHO_CSV = 'denuncias.csv'

# --- LOGIN ---
if 'admin_logado' not in st.session_state:
    st.title("🔑 Admin")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "09122307":
            st.session_state.admin_logado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

st.title("📊 Painel de Controle Administrativo")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    # Verificação de segurança para o arquivo antigo
    if 'Protocolo' not in df.columns:
        st.error("⚠️ Arquivo de dados antigo detectado.")
        if st.button("Resetar Banco de Dados"):
            os.remove(CAMINHO_CSV)
            st.rerun()
        st.stop()

    aba1, aba2, aba3 = st.tabs(["♻️ Lixo", "💡 Iluminação", "⚙️ Atualizar Status"])
    
    # Filtros para as abas
    df_luz = df[df['Tipo'].str.contains("Iluminação", na=False)]
    df_lixo = df[~df['Tipo'].str.contains("Iluminação", na=False)]

    with aba1:
        st.subheader("Ocorrências de Lixo")
        st.dataframe(df_lixo, use_container_width=True)
        
    with aba2:
        st.subheader("Ocorrências de Iluminação")
        st.dataframe(df_luz, use_container_width=True)
        
    with aba3:
        st.subheader("Gerenciar Situação")
        
        # --- CORREÇÃO DO ERRO AQUI ---
        # Usamos uma lista de strings formatadas para o selectbox
        lista_opcoes = df['Protocolo'].tolist()
        
        def formatar_exibicao(prot):
            # Busca a linha correspondente ao protocolo
            linha = df[df['Protocolo'] == prot].iloc[0]
            return f"[{prot}] - {linha['Endereco']} ({linha['Tipo']})"

        protocolo_selecionado = st.selectbox(
            "Selecione pelo Protocolo:", 
            options=lista_opcoes, 
            format_func=formatar_exibicao
        )
        
        status_opcoes = ["Pendente 🟡", "Em Manutenção 🛠️", "Resolvido ✅"]
        # Pega o status atual para deixar marcado no radio
        status_atual = df[df['Protocolo'] == protocolo_selecionado]['Status'].values[0]
        try:
            index_status = status_opcoes.index(status_atual)
        except:
            index_status = 0

        novo_status = st.radio("Novo Status:", status_opcoes, index=index_status)
        
        if st.button("💾 Salvar Alteração"):
            # Atualiza usando o Protocolo como referência
            df.loc[df['Protocolo'] == protocolo_selecionado, 'Status'] = novo_status
            df.to_csv(CAMINHO_CSV, index=False)
            st.success(f"Protocolo {protocolo_selecionado} atualizado!")
            st.rerun()

    # Botão de pânico
    st.sidebar.write("---")
    if st.sidebar.button("🗑️ APAGAR TUDO (CUIDADO)"):
        os.remove(CAMINHO_CSV)
        st.rerun()
else:
    st.info("Nenhuma denúncia encontrada.")
