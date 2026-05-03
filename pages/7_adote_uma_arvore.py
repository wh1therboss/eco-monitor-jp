import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="Adote uma Árvore | Biomas JP", layout="wide", page_icon="🌳")

# Criar pasta para fotos se não existir
if not os.path.exists("fotos_arvores"):
    os.makedirs("fotos_arvores")

CAMINHO_ARVORES = 'arvores_adotadas.csv'

def carregar_dados():
    if os.path.exists(CAMINHO_ARVORES):
        df = pd.read_csv(CAMINHO_ARVORES)
        # SEGURANÇA: Se a coluna nova não existir no arquivo antigo, a gente adiciona agora
        if "Ultima_Foto" not in df.columns:
            df["Ultima_Foto"] = "Sem registro"
        return df
    return pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "Motivo", "XP", "Status_Saude", "Ultima_Foto"])

def salvar_dados(df):
    df.to_csv(CAMINHO_ARVORES, index=False)

st.title("🌳 Sistema de Tutoria Ambiental")

tab1, tab2 = st.tabs(["📜 Adotar e Assinar", "🏡 Meu Jardim"])

# --- TAB 1: ADOÇÃO ---
with tab1:
    # ... (Seu código de seleção de espécies e contrato aqui)
    # Certifique-se de que no dicionário 'nova' ao salvar, inclua: "Ultima_Foto": "Sem registro"
    st.info("Selecione uma muda acima para formalizar o contrato.")
    if 'esp_sel' in st.session_state:
        # (Código do formulário e contrato que já fizemos antes)
        pass

# --- TAB 2: JARDIM E CÂMERA SOB DEMANDA ---
with tab2:
    df = carregar_dados()
    if df.empty:
        st.info("Nenhuma árvore no seu jardim ainda.")
    else:
        selecionada = st.selectbox("Selecione sua árvore:", df['Nome_Arvore'].tolist())
        idx = df[df['Nome_Arvore'] == selecionada].index[0]
        d = df.loc[idx]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Registro Diário")
            
            # LÓGICA DA CÂMERA: Só aparece se o usuário clicar no botão
            if "ativar_camera" not in st.session_state:
                st.session_state.ativar_camera = False

            if not st.session_state.ativar_camera:
                if st.button("📷 Abrir Câmera para Registro"):
                    st.session_state.ativar_camera = True
                    st.rerun()
            else:
                foto_tirada = st.camera_input("Foque na sua árvore e dispare!")
                if foto_tirada:
                    nome_f = f"fotos_arvores/{selecionada}_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
                    with open(nome_f, "wb") as f:
                        f.write(foto_tirada.getbuffer())
                    
                    df.loc[idx, 'Ultima_Foto'] = nome_f
                    df.loc[idx, 'XP'] += 50
                    salvar_dados(df)
                    st.success("Foto salva! +50 XP")
                    st.session_state.ativar_camera = False # Fecha a câmera após bater a foto
                    time.sleep(1)
                    st.rerun()
                
                if st.button("❌ Cancelar"):
                    st.session_state.ativar_camera = False
                    st.rerun()

        with col2:
            st.subheader("📊 Evolução")
            # Verifica se tem foto e se o arquivo realmente existe no PC
            foto_path = str(d['Ultima_Foto'])
            if foto_path != "Sem registro" and foto_path != "nan" and os.path.exists(foto_path):
                st.image(foto_path, caption=f"Última atualização de {d['Nome_Arvore']}", use_container_width=True)
            else:
                st.warning("Nenhuma foto registrada ainda. Use a câmera ao lado!")
            
            st.metric("XP Acumulado", d['XP'])
            st.write(f"🩺 **Saúde:** {d['Status_Saude']}")

st.sidebar.image("hamtaro.webp", width=100)
# Botão de reset para limpar erros de colunas antigas
if st.sidebar.button("🗑️ Resetar Tudo (Limpa Erros)"):
    if os.path.exists(CAMINHO_ARVORES): os.remove(CAMINHO_ARVORES)
    st.rerun()
