import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

def get_kworb_data(url):
    # Headers para que Kworb nos deje pasar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        # Leemos todas las tablas de la página
        tables = pd.read_html(response.text)
        if not tables:
            return pd.DataFrame()
            
        # Seleccionamos la tabla más grande (la que tiene los datos del chart)
        df = max(tables, key=len)
        
        # Lista de artistas para el filtro
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        
        # Identificar columnas por contenido (más seguro que por nombre)
        # 1. Buscamos la columna que tiene el " - " (Artista - Canción)
        col_title = None
        for col in df.columns:
            if df[col].astype(str).str.contains(" - ").any():
                col_title = col
                break
        
        if col_title is None: return pd.DataFrame()

        # 2. Identificar Puesto (Pos) y Movimiento (P+ o Chg)
        col_pos = df.columns[0] # Normalmente es la primera
        col_mov = df.columns[1] # Normalmente es la segunda

        # Filtrado estricto
        def filter_bts(text):
            artist = str(text).split(" - ")[0].upper().strip()
            return any(member == artist for member in solo_bts)

        df_filtered = df[df[col_title].apply(filter_bts)].copy()
        
        # Seleccionar columnas finales
        res = df_filtered[[col_pos, col_mov, col_title]].copy()
        res.columns = ['#', 'Mov', 'Canción']
        
        # Si es Spotify diario, intentamos traer los Streams
        if 'Streams' in df.columns:
            res['Streams'] = df_filtered['Streams']
            
        return res
    except:
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- BLOQUE SPOTIFY ---
st.header("📊 Spotify Charts")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spotify: Top Daily Songs")
    data_daily = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html")
    if not data_daily.empty:
        st.dataframe(data_daily, hide_index=True, use_container_width=True)
    else:
        st.info("Sin canciones de BTS en el Top 200 Diario.")

with col2:
    st.subheader("Spotify: Top Weekly Songs")
    data_weekly = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html")
    if not data_weekly.empty:
        st.dataframe(data_weekly, hide_index=True, use_container_width=True)
    else:
        st.info("Sin canciones de BTS en el Top Semanal.")

st.divider()

# --- BLOQUE OTRAS PLATAFORMAS ---
st.header("🎵 Otras Plataformas")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Apple Music: Top Songs")
    data_apple = get_kworb_data("https://kworb.net/charts/apple_s/hn.html")
    if not data_apple.empty:
        st.dataframe(data_apple, hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Apple Music hoy.")

with col4:
    st.subheader("Deezer: Top Songs")
    data_deezer = get_kworb_data("https://kworb.net/charts/deezer/hn.html")
    if not data_deezer.empty:
        st.dataframe(data_deezer, hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Deezer hoy.")

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
