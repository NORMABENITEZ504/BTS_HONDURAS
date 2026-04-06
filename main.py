import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BTS Charts Honduras (Kworb)", page_icon="💜")

st.title("💜 BTS & Soloists: Honduras Daily Chart")
st.markdown("Datos extraídos directamente de **Kworb.net** (Spotify Honduras)")

def get_kworb_data():
    url = "https://kworb.net/spotify/country/hn_daily.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        # Usamos pandas para leer todas las tablas del HTML
        tables = pd.read_html(response.text)
        df = tables[0] # La primera tabla es el chart diario
        
        # Kworb pone Artista y Título en una sola columna "Artist and Title"
        # Filtramos filas que contengan "BTS" o solistas
        solistas = ["BTS", "JUNG KOOK", "JIMIN", "V ", "SUGA", "J-HOPE", "RM", "JIN"]
        
        # Filtro de búsqueda (insensible a mayúsculas)
        pattern = '|'.join(solistas)
        df_bts = df[df['Artist and Title'].str.contains(pattern, case=False, na=False)].copy()
        
        # Limpiamos un poco los nombres de las columnas
        df_bts = df_bts.rename(columns={
            'Pos': 'Puesto',
            'Artist and Title': 'Artista y Canción',
            'Streams': 'Reproducciones',
            'P+': 'Movimiento'
        })
        
        return df_bts
    except Exception as e:
        st.error(f"Error al conectar con Kworb: {e}")
        return pd.DataFrame()

# --- MOSTRAR DATOS ---
if st.button('🔄 Actualizar desde Kworb'):
    st.cache_data.clear()

df_final = get_kworb_data()

if not df_final.empty:
    st.success(f"Se encontraron {len(df_final)} canciones en el Top 200 de Honduras.")
    
    # Diseño de la tabla
    st.subheader(f"Ranking al {datetime.now().strftime('%d/%m/%Y')}")
    
    # Formatear la columna de movimiento para que se vea mejor
    # (Kworb usa = para estable, + para subir y - para bajar)
    def style_move(val):
        if '+' in str(val): return f"🟩 {val}"
        if '-' in str(val): return f"🟥 {val}"
        return f"⬜ {val}"
    
    df_final['Movimiento'] = df_final['Movimiento'].apply(style_move)

    st.dataframe(
        df_final[['Puesto', 'Movimiento', 'Artista y Canción', 'Reproducciones']],
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("No se encontraron canciones de BTS o sus solistas en el Top 200 de hoy.")

st.caption("Fuente: Kworb.net - Spotify Daily Chart Honduras")
