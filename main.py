import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import streamlit as st
from datetime import datetime

# 1. Configuración de conexión Segura
try:
    # Intentamos leer de Streamlit Secrets
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

def get_bts_charts():
    # ID del Top 50 de Honduras (Asegúrate que sea este exacto)
    playlist_id = '37i9dQZEVXbJp9wj9p9v7f' 
    
    try:
        # Pedimos los datos (limitado a 50 para evitar errores de saturación)
        results = sp.playlist_items(playlist_id, fields='items.track(name,id,artists,album(images))', limit=50)
        tracks = results['items']
        
        bts_songs = []
        for i, item in enumerate(tracks):
            track = item['track']
            if not track: continue
            
            artists_names = [a['name'].upper() for a in track['artists']]
            
            if 'BTS' in artists_names:
                bts_songs.append({
                    'Rank': i + 1,
                    'Canción': track['name'],
                    'Artistas': ", ".join([a['name'] for a in track['artists']]),
                    'ID': track['id']
                })
        return pd.DataFrame(bts_songs)
    except Exception as e:
        st.error(f"Error al conectar con Spotify: {e}")
        return pd.DataFrame()

# --- INTERFAZ ---
st.set_page_config(page_title="BTS Charts Honduras", page_icon="💜")
st.title("💜 BTS Spotify Charts: Honduras")

# Botón para actualizar manualmente
if st.button('Actualizar Datos'):
    st.cache_data.clear()

df_new = get_bts_charts()

if not df_new.empty:
    st.subheader(f"Top Diario - {datetime.now().strftime('%d/%m/%Y')}")
    st.dataframe(df_new[['Rank', 'Canción', 'Artistas']], hide_index=True, use_container_width=True)
    st.success(f"¡Encontramos {len(df_new)} temas en el Top!")
else:
    st.info("No se encontraron canciones de BTS en el Top 50 de Honduras en este momento.")
