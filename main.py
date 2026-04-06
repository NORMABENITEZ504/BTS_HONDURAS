import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

def get_kworb_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        # 1. Extraer todas las tablas
        tables = pd.read_html(response.text)
        if not tables: return pd.DataFrame()
        df = max(tables, key=len) # La tabla con más datos es el chart

        # 2. Identificar columnas (Posición, Movimiento, Título)
        # Usamos índices porque los nombres de las columnas en Kworb varían mucho
        col_pos = df.columns[0]
        col_mov = df.columns[1]
        
        # Buscamos la columna que contiene el texto de la canción (suele ser la 3ra o tiene "Artist")
        col_title = None
        for col in df.columns:
            if 'Artist' in str(col) or 'Title' in str(col) or df[col].astype(str).str.contains("-").any():
                col_title = col
                break
        
        if col_title is None: return pd.DataFrame()

        # 3. FILTRO FLEXIBLE (Busca a los chicos en cualquier parte del nombre del artista)
        chicos = ["BTS", "JUNG KOOK", "JIMIN", "SUGA", "AGUST D", "J-HOPE", "RM", "JIN"]
        # El nombre del artista suele estar antes del guion
        def es_de_bts(text):
            text_clean = str(text).upper()
            artista = text_clean.split("-")[0].strip()
            # Verificamos si es BTS o un solista, o si el nombre contiene "V" como palabra sola
            return any(c in artista for c in chicos) or " V " in f" {artista} "

        df_filtered = df[df[col_title].apply(es_de_bts)].copy()
        
        # 4. Limpiar resultado final
        res = df_filtered[[col_pos, col_mov, col_title]].copy()
        res.columns = ['#', 'Mov', 'Canción']
        
        if 'Streams' in df.columns:
            res['Streams'] = df_filtered['Streams']
            
        return res
    except Exception as e:
        return pd.DataFrame()

# --- DISEÑO ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SPOTIFY ---
st.header("📊 Spotify Charts")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Spotify: Top Daily Songs")
    d1 = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html")
    if not d1.empty: st.dataframe(d1, hide_index=True, use_container_width=True)
    else: st.info("No hay canciones de BTS en el Top Diario.")

with c2:
    st.subheader("Spotify: Top Weekly Songs")
    d2 = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html")
    if not d2.empty: st.dataframe(d2, hide_index=True, use_container_width=True)
    else: st.info("No hay canciones de BTS en el Top Semanal.")

st.divider()

# --- APPLE & DEEZER ---
st.header("🎵 Otras Plataformas")
c3, c4 = st.columns(2)
with c3:
    st.subheader("Apple Music: Top Songs")
    d3 = get_kworb_data("https://kworb.net/charts/apple_s/hn.html")
    if not d3.empty: st.dataframe(d3, hide_index=True, use_container_width=True)
    else: st.info("Sin datos en Apple Music hoy.")

with c4:
    st.subheader("Deezer: Top Songs")
    d4 = get_kworb_data("https://kworb.net/charts/deezer/hn.html")
    if not d4.empty: st.dataframe(d4, hide_index=True, use_container_width=True)
    else: st.info("Sin datos en Deezer hoy.")

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
