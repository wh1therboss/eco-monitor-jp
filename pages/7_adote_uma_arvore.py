import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Adote uma Árvore | BIOGLOW", layout="wide")

# Inicializa o banco de dados se não existir
if not os.path.exists('arvores_adotadas.csv'):
    pd.DataFrame(columns=["Dono", "Nome_Arvore", "Especie", "Local", "Status", "Ultima_Foto"]).to_csv('arvores_adotadas.csv', index=False)

# Menu Superior (Repetir em todas as páginas para manter o estilo)
st.markdown("""
    <style> [data-testid="stSidebar"] { display: none; } </style>
    <div style="display: flex; justify-content: center; background-color: #111; padding: 15px; border-radius: 10px; gap: 20px; margin-bottom: 20px;">
        <a style="color: white; text-decoration: none; font-weight: bold;" href="/" target="_self">🏠 INÍCIO</a>
        <a style="color: white; text-decoration: none; font-weight: bold;" href="/adote_uma_arvore" target="_self">🌳 ADOTAR</a>
        <a style="color: white; text-decoration: none; font-weight: bold;" href="/Ilumina_JP" target="_self">💡 ILUMINA JP</a>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📜 Termo de Tutoria", "🏡 Meu Jardim"])

with tab1:
    st.header("Assine o Termo de Adoção")
    with st.form("form_adocao"):
        nome = st.text_input("Seu Nome:")
        arvore = st.text_input("Nome da Árvore:")
        especie = st.selectbox("Espécie:", ["Ipê", "Pau-Brasil", "Cajueiro"])
        
        # O Termo de Compromisso
        st.info(f"Eu, {nome if nome else '...'}, assumo o compromisso de cuidar da {arvore if arvore else 'minha árvore'}...")
        
        if st.form_submit_button("ASSINAR E ADOTAR"):
            # Lógica de salvar aqui
            st.success("Parabéns! Você agora é um tutor ambiental.")

with tab2:
    st.subheader("Suas Árvores")
    df = pd.read_csv('arvores_adotadas.csv')
    if df.empty:
        st.info("Você ainda não adotou nenhuma árvore.")
    else:
        st.dataframe(df)
