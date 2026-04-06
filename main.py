import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

# --- FUNCIONES DE EXTRACCIÓN (KWORB) ---
def get_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        
        # Filtro estricto de BTS y solistas
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        
        # Limpieza y filtrado
        df['Artista'] = df['Artist and Title'].str.split(" - ").str[0].str.strip().str.upper()
        df_filtered = df[df['Artista'].isin(solo_bts)].copy()
        return df_filtered
    except:
        return pd.DataFrame()

# --- TÍTULO PRINCIPAL ---
st.title("BTS Charts Honduras")
st.write(f"Última actualización: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN 1: SPOTIFY DAILY ---
st.header("📊 Spotify Charts")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spotify: Top Daily Songs")
    df_daily = get_data("https://kworb.net/spotify/country/hn_daily.html")
    if not df_daily.empty:
        st.dataframe(df_daily[['Pos', 'P+', 'Artist and Title', 'Streams']].rename(columns={'Pos':'#', 'P+':'Mov'}), hide_index=True)
    else:
        st.info("Sin datos diarios hoy.")

with col2:
    st.subheader("Spotify: Top Weekly Songs")
    df_weekly = get_data("https://kworb.net/spotify/country/hn_weekly.html")
    if not df_weekly.empty:
        st.dataframe(df_weekly[['Pos', 'P+', 'Artist and Title']].rename(columns={'Pos':'#', 'P+':'Mov'}), hide_index=True)
    else:
        st.info("Sin datos semanales hoy.")

st.divider()

# --- SECCIÓN 2: APPLE MUSIC & DEEZER ---
st.header("🎵 Otras Plataformas (Honduras)")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Apple Music: Top Songs")
    # Nota: Apple Music y Deezer en Kworb a veces usan estructuras distintas, 
    # este código intenta capturar la tabla estándar.
    df_apple = get_data("https://kworb.net/charts/apple_s/hn.html")
    if not df_apple.empty:
        st.dataframe(df_apple[['Pos', 'P+', 'Artist and Title']].rename(columns={'Pos':'#', 'P+':'Mov'}), hide_index=True)
    else:
        st.info("No hay datos de Apple Music disponibles.")

with col4:
    st.subheader("Deezer: Top Songs")
    df_deezer = get_data("https://kworb.net/charts/deezer/hn.html")
    if not df_deezer.empty:
        st.dataframe(df_deezer[['Pos', 'P+', 'Artist and Title']].rename(columns={'Pos':'#', 'P+':'Mov'}), hide_index=True)
    else:
        st.info("No hay datos de Deezer disponibles.")

st.divider()

# --- SECCIÓN 3: ENLACES Y REDES SOCIALES ---
st.header("🔗 Enlaces Oficiales")
left_link, right_link = st.columns(2)

with left_link:
    st.markdown("### 🎧 Streaming Oficial")
    st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
    st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
    st.markdown("- [Apple Music: BTS](https://music.apple.com/artist/bts/667061285)")
    st.markdown("- [Deezer: BTS](https://www.deezer.com/artist/4105021)")
    st.markdown("#### Solistas en Spotify")
    st.write("[Jung Kook](https://open.spotify.com/artist/6Ha9SArjAue9uRMQH13T9t) | [Jimin](https://open.spotify.com/artist/1pYpS9vNUn0949YpU66pBy) | [V](https://open.spotify.com/artist/3JsHnS6YvS6vS9z6S6vS9z)")
    st.write("[RM](https://open.spotify.com/artist/2EcnidS8vL936NidS8vL93) | [Jin](https://open.spotify.com/artist/5pYpS9vNUn0949YpU66pBy) | [j-hope](https://open.spotify.com/artist/0b1sIQumIAsNbqAoIClSpy) | [Agust D](https://open.spotify.com/artist/ klM87p3WdDb)")

with right_link:
    st.markdown("### 📱 Redes Sociales")
    st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
    st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
    st.markdown("- [TikTok: @bts_official_bighit](https://www.tiktok.com/@bts_official_bighit)")
    st.markdown("- [Facebook: BTS](https://www.facebook.com/bangtan.official)")
    st.markdown("#### Instagram de los Miembros")
    st.markdown("- [RM (@rkive)](https://www.instagram.com/rkive)")
    st.markdown("- [Jin (@jin)](https://www.instagram.com/jin)")
    st.markdown("- [SUGA (@agustd)](https://www.instagram.com/agustd)")
    st.markdown("- [j-hope (@uarmyhope)](https://www.instagram.com/uarmyhope)")
    st.markdown("- [Jimin (@j.m)](https://www.instagram.com/j.m)")
    st.markdown("- [V (@thv)](https://www.instagram.com/thv)")
    st.markdown("- [Jung Kook (@mnijungkook)] (https://www.instagram.com/mnijungkook?igsh=MWxueDE4MHh0aG9kYw==)")

st.caption("Creado para ARMY Honduras 💜")
