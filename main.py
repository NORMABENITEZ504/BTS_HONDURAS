import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras 🇭🇳", page_icon="💜", layout="wide")

# --- FUNCIÓN PARA CARGAR IMAGEN DE FONDO ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Reemplaza 'tu_imagen_de_fondo.png' con la ruta a la imagen que proporcionaste (image_3.png).
# Por ejemplo, si está en la misma carpeta que este script, solo pon el nombre del archivo.
# Asegúrate de que el archivo exista y sea accesible.
# image_path = 'image_3.png' # Descomenta y ajusta si tienes el archivo localmente
image_path = 'image_3.png' # Asumiendo que image_3.png está en el mismo directorio.

# Si la imagen no está disponible localmente, el código no funcionará.
# Para este ejemplo, usaré el nombre de archivo directo que asume que el archivo existe.

# --- ESTILOS CSS PERSONALIZADOS ---
try:
    bin_str = get_base64(image_path)
    page_bg_img = f'''
    <style>
    /* Fondo de la aplicación */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: repeat; /* Repetir el patrón */
        background-attachment: fixed;
    }}

    /* Estilos para las tablas */
    .stDataFrame table {{
        width: 100%;
        border-collapse: collapse;
    }}

    /* Estilo para el encabezado de la tabla (MOV, CANCIÓN, etc.) */
    .stDataFrame table thead tr th {{
        background-color: rgba(173, 216, 230, 0.5) !important; /* Celeste con 50% de transparencia */
        color: white !important; /* Texto blanco para legibilidad */
        border: 1px solid white !important; /* Bordes blancos para visibilidad */
    }}

    /* Estilo para el cuerpo de la tabla */
    .stDataFrame table tbody tr td {{
        background-color: rgba(173, 216, 230, 0.7) !important; /* Celeste con 70% de transparencia */
        color: white !important; /* Texto blanco para legibilidad */
        border: 1px solid white !important; /* Bordes blancos para visibilidad */
    }}

    /* Color morado para títulos principales de st */
    h1, h2, h3 {{
        color: #7D52B5 !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"No se pudo encontrar el archivo de imagen en la ruta especificada: {image_path}. Por favor, asegúrate de que el archivo existe y la ruta es correcta.")

# --- VARIABLES Y FUNCIONES DE DATOS ---
solo_bts = ["BTS", "JUNG KOOK", "JIMIN", "V", "SUGA", "J-HOPE", "RM", "JIN", "AGUST D"]

def icon_mov(val):
    val = str(val).strip()
    if val == "=" or val == "0" or val == "": return "➡️ ="
    if "+" in val: return f"🟩 {val}"
    if "-" in val: return f"🟥 {val}"
    return f"🔵 {val}"

def get_kworb_data(url, table_id):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': table_id})
        if not table: return pd.DataFrame()
        rows = []
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 8: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({
                    'Puesto': int(cols[0].text.strip()),
                    'Mov': icon_mov(cols[1].text.strip()),
                    'Canción': full_text,
                    'Streams': cols[6].text.strip(),
                    'Evolución': cols[7].text.strip()
                })
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

def get_simple_chart(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table: return pd.DataFrame()
        rows = []
        for tr in table.find_all('tr')[1:]:
            cols = tr.find_all('td')
            if len(cols) < 3: continue
            full_text = cols[2].get_text(separator=" ").strip()
            artist_name = full_text.split(" - ")[0].strip().upper()
            if any(member == artist_name for member in solo_bts):
                rows.append({'Puesto': int(cols[0].text.strip()), 'Mov': icon_mov(cols[1].text.strip()), 'Canción': full_text})
        return pd.DataFrame(rows)
    except: return pd.DataFrame()

# --- CABECERA ---
st.title("💜 BTS Charts Honduras")
# Usamos una fecha de ejemplo, puedes usar datetime.now() para la fecha actual.
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- SISTEMA DE PESTAÑAS ---
tab_spot, tab_ytm, tab_apple, tab_deezer, tab_yt, tab_social = st.tabs([
    "🎧 Spotify", "🎵 YouTube Music", "🍎 Apple Music", "🔊 Deezer", "📺 YouTube", "🔗 Redes"
])

with tab_spot:
    st.header("📊 Spotify Charts")
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        df_hd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        # Se usa st.dataframe para renderizar la tabla con los estilos CSS.
        st.dataframe(df_hd, hide_index=True)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.dataframe(df_hw, hide_index=True)

with tab_ytm:
    # --- TU SECCIÓN DE YOUTUBE MUSIC EXACTA ---
    st.header("🎧 YouTube Music Honduras")

    # 1. Configuración de Datos Manuales
    fecha_update_ytm = "8 de abril 2026"

    # Datos para el Top Diario
    data_yt_diario = [
        {"Puesto": 57, "Mov": "🟥 -44", "Canción": "Hooligan - BTS"},
        {"Puesto": 72, "Mov": "🟥 -29", "Canción": "2.0 - BTS"}
    ]

    # 2. Interfaz de la Sección
    st.write(f"Última actualización manual: **{fecha_update_ytm}**")

    col_manual_d, col_manual_w = st.columns(2)

    with col_manual_d:
        st.subheader("Top diario de canciones")
        df_yt_m_daily = pd.DataFrame(data_yt_diario)
        # Se usa st.dataframe para renderizar la tabla con los estilos CSS.
        st.dataframe(df_yt_m_daily, hide_index=True)

    with col_manual_w:
        st.subheader("Top semanal de canciones")
        st.info("No hay entradas de BTS en el chart semanal para esta fecha.")

with tab_apple:
    st.header("🍎 Apple Music Charts")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.subheader("Honduras 🇭🇳")
        df_ah = get_simple_chart("https://kworb.net/charts/apple_s/hn.html")
        st.dataframe(df_ah, hide_index=True)
    with ca2:
        st.subheader("Global 🌍")
        df_ag = get_simple_chart("https://kworb.net/apple_songs/")
        st.dataframe(df_ag, hide_index=True)

with tab_deezer:
    st.header("🔊 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        df_dh = get_simple_chart("https://kworb.net/charts/deezer/hn.html")
        st.dataframe(df_dh, hide_index=True)
    with cd2:
        st.subheader("Global 🌍")
        df_dg = get_simple_chart("https://kworb.net/charts/deezer/ww.html")
        st.dataframe(df_dg, hide_index=True)

with tab_yt:
    # Asegúrate de rellenar la lógica de YouTube aquí.
    # Por ahora, se mantiene la estructura vacía para evitar errores.
    st.header("📺 YouTube Video Charts")
    st.info("Lógica de YouTube por implementar.")

with tab_social:
    # --- REDES SOCIALES ---
    left, right = st.columns(2)
    with left:
        st.markdown("### Plataformas de Streaming Oficiales")
        st.markdown("- [Spotify: BTS](https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX)")
        st.markdown("- [YouTube: BANGTANTV](https://www.youtube.com/@BANGTANTV)")
        st.markdown("- [Apple Music: BTS](https://music.apple.com/artist/bts/667061285)")
        st.markdown("- [Deezer: BTS](https://www.deezer.com/artist/4105021)")
        st.write("**Spotify Solistas:** [JK](https://open.spotify.com/intl-es/artist/6HaGTQPmzraVmaVxvz6EUc) | [Jimin](https://open.spotify.com/intl-es/artist/1oSPZhvZMIrWW5I41kPkkY) | [V](https://open.spotify.com/artist/3JsHnjpbhX4SnySpvpa9DK) | [RM](https://open.spotify.com/intl-es/artist/2auC28zjQyVTsiZKNgPRGs) | [Jin](https://open.spotify.com/artist/5vV3bFXnN6D6N3Nj4xRvaV) | [Suga](https://open.spotify.com/intl-es/artist/5RmQ8k4l3HZ8JoPb4mNsML) | [j-hope](https://open.spotify.com/artist/0b1sIQumIAsNbqAoIClSpy)")
    with right:
        st.markdown("### Redes Sociales")
        st.markdown("- [Instagram: @bts.bighitofficial](https://www.instagram.com/bts.bighitofficial)")
        st.markdown("- [X (Twitter): @bts_bighit](https://x.com/bts_bighit)")
        st.markdown("- [TikTok: @bts_official_bighit](https://www.tiktok.com/@bts_official_bighit)")
        st.write("**Instagram Miembros:**")
        st.caption("[RM](https://www.instagram.com/rkive) | [Jin](https://www.instagram.com/jin) | [SUGA](https://www.instagram.com/agustd) | [j-hope](https://www.instagram.com/uarmyhope) | [Jimin](https://www.instagram.com/j.m) | [V](https://www.instagram.com/thv) | [JK](https://www.instagram.com/mnijungkook)")

st.markdown('<p style="text-align: center; color: #7D52B5; margin-top: 50px;">Hecho con amor para ARMY Honduras💜</p>', unsafe_allow_html=True)
