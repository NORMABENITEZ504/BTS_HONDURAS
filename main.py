import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜", layout="wide")

# Artistas permitidos
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def icon_mov(val):
    if val == "=": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

def get_kworb_data(url, table_id):
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
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': icon_mov(cols[1].text.strip()),
                    'Canción': full_text,
                    'Streams Totales': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                })
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SECCIÓN SPOTIFY ---
st.header("📊 Spotify Charts")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spotify: Top Daily Songs")
    df_daily = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
    if not df_daily.empty:
        st.dataframe(df_daily.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Top Diario hoy.")

with col2:
    st.subheader("Spotify: Top Weekly Songs")
    df_weekly = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
    if not df_weekly.empty:
        st.dataframe(df_weekly.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Top Semanal.")

st.divider()

# --- SECCIÓN SPOTIFY GLOBAL (2 COLUMNAS) ---
st.header("🌍 Spotify Charts: Global")

# 1. Definimos la función completa primero (para que traiga Streams y Evolución)
def get_global_data(url, table_id):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': table_id})
        if not table: return pd.DataFrame()

        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 7: continue 
            
            full_text = cols[2].get_text(separator=" ").strip()
            parts = full_text.split(" - ")
            artist_name = parts[0].strip().upper() 
            
            if any(member == artist_name for member in solo_bts):
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': icon_mov(cols[1].text.strip()), 
                    'Canción': full_text,
                    'Streams Totales': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                })
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

# 2. Creamos las columnas y mostramos los datos una sola vez
col_glob_d, col_glob_w = st.columns(2)

