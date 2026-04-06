import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

# --- FUNCIÓN PARA EXTRAER DATOS DE KWORB ---
def get_kworb_data(url, is_spotify=True):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            return pd.DataFrame()

        df = pd.read_html(str(table))[0]
        
        # Identificar columnas dinámicamente
        col_pos = [c for c in df.columns if 'Pos' in str(c)][0]
        col_mov = [c for c in df.columns if 'P+' in str(c) or 'Change' in str(c)][0]
        col_title = [c for c in df.columns if 'Artist' in str(c) or 'Title' in str(c)][0]
        
        # Filtro estricto de BTS y solistas
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        
        def filter_bts(text):
            artist = str(text).split(" - ")[0].upper().strip()
            return any(member == artist for member in solo_bts)

        df_filtered = df[df[col_title].apply(filter_bts)].copy()
        
        # Seleccionar y renombrar columnas básicas
        cols_to_show = [col_pos, col_mov, col_title]
        names = ['#', 'Mov', 'Canción']
        
        # Agregar Streams solo si es Spotify Diario y existe la columna
        if is_spotify and 'Streams' in df.columns:
            cols_to_show.append('Streams')
            names.append('Streams')
            
        res = df_filtered[cols_to_show].copy()
        res.columns = names
        return res
    except:
        return pd.DataFrame()

# --- DISEÑO DE LA PÁGINA ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN SPOTIFY ---
st.header("📊 Spotify Charts")
col_daily, col_weekly = st.columns(2)

with col_daily:
    st.subheader("Spotify: Top Daily Songs")
    df_sd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", is_spotify=True)
    if not df_sd.empty:
        st.dataframe(df_sd, hide_index=True, use_container_width=True)
    else:
        st.info("No hay datos diarios disponibles.")

with col_weekly:
    st.subheader("Spotify: Top Weekly Songs")
    df_sw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", is_spotify=True)
    if not df_sw.empty:
        st.dataframe(df_sw, hide_index=True, use_container_width=True)
    else:
        st.info("No hay datos semanales disponibles.")

st.divider()

# --- SECCIÓN APPLE & DEEZER ---
st.header("🎵 Otras Plataformas")
col_apple, col_deezer = st.columns(2)

with col_apple:
    st.subheader("Apple Music: Top Songs")
    df_am = get_kworb_data("https://kworb.net/charts/apple_s/hn.html", is_spotify=False)
    if not df_am.empty:
        st.dataframe(df_am, hide_index=True, use_container_width=True)
    else:
        st.info("Sin canciones en Apple Music hoy.")

with col_deezer:
    st.subheader("Deezer: Top Songs")
    df_dz = get_kworb_data("https://kworb.net/charts/deezer/hn.html", is_spotify=False)
    if not df_dz.empty:
        st.dataframe(df_dz, hide_index=True, use_container_width=True)
    else:
        st.info("Sin canciones en Deezer hoy.")

st.divider()

# --- SECCIÓN DE ENLACES Y REDES SOCIALES (DOS COLUMNAS) ---
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🎧 Perfiles Oficiales")
    st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
    st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
    st.markdown("- [Apple Music: BTS](https://music.apple.com/artist/bts/667061285)")
    st.markdown("- [Deezer: BTS](https://www.deezer.com/artist/4105021)")
    st.write("**Solistas en Spotify:**")
    st.caption("[JK](https://open.spotify.com/artist/6HaGArvgnhIPFWv2uCXYqI) | [Jimin](https://open.spotify.com/artist/1pYpS4v8u55uS9ZpZJzZ8Z) | [V](https://open.spotify.com/artist/3ESm3vD6Y7vSndf6XzSclm) | [RM](https://open.spotify.com/artist/2EcnshPshb8V3Xj609FshD) | [Jin](https://open.spotify.com/artist/5vAL9vS8XW3N3vS3v3v3v3) | [Suga](https://open.spotify.com/artist/0u69HUiOaN7Jp6v8z8z8z8) | [j-hope](https://open.spotify.com/artist/0b1886X9vYvYvYvYvYvYvY)")

with col_right:
    st.markdown("### 📱 Redes Sociales")
    st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
    st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
    st.markdown("- [TikTok: @bts_official_bighit](https://www.tiktok.com/@bts_official_bighit)")
    st.write("**Instagram de los Miembros:**")
    st.caption("[RM](https://www.instagram.com/rkive) | [Jin](https://www.instagram.com/jin) | [SUGA](https://www.instagram.com/agustd) | [j-hope](https://www.instagram.com/uarmyhope) | [Jimin](https://www.instagram.com/j.m) | [V](https://www.instagram.com/thv) | [JK](https://www.instagram.com/mnijungkook)")

st.caption("Hecho para ARMY Honduras 💜")
