import streamlit as st
import pandas as pd
from datetime import date
from settings import render_card_html, PRIMARY_COLOR, TEXT_COLOR
from data_manager import save_data 


@st.dialog("Editar Fornecedor")
def edit_dialog(id_fornecedor, dados):
    if not isinstance(dados, dict):
        st.error("Erro interno: Os dados não chegaram corretamente.")
        return
    with st.form("form_editar_completo"):

        try:
            val_data = pd.to_datetime(dados.get("DATA_AVALIACAO"))
        except:
            val_data = None

        col1, col2 = st.columns(2)
        with col1:
            n_qual = st.slider("Qualidade", 0, 5, int(dados.get("NOTA_QUALIDADE", 0)))
            n_praz = st.slider("Prazo", 0, 5, int(dados.get("NOTA_PRAZO", 0)))
        with col2:
            n_prec = st.slider("Preço", 0, 5, int(dados.get("NOTA_PRECO", 0)))
            n_agil = st.slider("Agilidade", 0, 5, int(dados.get("NOTA_AGILIDADE", 0)))
        nps_new = st.slider("NPS", 0, 10, int(dados.get("NPS", 0)))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            data_avaliacao = st.date_input("Data", value=val_data)
            obra = st.text_input("Obra", value=str(dados.get("OBRA", "")))
            area_servico = st.text_input("Área", value=str(dados.get("AREA_SERVICO", "")))
        with c2:
            fornecedor = st.text_input("Fornecedor", value=str(dados.get("FORNECEDOR", "")))
            contato = st.text_input("Contato", value=str(dados.get("CONTATO", "")))
            cidade = st.text_input("Cidade", value=str(dados.get("CIDADE", "")))
        observacoes = st.text_area("Observações", value=str(dados.get("OBSERVACOES", "")))
    
    
        st.markdown('<div class="save-btn">', unsafe_allow_html=True)
        if st.form_submit_button("Atualizar Dados", use_container_width=True):
            novos_dados = {
                    "DATA_AVALIACAO": data_avaliacao,
                    "OBRA": obra,
                    "AREA_SERVICO": area_servico,
                    "FORNECEDOR": fornecedor,
                    "CONTATO": contato,
                    "CIDADE": cidade,
                    "NOTA_PRECO": n_prec,
                    "NOTA_PRAZO": n_praz,
                    "NOTA_QUALIDADE": n_qual,
                    "NOTA_AGILIDADE": n_agil,
                    "NPS": nps_new,
                    "OBSERVACOES": observacoes
                }
        
            st.success("Fornecedor atualizado com sucesso!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard(df_raw, df_view, sheet_url):
    k1, k2, k3, k4 = st.columns(4)
    vencidos = len(df_view[df_view['STATUS'] == 'VENCIDO'])
    
    with k1: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>TOTAL</div><div class='kpi-value'>{len(df_view)}</div></div>", unsafe_allow_html=True)
    with k2: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>VENCIDOS</div><div class='kpi-value' style='color:{'#C62828' if vencidos else TEXT_COLOR}'>{vencidos}</div></div>", unsafe_allow_html=True)
    with k3: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>NPS MÉDIO</div><div class='kpi-value'>{df_view['NPS'].mean():.1f}</div></div>", unsafe_allow_html=True)
    with k4: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>OBRAS</div><div class='kpi-value'>{df_view['OBRA'].nunique()}</div></div>", unsafe_allow_html=True)

    if not df_view.empty:
        df_sorted = df_view.sort_values(by=['STATUS', 'NPS'], ascending=[False, False])
        
        cols = st.columns(3)
        for i, (index, row) in enumerate(df_sorted.iterrows()):
            with cols[i % 3]:
                with st.container():
                    st.markdown(render_card_html(row), unsafe_allow_html=True)
                
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Editar", key=f"bt_{index}", use_container_width=True):
                        edit_dialog(index, row.to_dict())
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhum dado encontrado.")