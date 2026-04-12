import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras 🇭🇳", page_icon="BTS_Logo.png", layout="wide")

# --- FUNCIÓN PARA CARGAR IMAGEN DE FONDO ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

image_path = 'BTSLOGO.png' 
bin_str = get_base64(image_path)

# --- ESTILOS CSS REFORZADOS ---
if bin_str:
    st.markdown(f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: repeat;
        background-attachment: fixed;
    }}
    [data-testid="stDataFrame"] td {{
        background-color: rgba(173, 216, 230, 0.7) !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}
    [data-testid="stDataFrame"] th {{
        background-color: rgba(173, 216, 230, 0.5) !important;
        color: #004aad !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 10px !important;
        border-radius: 15px 15px 0px 0px !important;
        border-bottom: 3px solid #004aad !important;
    }}
    .stTabs [data-baseweb="tab-list"] button p {{
        color: #004aad !important;
        font-weight: bold !important;
    }}
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: #004aad !important;
        padding: 12px 25px !important;
        border-radius: 12px !important;
        display: inline-block !important;
        border-left: 5px solid #004aad !important;
        margin-bottom: 25px !important;
    }}
    [data-testid="stColumn"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 1px solid #004aad !important;
    }}
    </style>
    ''', unsafe_allow_html=True)

# --- FUNCIONES DE EXTRACCIÓN DE DATOS ---
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D", "JUNGKOOK"]

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
            if any(member in full_text.upper() for member in solo_bts):
                rows.append({
                    'Puesto': int(cols[0].text.strip()), 'Mov': icon_mov(cols[1].text.strip()),
                    'Canción': full_text, 'Streams': cols[6].text.strip(), 'Evolución': cols[7].text.strip()
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
            if any(member in full_text.upper() for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': icon_mov(cols[1].text.strip()), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- FUNCIÓN NUEVA PARA B-CD.APP ---
def get_apple_bcd_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = []
        tables = soup.find_all('table')
        for table in tables:
            for tr in table.find_all('tr')[1:]:
                text = tr.get_text().upper()
                if any(m in text for m in solo_bts):
                    cols = tr.find_all('td')
                    if len(cols) >= 3:
                        rows.append({
                            'Puesto': cols[0].text.strip().replace("#", ""),
                            'Mov': icon_mov(cols[1].text.strip()),
                            'Canción': cols[2].get_text(separator=" ").strip()
                        })
        return pd.DataFrame(rows).drop_duplicates()
    except: return pd.DataFrame()

# --- CABECERA ---
st.title("📊 BTS Charts Honduras 🇭🇳")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- PESTAÑAS ---
tab_spot, tab_ytm, tab_apple, tab_itunes, tab_deezer, tab_playlist, tab_social = st.tabs([
    "🎧 Spotify", "🎵 YouTube Music", "🍎 Apple Music", "⭐ iTunes", "🔊 Deezer", "🎬 Playlist", "📱 Redes"
])

with tab_spot:
    st.header("🎧 Spotify Charts")
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        st.dataframe(get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily"), hide_index=True, use_container_width=True, height=600)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        st.dataframe(get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly"), hide_index=True, use_container_width=True, height=600)

with tab_ytm:
    st.header("🎵 YouTube Music Honduras")
    st.info("🚧 Sección en mantenimiento: Actualizando fuentes.")

with tab_apple:
    st.header("🍎 Apple Music Charts")
    
    data_apple_global = [
        {"Puesto": 3, "Mov": "➡️ =", "Canción": "SWIM - BTS"},
        {"Puesto": 10, "Mov": "🟩 +1", "Canción": "2.0 - BTS"},
        {"Puesto": 16, "Mov": "🟥 -1", "Canción": "Body to Body - BTS"},
        {"Puesto": 28, "Mov": "🟥 -1", "Canción": "Hooligan - BTS"},
        {"Puesto": 45, "Mov": "🟥 -8", "Canción": "NORMAL - BTS"},
        {"Puesto": 48, "Mov": "🟥 -8", "Canción": "FYA - BTS"},
        {"Puesto": 63, "Mov": "🟥 -9", "Canción": "Aliens - BTS"},
        {"Puesto": 72, "Mov": "🟥 -9", "Canción": "Like Animals - BTS"},
        {"Puesto": 94, "Mov": "🟥 -11", "Canción": "they don’t know ’bout us - BTS"},
        {"Puesto": 98, "Mov": "🟥 -19", "Canción": "Merry Go Round - BTS"}
    ]
    data_apple_manual = [{"Puesto": 84, "Mov": "🟩 +15", "Canción": "BTS - SWIM"}]

    col_ah, col_ag = st.columns(2)
    with col_ah:
        st.subheader("Honduras 🇭🇳")
        if not data_apple_manual: st.info("No hay entradas de BTS hoy.")
        else: st.dataframe(pd.DataFrame(data_apple_manual), hide_index=True, use_container_width=True)
            
    with col_ag:
        st.subheader("Global 🌍")
        st.dataframe(pd.DataFrame(data_apple_global), hide_index=True, use_container_width=True)

with tab_itunes:
    st.header("⭐ iTunes Top Songs")
    st.info("🚧 Sección en proceso de ajuste.")

with tab_deezer:
    st.header("🔊 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        st.dataframe(get_simple_chart("https://kworb.net/charts/deezer/hn.html"), hide_index=True, use_container_width=True)
    with cd2:
        st.subheader("Global 🌍")
        st.dataframe(get_simple_chart("https://kworb.net/charts/deezer/ww.html"), hide_index=True, use_container_width=True)

with tab_playlist:
    st.header("🎬 Generador de Playlists")
    opcion = st.selectbox("Elige una playlist:", ["Top BTS Honduras", "Solistas Focus"])
    links = {"Top BTS Honduras": "https://open.spotify.com/intl-es/artist/1oSPZhvZMIrWW5I41kPkkY3", "Solistas Focus": "https://open.spotify.com/intl-es/artist/1oSPZhvZMIrWW5I41kPkkY3"}
    st.markdown(f'<iframe src="{links[opcion]}" width="100%" height="380" frameborder="0" allow="encrypted-media"></iframe>', unsafe_allow_html=True)

with tab_social:
    st.header("📱 Redes Sociales")
    st.write("Sigue las cuentas oficiales.")

st.markdown('<p style="text-align: center; color: #004aad; margin-top: 50px;">Hecho con amor para ARMY Honduras 💜</p>', unsafe_allow_html=True)
