import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

# Lista de artistas permitidos
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def icon_mov(val):
    if val == "=": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

# --- FUNCIÓN DE EXTRACCIÓN (Tu fórmula original adaptada) ---
def get_kworb_data(url, table_id, is_spotify_daily=False):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': table_id})
        
        if not table: return pd.DataFrame()

        rows = []
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            
            full_text = cols[2].get_text(separator=" ").strip()
            parts = full_text.split(" - ")
            artist_name = parts[0].strip().upper() 
            
            if any(member == artist_name for member in solo_bts):
                data = {
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': cols[1].text.strip(),
                    'Canción': full_text
                }
                # Solo el diario tiene estas columnas adicionales según tu fórmula
                if is_spotify_daily:
                    data['Reproducciones'] = cols[6].text.strip()
                    data['Evolución'] = cols[7].text.strip()
                
                rows.append(data)
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- BLOQUE 1: SPOTIFY (DIARIO Y SEMANAL) ---
st.header("📊 Spotify Charts")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spotify: Top Daily Songs")
    df_daily = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily", is_spotify_daily=True)
    if not df_daily.empty:
        df_daily['Mov'] = df_daily['Mov'].apply(icon_mov)
        st.dataframe(df_daily.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones en el Top Diario hoy.")

with col2:
    st.subheader("Spotify: Top Weekly Songs")
    df_weekly = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
    if not df_weekly.empty:
        df_weekly['Mov'] = df_weekly['Mov'].apply(icon_mov)
        st.dataframe(df_weekly.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones en el Top Semanal.")

st.divider()

# --- BLOQUE 2: APPLE MUSIC Y DEEZER ---
st.header("🎵 Otras Plataformas")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Apple Music: Top Songs")
    # Apple Music no usa ID de tabla en Kworb, así que buscamos la tabla general
    df_apple = get_kworb_data("https://kworb.net/charts/apple_s/hn.html", None)
    if not df_apple.empty:
        df_apple['Mov'] = df_apple['Mov'].apply(icon_mov)
        st.dataframe(df_apple.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin entradas en Apple Music hoy.")

with col4:
    st.subheader("Deezer: Top Songs")
    df_deezer = get_kworb_data("https://kworb.net/charts/deezer/hn.html", None)
    if not df_deezer.empty:
        df_deezer['Mov'] = df_deezer['Mov'].apply(icon_mov)
        st.dataframe(df_deezer.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin entradas en Deezer hoy.")

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
