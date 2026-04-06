import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜")

def get_spotify_daily():
    url = "https://kworb.net/spotify/country/hn_daily.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # Leemos la tabla directamente
        df = pd.read_html(response.text)[0]
        
        # Lista de artistas oficial para el filtro
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

        # Filtro: El artista debe ser uno de los chicos
        def es_bts(text):
            artist = str(text).split(" - ")[0].upper().strip()
            return any(m == artist for m in solo_bts)

        df_filtered = df[df['Artist and Title'].apply(es_bts)].copy()

        # Seleccionamos las columnas del diario (con Streams)
        res = df_filtered[['Pos', 'P+', 'Artist and Title', 'Streams']].copy()
        res.columns = ['#', 'Mov', 'Canción', 'Streams']
        return res
    except:
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# Título solicitado arriba del cuadro
st.subheader("Spotify: Top Daily Songs")

# Ejecutar y mostrar datos
df_daily = get_spotify_daily()

if not df_daily.empty:
    st.dataframe(df_daily, hide_index=True, use_container_width=True)
    st.success(f"Se encontraron {len(df_daily)} canciones en el ranking diario.")
else:
    st.info("No se encontraron canciones de BTS en el Top 200 de hoy.")

st.caption("Fuente: Kworb.net")
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
