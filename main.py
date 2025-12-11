import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date
import pandas as pd

import settings
import data_manager
import dashboard

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Qualificaçao de Terceirizados", page_icon="Lavie1.png")

st.markdown("""
<style>
    .sidebar-logo-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    .sidebar-logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: white;
        letter-spacing: 2px;
    }
    .sidebar-logo-sub {
        font-size: 0.7rem;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 3px;
    }
</style>
""", unsafe_allow_html=True)

@st.dialog("Cadastrar Novo Fornecedor")
def form_cadastro_fornecedor():
    with st.form("form_novo_fornecedor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data_avaliacao = st.date_input("Data da Avaliação")
            obra = st.text_input("Obra")
            area_servico = st.text_input("Área de Serviço")
        with col2:
            fornecedor = st.text_input("Fornecedor")
            contato = st.text_input("Contato")
            cidade = st.text_input("Cidade")
            
        cl1, cl2 = st.columns(2)
        with cl1:
            nota_preco = st.slider("Nota Preço (0-5)", min_value=0, max_value=5, step=1)
            nota_prazo = st.slider("Nota Prazo (0-5)", min_value=0, max_value=5, step=1)
        with cl2:
            nota_qualidade = st.slider("Nota Qualidade (0-5)", min_value=0, max_value=5, step=1)
            nota_agilidade = st.slider("Nota Agilidade (0-5)", min_value=0, max_value=5, step=1)
            
        nps = st.slider("NPS (0-10)", min_value=0, max_value=10, step=1)
            
        observacoes = st.text_area("Observações")
        
        submitted = st.form_submit_button("Salvar Fornecedor")
        
        if submitted:
            novo_registro = {
                "DATA_AVALIACAO": data_avaliacao,
                "OBRA": obra,
                "AREA_SERVICO": area_servico,
                "FORNECEDOR": fornecedor,
                "CONTATO": contato,
                "CIDADE": cidade,
                "NOTA_PRECO": nota_preco,
                "NOTA_PRAZO": nota_prazo,
                "NOTA_QUALIDADE": nota_qualidade,
                "NOTA_AGILIDADE": nota_agilidade,
                "NPS": nps,
                "OBSERVACOES": observacoes
            }
            
            st.success("Fornecedor cadastrado com sucesso!")
            st.rerun()

settings.load_css()

df_raw, df_obras_cad, sheet_url = data_manager.get_data()

hoje = date.today()
df_raw['DIAS'] = df_raw['DATA_AVALIACAO'].apply(lambda x: (hoje - x).days if pd.notna(x) else 999)
df_raw['STATUS'] = df_raw['DIAS'].apply(lambda x: "VENCIDO" if x > 90 else "EM DIA")

with st.sidebar:
    st.image("Lavie.png")
    st.markdown("""
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-text">QUALIFICAÇÃO</div>
                <div class="sidebar-logo-sub">Terceirizados</div>
            </div>
        """, unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Gestão", "Configuracoes"],
        icons=["grid", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background": "transparent"},
            "nav-link": {"color": "#aaa", "font-size": "0.9rem", "margin":"6px", "text-align": "left"},
            "nav-link-selected": {
                "background-color": "rgba(227, 112, 38, 0.15)", 
                "color": "#E37026", 
                "border-left": "3px solid #E37026"
            },
            "icon": {"font-size": "1.1rem"}
        }
    )

list_obras = sorted(df_obras_cad['OBRA'].astype(str).unique()) if not df_obras_cad.empty else []
list_servs = sorted(df_raw['AREA_SERVICO'].astype(str).unique()) if not df_raw.empty else []

if selected == "Gestão":
    st.markdown("""
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-text">GESTÃO DE TERCEIROS</div>
            </div>
        """, unsafe_allow_html=True)
    with st.container():
        c1, c2 = st.columns(2)
        with c1: f_obra = st.multiselect("Filtrar Obra", list_obras)
        with c2: f_serv = st.multiselect("Filtrar Serviço", list_servs)
        st.markdown("---")
        
        sel_obras = f_obra if f_obra else list_obras
        sel_servs = f_serv if f_serv else list_servs
        df_view = df_raw[(df_raw['OBRA'].isin(sel_obras)) & (df_raw['AREA_SERVICO'].isin(sel_servs))]
    
    dashboard.render_dashboard(df_raw, df_view, sheet_url)

elif selected == "Configuracoes":
    tab_obras, tab_fornec = st.tabs(["GESTÃO DE OBRAS", "GESTÃO DE TERCEIRIZADOS"])

    with tab_obras:
        st.markdown(f"<h4 style='color:{settings.TEXT_COLOR}'>Adicionar Nova Obra</h4>", unsafe_allow_html=True)
        
        with st.container():
            with st.form("form_obra", clear_on_submit=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    new_obra = st.text_input("Nome do Empreendimento")
                with c2: 
                    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                    btn_save_obra = st.form_submit_button("CADASTRAR", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if btn_save_obra:
                    if new_obra:
                        row = pd.DataFrame([{"OBRA": new_obra.upper()}])
                        df_new = pd.concat([df_obras_cad, row], ignore_index=True).drop_duplicates()
                        data_manager.save_data(df_new, sheet_url.replace("AVALIACOES", "CADASTRO_OBRAS"), sheet_url)
                        st.success(f"Obra {new_obra} adicionada!")
                        st.rerun()
                    else:
                        st.warning("Digite o nome da obra.")

        st.markdown("---")
        st.markdown(f"<h5 style='color:#888; margin-bottom: 20px;'>OBRAS ATIVAS ({len(df_obras_cad)})</h5>", unsafe_allow_html=True)

        if not df_obras_cad.empty:
            cols = st.columns(4)
            for i, (index, row) in enumerate(df_obras_cad.iterrows()):
                with cols[i % 4]:
                    st.markdown(settings.render_project_card_html(row), unsafe_allow_html=True)
        else:
            st.info("Nenhuma obra cadastrada.")

    with tab_fornec:
        st.markdown(f"<h4 style='color:{settings.TEXT_COLOR}'>Cadastrar Novo Fornecedor</h4>", unsafe_allow_html=True)
        
        list_obras_form = sorted(df_obras_cad['OBRA'].astype(str).unique()) if not df_obras_cad.empty else []
        list_servs_form = sorted(df_raw['AREA_SERVICO'].astype(str).unique()) if not df_raw.empty else ["Geral"]

        if st.button("Adicionar Fornecedor", use_container_width=True):
            form_cadastro_fornecedor()

        st.markdown("---")
        
        df_unique_vendors = df_raw.drop_duplicates(subset=['FORNECEDOR'])
        
        st.markdown(f"<h5 style='color:#888; margin-bottom: 20px;'>CATÁLOGO DE PARCEIROS ({len(df_unique_vendors)})</h5>", unsafe_allow_html=True)
        
        if not df_unique_vendors.empty:
            cols = st.columns(3)
            for i, (index, row) in enumerate(df_unique_vendors.iterrows()):
                with cols[i % 3]:
                    st.markdown(settings.render_simple_vendor_html(row), unsafe_allow_html=True)
        else:
            st.info("Nenhum fornecedor na base.")

st.markdown("""
            <div style="position: fixed; bottom: 20px; width: 100%; text-align: center; color: #475569; font-size: 0.7rem;">
                Qualificaçao de Terceirizados • Lavie System
            </div>
        """, unsafe_allow_html=True)