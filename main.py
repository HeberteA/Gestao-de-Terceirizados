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
        margin-top: 15px;
        margin-bottom: 0px;
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


settings.load_css()

try:
    df_raw, df_obras_cad, df_servicos_cad, sheet_url = data_manager.get_data()
except ValueError:
    st.error("Erro nos dados: Verifique se o arquivo data_manager.py foi atualizado para retornar 4 valores.")
    st.stop()

hoje = date.today()
df_raw['DIAS'] = df_raw['DATA_AVALIACAO'].apply(lambda x: (hoje - x).days if pd.notna(x) else 999)
df_raw['STATUS'] = df_raw['DIAS'].apply(lambda x: "VENCIDO" if x > 90 else "EM DIA")

with st.sidebar:
    st.image("Lavie.png")
    st.divider()
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

if not df_obras_cad.empty:
    list_obras = sorted(df_obras_cad['OBRA'].astype(str).unique())
else:
    list_obras = []

if not df_servicos_cad.empty:
    list_servs = sorted(df_servicos_cad['SERVICO'].astype(str).unique())
else:
    list_servs = []

if selected == "Gestão":
    st.markdown("""
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-text">GESTÃO DE TERCEIROS</div>
            </div>
        """, unsafe_allow_html=True)
    st.header("", divider="orange")
    with st.container():
        c1, c2 = st.columns(2)
        
        opcoes_obras_filtro = sorted(list(set(list_obras + df_raw['OBRA'].unique().tolist()))) if not df_raw.empty else list_obras
        opcoes_servs_filtro = sorted(list(set(list_servs + df_raw['AREA_SERVICO'].unique().tolist()))) if not df_raw.empty else list_servs
        
        with c1: f_obra = st.multiselect("Filtrar Obra", options=opcoes_obras_filtro)
        with c2: f_serv = st.multiselect("Filtrar Serviço", options=opcoes_servs_filtro)
        
        df_view = df_raw.copy()
        if f_obra:
            df_view = df_view[df_view['OBRA'].isin(f_obra)]
        if f_serv:
            df_view = df_view[df_view['AREA_SERVICO'].isin(f_serv)]
    
    dashboard.render_dashboard(df_raw, df_view, sheet_url, list_obras, list_servs)

elif selected == "Configuracoes":
    st.markdown("""
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-text">CONFIGURAÇÕES</div>
            </div>
        """, unsafe_allow_html=True)
    st.header("", divider="orange")
    tab_obras, tab_servicos, tab_fornec = st.tabs(["Obras", "Serviços", "Fornecedores"])

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
        st.markdown(f"<h5 style='color:#888; margin-bottom: 20px;'>Obras Ativas ({len(df_obras_cad)})</h5>", unsafe_allow_html=True)

        if not df_obras_cad.empty:
            cols = st.columns(4)
            for i, (index, row) in enumerate(df_obras_cad.iterrows()):
                with cols[i % 4]:
                    st.markdown(settings.render_project_card_html(row), unsafe_allow_html=True)
        else:
            st.info("Nenhuma obra cadastrada.")

    with tab_servicos:
        st.markdown(f"<h4 style='color:{settings.TEXT_COLOR}'>Adicionar Novo Serviço</h4>", unsafe_allow_html=True)
        with st.container():
            with st.form("form_servico", clear_on_submit=True):
                c1, c2 = st.columns([3, 1])
                with c1: new_serv = st.text_input("Nome do Serviço")
                with c2: 
                    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                    btn_save_serv = st.form_submit_button("CADASTRAR", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if btn_save_serv:
                    if new_serv:
                        row = pd.DataFrame([{"SERVICO": new_serv.upper().strip()}])
                        df_new_serv = pd.concat([df_servicos_cad, row], ignore_index=True).drop_duplicates()
                        data_manager.save_data(df_new_serv, "CADASTRO_SERVICOS", sheet_url)
                        st.success(f"Serviço {new_serv} adicionado!")
                        st.rerun()

        st.markdown("---")
        st.markdown(f"<h5 style='color:#888;'>Serviços Cadastrados ({len(df_servicos_cad)})</h5>", unsafe_allow_html=True)
        if not df_servicos_cad.empty:
            st.dataframe(df_servicos_cad, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum serviço cadastrado na aba CADASTRO_SERVICOS.")

    with tab_fornec:
        st.markdown(f"<h4 style='color:{settings.TEXT_COLOR}'>Cadastrar Novo Fornecedor</h4>", unsafe_allow_html=True)

        with st.form("form_cadastro_padrao", clear_on_submit=True):
            
            c1, c2, c3 = st.columns(3)
            with c1: fornecedor = st.text_input("Nome do Fornecedor")
            with c2: obra = st.selectbox("Obra", options=list_obras, index=None, placeholder="Selecione a obra...")
            with c3: area_servico = st.selectbox("Área de Serviço", options=list_servs, index=None, placeholder="Selecione a área...")
            
            c4, c5, c6 = st.columns(3)
            with c4: data_avaliacao = st.date_input("Data da Avaliação")
            with c5: contato = st.text_input("Contato / Telefone")
            with c6: cidade = st.text_input("Cidade")

            st.markdown("---")
            st.markdown("<span style='font-size:0.8rem; color:#888'>CRITÉRIOS DE AVALIAÇÃO</span>", unsafe_allow_html=True)

            n1, n2, n3, n4, n5 = st.columns(5)
            with n1: nota_qualidade = st.number_input("Qualidade (0-5)", 0, 5, 0)
            with n2: nota_prazo = st.number_input("Prazo (0-5)", 0, 5, 0)
            with n3: nota_preco = st.number_input("Preço (0-5)", 0, 5, 0)
            with n4: nota_agilidade = st.number_input("Agilidade (0-5)", 0, 5, 0)
            with n5: nps = st.number_input("NPS (0-10)", 0, 10, 0)
        
            observacoes = st.text_area("Observações Gerais", height=80) 
    
            submitted = st.form_submit_button("Adicionar Fornecedor")
    
            if submitted:
                if not obra or not area_servico or not fornecedor:
                    st.warning("Preencha Obra, Área e Fornecedor!")
                else:
                    novo_registro = {
                        "DATA_AVALIACAO": data_avaliacao,
                        "OBRA": str(obra).upper().strip(),           
                        "AREA_SERVICO": str(area_servico).upper().strip(), 
                        "FORNECEDOR": str(fornecedor).upper().strip(),
                        "CONTATO": str(contato).upper().strip(),
                        "CIDADE": str(cidade).upper().strip(),
                        "NOTA_PRECO": nota_preco,
                        "NOTA_PRAZO": nota_prazo,
                        "NOTA_QUALIDADE": nota_qualidade,
                        "NOTA_AGILIDADE": nota_agilidade,
                        "NPS": nps,
                        "OBSERVACOES": str(observacoes).upper().strip() if observacoes else ""
                    }
            
                    row_add = pd.DataFrame([novo_registro])
                    df_final = pd.concat([df_raw, row_add], ignore_index=True)
                    data_manager.save_data(df_final, "AVALIACOES", sheet_url)
                    
                    st.success("Salvo com sucesso!")
                    st.rerun()

        st.markdown("---")
        
        df_unique_vendors = df_raw.drop_duplicates(subset=['FORNECEDOR'])
        
        st.markdown(f"<h5 style='color:#888; margin-bottom: 20px;'>Catálogo de Parceiros ({len(df_unique_vendors)})</h5>", unsafe_allow_html=True)
        
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
