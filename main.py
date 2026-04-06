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
st.header("📊 Spotify Charts Honduras")
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

# --- 1. FUNCIÓN DE ICONOS (Poner esto arriba para que no dé NameError) ---
def icon_mov_simple(val):
    val = str(val).strip()
    if val == "=" or val == "0" or val == "": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

# --- 2. FUNCIONES DE EXTRACCIÓN PARA APPLE MUSIC ---
def get_apple_hn():
    url = "https://kworb.net/charts/apple_s/hn.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table: return pd.DataFrame()
        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': cols[1].text.strip(), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

def get_apple_global():
    url = "https://kworb.net/apple_songs/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table: return pd.DataFrame()
        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': cols[1].text.strip(), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- 3. INTERFAZ EN COLUMNAS ---
st.header("🍎 Apple Music Charts")

col_apple_hn, col_apple_gl = st.columns(2)

with col_apple_hn:
    st.subheader("Honduras")
    df_apple_hn = get_apple_hn()
    if not df_apple_hn.empty:
        # Ahora ya no dará error porque la función está definida arriba
        df_apple_hn['Mov'] = df_apple_hn['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple_hn.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Apple Honduras.")

with col_apple_gl:
    st.subheader("Global")
    df_apple_gl = get_apple_global()
    if not df_apple_gl.empty:
        df_apple_gl['Mov'] = df_apple_gl['Mov'].apply(icon_mov_simple)
        st.dataframe(df_apple_gl.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Apple Global.")

# --- FUNCIONES DE EXTRACCIÓN (Honduras y Global) ---

def get_deezer_hn():
    url = "https://kworb.net/charts/deezer/hn.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table: return pd.DataFrame()
        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': cols[1].text.strip(), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

def get_deezer_global():
    url = "https://kworb.net/charts/deezer/ww.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table: return pd.DataFrame()
        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': cols[1].text.strip(), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

def icon_mov_simple(val):
    val = str(val).strip()
    if val == "=" or val == "0" or val == "": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

# --- INTERFAZ EN COLUMNAS ---
st.header("🎵 Deezer Charts")

col_hn, col_gl = st.columns(2)

with col_hn:
    st.subheader("Honduras")
    df_deezer = get_deezer_hn()
    if not df_deezer.empty:
        df_deezer['Mov'] = df_deezer['Mov'].apply(icon_mov_simple)
        st.dataframe(df_deezer.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos en Honduras.")

with col_gl:
    st.subheader("Global")
    df_deezer_gl = get_deezer_global()
    if not df_deezer_gl.empty:
        df_deezer_gl['Mov'] = df_deezer_gl['Mov'].apply(icon_mov_simple)
        st.dataframe(df_deezer_gl.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin datos Globales.")

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

