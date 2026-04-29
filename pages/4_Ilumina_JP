import streamlit as st

st.title("🔦 IluminaJP - Monitoramento de Iluminação")
st.write("Mapeamento de áreas escuras para instalação de postes solares.")

st.markdown("---")

area = st.text_input("Digite o nome da rua ou bairro com baixa iluminação:")
nivel_perigo = st.slider("Nível de escuridão (1 a 10):", 1, 10, 5)

if st.button("Reportar Ponto Escuro"):
    st.warning(f"Ponto registrado em {area}. Analisando viabilidade de placa solar...")

st.write("### 📊 Estatísticas de Iluminação")
st.bar_chart({"Pontos Reportados": [12, 45, 30, 10, 55], "Bairros": ["Centro", "Mangabeira", "Valentina", "Bessa", "Cristo"]})
