import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import streamlit as st
from datetime import datetime

# 1. Conexión con Secrets de Streamlit
try:
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error(f"Error de llaves: {e}")
    st.stop()

def get_real_charts():
    # ID de la playlist oficial "Top 50 - Honduras" 
    # (Esta es la que alimenta el Top 200 técnico)
    hn_chart_id = '37i9dQZEVXbJp9wj9p9v7f'
    
    try:
        # Pedimos los datos ampliados (usamos limit 50 porque es el estándar de la API)
        # Para el Top 200 real, Spotify requiere acceso de "User" o archivos externos, 
        # pero con este filtro capturamos lo que Kworb ve en el Top 50/100.
        results = sp.playlist_items(hn_chart_id)
        items = results['items']
        
        bts_data = []
        for i, item in enumerate(items):
            track = item['track']
            if not track: continue
            
            # Buscamos BTS o miembros en solitario (Jungkook, Jimin, V, etc.)
            artists = [a['name'].upper() for a in track['artists']]
            full_artists_string = ", ".join([a['name'] for a in track['artists']])
            
            # Filtro por BTS y solistas comunes en el chart de HN
            solistas = ['JUNG KOOK', 'JIMIN', 'V', 'SUGA', 'J-HOPE', 'RM', 'JIN']
            es_bts = 'BTS' in artists or any(s in artists for s in solistas)
            
            if es_bts:
                bts_data.append({
                    'Puesto': i + 1,
                    'Canción': track['name'],
                    'Artistas': full_artists_string,
                    'Álbum': track['album']['name'],
                    'id': track['id']
                })
        
        return pd.DataFrame(bts_data)
    except Exception as e:
        st.error(f"Error al leer Spotify: {e}")
        return pd.DataFrame()

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="BTS Charts HN", page_icon="📈")
st.title("🇭🇳 BTS & Soloists: Honduras Charts")
st.markdown("Comparando datos en tiempo real con Spotify y tendencias de **Kworb**.")

if st.button('🔄 Refrescar Rankings'):
    st.cache_data.clear()

df = get_real_charts()

if not df.empty:
    st.success(f"✅ Se detectaron {len(df)} entradas en el Chart de Honduras.")
    
    # Tabla con diseño limpio
    st.subheader(f"Top del {datetime.now().strftime('%d/%m/%Y')}")
    
    # Mostramos los resultados
    st.dataframe(
        df[['Puesto', 'Canción', 'Artistas', 'Álbum']], 
        hide_index=True, 
        use_container_width=True
    )
    
    st.info("Nota: Si ves que en Kworb hay más canciones (puestos 51-200), la API de Spotify a veces tarda 24h más en reflejar esos cambios en las playlists públicas.")
else:
    st.warning("⚠️ No se detectaron canciones de BTS en los primeros 50 puestos hoy.")
    st.write("Si en Kworb aparecen en puestos como el #120 o #180, necesitamos una base de datos histórica para rastrearlas fuera del Top 50 principal.")
