import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# ... (Mantenha suas funções de carregar_dados e salvar_dados lá em cima)

# --- ABA 1: ADOTAR E ASSINAR (VERSÃO COM CONTRATO PREMIUM) ---
with tab1:
    st.subheader("1. Selecione sua Muda Nativa")
    # Grid de seleção (mantenha o código das colunas que já temos)
    cols = st.columns(5)
    for i, (nome, emoji) in enumerate(especies.items()):
        with cols[i % 5]:
            st.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
            if st.button(f"Selecionar {nome}", key=f"btn_{nome}"):
                st.session_state.esp_sel = nome
                st.session_state.emo_sel = emoji

    if 'esp_sel' in st.session_state:
        st.divider()
        st.subheader("📝 Termo de Compromisso e Tutoria")
        
        with st.form("form_contrato"):
            c1, c2 = st.columns(2)
            with c1:
                tutor = st.text_input("Nome Completo do Tutor:")
                arvore_nome = st.text_input("Nome de Batismo da Árvore:")
            with c2:
                local = st.text_input("Endereço/Localização do Plantio:")
                motivo = st.text_area("Justificativa da Adoção (Sua motivação):")

            # --- O TERMO MELHORADO ---
            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 25px; border-radius: 5px; color: #1e293b; border-left: 10px solid #2f855a; font-family: serif; line-height: 1.6; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <h2 style="text-align: center; color: #2f855a; margin-top: 0;">ESTADO DA PARAÍBA</h2>
                <h3 style="text-align: center; margin-bottom: 20px;">Termo de Responsabilidade Ambiental № {datetime.now().strftime('%y%m%d')}-JP</h3>
                
                <p>Pelo presente instrumento, eu, <b>{tutor if tutor else "____________________"}</b>, doravante denominado(a) <b>TUTOR(A)</b>, 
                assumo perante o projeto <i>LEGO Explorers</i> e a comunidade de João Pessoa o compromisso solene de zelar pela vida e 
                pleno desenvolvimento da árvore batizada como <b>{arvore_nome if arvore_nome else "____________________"}</b>, 
                da espécie <b>{st.session_state.esp_sel}</b>.</p>
                
                <p><b>DAS OBRIGAÇÕES:</b><br>
                1. Promover o fornecimento hídrico adequado e nutrição do solo conforme as necessidades da espécie;<br>
                2. Realizar o monitoramento diário e registro fotográfico para fins de acompanhamento científico e XP;<br>
                3. Proteger a muda contra vandalismo, pragas e resíduos sólidos nas proximidades de suas raízes.</p>
                
                <p><b>DA MISSÃO:</b><br>
                Compreendo que esta árvore é parte vital da recuperação do bioma local, contribuindo para o microclima e a fauna urbana.</p>
                
                <p style="text-align: center; margin-top: 30px; border-top: 1px solid #ccc; padding-top: 10px;">
                    Assinado eletronicamente em {datetime.now().strftime('%d/%m/%Y')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            aceite = st.checkbox("Eu, na qualidade de tutor, aceito integralmente os termos acima e assumo o dever de cuidar desta vida.")
            
            if st.form_submit_button("ASSINAR E REGISTRAR TUTORIA ✒️"):
                if tutor and arvore_nome and local and aceite:
                    # (Mesma lógica de salvar que você já tem)
                    df = carregar_dados()
                    nova = {
                        "Dono": tutor, "Nome_Arvore": arvore_nome, "Especie": st.session_state.esp_sel,
                        "Local": local, "Motivo": motivo, "XP": 0, "Status_Saude": "Excelente", "Ultima_Foto": "Sem registro"
                    }
                    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                    salvar_dados(df)
                    st.balloons()
                    st.success(f"Oficializado! O tutor de {arvore_nome} agora é {tutor}.")
                    del st.session_state.esp_sel
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("⚠️ Para oficializar, preencha todos os campos e aceite o termo.")
