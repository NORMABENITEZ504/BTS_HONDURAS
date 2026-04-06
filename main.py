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

# --- FUNCIÓN DE EXTRACCIÓN MEJORADA ---
def get_kworb_data(url, is_spotify=False):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscamos la tabla principal de la página
        table = soup.find('table')
        
        if not table: return pd.DataFrame()

        # Leemos la tabla con pandas
        df = pd.read_html(str(table))[0]
        
        # Identificamos columnas por posición para que no falle si cambia el nombre
        # Col 0: Pos, Col 1: Movimiento, Col 2: Artista y Canción
        col_pos = df.columns[0]
        col_mov = df.columns[1]
        col_title = df.columns[2]

        rows = []
        for index, row in df.iterrows():
            if index == 0: continue # Saltamos encabezado si es necesario
            
            full_text = str(row[col_title])
            parts = full_text.split(" - ")
            artist_name = parts[0].strip().upper() 
            
            if any(member == artist_name for member in solo_bts):
                data = {
                    'Puesto': row[col_pos],
                    'Mov': icon_mov(str(row[col_mov])),
                    'Canción': full_text
                }
                
                # Si es Spotify (Diario o Semanal) y tiene la columna de Streams (columna 6)
                if is_spotify and len(df.columns) > 6:
                    data['Streams Totales'] = row[df.columns[6]]
                    data['Evolución'] = row[df.columns[7]]
                
                rows.append(data)
        return pd.DataFrame(rows)
    except:
        return pd.DataFrame()

# --- INTERFAZ ---
st.title("BTS Charts Honduras")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- BLOQUE 1: SPOTIFY ---
st.header("📊 Spotify Charts")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Spotify: Top Daily Songs")
    df_daily = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", is_spotify=True)
    if not df_daily.empty:
        st.dataframe(df_daily.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones en el Top Diario hoy.")

with col2:
    st.subheader("Spotify: Top Weekly Songs")
    # Usamos la misma lógica para el semanal
    df_weekly = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", is_spotify=True)
    if not df_weekly.empty:
        st.dataframe(df_weekly.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones en el Top Semanal.")

st.divider()

# --- BLOQUE 2: OTRAS PLATAFORMAS ---
st.header("🎵 Otras Plataformas")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Apple Music: Top Songs")
    df_apple = get_kworb_data("https://kworb.net/charts/apple_s/hn.html", is_spotify=False)
    if not df_apple.empty:
        st.dataframe(df_apple.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin entradas en Apple Music hoy.")

with col4:
    st.subheader("Deezer: Top Songs")
    df_deezer = get_kworb_data("https://kworb.net/charts/deezer/hn.html", is_spotify=False)
    if not df_deezer.empty:
        st.dataframe(df_deezer.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("Sin entradas en Deezer hoy.")

st.divider()

# --- SECCIÓN REDES SOCIALES ---
left, right = st.columns(2)
with left:
    st.markdown("### 🎧 Perfiles Oficiales")
    st.write("[Spotify](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX) | [YouTube](https://www.youtube.com/@BANGTANTV) | [Apple](https://music.apple.com/artist/bts/667061285) | [Deezer](https://www.deezer.com/artist/4105021)")
with right:
    st.markdown("### 📱 Redes Sociales")
    st.write("[Instagram](https://www.instagram.com/bts.bighitofficial) | [X](https://x.com/bts_bighit) | [TikTok](https://www.tiktok.com/@bts_official_bighit)")

st.caption("Creado para ARMY Honduras 💜")
