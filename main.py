import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras 🇭🇳", page_icon="💜", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Título principal alineado a la IZQUIERDA y MUCHO más grande */
    .main-title {
        text-align: left;
        color: #7D52B5;
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 5.5rem; /* Tamaño extra grande solicitado */
        font-weight: bold;
        margin-top: -50px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: left;
        color: #9B72CF;
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 2rem;
        margin-bottom: 40px;
    }
    h1, h2, h3 {
        color: #7D52B5 !important;
    }
    /* Estilo para los tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.3rem;
        font-weight: bold;
    }
    /* Estilo de tablas moraditas claro */
    .stTable {
        background-color: #F8F1FF;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA PINTAR TABLAS ---
def style_df(df):
    if df.empty: return df
    return df.style.set_properties(**{
        'background-color': '#F8F1FF',
        'color': '#4A148C',
        'border-color': '#E1BEE7'
    })

# --- VARIABLES Y FUNCIONES DE DATOS ---
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def icon_mov(val):
    val = str(val).strip()
    if val == "=" or val == "0" or val == "": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

def get_kworb_data(url, table_id):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': table_id})
        if not table: return pd.DataFrame()
        rows = []
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 8: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': icon_mov(cols[1].text.strip()),
                    'Canción': full_text,
                    'Streams': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                })
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

def get_simple_chart(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table: return pd.DataFrame()
        rows = []
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': icon_mov(cols[1].text.strip()), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- CABECERA ---
st.markdown('<p class="main-title">💜 BTS Charts Honduras</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Actualizado: {datetime.now().strftime("%d/%m/%Y")}</p>', unsafe_allow_html=True)

# --- SISTEMA DE PESTAÑAS ---
tab_spot, tab_apple, tab_deezer, tab_yt, tab_social = st.tabs([
    "🎧 Spotify", "🍎 Apple Music", "🎵 Deezer", "📺 YouTube", "🔗 Redes"
])

with tab_spot:
    st.header("📊 Spotify Charts")
    
    # HONDURAS PRIMERO
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        df_
