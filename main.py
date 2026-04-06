import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

# LISTA DE ARTISTAS (El filtro que ya sabemos que funciona)
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def get_data(url, platform_type):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        # Leemos la tabla directamente
        df = pd.read_html(response.text)[0]
        
        # Filtro: Buscamos en la columna que tiene el nombre (Artist and Title)
        def es_bts(text):
            artist = str(text).split(" - ")[0].upper().strip()
            return any(m == artist for m in solo_bts)

        df_filtered = df[df['Artist and Title'].apply(es_bts)].copy()

        # Seleccionamos columnas según la plataforma
        if platform_type == "spotify_daily":
            res = df_filtered[['Pos', 'P+', 'Artist and Title', 'Streams']].copy()
            res.columns = ['#', 'Mov', 'Canción', 'Streams']
        else:
            # Para Semanal, Apple y Deezer (que no tienen streams o no los ocupamos)
            res = df_filtered[['Pos', 'P+', 'Artist and Title']].copy()
            res.columns = ['#', 'Mov', 'Canción']
            
        return res
    except:
        return pd.DataFrame()

# --- TÍTULO ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN SPOTIFY ---
st.header("📊 Spotify Charts")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spotify: Top Daily Songs")
    df1 = get_data("https://kworb.net/spotify/country/hn_daily.html", "spotify_daily")
    if not df1.empty:
        st.dataframe(df1, hide_index=True, use_container_width=True)
    else:
        st.info("No se encontraron canciones hoy.")

with col2:
    st.subheader("Spotify: Top Weekly Songs")
    df2 = get_data("https://kworb.net/spotify/country/hn_weekly.html", "other")
    if not df2.empty:
        st.dataframe(df2, hide_index=True, use_container_width=True)
    else:
        st.info("No se encontraron canciones esta semana.")

st.divider()

# --- SECCIÓN OTRAS PLATAFORMAS ---
st.header("🎵 Otras Plataformas")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Apple Music: Top Songs")
    df3 = get_data("https://kworb.net/charts/apple_s/hn.html", "other")
    if not df3.empty:
        st.dataframe(df3, hide_index=True, use_container_width=True)
    else:
        st.info("Sin entradas en Apple Music.")

with col4:
    st.subheader("Deezer: Top Songs")
    df4 = get_data("https://kworb.net/charts/deezer/hn.html", "other")
    if not df4.empty:
        st.dataframe(df4, hide_index=True, use_container_width=True)
    else:
        st.info("Sin entradas en Deezer.")

st.divider()
# --- SECCIÓN REDES SOCIALES (2 COLUMNAS) ---
left, right = st.columns(2)

with left:
    st.markdown("### 🎧 Perfiles Oficiales")
    st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
    st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
    st.markdown("- [Apple Music: BTS](https://music.apple.com/artist/bts/667061285)")
    st.markdown("- [Deezer: BTS](https://www.deezer.com/artist/4105021)")
    st.write("**Spotify Solistas:** [JK](https://open.spotify.com/artist/6Ha9SArjAue9uRMQH13T9t) | [Jimin](https://open.spotify.com/artist/1pYpS9vNUn0949YpU66pBy) | [V](https://open.spotify.com/artist/3JsHnS6YvS6vS9z6S6vS9z) | [RM](https://open.spotify.com/artist/2EcnidS8vL936NidS8vL93) | [Jin](https://open.spotify.com/artist/5pYpS9vNUn0949YpU66pBy) | [Suga](https://open.spotify.com/artist/0b1sIQumIAsNbqAoIClSpy) | [j-hope](https://open.spotify.com/artist/)")

with right:
    st.markdown("### 📱 Redes Sociales")
    st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
    st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
    st.markdown("- [TikTok: @bts_official_bighit](https://www.tiktok.com/@bts_official_bighit)")
    st.write("**Instagram Miembros:**")
    st.caption("[RM](https://www.instagram.com/rkive) | [Jin](https://www.instagram.com/jin) | [SUGA](https://www.instagram.com/agustd) | [j-hope](https://www.instagram.com/uarmyhope) | [Jimin](https://www.instagram.com/j.m) | [V](https://www.instagram.com/thv) | [JK](https://www.instagram.com/jungkook_bighitentertainment)")

st.caption("Creado para ARMY Honduras 💜")
