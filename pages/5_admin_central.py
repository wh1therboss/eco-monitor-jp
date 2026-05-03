import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Painel Administrativo | EcoColeta", layout="wide", page_icon="⚖️")

# Estilização CSS para o Dashboard
st.markdown("""
    <style>
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #1e293b; color: white; }
    .status-badge { padding: 5px 10px; border-radius: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

CAMINHO_CSV = 'denuncias.csv'

# --- SISTEMA DE LOGIN ---
if 'admin_logado' not in st.session_state:
    st.title("🔐 Acesso Restrito")
    with st.container():
        senha = st.text_input("Insira a senha mestra:", type="password")
        if st.button("Acessar Sistema"):
            if senha == "09122307":
                st.session_state.admin_logado = True
                st.rerun()
            else:
                st.error("Credenciais inválidas.")
    st.stop()

# --- CARREGAMENTO DE DADOS ---
st.title("📊 Dashboard Administrativo - LEGO Explorers")

if os.path.exists(CAMINHO_CSV):
    df = pd.read_csv(CAMINHO_CSV)
    
    # 1. MÉTRICAS NO TOPO
    total = len(df)
    pendentes = len(df[df['Status'].str.contains("Pendente", na=False)])
    resolvidos = len(df[df['Status'].str.contains("Resolvido", na=False)])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total de Ocorrências", total)
    m2.metric("Pendentes", pendentes, delta=f"{pendentes} aguardando", delta_color="inverse")
    m3.metric("Resolvidos", resolvidos, delta=f"{resolvidos} finalizados")
    m4.metric("Eficiência", f"{(resolvidos/total*100 if total > 0 else 0):.1f}%")

    st.write("---")

    # 2. ABAS DE GESTÃO
    aba_mapa, aba_dados, aba_acoes = st.tabs(["🗺️ Mapa de Calor", "📋 Lista Completa", "⚙️ Gestão de Status"])

    with aba_mapa:
        st.subheader("📍 Distribuição Geográfica de Problemas")
        # Centralizado em João Pessoa
        m_admin = folium.Map(location=[-7.1153, -34.8611], zoom_start=13, tiles="cartodbpositron")
        
        for _, row in df.iterrows():
            cor = "red" if "Pendente" in row['Status'] else "blue" if "Manutenção" in row['Status'] else "green"
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=f"<b>Prot:</b> {row['Protocolo']}<br><b>Tipo:</b> {row['Tipo']}<br><b>Status:</b> {row['Status']}",
                icon=folium.Icon(color=cor, icon='info-sign')
            ).add_to(m_admin)
        
        st_folium(m_admin, width="100%", height=500)

    with aba_dados:
        st.subheader("🗂️ Banco de Dados Interativo")
        # Data Editor permite filtrar e ordenar clicando nas colunas
        st.data_editor(
            df.iloc[::-1], 
            use_container_width=True, 
            disabled=True, # Apenas visualização aqui
            column_config={
                "Status": st.column_config.TextColumn("Situação", help="Status atual da denúncia"),
                "Lat": None, "Lon": None # Esconde coordenadas chatas
            }
        )

    with aba_acoes:
        st.subheader("🛠️ Atualizar Situação")
        col_sel, col_stat = st.columns([2, 1])
        
        with col_sel:
            prot_list = df['Protocolo'].unique().tolist()
            selecionado = st.selectbox("Escolha um Protocolo para atualizar:", prot_list)
            
            # Mostra detalhes da denúncia selecionada antes de mudar
            detalhe = df[df['Protocolo'] == selecionado].iloc[0]
            st.info(f"**Tipo:** {detalhe['Tipo']} | **Local:** {detalhe['Endereco']}\n\n**Descrição:** {detalhe['Descricao']}")

        with col_stat:
            novo_status = st.select_slider(
                "Mudar Status para:",
                options=["Pendente 🟡", "Em Manutenção 🛠️", "Resolvido ✅"]
            )
            if st.button("Confirmar Atualização"):
                df.loc[df['Protocolo'] == selecionado, 'Status'] = novo_status
                df.to_csv(CAMINHO_CSV, index=False)
                st.success(f"Protocolo {selecionado} atualizado com sucesso!")
                st.rerun()

    # SIDEBAR CONFIGS
    st.sidebar.image("hamtaro.webp", width=100)
    st.sidebar.divider()
    if st.sidebar.button("🚪 Sair do Sistema"):
        del st.session_state.admin_logado
        st.rerun()
        
    if st.sidebar.checkbox("⚠️ Modo de Limpeza"):
        if st.sidebar.button("APAGAR TODAS AS DENÚNCIAS"):
            os.remove(CAMINHO_CSV)
            st.rerun()

else:
    st.info("Nenhum dado encontrado. As denúncias aparecerão aqui assim que forem enviadas.")
