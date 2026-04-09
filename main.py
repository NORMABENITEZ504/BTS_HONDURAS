import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras 🇭🇳", page_icon="💜", layout="wide")

# --- FUNCIÓN PARA CARGAR IMAGEN DE FONDO ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Asegúrate de que el archivo se llame exactamente BTSLOGO.png en tu carpeta
image_path = 'BTSLOGO.png' 

# --- ESTILOS CSS PERSONALIZADOS (Celeste Transparente) ---
bin_str = get_base64(image_path)
if bin_str:
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: repeat;
        background-attachment: fixed;
    }}

    /* Fondo de las celdas (Celeste 70% transparente) */
    [data-testid="stTable"] td, [data-testid="stDataFrame"] td {{
        background-color: rgba(173, 216, 230, 0.7) !important;
        color: #000000 !important;
    }}

    /* Fondo de encabezados (Celeste 50% transparente) */
    [data-testid="stTable"] th, [data-testid="stDataFrame"] th {{
        background-color: rgba(173, 216, 230, 0.5) !important;
        color: #4A148C !important;
    }}

    h1, h2, h3 {{
        color: #7D52B5 !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# --- FUNCIÓN style_df (ESTA ES LA QUE FALTABA) ---
def style_df(df):
    if df.empty: return df
    return df # El CSS de arriba ya se encarga del resto

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
st.title("💜 BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SISTEMA DE PESTAÑAS ---
tab_spot, tab_ytm, tab_apple, tab_deezer, tab_social = st.tabs([
    "🎧 Spotify", "🎵 YouTube Music", "🍎 Apple Music", "🔊 Deezer", "🔗 Redes"
])

with tab_spot:
    st.header("📊 Spotify Charts")
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        df_hd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        st.dataframe(style_df(df_hd), hide_index=True, use_container_width=True)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.dataframe(style_df(df_hw), hide_index=True, use_container_width=True)

with tab_ytm:
    st.header("🎧 YouTube Music Honduras")
    fecha_update_ytm = "8 de abril 2026"
    data_yt_diario = [
        {"Puesto": 57, "Mov": "🟥 -44", "Canción": "Hooligan - BTS"},
        {"Puesto": 72, "Mov": "🟥 -29", "Canción": "2.0 - BTS"}
    ]
    st.write(f"Última actualización manual: **{fecha_update_ytm}**")
    col_manual_d, col_manual_w = st.columns(2)
    with col_manual_d:
        st.subheader("Top diario de canciones")
        df_yt_m_daily = pd.DataFrame(data_yt_diario)
        st.dataframe(style_df(df_yt_m_daily), hide_index=True, use_container_width=True)
    with col_manual_w:
        st.subheader("Top semanal de canciones")
        st.info("No hay entradas de BTS en el chart semanal para esta fecha.")

with tab_apple:
    st.header("🍎 Apple Music Charts")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.subheader("Honduras 🇭🇳")
        df_ah = get_simple_chart("https://kworb.net/charts/apple_s/hn.html")
        st.dataframe(style_df(df_ah), hide_index=True, use_container_width=True)
    with ca2:
        st.subheader("Global 🌍
