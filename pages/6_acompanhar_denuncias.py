import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Consultar Protocolo | LEGO Explorers", layout="wide", page_icon="🕵️")

# --- CABEÇALHO ---
st.title("🕵️ Acompanhar Minha Denúncia")
st.markdown("---")

# Entrada do usuário: Deixa em maiúsculo e remove espaços extras
prot_input = st.text_input("Digite o código do seu Protocolo:", placeholder="Ex: LUM-A1B2C").upper().strip()

if st.button("Consultar Status"):
    if not prot_input:
        st.warning("⚠️ Por favor, insira um número de protocolo.")
    else:
        encontrado = False
        
        # 1. BUSCA NAS DENÚNCIAS DE LIXO (denuncias.csv)
        if os.path.exists('denuncias.csv'):
            df_lixo = pd.read_csv('denuncias.csv')
            if 'Protocolo' in df_lixo.columns:
                res_lixo = df_lixo[df_lixo['Protocolo'] == prot_input]
                if not res_lixo.empty:
                    r = res_lixo.iloc[0]
                    st.subheader("🗑️ Detalhes da Denúncia de Resíduos")
                    
                    # Estilo de Card para o Status
                    status_lixo = r['Status']
                    cor = "green" if "Resolvido" in status_lixo else "orange"
                    st.markdown(f"### Status: <span style='color:{cor};'>{status_lixo}</span>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**📍 Local:** {r.get('Endereco', 'Não informado')}")
                        st.write(f"**📝 Tipo:** {r.get('Tipo', 'Lixo Urbano')}")
                    with col2:
                        st.write(f"**📅 Data:** {r.get('Data', '---')}")
                        st.write(f"**👤 Autor:** {r.get('Autor', 'Anônimo')}")
                    encontrado = True

        # 2. BUSCA NO ILUMINA JP (alertas_iluminacao.csv)
        if not encontrado and os.path.exists('alertas_iluminacao.csv'):
            df_luz = pd.read_csv('alertas_iluminacao.csv')
            if 'Protocolo' in df_luz.columns:
                res_luz = df_luz[df_luz['Protocolo'] == prot_input]
                if not res_luz.empty:
                    r = res_luz.iloc[0]
                    st.subheader("💡 Detalhes do Alerta IluminaJP")
                    
                    status_luz = r['Status']
                    cor = "green" if "Resolvido" in status_luz else "orange"
                    st.markdown(f"### Status: <span style='color:{cor};'>{status_luz}</span>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Tenta pegar 'Endereço' ou 'Endereço_Completo'
                        loc = r.get('Endereço', r.get('Endereço_Completo', 'Local não informado'))
                        st.write(f"**📍 Local:** {loc}")
                        st.write(f"**🔦 Problema:** {r.get('Problema', 'Não especificado')}")
                    with col2:
                        st.write(f"**📅 Data:** {r.get('Data', '---')}")
                        st.write(f"**👤 Autor:** {r.get('Autor', 'Anônimo')}")
                    encontrado = True

        # 3. SE NÃO ACHAR EM NENHUM
        if not encontrado:
            st.error(f"❌ Protocolo **{prot_input}** não encontrado.")
            st.info("Verifique se digitou corretamente ou se a denúncia foi realizada com sucesso.")

# --- BARRA LATERAL ---
st.sidebar.image("hamtaro.webp", width=100)
st.sidebar.write("---")
st.sidebar.caption("LEGO Explorers - João Pessoa")
