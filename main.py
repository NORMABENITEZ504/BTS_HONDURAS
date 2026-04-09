import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras 🇭🇳", page_icon="💜", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS (Color ARMY) ---
st.markdown("""
    <style>
    /* Color de títulos y acentos */
    h1, h2, h3 {
        color: #7D52B5 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }
    /* Estilo de las tarjetas de métricas */
    div[data-testid="stMetricValue"] {
        color: #7D52B5;
    }
    /* Líneas divisorias moradas */
    hr {
        border-top: 2px solid #7D52B5;
    }
    /* Bordes de tablas y contenedores */
    .stDataFrame {
        border: 1px solid #7D52B5;
        border-radius: 10px;
    }
    /* Estilo para los tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VARIABLES Y FUNCIONES ---
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def icon_mov(val):
    val = str(val).strip()
    if val == "=" or val == "0" or val == "": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

def get_kworb_data(url, table_id, is_global=False):
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
                data = {
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': icon_mov(cols[1].text.strip()),
                    'Canción': full_text,
                    'Streams': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                }
                rows.append(data)
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
st.write(f"📊 **Reporte consolidado** | Actualizado: {datetime.now().strftime('%d/%m/%Y')}")

# --- SISTEMA DE PESTAÑAS (ORGANIZACIÓN TOP) ---
tab_spot, tab_apple, tab_deezer, tab_yt, tab_social = st.tabs([
    "🎧 Spotify", "🍎 Apple Music", "🎵 Deezer", "📺 YouTube", "🔗 Redes"
])

with tab_spot:
    st.header("🌍 Spotify Global vs Honduras 🇭🇳")
    
    # Global
    st.subheader("Spotify Global")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Global**")
        df_gd = get_kworb_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
        st.dataframe(df_gd, hide_index=True, use_container_width=True)
    with c2:
        st.markdown("**Top Semanal Global**")
        df_gw = get_kworb_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
        st.dataframe(df_gw, hide_index=True, use_container_width=True)
    
    st.divider()
    
    # Honduras
    st.subheader("Spotify Honduras")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Top Diario HN**")
        df_hd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        st.dataframe(df_hd, hide_index=True, use_container_width=True)
    with c4:
        st.markdown("**Top Semanal HN**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.dataframe(df_hw, hide_index=True, use_container_width=True)

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
    st.header("🎵 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        df_dh = get_simple_chart("https://kworb.net/charts/deezer/hn.html")
        st.dataframe(df_dh, hide_index=True, use_container_width=True)
    with cd2:
        st.subheader("Global 🌍")
        df_dg = get_simple_chart("https://kworb.net/charts/deezer/ww.html")
        st.dataframe(df_dg, hide_index=True, use_container_width=True)

with tab_yt:
    st.header("📺 YouTube Charts")
    st.markdown("""
        <div style="background-color: #F3E5F5; padding: 20px; border-radius: 15px; border-left: 5px solid #7D52B5; margin-bottom: 20px;">
            <p style="color: #4A148C; margin: 0;"><b>Nota de Streaming:</b> YouTube bloquea la visualización directa. Haz clic abajo para apoyar oficialmente desde la fuente.</p>
        </div>
    """, unsafe_allow_html=True)
    cy1, cy2 = st.columns(2)
    with cy1:
        st.info("🕒 Actualización Diaria")
        st.link_button("🔥 VER TOP DIARIO HN", "https://charts.youtube.com/charts/TopVideos/hn/daily", use_container_width=True)
    with cy2:
        st.success("📅 Resumen Semanal")
        st.link_button("👑 VER TOP SEMANAL HN", "https://charts.youtube.com/charts/TopVideos/hn/weekly", use_container_width=True)

with tab_social:
    st.header("🔗 Conecta con BTS")
    left, right = st.columns(2)
    with left:
        st.markdown("### 🎧 Perfiles de Música")
        st.markdown("- [Spotify](https://open.spotify.com/artist/3Nrfpe0tUOSuS7O4ST6URG) | [BANGTANTV](https://www.youtube.com/@BANGTANTV)")
        st.markdown("- [Apple Music](https://music.apple.com/artist/bts/667061285) | [Deezer](https://www.deezer.com/artist/4105021)")
        st.write("**Solistas en Spotify:**")
        st.caption("JK | Jimin | V | RM | Jin | Suga | j-hope")
    with right:
        st.markdown("### 📱 Redes Oficiales")
        st.markdown("- [Instagram](https://www.instagram.com/bts.bighitofficial) | [TikTok](https://www.tiktok.com/@bts_official_bighit)")
        st.markdown("- [X (Twitter)](https://x.com/bts_bighit)")
        st.write("**Instagram Miembros:**")
        st.caption("rkive | jin | agustd | uarmyhope | j.m | thv | mnijungkook")

st.divider()
st.caption("Hecho con 💜 para ARMY Honduras")
