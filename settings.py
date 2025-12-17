import streamlit as st
import pandas as pd

PRIMARY_COLOR = "#E37026"
BG_COLOR = "#F5F5F5"
TEXT_COLOR = "#BEBEBE"
CARD_BG = "#FFFFFF"

def load_css():
    st.markdown(f"""
        <style>
        .stApp {{ background: radial-gradient(circle at 10% 20%, #3b3b3b 0%, #000000 100%); font-family: 'Inter', sans-serif; color: #ffffff;}}
        .block-container {{ padding-top: 1.5rem; }}
        section[data-testid="stSidebar"] {{ background-color: #000000; border-right: 1px solid rgba(255,255,255,0.1);}}
        
        /* KPI CARDS */
        .kpi-card {{
            background-color: transparent; 
            background-image: linear-gradient(160deg, #1e1e1f 0%, #0a0a0c 100%); 
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px; 
            margin-top: 10px; 
            justify-content: space-between; 
            backdrop-filter: blur(10px);
            border-radius: 8px;
            border-left: 5px solid {PRIMARY_COLOR};
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }}
        .kpi-value {{ font-size: 28px; font-weight: 800; color: #ffffff; margin: 0; }}
        .kpi-label {{ font-size: 11px; color: #BEBEBE; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}

        /* VENDOR CONTAINER */
        .vendor-container {{
            background-color: transparent !important; 
            background-image: linear-gradient(160deg, #1e1e1f 0%, #0a0a0c 100%) !important; 
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }}
        .vendor-container:hover {{
            background-color: transparent !important; 
            background-image: linear-gradient(160deg, #1e1e1f 0%, #0a0a0c 100%) !important; 
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 8px 20px rgba(227, 112, 38, 0.1);
            transform: translateY(-2px);
        }}

        /* ELEMENTS INSIDE CARD */
        .vc-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .vc-name {{ font-size: 16px; font-weight: 800; color: #FFFFFF; text-transform: uppercase; margin: 0; }}
        .vc-service {{ background:rgba(227, 112, 38, 0.15); padding:2px 8px; border-radius:4px; font-size:0.7rem; color:#E37026; border:1px solid rgba(227, 112, 38, 0.2); }}
        .vc-obra {{ background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:0.7rem; color:#ccc; border:1px solid rgba(255,255,255,0.3); }}
        .vc-contact {{ background:rgba(255,255,255,0.1); padding:2px 8px; font-size: 11px; color: #ffffff; margin-top: 8px; gap: 5px; border-radius:4px; border:1px solid rgba(255,255,255,0.3);}}

        .badge-ok {{ font-size: 9px; padding: 3px 6px; border-radius: 4px; font-weight: 700; text-transform: uppercase; background:rgba(232, 245, 233, 0.1); color: #2E7D32; border:1px solid rgba(46, 125, 50,0.3);}}
        .badge-bad {{ font-size: 9px; padding: 3px 6px; border-radius: 4px; font-weight: 700; text-transform: uppercase; background:rgba(255, 235, 238, 0.1); color: #C62828; border:1px solid rgba(198, 40, 40, 0.3);}}

        .vc-obs {{ 
            font-size: 10px; 
            color: #999; 
            font-style: italic; 
            background: rgba(255,255,255,0.05); 
            padding: 6px; 
            border-radius: 4px; 
            margin-top: 10px; 
            border-left: 2px solid #555;
            line-height: 1.2;
        }}
        
        /* BARS */
        .metric-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 11px; color: #BEBEBE; }}
        .bar-wrapper {{ display: flex; gap: 3px; }}
        .bar-seg {{ width: 18px; height: 5px; background-color: #EEE; border-radius: 1px; }}
        .filled {{ background-color: {PRIMARY_COLOR}; }}

        /* NPS */
        .nps-box {{ background-color: transparent; background-image: linear-gradient(160deg, #1e1e1f 0%, #0a0a0c 100%);  padding: 8px; border-radius: 6px; margin-top: 10px; }}
        .nps-head {{ display: flex; justify-content: space-between; font-size: 10px; font-weight: 700; margin-bottom: 4px; color: #BEBEBE; }}
        .nps-track {{ width: 100%; height: 5px; background: #EEE; border-radius: 3px; overflow: hidden; }}
        .nps-bar {{ height: 100%; border-radius: 3px; }}

        /* FOOTER */
        .vc-footer {{ display: flex; justify-content: space-between; margin-top: 10px; pt: 8px; border-top: 1px solid #F5F5F5; font-size: 10px; color: #AAA; }}

        /* GENERIC CARD CONTAINER */
        .generic-card {{
            background-color: transparent; 
            background-image: linear-gradient(160deg, #1e1e1f 0%, #0a0a0c 100%); 
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s;
            position: relative;
        }}
        .generic-card:hover {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 8px 20px rgba(227, 112, 38, 0.1);
            transform: translateY(-3px);
        }}

        /* OBRA CARD STYLE */
        .obra-icon {{ font-size: 24px; color: {PRIMARY_COLOR}; margin-bottom: 10px; }}
        .obra-title {{ font-size: 16px; font-weight: 800; color: {PRIMARY_COLOR}; text-transform: uppercase; }}
        .obra-sub {{ font-size: 11px; color: #888; margin-top: 5px; }}

        /* VENDOR SIMPLE CARD STYLE */
        .vs-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
        .vs-avatar {{ width: 30px; height: 30px; background: #FFF3E0; color: {PRIMARY_COLOR}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; }}
        .vs-info {{ display: flex; flex-direction: column; }}
        .vs-name {{ font-size: 14px; font-weight: 700; color: #FFFFFF; }}
        .vs-tag {{ background:rgba(227, 112, 38, 0.15); padding:2px 8px; border-radius:4px; font-size:0.7rem; color:#E37026; border:1px solid rgba(227, 112, 38, 0.2);}}
        .vs-contact {{ font-size: 11px; color: #888; margin-top: 8px; display: flex; align-items: center; gap: 5px; }}

        /* BUTTON OVERRIDE */
        .stButton > button {{
            background-color: transparent;
            color: #FFFFFF;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 0px; 
            height: 35px;
            transition: all 0.2s;
        }}
        .stButton > button:hover {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-color: {PRIMARY_COLOR};
        }}
        
        /* MODAL SAVE BUTTON */
        .save-btn > button {{
            background-color: {PRIMARY_COLOR} !important;
            color: white !important;
            width: 100% !important;
            height: 45px !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def render_bars_html(value):
    val_int = int(round(value))
    html = '<div class="bar-wrapper">'
    for i in range(1, 6):
        cls = "filled" if i <= val_int else ""
        html += f'<div class="bar-seg {cls}"></div>'
    html += '</div>'
    return html

def render_card_html(row):
    status_cls = "badge-bad" if row['STATUS'] == 'VENCIDO' else "badge-ok"
    status_txt = f"VENCIDO ({row['DIAS']}d)" if row['STATUS'] == 'VENCIDO' else "EM DIA"
    contact = row.get('CONTATO', '-')
    
    nps_val = int(row['NPS'])
    nps_pct = min(nps_val * 10, 100)
    nps_c = "#2E7D32" if nps_val >= 9 else "#F9A825" if nps_val >= 7 else "#C62828"
    obs_text = str(row.get('OBSERVACOES', '')).strip()
    if obs_text and obs_text.lower() != "nan":
        display_obs = (obs_text[:80] + '...') if len(obs_text) > 80 else obs_text
        obs_html = f'<div class="vc-obs">"{display_obs}"</div>'
    else:
        obs_html = "" 
        
    return f"""
        <div class="vc-header">
            <div>
                <div class="vc-name">{row['FORNECEDOR']}</div>
                <span class="vc-service">{row['AREA_SERVICO']}</span>
                <span class="vc-obra">{row['OBRA']}</span>
            </div>
            <span class="{status_cls}">{status_txt}</span>
        </div>

        <div style="margin-bottom: 12px;">
            <div class="metric-row"><span>Qualidade</span>{render_bars_html(row['NOTA_QUALIDADE'])}</div>
            <div class="metric-row"><span>Prazo</span>{render_bars_html(row['NOTA_PRAZO'])}</div>
            <div class="metric-row"><span>Preco</span>{render_bars_html(row['NOTA_PRECO'])}</div>
            <div class="metric-row"><span>Agilidade</span>{render_bars_html(row['NOTA_AGILIDADE'])}</div>
        </div>

        <div class="vc-contact">
            <span>{contact}</span>
        </div>

        <div class="nps-box">
            <div class="nps-head">
                <span>NPS</span>
                <span style="color:{nps_c}">{nps_val}/10</span>
            </div>
            <div class="nps-track">
                <div class="nps-bar" style="width:{nps_pct}%; background:{nps_c};"></div>
            </div>
        </div>

        <div class="vc-footer">
            <span>Ref: {row['DATA_AVALIACAO'].strftime('%d/%m/%Y')}</span>
        </div>
    """

def render_project_card_html(row):
    return f"""
    <div class="generic-card">
        <div class="obra-title">{row['OBRA']}</div>
        <div class="obra-sub">Status: Ativo</div>
    </div>
    """

def render_simple_vendor_html(row):
    initials = row['FORNECEDOR'][:2].upper() if row['FORNECEDOR'] else "??"
    contact = row.get('CONTATO', '-')
    if pd.isna(contact) or contact == "": contact = "Sem contato"
    
    return f"""
    <div class="generic-card">
        <div class="vs-header">
            <div class="vs-avatar">{initials}</div>
            <div class="vs-info">
                <div class="vs-name">{row['FORNECEDOR']}</div>
                <div class="vs-tag">{row['AREA_SERVICO']}</div>
            </div>
        </div>
        <div class="vs-contact">
            <span>{contact}</span>
        </div>
    </div>
    """
