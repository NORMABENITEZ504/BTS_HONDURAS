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
        # Buscamos la tabla por su ID (como el código que te funcionó)
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
                # Usamos la lógica de columnas fijas (0, 1, 2, 6, 7)
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
    # Para el semanal usamos 'spotifyweekly' que es el ID que usa Kworb
    df_weekly = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
    if not df_weekly.empty:
        st.dataframe(df_weekly.sort_values('Puesto'), hide_index=True, use_container_width=True)
    else:
        st.info("No hay canciones de BTS en el Top Semanal.")

st.divider()

# --- SECCIÓN DE DEEZER ---
def get_deezer_data():
    url = "https://kworb.net/charts/deezer/hn.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # En Deezer buscamos la primera tabla de la página
        table = soup.find('table')
        if not table:
            return pd.DataFrame()

        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            # Deezer estructura: 0:Pos, 1:P+, 2:Artist and Title
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

st.subheader("Deezer: Top Songs")
df_deezer = get_deezer_data()

if not df_deezer.empty:
    def icon_mov(val):
        val = str(val).strip()
        if val == "=" or val == "" or val == "0": return "➡️ ="
        if "+" in val: return f"🟩 {val}"
        if "-" in val: return f"🟥 {val}"
        return f"🔵 {val}"

    df_deezer['Mov'] = df_deezer['Mov'].apply(icon_mov)
    
    # Mostramos solo Puesto, Movimiento y Canción
    st.dataframe(
        df_deezer[['Puesto', 'Mov', 'Canción']].sort_values('Puesto'), 
        hide_index=True, 
        use_container_width=True
    )
else:
    st.info("No se encontraron canciones de BTS en el Top de Deezer hoy.")

# --- SECCIÓN DE APPLE MUSIC ---
def get_apple_data():
    url = "https://kworb.net/charts/apple_s/hn.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Apple Music en Kworb suele ser la primera tabla de la página
        table = soup.find('table')
        if not table:
            return pd.DataFrame()

        rows = []
        solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            # Apple Music estructura: 0:Pos, 1:P+, 2:Artist and Title
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

st.subheader("Apple Music: Top Songs")
df_apple = get_apple_data()

if not df_apple.empty:
    def icon_mov(val):
        val = str(val).strip()
        if val == "=" or val == "" or val == "0": return "➡️ ="
        if "+" in val: return f"🟩 {val}"
        if "-" in val: return f"🟥 {val}"
        return f"🔵 {val}"

    df_apple['Mov'] = df_apple['Mov'].apply(icon_mov)
    
    # Mostramos Puesto, Movimiento y Canción
    st.dataframe(
        df_apple[['Puesto', 'Mov', 'Canción']].sort_values('Puesto'), 
        hide_index=True, 
        use_container_width=True
    )
else:
    st.info("No se encontraron canciones de BTS en el Top de Apple Music hoy.")
    
# --- SECCIÓN REDES SOCIALES (2 COLUMNAS) ---
left, right = st.columns(2)
with left:
    st.markdown("### 🎧 Perfiles Oficiales")
    st.write("[Spotify BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX) | [YouTube](https://www.youtube.com/@BANGTANTV)")
    st.write("[Apple Music](https://music.apple.com/artist/bts/667061285) | [Deezer](https://www.deezer.com/artist/4105021)")
with right:
    st.markdown("### 📱 Redes Sociales")
    st.write("[Instagram](https://www.instagram.com/bts.bighitofficial) | [X](https://x.com/bts_bighit) | [TikTok](https://www.tiktok.com/@bts_official_bighit)")
    st.caption("RM | Jin | SUGA | j-hope | Jimin | V | JK")

st.caption("Creado para ARMY Honduras 💜")
