import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import date

@st.cache_resource
def get_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        else:
            creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Erro de Conexao: {e}")
        st.stop()

def get_data():
    client = get_client()
    url = st.secrets.get("spreadsheet_url", "")
    if not url: st.stop()
    
    sh = client.open_by_url(url)
    ws_aval = sh.worksheet("AVALIACOES")
    ws_obras = sh.worksheet("CADASTRO_OBRAS")
    try:
        ws_servicos = sh.worksheet("CADASTRO_SERVICOS")
        df_servicos = pd.DataFrame(ws_servicos.get_all_records())
    except:
        df_servicos = pd.DataFrame(columns=["SERVICO"])

    df_aval = pd.DataFrame(ws_aval.get_all_records())
    df_obras = pd.DataFrame(ws_obras.get_all_records())
    
    if not df_aval.empty:
        df_aval['DATA_AVALIACAO'] = pd.to_datetime(df_aval['DATA_AVALIACAO'], errors='coerce').dt.date
        cols = ['NOTA_PRECO', 'NOTA_PRAZO', 'NOTA_QUALIDADE', 'NOTA_AGILIDADE', 'NPS']
        for c in cols:
            if c in df_aval.columns:
                df_aval[c] = pd.to_numeric(df_aval[c], errors='coerce').fillna(0)

    return df_aval, df_obras, df_servicos, url

def save_data(df, sheet_name, url): 
    client = get_client()
    ws = client.open_by_url(url).worksheet(sheet_name)
    df_s = df.copy()
    if 'DATA_AVALIACAO' in df_s.columns:
        df_s['DATA_AVALIACAO'] = df_s['DATA_AVALIACAO'].astype(str)
    ws.clear()
    ws.update([df_s.columns.values.tolist()] + df_s.values.tolist())
    st.cache_data.clear()
