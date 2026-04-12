import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras 🇭🇳", page_icon="BTS_Logo.png", layout="wide")

# --- FUNCIÓN PARA CARGAR IMAGEN DE FONDO ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

image_path = 'BTSLOGO.png' 
bin_str = get_base64(image_path)

# --- ESTILOS CSS REFORZADOS ---
if bin_str:
    st.markdown(f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: repeat;
        background-attachment: fixed;
    }}

    /* Estilo de las celdas de tablas */
    [data-testid="stDataFrame"] td {{
        background-color: rgba(173, 216, 230, 0.7) !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}

    /* Estilo de encabezados de tablas */
    [data-testid="stDataFrame"] th {{
        background-color: rgba(173, 216, 230, 0.5) !important;
        color: #004aad !important;
    }}

    /* Estilo de Pestañas */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 10px !important;
        border-radius: 15px 15px 0px 0px !important;
        border-bottom: 3px solid #004aad !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button p {{
        color: #004aad !important;
        font-weight: bold !important;
    }}

    /* Títulos y Subtítulos */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        color: #004aad !important;
        padding: 12px 25px !important;
        border-radius: 12px !important;
        display: inline-block !important;
        border-left: 5px solid #004aad !important;
        margin-bottom: 25px !important;
    }}

    /* Secciones de Redes y Columnas */
    [data-testid="stColumn"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 1px solid #004aad !important;
    }}
    </style>
    ''', unsafe_allow_html=True)

# --- FUNCIONES DE EXTRACCIÓN DE DATOS ---
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
                    'Puesto': int(cols[0].text.strip()), 'Mov': icon_mov(cols[1].text.strip()),
                    'Canción': full_text, 'Streams': cols[6].text.strip(), 'Evolución': cols[7].text.strip()
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
st.title("📊 BTS Charts Honduras 🇭🇳")
st.write(f"Actualizado el: {datetime.now().strftime('%d/%m/%Y')}")

# --- PESTAÑAS ---
tab_spot, tab_ytm, tab_apple, tab_itunes, tab_deezer, tab_social = st.tabs([
    "🎧 Spotify", "🎵 YouTube Music", "🍎 Apple Music", "⭐ iTunes", "🔊 Deezer", "📱 Redes"
])

with tab_spot:
    st.header("🎧 Spotify Charts")
    st.subheader("Honduras 🇭🇳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Diario Honduras**")
        df_hd = get_kworb_data("https://kworb.net/spotify/country/hn_daily.html", "spotifydaily")
        st.dataframe(df_hd, hide_index=True, use_container_width=True, height=600)
    with c2:
        st.markdown("**Top Semanal Honduras**")
        df_hw = get_kworb_data("https://kworb.net/spotify/country/hn_weekly.html", "spotifyweekly")
        st.dataframe(df_hw, hide_index=True, use_container_width=True, height=600)
    st.divider()
    st.subheader("Global 🌍")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Top Diario Global**")
        df_gd = get_kworb_data("https://kworb.net/spotify/country/global_daily.html", "spotifydaily")
        st.dataframe(df_gd, hide_index=True, use_container_width=True, height=600)
    with c4:
        st.markdown("**Top Semanal Global**")
        df_gw = get_kworb_data("https://kworb.net/spotify/country/global_weekly.html", "spotifyweekly")
        st.dataframe(df_gw, hide_index=True, use_container_width=True, height=600)

with tab_ytm:
    st.header("🎵 YouTube Music Honduras")
    fecha_update_ytm = "11 de abril 2026"
    data_yt_diario = [] 
    st.write(f"Última actualización: **{fecha_update_ytm}**")
    col_d, col_w = st.columns(2)
    with col_d:
        st.subheader("Top diario")
        if not data_yt_diario: st.warning("Hoy no hay canciones en el chart diario.")
        else: st.dataframe(pd.DataFrame(data_yt_diario), hide_index=True, use_container_width=True, height=600)
    with col_w:
        st.subheader("Top semanal")
        st.info("No hay entradas en el chart semanal.")

with tab_apple:

    # Datos Globales que proporcionaste
    data_apple_global = [
        {"Puesto": 3, "Mov": "➡️ =", "Canción": "SWIM - BTS"},
        {"Puesto": 10, "Mov": "🟩 +1", "Canción": "2.0 - BTS"},
        {"Puesto": 16, "Mov": "🟥 -1", "Canción": "Body to Body - BTS"},
        {"Puesto": 28, "Mov": "🟥 -1", "Canción": "Hooligan - BTS"},
        {"Puesto": 45, "Mov": "🟥 -8", "Canción": "NORMAL - BTS"},
        {"Puesto": 48, "Mov": "🟥 -8", "Canción": "FYA - BTS"},
        {"Puesto": 63, "Mov": "🟥 -9", "Canción": "Aliens - BTS"},
        {"Puesto": 72, "Mov": "🟥 -9", "Canción": "Like Animals - BTS"},
        {"Puesto": 94, "Mov": "🟥 -11", "Canción": "they don’t know ’bout us - BTS"},
        {"Puesto": 98, "Mov": "🟥 -19", "Canción": "Merry Go Round - BTS"}
    ]

    col_ah, col_ag = st.columns(2)
    
    with col_ah:
        st.subheader("Honduras 🇭🇳")
           st.header("🍎 Apple Music Top 100")
    st.subheader("Honduras 🇭🇳")
    
    # DATOS MANUALES (Aquí es donde tú anotas lo que ves en el link de Apple)
    # Solo cambia los números y nombres según lo que veas en el link
    data_apple_manual = [
        {"Puesto": 84, "Mov": "🟩 +15", "Canción": "BTS - SWIM"},
]
    st.header("🍎 Apple Music Charts")
            
    with col_ag:
        st.subheader("Global 🌍")
        if not data_apple_global:
            st.warning("No se detectan entradas en Apple Global.")
        else:
            df_apple_gl = pd.DataFrame(data_apple_global)
            st.dataframe(df_apple_gl, hide_index=True, use_container_width=True, height=600)
    if not data_apple_manual:
        st.info("No hay entradas de BTS en el Top 100 de Apple Music hoy.")
    else:
        df_apple = pd.DataFrame(data_apple_manual)
        st.dataframe(df_apple, hide_index=True, use_container_width=True, height=400)
    
with tab_itunes:
    st.header("⭐ iTunes Top Songs")
    st.subheader("Honduras 🇭🇳")
    
    # Mensaje de "En proceso" con estilo
    st.info("🚧 **Sección en proceso:** Estamos ajustando la extracción de datos para iTunes Honduras.")
    
    # Opcional: Puedes dejar un spinner o un mensaje de carga
    with st.spinner("Preparando actualización de iTunes..."):
        st.write("Próximamente verás aquí el Top Songs de iTunes Honduras.")
    
    # He comentado el código anterior por si lo necesitas luego, 
    # pero ahora no se mostrará la tabla vacía.
    # df_itunes_hn = get_itunes_data("https://kworb.net/charts/itunes/hn.html")
    # st.dataframe(df_itunes_hn, hide_index=True, use_container_width=True, height=600)

with tab_deezer:
    st.header("🔊 Deezer Charts")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.subheader("Honduras 🇭🇳")
        df_dh = get_simple_chart("https://kworb.net/charts/deezer/hn.html")
        st.dataframe(df_dh, hide_index=True, use_container_width=True, height=600)
    with cd2:
        st.subheader("Global 🌍")
        df_dg = get_simple_chart("https://kworb.net/charts/deezer/ww.html")
        st.dataframe(df_dg, hide_index=True, use_container_width=True, height=600)

with tab_social:
    left, right = st.columns(2)
    with left:
        st.markdown("### Plataformas Oficiales")
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

st.markdown('<p style="text-align: center; color: #004aad; margin-top: 50px;">Hecho con amor para ARMY Honduras 💜</p>', unsafe_allow_html=True)
