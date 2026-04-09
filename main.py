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
    /* Centrar títulos principales */
    .main-title {
        text-align: center;
        color: #7D52B5;
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #9B72CF;
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    h1, h2, h3 {
        color: #7D52B5 !important;
    }
    /* Estilo para los tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA PINTAR TABLAS DE MORADO CLARO ---
def style_df(df):
    if df.empty: return df
    # Color morado muy clarito (#F3E5F5)
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
                rows.append({
                    'Puesto': int(cols[0].text.strip()), 
                    'Mov': icon_mov(cols[1].text.strip()), 
                    'Canción': full_text
                })
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- CABECERA CENTRADA ---
st.markdown('<p class="main-title">💜 BTS Charts Honduras</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Actualizado: {datetime.now().strftime("%d/%m/%Y")}</p>', unsafe_allow_html=True)

# --- SISTEMA DE PESTAÑAS ---
tab_spot, tab_apple, tab_deezer, tab_yt, tab_social = st.tabs([
    "🎧 Spotify", "🍎 Apple Music", "🎵 Deezer", "📺 YouTube", "🔗 Redes"
])

with tab_spot:
    st.header("🌍 Spotify Global vs Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top Diario Global")
        df = get_kworb_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
        st.table(style_df(df)) # Usamos st.table para que el diseño morado sea estático y claro
    with c2:
        st.subheader("Top Semanal Global")
        df = get_kworb_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
        st.table(style_df(df))
    
    st.divider()
    
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Top Diario HN")
        df = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        st.table(style_df(df))
    with c4:
        st.subheader("Top Semanal HN")
        df = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.table(style_df(df))

with tab_apple:
    st.header("🍎 Apple Music Charts")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.subheader("Honduras 🇭🇳")
        df = get_simple_chart("https://kworb.net/charts/apple_s/hn.html")
        st.table(style_df(df))
    with ca2:
        st.subheader("Global 🌍")
        df = get_simple_chart("https://kworb.net/apple_songs/")
        st.table(style_df(df))

with tab_deezer:
    st.header("🎵 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        df = get_simple_chart("https://kworb.net/charts/deezer/hn.html")
        st.table(style_df(df))
    with cd2:
        st.subheader("Global 🌍")
        df = get_simple_chart("https://kworb.net/charts/deezer/ww.html")
        st.table(style_df(df))

with tab_yt:
    st.header("📺 YouTube Charts")
    st.markdown('<div style="background-color: #F8F1FF; padding: 20px; border-radius: 15px; border: 1px solid #7D52B5; text-align: center; color: #4A148C;">YouTube requiere ver los datos directamente en su sitio.</div>', unsafe_allow_html=True)
    cy1, cy2 = st.columns(2)
    with cy1:
        st.link_button("🔥 VER TOP DIARIO HN", "https://charts.youtube.com/charts/TopVideos/hn/daily", use_container_width=True)
    with cy2:
        st.link_button("👑 VER TOP SEMANAL HN", "https://charts.youtube.com/charts/TopVideos/hn/weekly", use_container_width=True)

with tab_social:
    st.header("🔗 Redes Oficiales")
    l, r = st.columns(2)
    with l:
        st.markdown("### 🎧 Música\n- [Spotify](http://googleusercontent.com/spotify.com/9)\n- [Apple](https://music.apple.com/artist/bts/667061285)")
    with r:
        st.markdown("### 📱 Social\n- [Instagram](https://www.instagram.com/bts.bighitofficial)\n- [TikTok](https://www.tiktok.com/@bts_official_bighit)")

st.markdown('<p style="text-align: center; color: #7D52B5; margin-top: 50px;">Hecho con 💜 para ARMY Honduras</p>', unsafe_allow_html=True)
