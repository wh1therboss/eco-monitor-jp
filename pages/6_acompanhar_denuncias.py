import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Status da Denúncia | LEGO Explorers", page_icon="🕵️")

st.title("🕵️ Acompanhar Minha Denúncia")
st.markdown("Insira o código do seu protocolo para verificar o andamento da solicitação.")

prot_input = st.text_input("Digite seu Protocolo:").upper().strip()

if st.button("Consultar"):
    encontrado = False
    
    # --- 1. BUSCA NAS DENÚNCIAS DE RESÍDUOS (LIXO) ---
    if os.path.exists('denuncias.csv'):
        df_lixo = pd.read_csv('denuncias.csv')
        # Verifica se a coluna Protocolo existe (evita erro se o CSV for antigo)
        if 'Protocolo' in df_lixo.columns:
            res_lixo = df_lixo[df_lixo['Protocolo'] == prot_input]
            if not res_lixo.empty:
                r = res_lixo.iloc[0]
                st.subheader("🗑️ Detalhes da Denúncia de Resíduos")
                st.success(f"**Status Atual:** {r['Status']}")
                st.write(f"📍 **Local:** {r['Endereco']}")
                st.write(f"📝 **Tipo:** {r.get('Tipo', 'Lixo Urbano')}")
                st.write(f"📅 **Data do Registro:** {r['Data']}")
                encontrado = True

    # --- 2. BUSCA NO ILUMINA JP (LUZ) ---
    if not encontrado and os.path.exists('alertas_iluminacao.csv'):
        df_luz = pd.read_csv('alertas_iluminacao.csv')
        # Se você ainda não criou a coluna Protocolo no IluminaJP, 
        # o Admin pode usar o índice ou o nome do autor como busca temporária
        if 'Protocolo' in df_luz.columns:
            res_luz = df_luz[df_luz['Protocolo'] == prot_input]
            if not res_luz.empty:
                r = res_luz.iloc[0]
                st.subheader("💡 Detalhes do Alerta IluminaJP")
                st.success(f"**Status Atual:** {r['Status']}")
                st.write(f"📍 **Local:** {r['Endereço_Completo']}")
                st.write(f"🔦 **Problema:** {r['Problema']}")
                st.write(f"📅 **Data do Registro:** {r['Data']}")
                encontrado = True

    if not encontrado:
        st.error("❌ Protocolo não encontrado. Verifique se o código está correto ou se a denúncia foi enviada.")

# --- DICA PARA O USUÁRIO ---
st.info("""
**Não tem o protocolo?** Os protocolos são gerados no momento do envio da denúncia. 
Caso tenha perdido, você também pode conferir o mapa geral na página de denúncias.
""")
