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
    /* Color para los encabezados */
    h1, h2, h3 {
        color: #7D52B5 !important;
    }
    /* Estilo para los tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA PINTAR TABLAS DE MORADO CLARO ---
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

# --- CABECERA (Original alineada a la izquierda) ---
st.title("💜 BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SISTEMA DE PESTAÑAS ---
tab_spot, tab_apple, tab_deezer, tab_yt, tab_social = st.tabs([
    "🎧 Spotify", "🍎 Apple Music", "🎵 Deezer", "📺 YouTube", "🔗 Redes"
])

with tab_spot:
    st.header("📊 Spotify Charts")
    
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        df_hd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        st.table(style_df(df_hd))
    with c2:
        st.markdown("**Top Semanal Honduras**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.table(style_df(df_hw))
    
    st.divider()
    
    st.subheader("Global 🌍")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Top Diario Global**")
        df_gd = get_kworb_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
        st.table(style_df(df_gd))
    with c4:
        st.markdown("**Top Semanal Global**")
        df_gw = get_kworb_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
        st.table(style_df(df_gw))

with tab_apple:
    st.header("🍎 Apple Music Charts")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.subheader("Honduras 🇭🇳")
        df_ah = get_simple_chart("https://kworb.net/charts/apple_s/hn.html")
        st.table(style_df(df_ah))
    with ca2:
        st.subheader("Global 🌍")
        df_ag = get_simple_chart("https://kworb.net/apple_songs/")
        st.table(style_df(df_ag))

with tab_deezer:
    st.header("🎵 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        df_dh = get_simple_chart("https://kworb.net/charts/deezer/hn.html")
        st.table(style_df(df_dh))
    with cd2:
        st.subheader("Global 🌍")
        df_dg = get_simple_chart("https://kworb.net/charts/deezer/ww.html")
        st.table(style_df(df_dg))

with tab_yt:
    st.header("📺 YouTube Charts Honduras")
    c_y1, c_y2 = st.columns(2)
    with c_y1:
        st.info("🕒 **Actualización Diaria**")
        st.link_button("🔥 VER TOP DIARIO", "https://charts.youtube.com/charts/TopVideos/hn/daily", use_container_width=True)
    with c_y2:
        st.success("📅 **Resumen Semanal**")
        st.link_button("👑 VER TOP SEMANAL", "https://charts.youtube.com/charts/TopVideos/hn/weekly", use_container_width=True)

with tab_social:
    # --- SECCIÓN REDES SOCIALES ---
    left, right = st.columns(2)

    with left:
        st.markdown("### Perfiles Oficiales")
        st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
        st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
        st.markdown("- [Apple Music: BTS](https://music.apple.com/artist/bts/667061285)")
        st.markdown("- [Deezer: BTS](https://www.deezer.com/artist/4105021)")
        st.write("**Spotify Solistas:** [JK](https://open.spotify.com/intl-es/artist/6HaGTQPmzraVmaVxvz6EUc) | [Jimin](https://open.spotify.com/intl-es/artist/1oSPZhvZMIrWW5I41kPkkY) | [V](https://open.spotify.com/artist/3JsHnjpbhX4SnySpvpa9DK) | [RM](https://open.spotify.com/intl-es/artist/2auC28zjQyVTsiZKNgPRGs) | [Jin](https://open.spotify.com/artist/5vV3bFXnN6D6N3Nj4xRvaV) | [Suga](https://open.spotify.com/intl-es/artist/5RmQ8k4l3HZ8JoPb4mNsML) | [j-hope](https://open.spotify.com/artist/0b1sIQumIAsNbqAoIClSpy)")

    with right:
        st.markdown("### Redes Sociales")
        st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
        st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
        st.markdown("- [TikTok: @bts_official_bighit](https://www.tiktok.com/@bts_official_bighit)")
        st.write("**Instagram Miembros:**")
        st.caption("[RM](https://www.instagram.com/rkive) | [Jin](https://www.instagram.com/jin) | [SUGA](https://www.instagram.com/agustd) | [j-hope](https://www.instagram.com/uarmyhope) | [Jimin](https://www.instagram.com/j.m) | [V](https://www.instagram.com/thv) | [JK](https://www.instagram.com/mnijungkook)")

st.markdown('<p style="text-align: center; color: #7D52B5; margin-top: 50px;">Hecho con 💜 para ARMY Honduras</p>', unsafe_allow_html=True)
