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

# --- ESTILOS CSS REFORZADOS (PARA TABLAS LARGAS) ---
if bin_str:
    st.markdown(f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: repeat;
        background-attachment: fixed;
    }}

    /* --- FORZAR TABLAS COMPLETAS SIN SCROLL --- */
    /* Quitamos el límite de altura de los contenedores de Streamlit */
    [data-testid="stDataFrame"] > div:first-child {{
        height: auto !important;
    }}
    
    [data-testid="stDataFrame"] {{
        width: 100% !important;
        height: auto !important;
    }}

    /* Estilo de las celdas (Celeste transparente) */
    [data-testid="stDataFrame"] td {{
        background-color: rgba(173, 216, 230, 0.7) !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* Estilo de encabezados */
    [data-testid="stDataFrame"] th {{
        background-color: rgba(173, 216, 230, 0.5) !important;
        color: #004aad !important;
    }}

    /* --- ESTILO DE PESTAÑAS (TABS) --- */
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

    /* --- TÍTULOS CON FONDO BLANCO --- */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: #004aad !important;
        padding: 12px 25px !important;
        border-radius: 12px !important;
        display: inline-block !important;
        border-left: 5px solid #004aad !important;
        margin-bottom: 25px !important;
    }}

    /* --- SECCIÓN REDES --- */
    [data-testid="stColumn"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 1px solid #004aad !important;
    }}
    </style>
    ''', unsafe_allow_html=True)

# --- FUNCIONES DE DATOS ---
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

# --- CABECERA ---
st.title("📊 BTS Charts Honduras 🇭🇳")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- PESTAÑAS ---
tab_spot, tab_ytm, tab_apple, tab_deezer, tab_social = st.tabs([
    "🎧 Spotify", "🎵 YouTube Music", "🍎 Apple Music", "🔊 Deezer", "📱 Redes"
])

with tab_spot:
    st.header("🎧 Spotify Charts")
    
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        df_hd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        # Ajustamos el height a 600 o más para que se vea toda la lista sin scroll
        st.dataframe(df_hd, hide_index=True, use_container_width=True, height=600)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.dataframe(df_hw, hide_index=True, use_container_width=True, height=600)

    st.divider()

    st.subheader("Global 🌍")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Top Diario Global**")
        df_gd = get_kworb_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
        st.dataframe(df_gd, hide_index=True, use_container_width=True, height=600)
    with c4:
        st.markdown("**Top Semanal Global**")
        df_gw = get_kworb_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
        st.dataframe(df_gw, hide_index=True, use_container_width=True, height=600)

# El resto de las pestañas (Apple, Deezer) también deberían llevar height=600 
# para que no se corten.

st.markdown('<p style="text-align: center; color: #004aad; margin-top: 50px;">Hecho con amor para ARMY Honduras 💜</p>', unsafe_allow_html=True)
