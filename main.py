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

# Ruta de tu imagen cargada
image_path = 'BTSLOGO.png' 
bin_str = get_base64(image_path)

# --- ESTILOS CSS PERSONALIZADOS ---
if bin_str:
    st.markdown(f'''
    <style>
    /* Fondo de la aplicación */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: repeat;
        background-attachment: fixed;
    }}

    /* --- ESPACIADO Y ESTILO DE PESTAÑAS --- */
    .stTabs {{
        margin-top: 30px !important; /* Espacio arriba de las pestañas */
        margin-bottom: 30px !important; /* Espacio abajo de las pestañas */
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
        font-size: 1.1rem !important;
    }}

    /* --- ESTILO DE TABLAS --- */
    [data-testid="stDataFrame"] {{
        margin-top: 20px !important; /* Espacio arriba de cada tabla */
        margin-bottom: 40px !important; /* Espacio abajo de cada tabla */
    }}

    [data-testid="stDataFrame"] td {{
        background-color: rgba(173, 216, 230, 0.7) !important;
        color: #000000 !important;
        font-weight: bold;
    }}

    [data-testid="stDataFrame"] th {{
        background-color: rgba(173, 216, 230, 0.5) !important;
        color: #004aad !important;
    }}

    /* --- TÍTULOS Y SUBTÍTULOS CON MÁRGENES --- */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: #004aad !important;
        padding: 12px 25px !important;
        border-radius: 12px !important;
        display: inline-block !important;
        border-left: 5px solid #004aad !important;
        font-weight: bold !important;
        margin-bottom: 25px !important; /* ESPACIO DEBAJO DE TÍTULOS */
        margin-top: 15px !important; /* ESPACIO ARRIBA DE TÍTULOS */
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }}

    /* --- SECCIÓN DE REDES SOCIALES --- */
    [data-testid="stVerticalBlock"] [data-testid="stColumn"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        border: 1px solid #004aad !important;
        margin-top: 20px !important;
    }}

    /* Pie de página */
    .stMarkdown p[style*="text-align: center"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: #004aad !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        display: inline-block !important;
        border: 1px solid #004aad !important;
        margin-top: 50px !important;
    }}
    </style>
    ''', unsafe_allow_html=True)

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
st.title("BTS Charts Honduras'BTS_Logo.png'")
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
        st.dataframe(df_hd, hide_index=True, use_container_width=True)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.dataframe(df_hw, hide_index=True, use_container_width=True)

    st.divider()

    st.subheader("Global 🌍")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Top Diario Global**")
        df_gd = get_kworb_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
        st.dataframe(df_gd, hide_index=True, use_container_width=True)
    with c4:
        st.markdown("**Top Semanal Global**")
        df_gw = get_kworb_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
        st.dataframe(df_gw, hide_index=True, use_container_width=True)

with tab_ytm:
    st.header("🎧 YouTube Music Honduras")
    fecha_update_ytm = "8 de abril 2026"
    st.write(f"Última actualización manual: **{fecha_update_ytm}**")
    data_yt_diario = [
        {"Puesto": 57, "Mov": "🟥 -44", "Canción": "Hooligan - BTS"},
        {"Puesto": 72, "Mov": "🟥 -29", "Canción": "2.0 - BTS"}
    ]
    col_manual_d, col_manual_w = st.columns(2)
    with col_manual_d:
        st.subheader("Top diario de canciones")
        df_yt_m_daily = pd.DataFrame(data_yt_diario)
        st.dataframe(df_yt_m_daily, hide_index=True, use_container_width=True)
    with col_manual_w:
        st.subheader("Top semanal de canciones")
        st.info("No hay entradas de BTS en el chart semanal para esta fecha.")

with tab_apple:
    st.header("🍎 Apple Music Charts")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.subheader("Honduras 🇭🇳")
        df_ah = get_simple_chart("https://kworb.net/charts/apple_s/hn.html")
        st.dataframe(df_ah, hide_index=True, use_container_width=True)
    with ca2:
        st.subheader("Global 🌍")
        df_ag = get_simple_chart("https://kworb.net/apple_songs/")
        st.dataframe(df_ag, hide_index=True, use_container_width=True)

with tab_deezer:
    st.header("🔊 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        df_dh = get_simple_chart("https://kworb.net/charts/deezer/hn.html")
        st.dataframe(df_dh, hide_index=True, use_container_width=True)
    with cd2:
        st.subheader("Global 🌍")
        df_dg = get_simple_chart("https://kworb.net/charts/deezer/ww.html")
        st.dataframe(df_dg, hide_index=True, use_container_width=True)

with tab_social:
    left, right = st.columns(2)
    with left:
        st.markdown("### Plataformas de Streaming Oficiales")
        st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
        st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
        st.write("**Spotify Solistas:** [JK](https://open.spotify.com/intl-es/artist/6HaGTQPmzraVmaVxvz6EUc) | [Jimin](https://open.spotify.com/intl-es/artist/1oSPZhvZMIrWW5I41kPkkY) | [V](https://open.spotify.com/artist/3JsHnjpbhX4SnySpvpa9DK) | [RM](https://open.spotify.com/intl-es/artist/2auC28zjQyVTsiZKNgPRGs) | [Jin](https://open.spotify.com/artist/5vV3bFXnN6D6N3Nj4xRvaV) | [Suga](https://open.spotify.com/intl-es/artist/5RmQ8k4l3HZ8JoPb4mNsML) | [j-hope](https://open.spotify.com/artist/0b1sIQumIAsNbqAoIClSpy)")
    with right:
        st.markdown("### Redes Sociales")
        st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
        st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
        st.write("**Instagram Miembros:**")
        st.caption("[RM](https://www.instagram.com/rkive) | [Jin](https://www.instagram.com/jin) | [SUGA](https://www.instagram.com/agustd) | [j-hope](https://www.instagram.com/uarmyhope) | [Jimin](https://www.instagram.com/j.m) | [V](https://www.instagram.com/thv) | [JK](https://www.instagram.com/mnijungkook)")

st.markdown('<p style="text-align: center; color: #004aad; margin-top: 50px;">Hecho con amor para ARMY Honduras 💜</p>', unsafe_allow_html=True)
