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

# --- ESTILOS CSS ---
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
    h1, h2, h3 {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: #004aad !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
    }}
    </style>
    ''', unsafe_allow_html=True)

# --- LISTA DE ARTISTAS ---
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def icon_mov(val):
    val = str(val).strip()
    if val == "=" or val == "0" or val == "": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

# --- FUNCIÓN DE ITUNES MEJORADA ---
def get_itunes_data(url):
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
            
            # Obtenemos todo el texto de la celda de la canción/artista
            full_text = cols[2].get_text(" ").strip()
            text_upper = full_text.upper()
            
            # Verificamos si alguno de nuestros artistas está en ese texto
            if any(member in text_upper for member in solo_bts):
                rows.append({
                    'Puesto': cols[0].text.strip(), 
                    'Mov': icon_mov(cols[1].text.strip()), 
                    'Canción': full_text
                })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame()

# (Las demás funciones get_kworb_data y get_simple_chart se mantienen igual)
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
            full_text = cols[2].get_text(" ").strip()
            if any(member in full_text.upper() for member in solo_bts):
                rows.append({
                    'Puesto': cols[0].text.strip(), 'Mov': icon_mov(cols[1].text.strip()),
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
            full_text = cols[2].get_text(" ").strip()
            if any(member in full_text.upper() for member in solo_bts):
                rows.append({'Puesto': cols[0].text.strip(), 'Mov': icon_mov(cols[1].text.strip()), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- INTERFAZ ---
st.title("📊 BTS Charts Honduras 🇭🇳")

tabs = st.tabs(["🎧 Spotify", "🎵 YouTube Music", "🍎 Apple Music", "⭐ iTunes", "🔊 Deezer", "📱 Redes"])

with tabs[0]: # Spotify
    st.header("🎧 Spotify Charts")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        st.dataframe(get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily"), hide_index=True, use_container_width=True, height=600)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        st.dataframe(get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly"), hide_index=True, use_container_width=True, height=600)

with tabs[1]: # YouTube
    st.header("🎵 YouTube Music")
    st.info("Actualizando datos...")

with tabs[2]: # Apple
    st.header("🍎 Apple Music")
    st.dataframe(get_simple_chart("https://kworb.net/charts/apple_s/hn.html"), hide_index=True, use_container_width=True, height=600)

with tabs[3]: # iTunes
    st.header("⭐ iTunes Honduras")
    df_itunes = get_itunes_data("https://kworb.net/charts/itunes/hn.html")
    if df_itunes.empty:
        st.warning("No se detectan entradas de BTS/Solistas en el Top actual de iTunes Honduras.")
    else:
        st.dataframe(df_itunes, hide_index=True, use_container_width=True, height=600)

with tabs[4]: # Deezer
    st.header("🔊 Deezer")
    st.dataframe(get_simple_chart("https://kworb.net/charts/deezer/hn.html"), hide_index=True, use_container_width=True, height=600)

with tabs[5]: # Redes
    st.header("📱 Redes Sociales")
    st.write("Sigue a BTS en sus cuentas oficiales.")