with col_glob_d:
    st.subheader("Spotify: Top Daily Songs (Global)")
    df_glob_d = get_global_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
    if not df_glob_d.empty:
        st.dataframe(df_glob_d.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Top Diario Global.")

with col_glob_w:
    st.subheader("Spotify: Top Weekly Songs (Global)")
    df_glob_w = get_global_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
    if not df_glob_w.empty:
        st.dataframe(df_glob_w.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Top Semanal Global.")

st.divider()

# --- SECCIÓN APPLE MUSIC ---
st.header("🍎 Apple Music Charts")
c3, c4 = st.columns(2)
with c3:
    st.subheader("Apple Music: Honduras")
    df3 = get_generic_data("https://kworb.net/charts/apple_s/hn.html")
    if not df3.empty:
        df3['Mov'] = df3['Mov'].apply(icon_mov_simple)
        st.dataframe(df3.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else: st.info("Sin datos.")
with c4:
    st.subheader("Apple Music: Global")
    df4 = get_generic_data("https://kworb.net/apple_songs/")
    if not df4.empty:
        df4['Mov'] = df4['Mov'].apply(icon_mov_simple)
        st.dataframe(df4.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else: st.info("Sin datos.")

# --- SECCIÓN DEEZER ---
st.header("🎵 Deezer Charts")
c5, c6 = st.columns(2)
with c5:
    st.subheader("Deezer: Honduras")
    df5 = get_generic_data("https://kworb.net/charts/deezer/hn.html")
    if not df5.empty:
        df5['Mov'] = df5['Mov'].apply(icon_mov_simple)
        st.dataframe(df5.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else: st.info("Sin datos.")
with c6:
    st.subheader("Deezer: Global")
    df6 = get_generic_data("https://kworb.net/charts/deezer/ww.html")
    if not df6.empty:
        df6['Mov'] = df6['Mov'].apply(icon_mov_simple)
        st.dataframe(df6.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else: st.info("Sin datos.")

st.divider()

# Creamos las dos columnas
col_apple_hn, col_apple_gl = st.columns(2)

with col_apple_hn:
    st.subheader("Apple Music: Top Songs (Honduras)")
    df_apple_hn = get_apple_data("https://kworb.net/charts/apple_s/hn.html")
    if not df_apple_hn.empty:
        df_apple_hn['Mov'] = df_apple_hn['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple_hn.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en Apple Music Honduras hoy.")

with col_apple_gl:
    st.subheader("Apple Music: Top Songs (Global)")
    # URL Global que proporcionaste
    df_apple_gl = get_apple_data("https://kworb.net/apple_songs/")
    if not df_apple_gl.empty:
        df_apple_gl['Mov'] = df_apple_gl['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple_gl.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Chart Global de Apple Music.")

st.divider()
# --- SECCIÓN APPLE MUSIC (HONDURAS VS GLOBAL) ---
st.header("🍎 Apple Music Charts")

def get_apple_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # En las páginas de Apple Music, Kworb usa la primera tabla disponible
        table = soup.find('table')
        if not table: return pd.DataFrame()
        
        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            # Apple Music estructura: 0:Pos, 1:Mov, 2:Artist and Title
            if len(cols) < 3: continue
            
            full_text = cols[2].get_text(separator=" ").strip()
            parts = full_text.split(" - ")
            artist_name = parts[0].strip().upper() 
            
            if any(member == artist_name for member in solo_bts):
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': cols[1].text.strip(),
                    'Canción': full_text
                })
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

# Creamos las dos columnas
col_apple_hn, col_apple_gl = st.columns(2)

with col_apple_hn:
    st.subheader("Apple Music: Top Songs (Honduras)")
    df_apple_hn = get_apple_data("https://kworb.net/charts/apple_s/hn.html")
    if not df_apple_hn.empty:
        df_apple_hn['Mov'] = df_apple_hn['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple_hn.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en Apple Music Honduras hoy.")

with col_apple_gl:
    st.subheader("Apple Music: Top Songs (Global)")
    # URL Global que proporcionaste
    df_apple_gl = get_apple_data("https://kworb.net/apple_songs/")
    if not df_apple_gl.empty:
        df_apple_gl['Mov'] = df_apple_gl['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple_gl.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Chart Global de Apple Music.")

st.divider()

# --- MOSTRAR TABLAS A LA PAR ---
def icon_mov_simple(val):
    val = str(val).strip()
    if val == "=" or val == "" or val == "0": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

with col_apple: # Columna izquierda: Apple Music
    st.subheader("Apple Music: Top Songs")
    df_apple = get_apple_data()
    if not df_apple.empty:
        df_apple['Mov'] = df_apple['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple[['Puesto', 'Mov', 'Canción']].sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Apple Music.")

with col_deezer: # Columna derecha: Deezer
    st.subheader("Deezer: Top Songs")
    df_deezer = get_deezer_data()
    if not df_deezer.empty:
        df_deezer['Mov'] = df_deezer['Mov'].apply(icon_mov_simple)
        st.dataframe(df_deezer[['Puesto', 'Mov', 'Canción']].sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Deezer.")

st.divider()

# --- SECCIÓN REDES SOCIALES (RESTAURADA EXACTAMENTE COMO LA QUERÍAS) ---
left, right = st.columns(2)

with left:
    st.markdown("### Perfiles Oficiales")
    st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
    st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
    st.markdown("- [Apple Music: BTS](https://music.apple.com/artist/bts/667061285)")
    st.markdown("- [Deezer: BTS](https://www.deezer.com/artist/4105021)")
    st.write("**Spotify Solistas:** [JK](https://open.spotify.com/artist/6Ha9SArjAue9uRMQH13T9t) | [Jimin](https://open.spotify.com/artist/1pYpS9vNUn0949YpU66pBy) | [V](https://open.spotify.com/artist/3JsHnS6YvS6vS9z6S6vS9z) | [RM](https://open.spotify.com/artist/2EcnidS8vL936NidS8vL93) | [Jin](https://open.spotify.com/artist/5pYpS9vNUn0949YpU66pBy) | [Suga](https://open.spotify.com/artist/0b1sIQumIAsNbqAoIClSpy) | [j-hope](https://open.spotify.com/artist/)")

with right:
    st.markdown("### Redes Sociales")
    st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
    st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
    st.markdown("- [TikTok: @bts_official_bighit](https://www.tiktok.com/@bts_official_bighit)")
    st.write("**Instagram Miembros:**")
    st.caption("[RM](https://www.instagram.com/rkive) | [Jin](https://www.instagram.com/jin) | [SUGA](https://www.instagram.com/agustd) | [j-hope](https://www.instagram.com/uarmyhope) | [Jimin](https://www.instagram.com/j.m) | [V](https://www.instagram.com/thv) | [JK](https://www.instagram.com/mnijungkook)")

st.caption("Creado para ARMY Honduras 💜")

